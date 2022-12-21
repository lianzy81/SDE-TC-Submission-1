"""Flask App WSGI entry point:

    Execute this command to run Flask app:  gunicorn --bind 0.0.0.0:8050 wsgi:app
"""
from flask_app import create_app

# Init and get Flask app
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050")
