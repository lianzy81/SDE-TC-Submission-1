"""Module to create Plotly Dash dashboard application."""
import dash
from dash import html
from .layouts import html_index_string, header_main, layout_main
from .callbacks import init_callbacks

def create_dashboard(server):
    """Create and initialize a Plotly Dash dashboard object for binding to input server.

    Args:
        server (Flask app): parent Flask app upon which newly created Plotly Dash app will be embedded.

    Returns:
        dash_app.server: parent Flask app which has an embedded Plotly Dash app initialized with layout, callbacks, etc..

    Note that:
        requests_pathname_prefix: the prefix for the AJAX calls that originate from the client (the web browser).
        routes_pathname_prefix: the prefix for the API routes on the backend (e.g. Flask server).
        url_base_pathname: will set `requests_pathname_prefix` and `routes_pathname_prefix` to the same value.
    """
    # create Dash app
    dash_app = dash.Dash(
        __name__,
        server=server,
        title='Covid-19 Monitoring - Dashboard',
        url_base_pathname="/dashboard/",
        assets_folder="assets",
        external_stylesheets=["assets/bootstrap.min.css"],
    )

    # After dash_app is created and loaded
    #==============================
    # initialize config
    dash_app.config.suppress_callback_exceptions = True
    dash_app.css.config.serve_locally = True
    dash_app.scripts.config.serve_locally = True

    # initialize index_string
    dash_app.index_string = html_index_string

    # initialize layout
    dash_app.layout = html.Div([
        header_main,
        layout_main
    ])

    # initialize callbacks
    init_callbacks(dash_app)

    return dash_app.server
