""" Initialize the Flask app."""
from flask import Flask
from flask_app.config import ProdConfig

def create_app():
    """ Initialize the core application with embedded Dash app."""
    app = Flask(__name__)
    app.config.from_object(ProdConfig)

    with app.app_context():
        # import function to create Dash applications
        from .dash.dashboard import create_dashboard

        # create and register isolated Dash apps onto parent Flask app
        app = create_dashboard(app)

        return app
