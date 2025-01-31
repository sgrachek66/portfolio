import os
from flask import Flask
from flask_ckeditor import CKEditor

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
        
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'portfolio.sqlite'),
    )
    
    # Configure CKEditor to load from CDN
    app.config['CKEDITOR_SERVE_LOCAL'] = False
    app.config['CKEDITOR_PKG_TYPE'] = 'full'
    app.config['CKEDITOR_CDN_CUSTOM'] = 'https://cdn.ckeditor.com/4.25.0/full/ckeditor.js'
    
    # Initialize CKEditor after configuration
    ckeditor = CKEditor(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import db
    db.init_app(app)
    
    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import blog
    app.register_blueprint(blog.bp)
    
    
    
    @app.route('/check-requirements')
    def check_requirements():
        try:
            import flask
            import gunicorn
            return "Requirements installed successfully!"
        except ImportError as e:
            return f"Missing requirement: {str(e)}"
    
    
    return app