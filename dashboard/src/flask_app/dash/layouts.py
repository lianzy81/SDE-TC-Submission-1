"""Layout of static components for Dash app.
    html_index_string: index string
    header_main: top-most header of dashboard.
    layout_main: main components of dashboard.
"""
from dash import html, dcc
from datetime import datetime as dt

#===============================#
#                               #
#         INDEX STRING          #
#                               #
#===============================#
html_index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div> </div>
    </body>
</html>
'''

#===============================#
#                               #
#         HEADER - MAIN         #
#                               #
#===============================#
header_main = html.Div([
    html.Div([
            html.Label('Covid-19 Statistics',
                    style = {'font-weight':'bold',
                                'font-size':'30px',
                                'color':'#0a527f'}),
            html.Br(),
    ],
    style={'display':'inline-block', 'padding-left':'15px'})
],
style={'padding-top':'15px'},
className="main-header"
)

#===============================#
#                               #
#        LAYOUT - MAIN          #
#                               #
#===============================#
main_tab_style={'display':'inline-block','width':'95%','padding':'15px'}

layout_main = html.Div([
    html.Div(
    children=[
        #======================================#
        #                                      #
        # COVID-19 CASES OVER TIME             #
        #                                      #
        #======================================#
        #====================
        # (A) COUNTRY
        html.Label(
            "Country:", 
            style={
                "width": "8%",
                "font-weight": "bold",
                "font-size": "18px",},
        ),
        dcc.Dropdown(
            id="selected-country",
            options=[
                {"label": "Singapore", "value": "singapore"},
            ],
            value="singapore",
            style={
                "width": "30%",
                "display": "inline-block",
                "verticalAlign": "middle",
            },
        ),
        html.Br(),

        #====================
        # (B) STATUS
        html.Label(
            "Status:", 
            style={
                "width": "8%",
                "font-weight": "bold",
                "font-size": "18px",},
        ),
        dcc.Dropdown(
            id="selected-status",
            options=[
                {"label": "Confirmed", "value": "confirmed"},
            ],
            value="confirmed",
            style={
                "width": "30%",
                "display": "inline-block",
                "verticalAlign": "middle",
            },
        ),

        #==========================
        # (C) COVID19 CASES GRAPH
        html.Div(id='covid19_graph', style={"width":"75%"}),
        html.Br(),
        html.Br(),
    ],
    style=main_tab_style),
],
style=main_tab_style,
className="main-page")
