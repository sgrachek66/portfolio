from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from portfolio.auth import login_required
from portfolio.db import get_db
from portfolio.utils.security import sanitize_html
from portfolio.webforms import PostForm

bp = Blueprint('home', __name__,)

@bp.route('/')
def index():
    
    return render_template('home/home.html')
