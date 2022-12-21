""" Callbacks for Dash app. """
import requests
from dash import Input, Output, dcc
import plotly.express as px
import pandas as pd

# ===========================
# Initialize globals
HOST = "https://api.covid19api.com"

# ===========================
# Initialize callbacks
def init_callbacks(app):
    """Wrapper to initialize callbacks and underlying functions for Dash app.

    The Output and Input fields for each callback are referenced by the "id" of objects defined in layouts.py.

    Args:
        app (Dash object): Dash app created via a dash.Dash() call
    """
    # ==========================
    # MULTIDATE BATCH MIGRATION
    @app.callback(
        Output("covid19_graph", "children"),
        [
            Input("selected-country", "value"),
            Input("selected-status", "value"),
        ],
    )
    def get_covid_19_graph(selected_country="singapore", selected_status="confirmed"):
        """Retrieves covid-19 data via API call to HOST and generates histogram of cases over time.

        Args:
            selected_country (str): _description_. Defaults to "singapore".
            selected_status (str): _description_. Defaults to "confirmed".

        Returns:
            dcc.Graph component: that contains the histogram figure to be visualized
        """
        # Make API request to host
        # - response is a list of dictionaries of covid-data
        # - each dictonary is a single row of data
        url_string = f"{HOST}/country/{selected_country}/status/{selected_status}"
        print(f"Making API request to {url_string}")
        response = requests.get(url=url_string).json()

        # Create pandas dataframe from response data where 
        # only interested columns "Date" and "Cases" are loaded
        df = pd.DataFrame.from_records(data=response, columns=["Date","Cases"])

        # Compute daily cases from "Cases"
        df["Daily Cases"] = df["Cases"].diff()
        
        # Generate histogram
        fig = px.bar(
            df, x="Date", y="Daily Cases", title="Covid-19 Daily Case Count - Singapore", 
            template="plotly_white", range_y = [0, df["Daily Cases"].max()+2000])
        fig.update_traces(marker_color='red')
        fig.update_layout(bargap=0, yaxis_title="")
        child = dcc.Graph(figure=fig)

        return child
