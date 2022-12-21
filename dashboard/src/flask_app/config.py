"""Flask App Config
"""
class Config:
    """ Base config. """

    # General
    # --------------------------
    FLASK_APP = "wsgi.py"


class ProdConfig(Config):
    """ Production config """

    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    """ Development config """

    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
