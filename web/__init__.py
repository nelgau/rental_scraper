from flask import Flask, session, g, render_template
from flask_bootstrap import Bootstrap

from .rentals import rentals

def create_app(configfile=None):
    app = Flask(__name__)
    Bootstrap(app)
    app.register_blueprint(rentals)
    return app
