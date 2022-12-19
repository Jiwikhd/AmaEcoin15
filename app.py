from dash import Dash, html, dcc
import dash_auth
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container

import dash
from dash import dash_table
from PIL import Image
import sys
import sympy as smp

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

Ecoinnovazione_logo = Image.open("assets/ECOI.png")
#Ecoinnovazione_logo = "https://www.emiliaromagnastartup.it/sites/default/files/ecoinnovazione.jpg"
Amadori_logo = Image.open("assets/Amadori.png")
VALID_USERNAME_PASSWORD_PAIRS = {
    'Amadori': 'Packaging_tool_2022'
}
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div([
    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=Ecoinnovazione_logo, height="100px", style={"margin-left": "0px"})),
                            dbc.Col(html.Img(src=Amadori_logo, height="100px", style={"float": "right"})),
                        ],
                        align="center",
                        className="g-0",

                    ),
                    style={"textDecoration": "none", 'color': 'dark', "width":"100%"},
                )

            ]
        ),
        color="#DAF0AD",
        dark=False,
	style={'backgroundColor': '#DAF0AD', "width":"100%"},

    ),

             dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(f"{page['name']}", href=page["path"])
        for page in dash.page_registry.values()
        ],
        nav=True,
        label="Altre Pagine",
        color="dark",
        className="m-1",
        style={'float': 'right', "margin-right":"10px"}
    ),
           
    dcc.Store(id="session"),
    dcc.Store(id="sessiondata"),
    dcc.Store(id="sessioncolumn"),
    dcc.Store(id="sessiondataexcel"),
    dcc.Store(id="sessioncolumnexcel"),
    dcc.Store(id="sessionweight"),
    dcc.Store(id="sessionpeso"),
    dcc.Store(id="sessionpesob"),
    dcc.Store(id="sessionvolte"),


	dash.page_container
])



if __name__ == '__main__':
	app.run_server(debug=True)
