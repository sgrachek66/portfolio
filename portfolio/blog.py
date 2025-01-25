from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from portfolio.auth import login_required
from portfolio.db import get_db
from portfolio.utils.security import sanitize_html
from portfolio.webforms import PostForm

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = PostForm()
    
    if form.validate_on_submit():
        title = form.title.data
        raw_body = form.content.data # from the CKEditorField
        
        body = sanitize_html(raw_body)
        error = None
        
        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/create.html', form=form)

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    
    return post


@bp.route('/<int:id>/detail', methods=('GET',))
def detail(id):
    post = get_post(id, False)
    return render_template('blog/detail.html', post=post)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    
    form = PostForm()
    
    if request.method == 'GET':
        # Pre-fill the form fields with exisiting data
        form.title.data = post['title']
        form.content.data = post['body']
    else:
        # If POST, check validation
        if form.validate_on_submit():
            title = form.title.data
            raw_body = form.content.data
            body = sanitize_html(raw_body)
            
            error = None
            if not title:
                error = 'Title is required.'
            
            if error:
                flash(error)
            else:
                db = get_db()
                db.execute(
                    'UPDATE post SET title = ?, body = ?'
                    ' WHERE id = ?',
                    (title, body, id)
                )
                db.commit()
                return redirect(url_for('blog.index'))
    
    return render_template('blog/update.html', form=form, post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))