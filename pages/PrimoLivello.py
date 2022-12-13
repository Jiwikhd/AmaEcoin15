import dash
from dash import Dash, dcc, State, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
import base64
import numpy as np
from dash import dash_table
import sys
import sympy as smp


import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image
import pandas as pd

img_path = "assets/cc.jpg"
pil_image0 = Image.open("assets/acid.jpg")
pil_image = Image.open(img_path)
pil_image2 = Image.open("assets/landuse.jpg")
pil_image3 = Image.open("assets/ozone.jpg")
pil_image4 = Image.open("assets/risorse.jpg")
pil_image5 = Image.open("assets/particolo.jpg")
pil_image6 = Image.open("assets/wtr.jpg")
pil_image_pdf = Image.open("assets/PDF3.png")

df = pd.read_csv('assets/Database.csv', encoding='unicode_escape')
colors = {
    'background': '#DAF0AD'
}
dash.register_page(__name__, path='/')

layout = html.Div([
    html.Br(),
    html.Br(),

    dbc.ListGroupItem(dbc.Row([
            dbc.Col(html.P("A) IMBALLAGGIO PRIMARIO"), width=8),

            dbc.Col(dbc.Row([dbc.Col(html.P("Peso netto [g] / unità:"), width=6),dbc.Col(dbc.Input(type="number", id='pwb', value=0,min=0, size="sm",persistence=True,persistence_type='memory'), width=3)],className="g-0"))]),
                      style={ "color":"white","height":"50px","margin-bottom":"20px"}, color="#004e18", active=False),


    dbc.Row([dbc.Col(dbc.Alert(html.H3("Soluzione A")
        , color="#A38000", style={'width': '100%'})),
        dbc.Col(dbc.Alert(html.H3("Soluzione B")
            , color="#D9AA00", style={'width': '100%',"color":"black"}))], style={"margin-left": "10px", "margin-right": "10px"}),


    html.Br(),

    dbc.Row([dbc.Col(dbc.Table([
                html.Thead(html.Tr(
                    [html.Th("Componente", style={'width': '20%'}), html.Th("Composizione", style={'width': '24%'}),
                     html.Th("Specifiche", style={'width': '26%'}),
                     html.Th("Peso Componente", style={'width': '9%'}), html.Th("Prezzo", style={'width': '10%'}),
                     html.Th("Distanza di Fornitura", style={'width': '11%'}),
                     ])),

                html.Tr([html.Td(
                    dbc.Switch(label='Vassoio preformato', value=False, id='check1', style={'margin-left': '15%'},input_class_name='bg-warning',persistence=True,persistence_type='memory')),
                    html.Td(dcc.Dropdown(df.loc[(df['Componente'] == 'Vassoio preformato')]['Composizione'], 'PET',
                                         id='dd1',persistence=True,persistence_type='memory')),
                    html.Td(dbc.Table([
                                       html.Tr([dbc.Row(html.P('Contenuto di riciclato(tot):', id='rtext'),align = "center" ,style={"text-align":"center",'verticalAlign': 'middle',"margin-bottom":"0px"}), dbc.Row([dbc.Col(dbc.Input(type="number",min=0,max=100, id='rinput', value=0, size="sm",persistence=True,persistence_type='memory')), dbc.Col(html.P(' % w/w'))], style={"margin-top":"0px"}, align = "center")]),
                                       html.Tr([dbc.Row(html.P('Post-consumo:', id='stype3'), style={"text-align":"center",'verticalAlign': 'middle'}),dbc.Row([dbc.Col(dbc.Input(type="number", id='stype2',min=0,max=100, value=0, size="sm",persistence=True,persistence_type='memory')), dbc.Col(html.P(' %', style={"text-align":"middle",'height': '100%'}))])]),
                                       html.Tr([dbc.Row(html.P('Pre-consumo:', id='stype'), style={"text-align":"center",'verticalAlign': 'middle'}),dbc.Row([dbc.Col(dbc.Input(type="number", id='stype4',min=0,max=100, value=0, size="sm", disabled=True,persistence=True,persistence_type='memory')), dbc.Col(html.P(' %'))])])],
                                      bordered=False, id="tablehide")),
                    html.Td(dbc.Row(
                        [dbc.Input(type="number", id='input1', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("g / pezzo", id="unit1")],
                        style={"margin-left": "1px"})),
                    html.Td(dbc.Row([dbc.Input(type="number", id='input11', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'),
                                     html.P("€ / pezzo", id="unit11")])),
                    html.Td(dbc.Row([dbc.Input(type="number", id='dd11', value=0,min=0, size="sm",persistence=True,persistence_type='memory'),
                                     html.P("km", id="unit111")])),
                ]),


                html.Tr(
                    [html.Td(dbc.Switch(label='Pad assorbente', value=False, id='check2', style={'margin-left': '15%'},input_class_name='bg-warning',persistence=True,persistence_type='memory')),
                     html.Td(dcc.Dropdown(df.loc[(df['Componente'] == 'Pad assorbente')]['Composizione'], 'Carta + PE',
                                          id='dd2',persistence=True,persistence_type='memory')),
                     html.Td(html.P('')),
                     html.Td(dbc.Row(
                         [dbc.Input(type="number", id='input2', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("g / pezzo", id="unit2")])),
                     html.Td(dbc.Row([dbc.Input(type="number", id='input22', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'),
                                      html.P("€ / pezzo", id="unit22")])),
                     html.Td(dbc.Row([dbc.Input(type="number", id='dd22', value=0,min=0, size="sm",persistence=True,persistence_type='memory'),
                                      html.P("km", id="unit222")])),
                     ]),

                html.Tr([html.Td(
                    dbc.Switch(label='Top flessibile', value=False, id='check3', style={'margin-left': '15%'},input_class_name='bg-warning',persistence=True,persistence_type='memory')),

                    html.Td(dbc.Table([html.Tr(dbc.Row([dbc.Col([dbc.Row(html.P('% PET')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pet1",persistence=True,persistence_type='memory'))], style={"margin-right":"0px"}),dbc.Col([dbc.Row(html.P('% PP')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pp1",persistence=True,persistence_type='memory'), style={"margin-left":"1px"})])], className="g-0")),
                    html.Tr(dbc.Row([dbc.Col([dbc.Row(html.P('% PA')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pa1",persistence=True,persistence_type='memory'))]),dbc.Col([dbc.Row(html.P('% PVC')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pvc1",persistence=True,persistence_type='memory'), style={"margin-left":"1px"})])], className="g-0")),
                                       html.Tr(dbc.Row([dbc.Col([dbc.Row(html.P('% PE')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pe1",persistence=True,persistence_type='memory'))], width=5),dbc.Col([dbc.Row(html.P('% EVOH/EVA')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="evoh1",persistence=True,persistence_type='memory'), style={"margin-left":"1px"})])], className="g-0")),
                                       html.Tr(dbc.Badge("Primary", color="primary", className="me-1", id="topsum"))
                                       ],
                                      bordered=False, id="polym3")),
                    html.Td(dbc.Row(
                        [dbc.Input(type="number", id='area', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("Inserire l'area (m\u00b2)")], style={"margin-right":"2px"}, id="row31")),
                    html.Td(dbc.Row(
                        [dbc.Input(type="number", id='input3', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P(" g / m\u00b2 ", id="unit3")], id="row32")),
                    html.Td(dbc.Row([dbc.Input(type="number", id='input33', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'),
                                     html.P(" € / m\u00b2 ", id="unit33")], id="row33")),
                    html.Td(dbc.Row([dbc.Input(type="number", id='dd33', value=0,min=0, size="sm",persistence=True,persistence_type='memory'),
                                     html.P("km", id="unit333")], id="row34")),

                ]),

                html.Tr([html.Td(
                    dbc.Switch(label='Bottom flessibile', value=False, id='check4', style={'margin-left': '15%'},input_class_name='bg-warning',persistence=True,persistence_type='memory')),

html.Td(dbc.Table([html.Tr(dbc.Row([dbc.Col([dbc.Row(html.P('% PET')),
                                                dbc.Row(dbc.Input(type="number",value=0, size="sm",min=0,max=100, id="pet2",persistence=True,persistence_type='memory'))]),dbc.Col([dbc.Row(html.P('% PP')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pp2",persistence=True,persistence_type='memory'), style={"margin-left":"1px"})])], className="g-0")),
                    html.Tr(dbc.Row([dbc.Col([dbc.Row(html.P('% PA')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pa2",persistence=True,persistence_type='memory'))]),dbc.Col([dbc.Row(html.P('% PVC')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pvc2",persistence=True,persistence_type='memory'), style={"margin-left":"1px"})])], className="g-0")),
                                       html.Tr(dbc.Row([dbc.Col([dbc.Row(html.P('% PE')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pe2",persistence=True,persistence_type='memory'))], width=5),dbc.Col([dbc.Row(html.P('% EVOH/EVA')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="evoh2",persistence=True,persistence_type='memory'), style={"margin-left":"1px"})])], className="g-0")),
                                       html.Tr(dbc.Badge("Primary", color="primary", className="me-1", id="botsum"))
                                       ],
                                      bordered=False, id="polym4")),

                    html.Td(dbc.Row(
                        [dbc.Input(type="number", id='area2', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("Inserire l'area (m\u00b2)")], style={"margin-right":"2px"}, id="row41")),
                    html.Td(dbc.Row(
                        [dbc.Input(type="number", id='input4', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("g / m\u00b2", id="unit4")], id="row42")),
                    html.Td(dbc.Row(
                        [dbc.Input(type="number", id='input44', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("€ / m\u00b2", id="unit44")], id="row43")),
                    html.Td(dbc.Row([dbc.Input(type="number", id='dd44', value=0,min=0, size="sm",persistence=True,persistence_type='memory'),
                                     html.P("km", id="unit444")], id="row44")),
                ]),

                html.Tr([html.Td(
                    dbc.Switch(label='Supporto in cellulosa', value=False, id='check5', style={'margin-left': '15%'},input_class_name='bg-warning',persistence=True,persistence_type='memory')),
                    html.Td(dcc.Dropdown(df.loc[(df['Componente'] == 'Supporto in cellulosa')]['Composizione'],
                                         'cartene', id='dd5',persistence=True,persistence_type='memory')),
                    html.Td(dbc.Row(
                        [dbc.Input(type="number", id='area3', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("Inserire l'area (m\u00b2)")], style={"margin-right":"2px"}, id="areadis3")),
                    html.Td(dbc.Row(
                        [dbc.Input(type="number", id='input5', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("g / m\u00b2", id="unit5")])),
                    html.Td(dbc.Row(
                        [dbc.Input(type="number", id='input55', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("€ / m\u00b2", id="unit55")])),
                    html.Td(dbc.Row([dbc.Input(type="number", id='dd55', value=0,min=0, size="sm",persistence=True,persistence_type='memory'),
                                     html.P("km", id="unit555")])),
                ]),

                html.Tr([html.Td(dbc.Switch(label='Busta', value=False, id='check6', style={'margin-left': '15%'},input_class_name='bg-warning',persistence=True,persistence_type='memory')),
                         html.Td(
                             dcc.Dropdown(df.loc[(df['Componente'] == 'Busta')]['Composizione'], 'Carta+PP', id='dd6',persistence=True,persistence_type='memory')),
                         html.Td(dbc.Row(
                        [dbc.Input(type="number", id='area4', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("Inserire l'area (m\u00b2)")], style={"margin-right":"2px"}, id="areadis4")),
                         html.Td(dbc.Row([dbc.Input(type="number", id='input6', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'),
                                          html.P("g / m\u00b2", id="unit6")])),
                         html.Td(dbc.Row([dbc.Input(type="number", id='input66', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'),
                                          html.P("€ / m\u00b2", id="unit66")])),
                         html.Td(dbc.Row([dbc.Input(type="number", id='dd66', value=0,min=0, size="sm",persistence=True,persistence_type='memory'),
                                          html.P("km", id="unit666")])),
                         ]),


            ],id="tavol1" ,bordered=True)), dbc.Col(dbc.Table([
                html.Thead(html.Tr(
                    [html.Th("Componente", style={'width': '20%'}), html.Th("Composizione", style={'width': '24%'}),
                     html.Th("Specifiche", style={'width': '26%'}),
                     html.Th("Peso Componente", style={'width': '9%'}), html.Th("Prezzo", style={'width': '10%'}),
                     html.Th("Distanza di Fornitura", style={'width': '11%'}),
                     ])),

                html.Tr([html.Td(
                    dbc.Switch(label='Vassoio preformato', value=False, id='check1b', style={'margin-left': '15%'},
                               input_class_name='bg-warning',persistence=True,persistence_type='memory')),
                    html.Td(dcc.Dropdown(df.loc[(df['Componente'] == 'Vassoio preformato')]['Composizione'], 'PET',
                                         id='dd1b',persistence=True,persistence_type='memory')),
                    html.Td(dbc.Table([
                                       html.Tr([dbc.Row(html.P('Contenuto di riciclato(tot):', id='rtextb'),align = "center" ,style={"text-align":"center",'verticalAlign': 'middle',"margin-bottom":"0px"}), dbc.Row([dbc.Col(dbc.Input(type="number",min=0,max=100, id='rinputb', value=0, size="sm",persistence=True,persistence_type='memory')), dbc.Col(html.P(' % w/w'))], style={"margin-top":"0px"}, align = "center")]),
                                       html.Tr([dbc.Row(html.P('Post-consumo:', id='stype3b'), style={"text-align":"center",'verticalAlign': 'middle'}),dbc.Row([dbc.Col(dbc.Input(type="number", id='stype2b',min=0,max=100, value=0, size="sm",persistence=True,persistence_type='memory')), dbc.Col(html.P(' %', style={"text-align":"middle",'height': '100%'}))])]),
                                       html.Tr([dbc.Row(html.P('Pre-consumo:', id='stypeb'), style={"text-align":"center",'verticalAlign': 'middle'}),dbc.Row([dbc.Col(dbc.Input(type="number", id='stype4b',min=0,max=100, value=0, size="sm", disabled=True,persistence=True,persistence_type='memory')), dbc.Col(html.P(' %'))])])],
                                      bordered=False, id="tablehideb")),
                    html.Td(dbc.Row(
                        [dbc.Input(type="number", id='input1b', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("g / pezzo", id="unit1b")],
                        style={"margin-left": "1px"})),
                    html.Td(dbc.Row([dbc.Input(type="number", id='input11b', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'),
                                     html.P("€ / pezzo", id="unit11b")])),
                    html.Td(dbc.Row([dbc.Input(type="number", id='dd11b', value=0,min=0, size="sm",persistence=True,persistence_type='memory'),
                                     html.P("km", id="unit111b")])),
                ]),



                html.Tr(
                    [html.Td(dbc.Switch(label='Pad assorbente', value=False, id='check2b', style={'margin-left': '15%'},
                                        input_class_name='bg-warning',persistence=True,persistence_type='memory')),
                     html.Td(dcc.Dropdown(df.loc[(df['Componente'] == 'Pad assorbente')]['Composizione'], 'Carta + PE',
                                          id='dd2b',persistence=True,persistence_type='memory')),
                     html.Td(html.P('')),
                     html.Td(dbc.Row([dbc.Input(type="number", id='input2b', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'),
                                      html.P("g / pezzo", id="unit2b")])),
                     html.Td(dbc.Row([dbc.Input(type="number", id='input22b', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'),
                                      html.P("€ / pezzo", id="unit22b")])),
                     html.Td(dbc.Row([dbc.Input(type="number", id='dd22b', value=0,min=0, size="sm",persistence=True,persistence_type='memory'),
                                      html.P("km", id="unit222b")])),
                     ]),

                html.Tr([html.Td(
                    dbc.Switch(label='Top flessibile', value=False, id='check3b', style={'margin-left': '15%'},
                               input_class_name='bg-warning',persistence=True,persistence_type='memory')),

                html.Td(dbc.Table([html.Tr(dbc.Row([dbc.Col([dbc.Row(html.P('% PET')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pet1b",persistence=True,persistence_type='memory'))]),dbc.Col([dbc.Row(html.P('% PP')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pp1b",persistence=True,persistence_type='memory'), style={'margin-left': '1%'})])], className="g-0")),
                    html.Tr(dbc.Row([dbc.Col([dbc.Row(html.P('% PA')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pa1b",persistence=True,persistence_type='memory'))]),dbc.Col([dbc.Row(html.P('% PVC')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pvc1b",persistence=True,persistence_type='memory'), style={'margin-left': '1%'})])], className="g-0")),
                                       html.Tr(dbc.Row([dbc.Col([dbc.Row(html.P('% PE')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pe1b",persistence=True,persistence_type='memory'))], width=5),dbc.Col([dbc.Row(html.P('% EVOH/EVA')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="evoh1b",persistence=True,persistence_type='memory'), style={'margin-left': '1%'})])], className="g-0")),
                                                html.Tr(dbc.Badge("Primary", color="primary", className="me-1", id="topsumb"))
                                       ],
                                      bordered=False, id="areadisb")),
                    html.Td(dbc.Row(
                        [dbc.Input(type="number", id='areab', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("Inserire l'area (m\u00b2)")], style={"margin-right":"2px"}, id="row31b")),
                    html.Td(dbc.Row([dbc.Input(type="number", id='input3b', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'),
                                     html.P(" g / m\u00b2 ", id="unit3b")], id="row32b")),
                    html.Td(dbc.Row([dbc.Input(type="number", id='input33b', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'),
                                     html.P(" € / m\u00b2 ", id="unit33b")], id="row33b")),
                    html.Td(dbc.Row([dbc.Input(type="number", id='dd33b', value=0,min=0, size="sm",persistence=True,persistence_type='memory'),
                                     html.P("km", id="unit333b")], id="row34b")),

                ]),

                html.Tr([html.Td(
                    dbc.Switch(label='Bottom flessibile', value=False, id='check4b', style={'margin-left': '15%'},
                               input_class_name='bg-warning',persistence=True,persistence_type='memory')),

html.Td(dbc.Table([html.Tr(dbc.Row([dbc.Col([dbc.Row(html.P('% PET')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pet2b",persistence=True,persistence_type='memory'))]),dbc.Col([dbc.Row(html.P('% PP')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pp2b",persistence=True,persistence_type='memory'), style={'margin-left': '1%'})])], className="g-0")),
                    html.Tr(dbc.Row([dbc.Col([dbc.Row(html.P('% PA')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pa2b",persistence=True,persistence_type='memory'))]),dbc.Col([dbc.Row(html.P('% PVC')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pvc2b",persistence=True,persistence_type='memory'), style={'margin-left': '1%'})])], className="g-0")),
                                       html.Tr(dbc.Row([dbc.Col([dbc.Row(html.P('% PE')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="pe2b",persistence=True,persistence_type='memory'))], width=5),dbc.Col([dbc.Row(html.P('% EVOH/EVA')),
                                                dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id="evoh2b",persistence=True,persistence_type='memory'), style={'margin-left': '1%'})])], className="g-0")),
                                                html.Tr(dbc.Badge("Primary", color="primary", className="me-1", id="botsumb"))
                                       ],
                                      bordered=False, id="areadis2b")),
                    html.Td(dbc.Row(
                        [dbc.Input(type="number", id='area2b', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("Inserire l'area (m\u00b2)")], style={"margin-right":"2px"}, id="row41b")),
                    html.Td(dbc.Row(
                        [dbc.Input(type="number", id='input4b', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("g / m\u00b2", id="unit4b")], id="row42b")),
                    html.Td(dbc.Row([dbc.Input(type="number", id='input44b', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'),
                                     html.P("€ / m\u00b2", id="unit44b")], id="row43b")),
                    html.Td(dbc.Row([dbc.Input(type="number", id='dd44b', value=0,min=0, size="sm",persistence=True,persistence_type='memory'),
                                     html.P("km", id="unit444b")], id="row44b")),

                ]),

                html.Tr([html.Td(
                    dbc.Switch(label='Supporto in cellulosa', value=False, id='check5b', style={'margin-left': '15%'},
                               input_class_name='bg-warning',persistence=True,persistence_type='memory')),
                    html.Td(dcc.Dropdown(df.loc[(df['Componente'] == 'Supporto in cellulosa')]['Composizione'],
                                         'cartene', id='dd5b',persistence=True,persistence_type='memory')),
                    html.Td(dbc.Row(
                        [dbc.Input(type="number", id='area3b', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("Inserire l'area (m\u00b2)")], style={"margin-right":"2px"}, id="areadis3b")),
                    html.Td(dbc.Row(
                        [dbc.Input(type="number", id='input5b', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("g / m\u00b2", id="unit5b")])),
                    html.Td(dbc.Row([dbc.Input(type="number", id='input55b', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'),
                                     html.P("€ / m\u00b2", id="unit55b")])),
                    html.Td(dbc.Row([dbc.Input(type="number", id='dd55b', value=0,min=0, size="sm",persistence=True,persistence_type='memory'),
                                     html.P("km", id="unit555b")])),

                ]),

                html.Tr([html.Td(dbc.Switch(label='Busta', value=False, id='check6b', style={'margin-left': '15%'},
                                            input_class_name='bg-warning',persistence=True,persistence_type='memory')),
                         html.Td(
                             dcc.Dropdown(df.loc[(df['Componente'] == 'Busta')]['Composizione'], 'Carta+PP',
                                          id='dd6b',persistence=True,persistence_type='memory')),
                         html.Td(dbc.Row(
                        [dbc.Input(type="number", id='area4b', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'), html.P("Inserire l'area (m\u00b2)")], style={"margin-right":"2px"}, id="areadis4b")),
                         html.Td(dbc.Row([dbc.Input(type="number", id='input6b', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'),
                                          html.P("g / m\u00b2", id="unit6b")])),
                         html.Td(dbc.Row([dbc.Input(type="number", id='input66b', value=0.001,min=0, size="sm",persistence=True,persistence_type='memory'),
                                          html.P("€ / m\u00b2", id="unit66b")])),
                         html.Td(dbc.Row([dbc.Input(type="number", id='dd66b', value=0,min=0, size="sm"),
                                          html.P("km", id="unit666b")])),

                         ]),




            ],id="tavol2" ,bordered=True))], style={"font-size":"11px", "margin-left":"10px", "margin-right":"10px"}),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Checkbox(label="Nessun imb. primario", id="tavolo1", value=False )),
        dbc.Col(dbc.Checkbox(label="Nessun imb. primario", id="tavolo2", value=False ))
    ], style={"font-size":"14px", "margin-left":"10px", "margin-right":"10px"}),
    html.Br(),

    html.Br(),

    dbc.Alert([dbc.Row(html.H2("Risultati per la produzione, la fornitura e il fine vita dell'imballaggio primario",
                    style={"color": "white", "text-align": "center", "margin-top":"10px"})), dbc.Button("Salva i dati / Calcola i risultati",
            color="danger",
            className="position-absolute top-0 start-50 translate-middle",id="submit-val", n_clicks=None)], color="#004e18",style={"margin-left": "20px", "margin-right": "20px"},className="position-relative"),



            dbc.Tooltip(id="alert1", target="dd1"),
            dbc.Tooltip(id="alert2", target="dd2"),

            dbc.Tooltip(id="alert5", target="dd5"),
            dbc.Tooltip(id="alert6", target="dd6"),
            dbc.Tooltip(id="alert8", target="rtext"),
            dbc.Tooltip(id="alert10", target="stype3"),

            dbc.Tooltip(id="alert1b", target="dd1b"),
            dbc.Tooltip(id="alert2b", target="dd2b"),

            dbc.Tooltip(id="alert5b", target="dd5b"),
            dbc.Tooltip(id="alert6b", target="dd6b"),
            dbc.Tooltip(id="alert8b", target="rtextb"),
            dbc.Tooltip(id="alert10b", target="stype3b"),

        html.Br(),
        html.Div(dbc.Row([dbc.Col(dbc.Row([
                dbc.Col(dbc.Card([dbc.CardHeader(html.H6("Carbon Footprint")),
                          dbc.CardBody([html.H6(id='card1', className="card-title")])], color="#A38000")),
                dbc.Col(dbc.Card([dbc.CardHeader(html.H6("Peso Totale")),
                          dbc.CardBody([html.H6(id ='alertmsg', className="card-title")])], color="#A38000")),
                dbc.Col(dbc.Card(
                    [dbc.CardHeader(html.H6("Costo")), dbc.CardBody([html.H6(id='card2', className="card-title")])],
                    color="#A38000")),


            ])),
            dbc.Col(dbc.Row([
                dbc.Col(dbc.Card([dbc.CardHeader(html.H6("Carbon Footprint")),
                          dbc.CardBody([html.H6(id='card1b', className="card-title")])], color="#D9AA00")),
                dbc.Col(dbc.Card([dbc.CardHeader(html.H6("Peso Totale")),
                          dbc.CardBody([html.H6(id ='alertmsgb', className="card-title")])], color="#D9AA00")),
                dbc.Col(dbc.Card(
                    [dbc.CardHeader(html.H6("Costo")), dbc.CardBody([html.H6(id='card2b', className="card-title")])],
                    color="#D9AA00")),


            ]))
        ], style={"margin-right": "1%", "margin-left": "1%"})),
        html.Br(),
        html.Br(),
        dbc.Row([dbc.Col(dbc.Badge("Carbon Footprint", color="primary", className="me-1")), dbc.Col(dbc.Badge("Costo", color="primary", className="me-1"))], style={"margin-left": "10px", "margin-right": "10px"}),
        dbc.Row([dbc.Col(dcc.Graph(id='indicator-graphic')), dbc.Col(dcc.Graph(id='indicator-graphic2'))], style={"margin-left": "10px", "margin-right": "10px"}),
        html.Br(),



    dbc.Card([dbc.CardBody([html.H5("Considerando gli aspetti ambientali più rilevanti riportati in tabella e applicando gli step di normalizzazione e pesatura secondo la metodologia dell’Environmental Footprint, dal punto di vista ambientale", className="card-title",style={'text-align': 'center'})]),
        dbc.CardHeader(
            [html.H2(id='resultsent', className="card-title",style={'text-align': 'center'})]
        ),

        dbc.CardBody([html.H5("Questo miglioramento complessivo è dato dall’insieme di queste variazioni: ", className="card-title",style={'text-align': 'center'})])
    ], color="#B10D00",
        style={"width": "70%", "margin-right": "15%","margin-left": "15%", "margin-top": "60px", "color": "white"}, id= "resultcardresult"),
        dbc.Table([
        html.Thead(html.Tr(
                    [html.Th("Indicatore", style={'width': '50%'}),html.Th("UdM", style={'width': '20%'}), html.Th("Soluzione A", style={'width': '15%'}),
                     html.Th("Soluzione B", style={'width': '15%'}),

                     ])),
        html.Tr([

                         html.Td(dbc.Row([dbc.Col(html.Img(src = pil_image0, height="70px", width="70px"), width=2),dbc.Col(html.P('Acidificazione'))])),
                         html.Td(html.P("Mole of H+ eq.",style={"font-size":"16px"})),
                         html.Td(html.H5(id="GWPtotA0")),
                         html.Td(html.H5(id="GWPdf0"),id="colordf0", style={"color":"white","background-color":"red"}),


                    ]),
        html.Tr([

                         html.Td(dbc.Row([dbc.Col(html.Img(src = pil_image, height="70px", width="70px"), width=2),dbc.Col(html.P('Cambiamento climatico'))])),
                         html.Td(html.P("kg CO2 eq.",style={"font-size":"16px"})),
                         html.Td(html.H5(id="GWPtotA")),
                         html.Td(html.H5(id="GWPdf"),id="colordf", style={"color":"white","background-color":"red"}),


                    ]),
        html.Tr([

                html.Td(dbc.Row([dbc.Col(html.Img(src = pil_image2, height="70px", width="70px"), width=2),dbc.Col(html.P('Uso del suolo '))])),
            html.Td(html.P("Pt", style={"font-size": "16px"})),

            html.Td(html.H5(id="GWPtotA2")),
                html.Td(html.H5(id="GWPdf2"), id="colordf2", style={"color": "white", "background-color": "red"}),

            ]),
        html.Tr([

                html.Td(dbc.Row([dbc.Col(html.Img(src = pil_image3, height="70px", width="70px"), width=2),dbc.Col(html.P('Formazione di ozono fotochimico, salute umana '))])),
            html.Td(html.P("kg NMVOC eq.", style={"font-size": "16px"})),

            html.Td(html.H5(id="GWPtotA3")),
                html.Td(html.H5(id="GWPdf3"), id="colordf3", style={"color": "white", "background-color": "red"}),

            ]),
        html.Tr([

                html.Td(dbc.Row([dbc.Col(html.Img(src = pil_image4, height="70px", width="70px"), width=2),dbc.Col(html.P('Uso di risorse fossili'))])),
            html.Td(html.P("MJ", style={"font-size": "16px"})),

            html.Td(html.H5(id="GWPtotA4")),
                html.Td(html.H5(id="GWPdf4"), id="colordf4", style={"color": "white", "background-color": "red"}),

            ]),
        html.Tr([

                html.Td(dbc.Row([dbc.Col(html.Img(src = pil_image5, height="70px", width="70px"), width=2),dbc.Col(html.P('Particolato'))])),
            html.Td(html.P("Disease incidences", style={"font-size": "16px"})),

            html.Td(html.H5(id="GWPtotA5")),
                html.Td(html.H5(id="GWPdf5"), id="colordf5", style={"color": "white", "background-color": "red"}),

            ]),

        html.Tr([

                html.Td(dbc.Row([dbc.Col(html.Img(src = pil_image6, height="70px", width="70px"), width=2),dbc.Col(html.P('Uso acqua'))])),
            html.Td(html.P("m³ eq.", style={"font-size": "16px"})),

            html.Td(html.H5(id="GWPtotA6")),
                html.Td(html.H5(id="GWPdf6"), id="colordf6", style={"color": "white", "background-color": "red"}),

            ]),
        ],style={"width":"70%", "margin-left":"15%","margin-right":"15%","font-size":"16px"}, bordered=True),

    dbc.Button(dbc.Row([dbc.Col(html.Img(src=pil_image_pdf, height="32px", width="32px"), width=2),
                        dbc.Col(html.P("Manual", style={"margin-left": "10px"}))]), id="btnpdf", n_clicks=0,
               style={"float": "right", "margin-right": "30px", "height": "45px", "background-color":"#004e18"}),
    dcc.Download(id="downloadpdf"),
    html.Br(),

    html.Br(),
    html.Br(),

    html.Div(id='dashtable', style={'width': '75%', "float": "right","display":"None", "overflow": "scroll", "maxHeight": "170px",
                                    "margin-right": "20px"}),
    html.Br(),
    html.P("© Ecoinnovazione srl 2022. Tutti i diritti riservati", style={"margin-left": "10px", "font-size": "11px"}),
    html.Br(),



], style={'backgroundColor': colors['background']})
#-------------------------------------------------------------------------

@callback(

    Output(component_id='pwb', component_property='invalid'),
    Output(component_id='area', component_property='invalid'),
    Output(component_id='area2', component_property='invalid'),
    Output(component_id='area3', component_property='invalid'),
    Output(component_id='area4', component_property='invalid'),
    Output(component_id='input1', component_property='invalid'),
    Output(component_id='input2', component_property='invalid'),
    Output(component_id='input3', component_property='invalid'),
    Output(component_id='input4', component_property='invalid'),
    Output(component_id='input5', component_property='invalid'),
    Output(component_id='input6', component_property='invalid'),
    Output(component_id='input11', component_property='invalid'),
    Output(component_id='input22', component_property='invalid'),
    Output(component_id='input33', component_property='invalid'),
    Output(component_id='input44', component_property='invalid'),
    Output(component_id='input55', component_property='invalid'),
    Output(component_id='input66', component_property='invalid'),
    Output(component_id='areab', component_property='invalid'),
    Output(component_id='area2b', component_property='invalid'),
    Output(component_id='area3b', component_property='invalid'),
    Output(component_id='area4b', component_property='invalid'),
    Output(component_id='input1b', component_property='invalid'),
    Output(component_id='input2b', component_property='invalid'),
    Output(component_id='input3b', component_property='invalid'),
    Output(component_id='input4b', component_property='invalid'),
    Output(component_id='input5b', component_property='invalid'),
    Output(component_id='input6b', component_property='invalid'),
    Output(component_id='input11b', component_property='invalid'),
    Output(component_id='input22b', component_property='invalid'),
    Output(component_id='input33b', component_property='invalid'),
    Output(component_id='input44b', component_property='invalid'),
    Output(component_id='input55b', component_property='invalid'),
    Output(component_id='input66b', component_property='invalid'),
    Input(component_id='pwb', component_property='value'),
    Input(component_id='area', component_property='value'),
    Input(component_id='area2', component_property='value'),
    Input(component_id='area3', component_property='value'),
    Input(component_id='area4', component_property='value'),
    Input(component_id='input1', component_property='value'),
    Input(component_id='input2', component_property='value'),
    Input(component_id='input3', component_property='value'),
    Input(component_id='input4', component_property='value'),
    Input(component_id='input5', component_property='value'),
    Input(component_id='input6', component_property='value'),
    Input(component_id='input11', component_property='value'),
    Input(component_id='input22', component_property='value'),
    Input(component_id='input33', component_property='value'),
    Input(component_id='input44', component_property='value'),
    Input(component_id='input55', component_property='value'),
    Input(component_id='input66', component_property='value'),
    Input(component_id='areab', component_property='value'),
    Input(component_id='area2b', component_property='value'),
    Input(component_id='area3b', component_property='value'),
    Input(component_id='area4b', component_property='value'),
    Input(component_id='input1b', component_property='value'),
    Input(component_id='input2b', component_property='value'),
    Input(component_id='input3b', component_property='value'),
    Input(component_id='input4b', component_property='value'),
    Input(component_id='input5b', component_property='value'),
    Input(component_id='input6b', component_property='value'),
    Input(component_id='input11b', component_property='value'),
    Input(component_id='input22b', component_property='value'),
    Input(component_id='input33b', component_property='value'),
    Input(component_id='input44b', component_property='value'),
    Input(component_id='input55b', component_property='value'),
    Input(component_id='input66b', component_property='value'),

)
def inputpeso(pwb, input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, input11, input12, input13, input14, input15, input16,input1b, input2b, input3b, input4b, input5b, input6b, input7b, input8b, input9b, input10b, input11b, input12b, input13b, input14b, input15b, input16b):
    if (pwb == 0) or (pwb == None):
        output0 = True
    else:
        output0 = False

    if input1 ==0:
        output1 = True
    else:
        output1 = False
    if input2 ==0:
        output2 = True
    else:
        output2 = False
    if input3 ==0:
        output3 = True
    else:
        output3 = False
    if input4 ==0:
        output4 = True
    else:
        output4 =False
    if input5 ==0:
        output5 = True
    else:
        output5 = False
    if input6 ==0:
        output6 = True
    else:
        output6 = False
    if input7 ==0:
        output7 = True
    else:
        output7 = False
    if input8 ==0:
        output8 = True
    else:
        output8 = False
    if input9 ==0:
        output9 = True
    else:
        output9 = False
    if input10 ==0:
        output10 = True
    else:
        output10 = False
    if input11 ==0:
        output11 = True
    else:
        output11 = False
    if input12 ==0:
        output12 =True
    else:
        output12 = False
    if input13 ==0:
        output13 =True
    else:
        output13 = False
    if input14 ==0:
        output14 = True
    else:
        output14 = False
    if input15 ==0:
        output15 = True
    else:
        output15 = False
    if input16 ==0:
        output16 = True
    else:
        output16 = False
    if input1b ==0:
        output1b = True
    else:
        output1b = False
    if input2b ==0:
        output2b = True
    else:
        output2b = False
    if input3b ==0:
        output3b = True
    else:
        output3b = False
    if input4b ==0:
        output4b = True
    else:
        output4b = False
    if input5b ==0:
        output5b = True
    else:
        output5b = False
    if input6b ==0:
        output6b = True
    else:
        output6b = False
    if input7b ==0:
        output7b = True
    else:
        output7b = False
    if input8b ==0:
        output8b = True
    else:
        output8b= False
    if input9b ==0:
        output9b = True
    else:
        output9b = False
    if input10b ==0:
        output10b = True
    else:
        output10b = False
    if input11b ==0:
        output11b = True
    else:
        output11b = False
    if input12b ==0:
        output12b = True
    else:
        output12b = False
    if input13b ==0:
        output13b = True
    else:
        output13b = False
    if input14b ==0:
        output14b = True
    else:
        output14b = False
    if input15b ==0:
        output15b = True
    else:
        output15b = False
    if input16b ==0:
        output16b = True
    else:
        output16b = False

    return output0, output1, output2, output3, output4, output5, output6, output7, output8, output9, output10, output11, output12, output13, output14, output15, output16, output1b, output2b, output3b, output4b, output5b, output6b, output7b, output8b, output9b, output10b, output11b, output12b, output13b, output14b, output15b, output16b

@callback(

    Output(component_id='downloadpdf', component_property='data'),
    Input("btnpdf", 'n_clicks'),

)
def dlpdf(btnpdf):
    if btnpdf != 0:
        return dcc.send_file("assets/Amadori_Manual.pdf")


@callback(

    Output(component_id='stype4', component_property='value'),
    Output(component_id='stype4b', component_property='value'),
    Output(component_id='stype2', component_property='disabled'),
    Output(component_id='stype2b', component_property='disabled'),
    Output(component_id='stype2', component_property='value'),
    Output(component_id='stype2b', component_property='value'),
    [Input("rinput", 'value'),
     Input("rinputb", 'value'),
     Input("stype2", 'value'),
     Input("stype2b", 'value')],
)
def update_preconsumo(rinput1, rinput2, input1, input2):
    if rinput1 == 0:
        post = 0
        pre = True
        preval = 0
    else:
        post = 100-input1
        pre = False
        preval = input1
    if rinput2 == 0:
        postb = 0
        preb = True
        prevalb = 0
    else:
        postb = 100-input2
        preb = False
        prevalb = input2

    return post, postb, pre, preb, preval, prevalb

@callback(

    Output(component_id='topsum', component_property='children'),
    Output(component_id='topsum', component_property='color'),
    Output(component_id='botsum', component_property='children'),
    Output(component_id='botsum', component_property='color'),
    Output(component_id='topsumb', component_property='children'),
    Output(component_id='topsumb', component_property='color'),
    Output(component_id='botsumb', component_property='children'),
    Output(component_id='botsumb', component_property='color'),
    [Input(component_id='pet1', component_property='value'),
     Input(component_id='pp1', component_property='value'),
     Input(component_id='pa1', component_property='value'),
     Input(component_id='pvc1', component_property='value'),
     Input(component_id='pe1', component_property='value'),
     Input(component_id='evoh1', component_property='value'),
     Input(component_id='pet2', component_property='value'),
     Input(component_id='pp2', component_property='value'),
     Input(component_id='pa2', component_property='value'),
     Input(component_id='pvc2', component_property='value'),
     Input(component_id='pe2', component_property='value'),
     Input(component_id='evoh2', component_property='value'),
     Input(component_id='pet1b', component_property='value'),
     Input(component_id='pp1b', component_property='value'),
     Input(component_id='pa1b', component_property='value'),
     Input(component_id='pvc1b', component_property='value'),
     Input(component_id='pe1b', component_property='value'),
     Input(component_id='evoh1b', component_property='value'),
     Input(component_id='pet2b', component_property='value'),
     Input(component_id='pp2b', component_property='value'),
     Input(component_id='pa2b', component_property='value'),
     Input(component_id='pvc2b', component_property='value'),
     Input(component_id='pe2b', component_property='value'),
     Input(component_id='evoh2b', component_property='value')
     ],
)
def update_preconsumo(input11,input12,input13,input14,input15,input16, input21, input22,input23,input24,input25,input26,
                      input11b,input12b,input13b,input14b,input15b,input16b, input21b, input22b,input23b,input24b,input25b,input26b):
    sum1 = input11+input12+input13+input14+input15+input16
    sum2 = input21+input22+input23+input24+input25+input26
    sum1b = input11b + input12b + input13b + input14b + input15b + input16b
    sum2b = input21b + input22b + input23b + input24b + input25b + input26b
    if sum1 > 100:
        text1 = "Sum: {} %".format(sum1)
        color1 = "danger"
    if sum1 < 100:
        text1 = "Sum: {} %".format(sum1)
        color1 = "danger"
    if sum1 == 100:
        text1 = "Sum: {} %".format(sum1)
        color1 = "success"
    if sum2 > 100:
        text2 = "Sum: {} %".format(sum2)
        color2 = "danger"
    if sum2 < 100:
        text2 = "Sum: {} %".format(sum2)
        color2 = "danger"
    if sum2 == 100:
        text2 = "Sum: {} %".format(sum2)
        color2 = "success"
    if sum1b > 100:
        text1b = "Sum: {} %".format(sum1b)
        color1b = "danger"
    if sum1b < 100:
        text1b = "Sum: {} %".format(sum1b)
        color1b = "danger"
    if sum1b == 100:
        text1b = "Sum: {} %".format(sum1b)
        color1b = "success"
    if sum2b > 100:
        text2b = "Sum: {} %".format(sum2b)
        color2b = "danger"
    if sum2b < 100:
        text2b = "Sum: {} %".format(sum2b)
        color2b = "danger"
    if sum2b == 100:
        text2b = "Sum: {} %".format(sum2b)
        color2b = "success"

    return text1, color1, text2, color2, text1b, color1b, text2b, color2b


#-----------------------------------------------------------------
@callback(
    Output(component_id='dashtable', component_property='children'),
    Output(component_id="sessiondataexcel", component_property="data"),
    Output(component_id="sessioncolumnexcel", component_property="data"),
    Output(component_id='card1', component_property='children'),
    Output(component_id='alertmsg', component_property='children'),
    Output(component_id='card2', component_property='children'),
    Output(component_id='card1b', component_property='children'),
    Output(component_id='alertmsgb', component_property='children'),
    Output(component_id='card2b', component_property='children'),
    Output(component_id='resultsent', component_property='children'),
    Output(component_id='colordf0', component_property='style'),
    Output(component_id='GWPtotA0', component_property='children'),
    Output(component_id='GWPdf0', component_property='children'),
    Output(component_id='colordf', component_property='style'),
    Output(component_id='GWPtotA', component_property='children'),
    Output(component_id='GWPdf', component_property='children'),
    Output(component_id='colordf2', component_property='style'),
    Output(component_id='GWPtotA2', component_property='children'),
    Output(component_id='GWPdf2', component_property='children'),
    Output(component_id='colordf3', component_property='style'),
    Output(component_id='GWPtotA3', component_property='children'),
    Output(component_id='GWPdf3', component_property='children'),
    Output(component_id='colordf4', component_property='style'),
    Output(component_id='GWPtotA4', component_property='children'),
    Output(component_id='GWPdf4', component_property='children'),
    Output(component_id='colordf5', component_property='style'),
    Output(component_id='GWPtotA5', component_property='children'),
    Output(component_id='GWPdf5', component_property='children'),
    Output(component_id='colordf6', component_property='style'),
    Output(component_id='GWPtotA6', component_property='children'),
    Output(component_id='GWPdf6', component_property='children'),
    Output(component_id='indicator-graphic', component_property='figure'),
    Output(component_id='indicator-graphic2', component_property='figure'),
    Output(component_id="session", component_property="data"),
    Output(component_id="sessiondata", component_property="data"),
    Output(component_id="sessioncolumn", component_property="data"),
    Output(component_id="sessionweight", component_property="data"),
    Output(component_id="sessionpeso", component_property="data"),
    Output(component_id="sessionpesob", component_property="data"),
    Output(component_id="resultcardresult", component_property="color"),
    [Input("submit-val", 'n_clicks'),
     State(component_id='tavolo1', component_property='value'),
     State(component_id='tavolo2', component_property='value'),
     State(component_id='check1', component_property='value'),
     State(component_id='dd1', component_property='value'),
     State(component_id='stype2', component_property='value'),
     State(component_id='stype4', component_property='value'),
     State(component_id='rinput', component_property='value'),
     State(component_id='input1', component_property='value'),
     State(component_id='dd11', component_property='value'),
     State(component_id='check2', component_property='value'),
     State(component_id='dd2', component_property='value'),
     State(component_id='input2', component_property='value'),
     State(component_id='check3', component_property='value'),
     State(component_id='input3', component_property='value'),
     State(component_id='area', component_property='value'),
     State(component_id='check4', component_property='value'),
     State(component_id='input4', component_property='value'),
     State(component_id='area2', component_property='value'),
     State(component_id='check5', component_property='value'),
     State(component_id='dd5', component_property='value'),
     State(component_id='input5', component_property='value'),
     State(component_id='area3', component_property='value'),
     State(component_id='check6', component_property='value'),
     State(component_id='dd6', component_property='value'),
     State(component_id='input6', component_property='value'),
     State(component_id='area4', component_property='value'),
     State(component_id='pet1', component_property='value'),
     State(component_id='pp1', component_property='value'),
     State(component_id='pa1', component_property='value'),
     State(component_id='pvc1', component_property='value'),
     State(component_id='pe1', component_property='value'),
     State(component_id='evoh1', component_property='value'),
     State(component_id='pet2', component_property='value'),
     State(component_id='pp2', component_property='value'),
     State(component_id='pa2', component_property='value'),
     State(component_id='pvc2', component_property='value'),
     State(component_id='pe2', component_property='value'),
     State(component_id='evoh2', component_property='value'),
     State(component_id='dd22', component_property='value'),
     State(component_id='dd33', component_property='value'),
     State(component_id='dd44', component_property='value'),
     State(component_id='dd55', component_property='value'),
     State(component_id='dd66', component_property='value'),
     State(component_id='input11', component_property='value'),
     State(component_id='input22', component_property='value'),
     State(component_id='input33', component_property='value'),
     State(component_id='input44', component_property='value'),
     State(component_id='input55', component_property='value'),
     State(component_id='input66', component_property='value'),
     State(component_id='check1b', component_property='value'),
     State(component_id='dd1b', component_property='value'),
     State(component_id='stype2b', component_property='value'),
     State(component_id='stype4b', component_property='value'),
     State(component_id='rinputb', component_property='value'),
     State(component_id='input1b', component_property='value'),
     State(component_id='dd11b', component_property='value'),
     State(component_id='check2b', component_property='value'),
     State(component_id='dd2b', component_property='value'),
     State(component_id='input2b', component_property='value'),
     State(component_id='check3b', component_property='value'),
     State(component_id='input3b', component_property='value'),
     State(component_id='areab', component_property='value'),
     State(component_id='check4b', component_property='value'),
     State(component_id='input4b', component_property='value'),
     State(component_id='area2b', component_property='value'),
     State(component_id='check5b', component_property='value'),
     State(component_id='dd5b', component_property='value'),
     State(component_id='input5b', component_property='value'),
     State(component_id='area3b', component_property='value'),
     State(component_id='check6b', component_property='value'),
     State(component_id='dd6b', component_property='value'),
     State(component_id='input6b', component_property='value'),
     State(component_id='area4b', component_property='value'),
     State(component_id='pet1b', component_property='value'),
     State(component_id='pp1b', component_property='value'),
     State(component_id='pa1b', component_property='value'),
     State(component_id='pvc1b', component_property='value'),
     State(component_id='pe1b', component_property='value'),
     State(component_id='evoh1b', component_property='value'),
     State(component_id='pet2b', component_property='value'),
     State(component_id='pp2b', component_property='value'),
     State(component_id='pa2b', component_property='value'),
     State(component_id='pvc2b', component_property='value'),
     State(component_id='pe2b', component_property='value'),
     State(component_id='evoh2b', component_property='value'),
     State(component_id='dd22b', component_property='value'),
     State(component_id='dd33b', component_property='value'),
     State(component_id='dd44b', component_property='value'),
     State(component_id='dd55b', component_property='value'),
     State(component_id='dd66b', component_property='value'),
     State(component_id='input11b', component_property='value'),
     State(component_id='input22b', component_property='value'),
     State(component_id='input33b', component_property='value'),
     State(component_id='input44b', component_property='value'),
     State(component_id='input55b', component_property='value'),
     State(component_id='input66b', component_property='value'),
     State(component_id='pwb', component_property='value'),

     ],
     prevent_initial_call=True,
     suppress_callback_exceptions = True)
def update_avali(inputdokmeh,tavolo1,tavolo2, input_1, input_11, input_2, input_3, input_4, input_111, traspvas,
input_21, input_22, input_222, input_31,  input_333, area3, input_41,  input_444, area4,
                      input_51, input_55, input_555, area5, input_61, input_66, input_666, area6,
                      pet1, pp1, pa1, pvc1, pe1, evoh1,
                      pet2, pp2, pa2, pvc2, pe2, evoh2,
                      trasppad, trasptop, traspbot, traspsup, traspbus,
                      cost1, cost2, cost3, cost4, cost5, cost6,
input_1b, input_11b, input_2b, input_3b, input_4b, input_111b, traspvasb,
input_21b, input_22b, input_222b, input_31b,  input_333b, area3b, input_41b,  input_444b, area4b,
                      input_51b, input_55b, input_555b, area5b, input_61b, input_66b, input_666b, area6b,
                      pet1b, pp1b, pa1b, pvc1b, pe1b, evoh1b,
                      pet2b, pp2b, pa2b, pvc2b, pe2b, evoh2b,
                      trasppadb, trasptopb, traspbotb, traspsupb, traspbusb,
                      cost1b, cost2b, cost3b, cost4b, cost5b, cost6b, pwb

                 ):

    Inputexcel = pd.DataFrame({

        "Soluzione":["A ({})".format(not tavolo1), "A ({})".format(not tavolo1), "A ({})".format(not tavolo1), "A ({})".format(not tavolo1), "A ({})".format(not tavolo1), "A ({})".format(not tavolo1), "B ({})".format(not tavolo2), "B ({})".format(not tavolo2), "B ({})".format(not tavolo2), "B ({})".format(not tavolo2), "B ({})".format(not tavolo2),"B ({})".format(not tavolo2) ],
        "Componente": ["Vassoio preformato", "Pad assorbente", "Top flessibile", "Bottom flessibile", "Supporto in cellulosa", "Busta", "Vassoio preformato", "Pad assorbente", "Top flessibile", "Bottom flessibile", "Supporto in cellulosa", "Busta"],
        "Status": [input_1, input_21, input_31, input_41, input_51, input_61, input_1b, input_21b, input_31b, input_41b, input_51b, input_61b],
        "Composizione" : [input_11, input_22, "{}% PET, {}% PP, {}% PA, {}% PVC, {}% PE, {}% EVOH/EVA".format(pet1, pp1, pa1, pvc1, pe1, evoh1) , "{}% PET, {}% PP, {}% PA, {}% PVC, {}% PE, {}% EVOH/EVA".format(pet2, pp2, pa2, pvc2, pe2, evoh2), input_55, input_66, input_11b, input_22b, "{}% PET, {}% PP, {}% PA, {}% PVC, {}% PE, {}% EVOH/EVA".format(pet1b, pp1b, pa1b, pvc1b, pe1b, evoh1b) , "{}% PET, {}% PP, {}% PA, {}% PVC, {}% PE, {}% EVOH/EVA".format(pet2b, pp2b, pa2b, pvc2b, pe2b, evoh2b), input_55b, input_66b ],
        "Specifiche" : ["{}% contenuto riciclato {}% pre-consumer {}% post-consumer".format(input_4, input_3, input_2), "None", "area: {} m2".format(area3), "area: {} m2".format(area4), "area: {} m2".format(area5), "area: {} m2".format(area6), "{}% contenuto riciclato {}% pre-consumer {}% post-consumer".format(input_4b, input_3b, input_2b), "None", "area: {} m2".format(area3b), "area: {} m2".format(area4b), "area: {} m2".format(area5b), "area: {} m2".format(area6b)],
        "Peso componente" : ["{} g".format(input_111), "{} g".format(input_222), "{} g/m2".format(input_333), "{} g/m2".format(input_444), "{} g/m2".format(input_555), "{} g/m2".format(input_666), "{} g".format(input_111b), "{} g".format(input_222b), "{} g/m2".format(input_333b), "{} g/m2".format(input_444b), "{} g/m2".format(input_555b), "{} g/m2".format(input_666b)],
        "Prezzo" : ["{} €/pezzo".format(cost1), "{} €/pezzo".format(cost2), "{} €/m2".format(cost3), "{} €/m2".format(cost4), "{} €/m2".format(cost5), "{} €/m2".format(cost6), "{} €/pezzo".format(cost1b), "{} €/pezzo".format(cost2b), "{} €/m2".format(cost3b), "{} €/m2".format(cost4b), "{} €/m2".format(cost5b), "{} €/m2".format(cost6b)],
        "Distanza di Fornitura": ["{} km".format(traspvas), "{} km".format(trasppad), "{} km".format(trasptop), "{} km".format(traspbot), "{} km".format(traspsup), "{} km".format(traspbus), "{} km".format(traspvasb), "{} km".format(trasppadb), "{} km".format(trasptopb), "{} km".format(traspbotb), "{} km".format(traspsupb), "{} km".format(traspbusb)]

    })



    impacts = ["Acidificazione", "Cambiamento climatico tot"
               , "Uso del suolo", "Particolato",
               "Formazione di ozono fotochimico, salute umana", "Uso di risorse fossili",
                "Uso acqua"]



    if (inputdokmeh != 0) & (tavolo1==False) &(input_1 == True) & (input_11 == 'PET'):

        Vassoio = []
        EoL_Vassoio = []
        Trasporto_Vassoio = []
        vaspeso = input_111* 0.001
        vasprez = cost1


        for i in impacts:
            impact_vassoio = ((
                                      ((input_4 * 0.01)
                                     *
                                     (
                                             ( (df.loc[(df['Componente'] == 'r-PET-pre')][i].values[0] * 0.5 + (0.5) * (df.loc[(df['Componente'] == 'PET-virgin')][i].values[0] * 0.9)) * input_3 * 0.01) +
                                             ( (df.loc[(df['Componente'] == 'r-PET-post')][i].values[0] * 0.5 + (0.5) * (df.loc[(df['Componente'] == 'PET-virgin')][i].values[0] * 0.9)) * input_2 * 0.01)
                                     ))
                                     +
                                     (df.loc[(df['Componente'] == 'PET-virgin')][i].values[0] * (100 - input_4) * 0.01)
                              )/(0.98) + (df.loc[(df['Componente'] == 'lamination vassoio')][i].values[0])) * (input_111 * 0.001)
            eol = ((df.loc[(df['Composizione'] == 'EoL PET')][i].values[0] * 1) * (input_111 * 0.001))
            trasp = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (traspvas * input_111 * 0.001)
            Trasporto_Vassoio.append(trasp)
            EoL_Vassoio.append(eol)
            Vassoio.append(impact_vassoio)


    elif (inputdokmeh != 0) & (tavolo1==False)& (input_1 == True) & (input_11 == 'PET/PE'):

        Vassoio = []
        EoL_Vassoio = []
        Trasporto_Vassoio = []
        vaspeso = input_111* 0.001
        vasprez = cost1


        for i in impacts:

            impact_vassoio = (
                    ((
                            0.8 *
                     (
                         (
                                 (
                                         (input_4 * 0.01) *
                                         (
                                          ((df.loc[(df['Componente'] == 'r-PET-pre')][i].values[0] * 0.5 + (0.5) * (df.loc[(df['Componente'] == 'PET-virgin')][i].values[0] * 0.9)) * input_3 * 0.01)
                                          +
                                          ((df.loc[(df['Componente'] == 'r-PET-post')][i].values[0] * 0.5 + (0.5) * (df.loc[(df['Componente'] == 'PET-virgin')][i].values[0] * 0.9)) * input_2 * 0.01)
                                         )
                                 )
                                 +
                                 (df.loc[(df['Componente'] == 'PET-virgin')][i].values[0] * (100 - input_4) * 0.01)
                         )
                     )
                     + 0.2 * (df.loc[(df['Composizione'] == 'PET/PE')][i].values[0] *1)
                    )/0.98 + df.loc[(df['Componente'] == 'lamination vassoio')][i].values[0])
                    * (input_111 * 0.001)
            )
            eol = (df.loc[(df['Composizione'] == 'EoL PET/PE')][i].values[0]) * (input_111 * 0.001)
            trasp = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (traspvas * input_111 * 0.001)
            Trasporto_Vassoio.append(trasp)
            EoL_Vassoio.append(eol)
            Vassoio.append(impact_vassoio)

    elif (inputdokmeh != 0)& (tavolo1==False) & (input_1 == True) & (input_11 == 'XPS'):

        Vassoio = []
        EoL_Vassoio = []
        Trasporto_Vassoio = []
        vaspeso = input_111* 0.001
        vasprez = cost1


        for i in impacts:
            impact_vassoio = ((
                                     (input_4 * 0.01)
                                     *
                                     (
                                             ( (df.loc[(df['Componente'] == 'r-XPS-pre')][i].values[0] * 0.5 + (0.5) * (df.loc[(df['Composizione'] == 'XPS')][i].values[0] * 0.9)) * input_3 * 0.01) +
                                             ( (df.loc[(df['Componente'] == 'r-XPS-post')][i].values[0] * 0.5 + (0.5) * (df.loc[(df['Composizione'] == 'XPS')][i].values[0] * 0.9)) * input_2 * 0.01)
                                     )
                                     +
                                     (df.loc[(df['Composizione'] == 'XPS')][i].values[0] * (100 - input_4) * 0.01)
                              )/0.98 + df.loc[(df['Componente'] == 'lamination vassoio')][i].values[0]) * (input_111 * 0.001)
            eol = ((df.loc[(df['Composizione'] == 'EoL XPS')][i].values[0] * 1)  * (input_111 * 0.001))
            trasp = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (traspvas * input_111 * 0.001)
            Trasporto_Vassoio.append(trasp)
            EoL_Vassoio.append(eol)

            Vassoio.append(impact_vassoio)

    elif (inputdokmeh != 0)& (tavolo1==False) & (input_1 == True):

        EoL_Vassoio = []
        Vassoio = []
        Trasporto_Vassoio = []
        vaspeso = input_111* 0.001
        vasprez = cost1


        for i in impacts:

            impact_vassoio= df.loc[(df['Composizione'] == input_11)][i].values[0] * (input_111 * 0.001)
            eol = ((df.loc[(df['Componente'] == 'EoL') & (df['Specifiche'] == input_11)][i].values[0] * 1)  * (input_111 * 0.001))
            trasp = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (traspvas * input_111 * 0.001)
            Trasporto_Vassoio.append(trasp)
            EoL_Vassoio.append(eol)
            Vassoio.append(impact_vassoio)

    else:
        Trasporto_Vassoio = [0,0,0,0,0,0,0]
        EoL_Vassoio = [0,0,0,0,0,0,0]
        Vassoio = [0,0,0,0,0,0,0]
        vaspeso = 0
        vasprez = 0

    if (inputdokmeh != 0)& (tavolo2==False) & (input_1b == True) & (input_11b == 'PET'):


        Vassoiob = []
        EoL_Vassoiob = []
        Trasporto_Vassoiob = []
        vaspesob = input_111b * 0.001
        vasprezb = cost1b

        for i in impacts:
            impact_vassoiob = ((
                                          ((input_4b * 0.01)
                                           *
                                           (
                                                   ((df.loc[(df['Componente'] == 'r-PET-pre')][i].values[0] * 0.5 + (
                                                       0.5) * (df.loc[(df['Componente'] == 'PET-virgin')][i].values[
                                                                   0] * 0.9)) * input_3b * 0.01) +
                                                   ((df.loc[(df['Componente'] == 'r-PET-post')][i].values[0] * 0.5 + (
                                                       0.5) * (df.loc[(df['Componente'] == 'PET-virgin')][i].values[
                                                                   0] * 0.9)) * input_2b * 0.01)
                                           ))
                                          +
                                          (df.loc[(df['Componente'] == 'PET-virgin')][i].values[0] * (
                                                      100 - input_4b) * 0.01)
                                  ) / (0.98) + (df.loc[(df['Componente'] == 'lamination vassoio')][i].values[0])) * (
                                             input_111b * 0.001)
            eolb = ((df.loc[(df['Composizione'] == 'EoL PET')][i].values[0] * 1) * (input_111b * 0.001))
            traspb = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (traspvasb * input_111b * 0.001)
            Trasporto_Vassoiob.append(traspb)
            EoL_Vassoiob.append(eolb)
            Vassoiob.append(impact_vassoiob)

        #       return Vassoio[0], Vassoio[1], Vassoio[2], Vassoio[3], Vassoio[4], Vassoio[5], Vassoio[6], Vassoio[7],Vassoio[8], Vassoio[9], Vassoio[10], Vassoio[11], Vassoio[12], Vassoio[13], Vassoio[14], Vassoio[15], Vassoio[16], Vassoio[17], Vassoio[18]

    elif (inputdokmeh != 0)& (tavolo2==False) & (input_1b == True) & (input_11b == 'PET/PE'):

        Vassoiob = []
        EoL_Vassoiob = []
        Trasporto_Vassoiob = []
        vaspesob = input_111b * 0.001
        vasprezb = cost1b

        for i in impacts:
            impact_vassoiob = (
                        ((
                                 0.8 *
                                 (
                                     (
                                             (
                                                     (input_4b * 0.01) *
                                                     (
                                                             ((df.loc[(df['Componente'] == 'r-PET-pre')][i].values[
                                                                   0] * 0.5 + (0.5) * (
                                                                           df.loc[(df['Componente'] == 'PET-virgin')][
                                                                               i].values[0] * 0.9)) * input_3b * 0.01)
                                                             +
                                                             ((df.loc[(df['Componente'] == 'r-PET-post')][i].values[
                                                                   0] * 0.5 + (0.5) * (
                                                                           df.loc[(df['Componente'] == 'PET-virgin')][
                                                                               i].values[0] * 0.9)) * input_2b * 0.01)
                                                     )
                                             )
                                             +
                                             (df.loc[(df['Componente'] == 'PET-virgin')][i].values[0] * (
                                                         100 - input_4b) * 0.01)
                                     )
                                 )
                                 + 0.2 * (df.loc[(df['Composizione'] == 'PET/PE')][i].values[0] * 1)
                         ) / 0.98 + df.loc[(df['Componente'] == 'lamination vassoio')][i].values[0])
                        * (input_111b * 0.001)
                )
            eolb = ((df.loc[(df['Composizione'] == 'EoL PET')][i].values[0] * 0.8) + (
                            df.loc[(df['Composizione'] == 'EoL PE')][i].values[0] * 0.2)) * (input_111b * 0.001)
            traspb = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (traspvasb * input_111b * 0.001)
            Trasporto_Vassoiob.append(traspb)
            EoL_Vassoiob.append(eolb)
            Vassoiob.append(impact_vassoiob)

    elif (inputdokmeh != 0)& (tavolo2==False) & (input_1b == True) & (input_11b == 'XPS'):

        Vassoiob = []
        EoL_Vassoiob = []
        Trasporto_Vassoiob = []
        vaspesob = input_111b * 0.001
        vasprezb = cost1b

        for i in impacts:
            impact_vassoiob = ((
                                          (input_4b * 0.01)
                                          *
                                          (
                                                  ((df.loc[(df['Componente'] == 'r-XPS-pre')][i].values[0] * 0.5 + (
                                                      0.5) * (df.loc[(df['Composizione'] == 'XPS')][i].values[
                                                                  0] * 0.9)) * input_3b * 0.01) +
                                                  ((df.loc[(df['Componente'] == 'r-XPS-post')][i].values[0] * 0.5 + (
                                                      0.5) * (df.loc[(df['Composizione'] == 'XPS')][i].values[
                                                                  0] * 0.9)) * input_2b * 0.01)
                                          )
                                          +
                                          (df.loc[(df['Composizione'] == 'XPS')][i].values[0] * (100 - input_4b) * 0.01)
                                  ) / 0.98 + df.loc[(df['Componente'] == 'lamination vassoio')][i].values[0]) * (
                                             input_111b * 0.001)
            eolb = ((df.loc[(df['Composizione'] == 'EoL XPS')][i].values[0] * 1) * (input_111b * 0.001))
            traspb = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (traspvasb * input_111b * 0.001)
            Trasporto_Vassoiob.append(traspb)
            EoL_Vassoiob.append(eolb)

            Vassoiob.append(impact_vassoiob)

    elif (inputdokmeh != 0)& (tavolo2==False) & (input_1b == True):

        EoL_Vassoiob = []
        Vassoiob = []
        Trasporto_Vassoiob = []
        vaspesob = input_111b * 0.001
        vasprezb = cost1b

        for i in impacts:
            impact_vassoiob = df.loc[(df['Composizione'] == input_11b)][i].values[0] * (input_111b * 0.001)
            eolb = ((df.loc[(df['Componente'] == 'EoL') & (df['Specifiche'] == input_11b)][i].values[0] * 1) * (
                            input_111b * 0.001))
            traspb = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (traspvasb * input_111b * 0.001)
            Trasporto_Vassoiob.append(traspb)
            EoL_Vassoiob.append(eolb)
            Vassoiob.append(impact_vassoiob)

    else:
            Trasporto_Vassoiob = [0,0,0,0,0,0,0]
            EoL_Vassoiob = [0,0,0,0,0,0,0]
            Vassoiob = [0,0,0,0,0,0,0]
            vaspesob = 0
            vasprezb = 0


    if (inputdokmeh != 0)& (tavolo1==False) & (input_21 == True):

        Pad = []
        Pad_EoL = []
        Pad_Trasporto = []
        padpeso = input_222 * 0.001
        padprez = cost2
        for i in impacts:
            impact_pad = df.loc[(df['Composizione'] == input_22)][i].values[0] * (input_222 * 0.001)
            eol = ((df.loc[(df['Componente'] == 'EoL') & (df['Specifiche'] == input_22)][i].values[0] * 1) * (
                        input_222 * 0.001))
            trasp = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (trasppad * input_222 * 0.001)
            Pad_Trasporto.append(trasp)
            Pad_EoL.append(eol)
            Pad.append(impact_pad)

    else:
        Pad = [0,0,0,0,0,0,0]
        Pad_EoL = [0,0,0,0,0,0,0]
        Pad_Trasporto = [0,0,0,0,0,0,0]
        padpeso = 0
        padprez = 0

    if (inputdokmeh != 0)& (tavolo1==False) &(pet1+pp1+pa1+pvc1+pe1+evoh1 !=0)& (input_31 == True):

        Top = []
        Top_EoL = []
        Top_Trasporto = []
        toppeso = input_333 * area3 * 0.001
        topprez = cost3 * area3


        for i in impacts:
            impact_top = ( (((df.loc[(df['Composizione'] == "PET1")][i].values[0] * (pet1*0.01)) +
                           (df.loc[(df['Composizione'] == "PP1")][i].values[0] * (pp1*0.01)) +
                           (df.loc[(df['Composizione'] == "PA1")][i].values[0] * (pa1*0.01)) +
                           (df.loc[(df['Composizione'] == "PVC1")][i].values[0] * (pvc1*0.01)) +
                           (df.loc[(df['Composizione'] == "PE1")][i].values[0] * (pe1*0.01)) +
                           (df.loc[(df['Composizione'] == "EVA/EVOH1")][i].values[0] * (evoh1*0.01)))/0.96) +
                           df.loc[(df['Componente'] == 'lamination topbot')][i].values[0]

                           ) * (input_333* area3 * 0.001)
            trasp = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (trasptop * input_333* area3 * 0.001)
            Top_Trasporto.append(trasp)

            eol = (((df.loc[(df['Composizione'] == "EoL PET")][i].values[0] * (pet1 * 0.01)) +
                           (df.loc[(df['Composizione'] == "EoL PP")][i].values[0] * (pp1 * 0.01)) +
                           (df.loc[(df['Composizione'] == "EoL PA")][i].values[0] * (pa1 * 0.01)) +
                           (df.loc[(df['Composizione'] == "EoL PVC")][i].values[0] * (pvc1 * 0.01)) +
                           (df.loc[(df['Composizione'] == "EoL PE")][i].values[0] * (pe1 * 0.01)) +
                           (df.loc[(df['Composizione'] == "EoL EVOH")][i].values[0] * (evoh1 * 0.01)))) * (input_333 * area3 * 0.001)
            Top_EoL.append(eol)
            Top.append(impact_top)


    else:
        Top = [0,0,0,0,0,0,0]
        Top_EoL = [0,0,0,0,0,0,0]
        Top_Trasporto = [0,0,0,0,0,0,0]
        toppeso = 0
        topprez = 0

    if (inputdokmeh != 0)& (tavolo1==False)&(pet2+pp2+pa2+pvc2+pe2+evoh2 !=0) & (input_41 == True):

        Bottom = []
        Bottom_EoL = []
        Bottom_Trasporto = []
        botpeso = input_444 * area4 * 0.001
        botprez = cost4 * area4



        for i in impacts:
            impact_bottom = ((((df.loc[(df['Composizione'] == "PET1")][i].values[0] * (pet2 * 0.01)) +
                           (df.loc[(df['Composizione'] == "PP1")][i].values[0] * (pp2 * 0.01)) +
                           (df.loc[(df['Composizione'] == "PA1")][i].values[0] * (pa2 * 0.01)) +
                           (df.loc[(df['Composizione'] == "PVC1")][i].values[0] * (pvc2 * 0.01)) +
                           (df.loc[(df['Composizione'] == "PE1")][i].values[0] * (pe2 * 0.01)) +
                           (df.loc[(df['Composizione'] == "EVA/EVOH2")][i].values[0] * (evoh2 * 0.01))) / 0.96) +
                          df.loc[(df['Componente'] == 'lamination topbot')][i].values[0]

                          ) * (input_444 * area4 * 0.001)
            eol = (((df.loc[(df['Composizione'] == "EoL PET")][i].values[0] * (pet2 * 0.01)) +
                    (df.loc[(df['Composizione'] == "EoL PP")][i].values[0] * (pp2 * 0.01)) +
                    (df.loc[(df['Composizione'] == "EoL PA")][i].values[0] * (pa2 * 0.01)) +
                    (df.loc[(df['Composizione'] == "EoL PVC")][i].values[0] * (pvc2 * 0.01)) +
                    (df.loc[(df['Composizione'] == "EoL PE")][i].values[0] * (pe2 * 0.01)) +
                    (df.loc[(df['Composizione'] == "EoL EVOH")][i].values[0] * (evoh2 * 0.01)))) * (
                              input_444 * area4 * 0.001)
            trasp = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (traspbot * input_444 * area4 * 0.001)
            Bottom_Trasporto.append(trasp)
            Bottom_EoL.append(eol)
            Bottom.append(impact_bottom)

    else:
        Bottom = [0,0,0,0,0,0,0]
        Bottom_EoL = [0,0,0,0,0,0,0]
        Bottom_Trasporto = [0,0,0,0,0,0,0]
        botpeso = 0
        botprez = 0


    if (inputdokmeh != 0)& (tavolo1==False) & (input_51 == True):

        Supporto = []
        Supporto_EoL = []
        Supporto_Trasporto = []
        suppeso = input_555 * area5 * 0.001
        supprez = cost5 * area5


        for i in impacts:
            impact_supporto = df.loc[(df['Composizione'] == input_55)][i].values[0] * (input_555 * area5 * 0.001)
            eol = ((df.loc[(df['Componente'] == 'EoL') & (df['Specifiche'] == input_55)][i].values[0] * 1) * (
                        input_555 * area5 * 0.001))
            trasp = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (traspsup * input_555 * area5 * 0.001)
            Supporto_Trasporto.append(trasp)
            Supporto_EoL.append(eol)
            Supporto.append(impact_supporto)

    else:
        Supporto = [0,0,0,0,0,0,0]
        Supporto_EoL = [0,0,0,0,0,0,0]
        Supporto_Trasporto = [0,0,0,0,0,0,0]
        suppeso = 0
        supprez = 0


    if (inputdokmeh != 0)& (tavolo1==False) & (input_61 == True):

        Busta = []
        Busta_EoL = []
        Busta_Trasporto = []
        bustapeso = input_666 * area6 * 0.001
        bustaprez = cost6 * area6

        for i in impacts:
            impact_busta = df.loc[(df['Composizione'] == input_66)][i].values[0] * (input_666 * area6 * 0.001)
            eol = ((df.loc[(df['Componente'] == 'EoL') & (df['Specifiche'] == input_66)][i].values[0] * 1) * (
                    input_666 * area6 * 0.001))
            trasp = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (traspbus * input_666 * area6 * 0.001)
            Busta_Trasporto.append(trasp)
            Busta_EoL.append(eol)
            Busta.append(impact_busta)


    else:
        Busta = [0,0,0,0,0,0,0]
        Busta_EoL = [0,0,0,0,0,0,0]
        Busta_Trasporto = [0,0,0,0,0,0,0]
        bustapeso = 0
        bustaprez = 0


    if (inputdokmeh != 0)& (tavolo2==False) & (input_21b == True):

        Padb = []
        Pad_EoLb = []
        Pad_Trasportob = []
        padpesob = input_222b * 0.001
        padprezb = cost2b
        for i in impacts:
            impact_padb = df.loc[(df['Composizione'] == input_22b)][i].values[0] * (input_222b * 0.001)
            eolb = ((df.loc[(df['Componente'] == 'EoL') & (df['Specifiche'] == input_22b)][i].values[0] * 1) * (
                        input_222b * 0.001))
            traspb = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (trasppadb * input_222b * 0.001)
            Pad_Trasportob.append(traspb)
            Pad_EoLb.append(eolb)
            Padb.append(impact_padb)


    else:
        Padb = [0,0,0,0,0,0,0]
        Pad_EoLb = [0,0,0,0,0,0,0]
        Pad_Trasportob = [0,0,0,0,0,0,0]
        padpesob = 0
        padprezb = 0


    if (inputdokmeh != 0)& (tavolo2==False)&(pet1b+pp1b+pa1b+pvc1b+pe1b+evoh1b !=0) & (input_31b == True):

        Topb = []
        Top_EoLb = []
        Top_Trasportob = []
        toppesob = input_333b * area3b * 0.001
        topprezb = cost3b * area3b


        for i in impacts:
            impact_topb = ( (((df.loc[(df['Composizione'] == "PET1")][i].values[0] * (pet1b*0.01)) +
                           (df.loc[(df['Composizione'] == "PP1")][i].values[0] * (pp1b*0.01)) +
                           (df.loc[(df['Composizione'] == "PA1")][i].values[0] * (pa1b*0.01)) +
                           (df.loc[(df['Composizione'] == "PVC1")][i].values[0] * (pvc1b*0.01)) +
                           (df.loc[(df['Composizione'] == "PE1")][i].values[0] * (pe1b*0.01)) +
                           (df.loc[(df['Composizione'] == "EVA/EVOH1")][i].values[0] * (evoh1b*0.01)))/0.96) +
                           df.loc[(df['Componente'] == 'lamination topbot')][i].values[0]

                           ) * (input_333b* area3b * 0.001)
            traspb = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (trasptopb * input_333b * area3b * 0.001)
            Top_Trasportob.append(traspb)

            eolb = (((df.loc[(df['Composizione'] == "EoL PET")][i].values[0] * (pet1b * 0.01)) +
                           (df.loc[(df['Composizione'] == "EoL PP")][i].values[0] * (pp1b * 0.01)) +
                           (df.loc[(df['Composizione'] == "EoL PA")][i].values[0] * (pa1b * 0.01)) +
                           (df.loc[(df['Composizione'] == "EoL PVC")][i].values[0] * (pvc1b * 0.01)) +
                           (df.loc[(df['Composizione'] == "EoL PE")][i].values[0] * (pe1b * 0.01)) +
                           (df.loc[(df['Composizione'] == "EoL EVOH")][i].values[0] * (evoh1b * 0.01)))) * (input_333b * area3b * 0.001)
            Top_EoLb.append(eolb)
            Topb.append(impact_topb)

    else:
        Topb = [0,0,0,0,0,0,0]
        Top_EoLb = [0,0,0,0,0,0,0]
        Top_Trasportob = [0,0,0,0,0,0,0]
        toppesob = 0
        topprezb = 0

    if (inputdokmeh != 0)& (tavolo2==False)&(pet2b+pp2b+pa2b+pvc2b+pe2b+evoh2b !=0) & (input_41b == True):

        Bottomb = []
        Bottom_EoLb = []
        Bottom_Trasportob = []
        botpesob = input_444b * area4b * 0.001
        botprezb = cost4b * area4b

        for i in impacts:
            impact_bottomb = ((((df.loc[(df['Composizione'] == "PET1")][i].values[0] * (pet2b * 0.01)) +
                           (df.loc[(df['Composizione'] == "PP1")][i].values[0] * (pp2b * 0.01)) +
                           (df.loc[(df['Composizione'] == "PA1")][i].values[0] * (pa2b * 0.01)) +
                           (df.loc[(df['Composizione'] == "PVC1")][i].values[0] * (pvc2b * 0.01)) +
                           (df.loc[(df['Composizione'] == "PE1")][i].values[0] * (pe2b * 0.01)) +
                           (df.loc[(df['Composizione'] == "EVA/EVOH2")][i].values[0] * (evoh2b * 0.01))) / 0.96) +
                          df.loc[(df['Componente'] == 'lamination topbot')][i].values[0]

                          ) * (input_444b * area4b * 0.001)
            eolb = (((df.loc[(df['Composizione'] == "EoL PET")][i].values[0] * (pet2b * 0.01)) +
                    (df.loc[(df['Composizione'] == "EoL PP")][i].values[0] * (pp2b * 0.01)) +
                    (df.loc[(df['Composizione'] == "EoL PA")][i].values[0] * (pa2b * 0.01)) +
                    (df.loc[(df['Composizione'] == "EoL PVC")][i].values[0] * (pvc2b * 0.01)) +
                    (df.loc[(df['Composizione'] == "EoL PE")][i].values[0] * (pe2b * 0.01)) +
                    (df.loc[(df['Composizione'] == "EoL EVOH")][i].values[0] * (evoh2b * 0.01)))) * (
                              input_444b * area4b * 0.001)
            traspb = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (traspbotb * input_444b * area4b * 0.001)
            Bottom_Trasportob.append(traspb)
            Bottom_EoLb.append(eolb)
            Bottomb.append(impact_bottomb)

    else:
        Bottomb = [0,0,0,0,0,0,0]
        Bottom_EoLb = [0,0,0,0,0,0,0]
        Bottom_Trasportob = [0,0,0,0,0,0,0]
        botpesob = 0
        botprezb = 0

    if (inputdokmeh != 0)& (tavolo2==False) & (input_51b == True):

        Supportob = []
        Supporto_EoLb = []
        Supporto_Trasportob = []
        suppesob = input_555b * area5b * 0.001
        supprezb = cost5b * area5b


        for i in impacts:
            impact_supportob = df.loc[(df['Composizione'] == input_55b)][i].values[0] * (input_555b * area5b * 0.001)
            eolb = ((df.loc[(df['Componente'] == 'EoL') & (df['Specifiche'] == input_55b)][i].values[0] * 1) * (
                        input_555b * area5b * 0.001))
            traspb = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (traspsupb * input_555b * area5b * 0.001)
            Supporto_Trasportob.append(traspb)
            Supporto_EoLb.append(eolb)
            Supportob.append(impact_supportob)

    else:
        Supportob = [0,0,0,0,0,0,0]
        Supporto_EoLb = [0,0,0,0,0,0,0]
        Supporto_Trasportob = [0,0,0,0,0,0,0]
        suppesob = 0
        supprezb = 0

    if (inputdokmeh != 0)& (tavolo2==False) & (input_61b == True):

        Bustab = []
        Busta_EoLb = []
        Busta_Trasportob = []
        bustapesob = input_666b * area6b * 0.001
        bustaprezb = cost6b * area6b

        for i in impacts:
            impact_bustab = df.loc[(df['Composizione'] == input_66b)][i].values[0] * (input_666b * area6b * 0.001)
            eolb = ((df.loc[(df['Componente'] == 'EoL') & (df['Specifiche'] == input_66b)][i].values[0] * 1) * (
                    input_666b * area6b * 0.001))
            traspb = df.loc[(df['Componente'] == 'Trasporto')][i].values[0] * (traspbusb * input_666b * area6b * 0.001)
            Busta_Trasportob.append(traspb)
            Busta_EoLb.append(eolb)
            Bustab.append(impact_bustab)


    else:
        Bustab = [0,0,0,0,0,0,0]
        Busta_EoLb = [0,0,0,0,0,0,0]
        Busta_Trasportob = [0,0,0,0,0,0,0]
        bustapesob = 0
        bustaprezb = 0

    pestotb = (input_111b * 0.001) + (input_222b * 0.001)+ (input_333b * area3b * 0.001) + (input_444b * area4b * 0.001) +(input_555b * area5b * 0.001) + (input_666b * area6b * 0.001)
    pestot = (input_111 * 0.001) + (input_222 * 0.001)+ (input_333 * area3 * 0.001) + (input_444 * area4 * 0.001) +(input_555 * area5 * 0.001) + (input_666 * area6 * 0.001)

    vastable = pd.DataFrame({"Indicator":impacts,"Vassoio":Vassoio, "EoL Vassoio": EoL_Vassoio ,"Transport Vassoio": Trasporto_Vassoio,
                             "Vassoiob":Vassoiob, "EoL Vassoiob": EoL_Vassoiob,"Transport Vassoiob": Trasporto_Vassoiob,
                             "Pad": Pad, "EoL Pad": Pad_EoL, "Transport Pad": Pad_Trasporto,
                             "Padb": Padb, "EoL Padb": Pad_EoLb, "Transport Padb": Pad_Trasportob,
                             "Top": Top, "EoL Top": Top_EoL, "Transport Top": Top_Trasporto,
                             "Topb": Topb, "EoL Topb": Top_EoLb, "Transport Topb": Top_Trasportob,
                             "Bottom": Bottom, "EoL Bottom": Bottom_EoL, "Transport Bottom": Bottom_Trasporto,
                             "Bottomb": Bottomb, "EoL Bottomb": Bottom_EoLb, "Transport Bottomb": Bottom_Trasportob,
                             "Supporto": Supporto, "EoL Supporto": Supporto_EoL, "Transport Supporto": Supporto_Trasporto,
                             "Supportob": Supportob, "EoL Supportob": Supporto_EoLb,
                             "Transport Supportob": Supporto_Trasportob,
                             "Busta": Busta, "EoL Busta": Busta_EoL, "Transport Busta": Busta_Trasporto,
                             "Bustab": Bustab, "EoL Bustab": Busta_EoLb, "Transport Bustab": Busta_Trasportob

                             })
    col_list = ["Vassoio","EoL Vassoio","Transport Vassoio","Pad","EoL Pad","Transport Pad","Top","EoL Top","Transport Top","Bottom","EoL Bottom","Transport Bottom",
                "Supporto", "EoL Supporto", "Transport Supporto","Busta", "EoL Busta","Transport Busta"]
    col_listb = ["Vassoiob", "EoL Vassoiob", "Transport Vassoiob", "Padb", "EoL Padb", "Transport Padb", "Topb", "EoL Topb",
                "Transport Topb", "Bottomb", "EoL Bottomb", "Transport Bottomb",
                "Supportob", "EoL Supportob", "Transport Supportob", "Bustab", "EoL Bustab", "Transport Bustab"]

    vastable['sum'] = vastable[col_list].sum(axis=1)
    vastable['sumb'] = vastable[col_listb].sum(axis=1)
    maintable = dash_table.DataTable(vastable.to_dict('records'),[{'name': i, 'id': i} for i in vastable.columns])
    excelinput = dash_table.DataTable(Inputexcel.to_dict('records'),[{'name': i, 'id': i} for i in Inputexcel.columns])

    sumweight = vaspeso+padpeso+toppeso+botpeso+suppeso+bustapeso
    sumprezzo = vasprez + padprez + topprez + botprez + supprez + bustaprez

    sumweightb = vaspesob + padpesob + toppesob + botpesob + suppesob + bustapesob
    sumprezzob = vasprezb + padprezb + topprezb + botprezb + supprezb + bustaprezb

    if (tavolo1 == False) & ((input_1 == True) or (input_21 == True) or (input_31 == True) or (input_41 == True) or (input_51 == True) or (input_61 == True)) & (sumweight==0):
        alertweight = {"display":"block"}
    else:
        alertweight = {"display":"none"}

    msg1 = "{} g CO2 eq.".format(round(vastable.iloc[1,37]*1000, 1))
    msg2 = "{} g".format(round(sumweight*1000, 1))
    msg3 = "{} €".format(round(sumprezzo, 4))

    msg1b = "{} g CO2 eq.".format(round(vastable.iloc[1, 38]*1000, 1))
    msg2b = "{} g".format(round(sumweightb*1000, 1))
    msg3b = "{} €".format(round(sumprezzob, 4))

    if ((tavolo1 == True) & (tavolo2 == False)) or (((input_1 == False) & (input_21 == False) & (input_31 == False) & (input_41 == False) & (input_51 == False) & (input_61 == False)) & ((input_1b == True) or (input_21b == True) or (input_31b == True) or (input_41b == True) or (input_51b == True) or (input_61b == True))):
        weighting = 0
        weightingb = ((vastable.iloc[0, 38] / 55.5) * 6.639999984064) + (
                    (vastable.iloc[1, 38] / 7760) * 22.1899998768455) + (
                                 (vastable.iloc[2, 38] / 1330000) * 8.4199999720456) + (
                                 (vastable.iloc[3, 38] / 0.000637) * 9.5399999940852) + (
                                 (vastable.iloc[4, 38] / 40.6) * 5.10000000969) + (
                                 (vastable.iloc[5, 38] / 65300) * 8.9200000253328) + (
                                 (vastable.iloc[6, 38] / 11500) * 9.0300000168861)

    elif ((tavolo1 == False) & (tavolo2 == True)) or (((input_1b == False) & (input_21b == False) & (input_31b == False) & (input_41b == False) & (input_51b == False) & (input_61b == False)) & ((input_1 == True) or (input_21 == True) or (input_31 == True) or (input_41 == True) or (input_51 == True) or (input_61 == True))):
        weighting = ((vastable.iloc[0, 37] / 55.5) * 6.639999984064) + (
                    (vastable.iloc[1, 37] / 7760) * 22.1899998768455) + (
                                (vastable.iloc[2, 37] / 1330000) * 8.4199999720456) + (
                                (vastable.iloc[3, 37] / 0.000637) * 9.5399999940852) + (
                                (vastable.iloc[4, 37] / 40.6) * 5.10000000969) + (
                                (vastable.iloc[5, 37] / 65300) * 8.9200000253328) + (
                                (vastable.iloc[6, 37] / 11500) * 9.0300000168861)
        weightingb = 0

    elif ((tavolo1 == True) & (tavolo2 == True)) or ((input_1 == False) & (input_21 == False) &(input_31 == False) &(input_41 == False) &(input_51 == False) &(input_61 == False) & (input_1b == False) & (input_21b == False) &(input_31b == False) &(input_41b == False) &(input_51b == False) &(input_61b == False)):
        weighting = 0
        weightingb = 0

    elif (tavolo1 == False) & (tavolo2 == False):
        weighting = ((vastable.iloc[0, 37] / 55.5) * 6.639999984064) + (
                    (vastable.iloc[1, 37] / 7760) * 22.1899998768455) + (
                                (vastable.iloc[2, 37] / 1330000) * 8.4199999720456) + (
                                (vastable.iloc[3, 37] / 0.000637) * 9.5399999940852) + (
                                (vastable.iloc[4, 37] / 40.6) * 5.10000000969) + (
                                (vastable.iloc[5, 37] / 65300) * 8.9200000253328) + (
                                (vastable.iloc[6, 37] / 11500) * 9.0300000168861)
        weightingb = ((vastable.iloc[0, 38] / 55.5) * 6.639999984064) + (
                    (vastable.iloc[1, 38] / 7760) * 22.1899998768455) + (
                                 (vastable.iloc[2, 38] / 1330000) * 8.4199999720456) + (
                                 (vastable.iloc[3, 38] / 0.000637) * 9.5399999940852) + (
                                 (vastable.iloc[4, 38] / 40.6) * 5.10000000969) + (
                                 (vastable.iloc[5, 38] / 65300) * 8.9200000253328) + (
                                 (vastable.iloc[6, 38] / 11500) * 9.0300000168861)




    if (inputdokmeh!=0) & (weighting > weightingb):
        msg4 = "La soluzione B risulta preferibile"
        colorresult = "#B10D00"
    elif (inputdokmeh!=0) & (weighting < weightingb):
        msg4 = "La soluzione A risulta preferibile"
        colorresult = "#B10D00"
    else:
        msg4 = "Le soluzioni risultano equivalenti"
        colorresult = "#E3B30C"


    if ((tavolo1 == True) & (tavolo2 == False)) or (((input_1 == False) & (input_21 == False) & (input_31 == False) & (input_41 == False) & (input_51 == False) & (input_61 == False)) & ((input_1b == True) or (input_21b == True) or (input_31b == True) or (input_41b == True) or (input_51b == True) or (input_61b == True))):
        difference0 = 100
        difference = 100
        difference2 = 100
        difference3 = 100
        difference4 = 100
        difference5 = 100
        difference6 = 100
        GWPtotA0 = 0
        GWPtotA = 0
        GWPtotA2 = 0
        GWPtotA3 = 0
        GWPtotA4 = 0
        GWPtotA5 = 0
        GWPtotA6 = 0
    elif ((tavolo1 == False) & (tavolo2 == True)) or (((input_1b == False) & (input_21b == False) & (input_31b == False) & (input_41b == False) & (input_51b == False) & (input_61b == False)) & ((input_1 == True) or (input_21 == True) or (input_31 == True) or (input_41 == True) or (input_51 == True) or (input_61 == True))):
        difference0 = -100
        difference = -100
        difference2 = -100
        difference3 = -100
        difference4 = -100
        difference5 = -100
        difference6 = -100
        GWPtotA0 = "{}".format("{:.2e}".format(vastable.iloc[0, 37]))
        GWPtotA = "{}".format("{:.2e}".format(vastable.iloc[1, 37]))
        GWPtotA2 = "{}".format("{:.2e}".format(vastable.iloc[2, 37]))
        GWPtotA3 = "{}".format("{:.2e}".format(vastable.iloc[3, 37]))
        GWPtotA4 = "{}".format("{:.2e}".format(vastable.iloc[4, 37]))
        GWPtotA5 = "{}".format("{:.2e}".format(vastable.iloc[5, 37]))
        GWPtotA6 = "{}".format("{:.2e}".format(vastable.iloc[6, 37]))
    elif ((tavolo1 == True) & (tavolo2 == True)) or ((input_1 == False) & (input_21 == False) &(input_31 == False) &(input_41 == False) &(input_51 == False) &(input_61 == False) & (input_1b == False) & (input_21b == False) &(input_31b == False) &(input_41b == False) &(input_51b == False) &(input_61b == False)):
        difference0 = 0
        difference = 0
        difference2 = 0
        difference3 = 0
        difference4 = 0
        difference5 = 0
        difference6 = 0
        GWPtotA0 = 0
        GWPtotA = 0
        GWPtotA2 = 0
        GWPtotA3 = 0
        GWPtotA4 = 0
        GWPtotA5 = 0
        GWPtotA6 = 0
    elif (tavolo1 == False) & (tavolo2 == False):
        difference0 = ((vastable.iloc[0, 38] - vastable.iloc[0, 37]) / (vastable.iloc[0, 37])) * 100
        difference = ((vastable.iloc[1, 38] - vastable.iloc[1, 37]) / (vastable.iloc[1, 37])) * 100
        difference2 = ((vastable.iloc[2, 38] - vastable.iloc[2, 37]) / (vastable.iloc[2, 37])) * 100
        difference3 = ((vastable.iloc[3, 38] - vastable.iloc[3, 37]) / (vastable.iloc[3, 37])) * 100
        difference4 = ((vastable.iloc[4, 38] - vastable.iloc[4, 37]) / (vastable.iloc[4, 37])) * 100
        difference5 = ((vastable.iloc[5, 38] - vastable.iloc[5, 37]) / (vastable.iloc[5, 37])) * 100
        difference6 = ((vastable.iloc[6, 38] - vastable.iloc[6, 37]) / (vastable.iloc[6, 37])) * 100
        GWPtotA0 = "{}".format("{:.2e}".format(vastable.iloc[0, 37]))
        GWPtotA = "{}".format("{:.2e}".format(vastable.iloc[1, 37]))
        GWPtotA2 = "{}".format("{:.2e}".format(vastable.iloc[2, 37]))
        GWPtotA3 = "{}".format("{:.2e}".format(vastable.iloc[3, 37]))
        GWPtotA4 = "{}".format("{:.2e}".format(vastable.iloc[4, 37]))
        GWPtotA5 = "{}".format("{:.2e}".format(vastable.iloc[5, 37]))
        GWPtotA6 = "{}".format("{:.2e}".format(vastable.iloc[6, 37]))




    difmsg0 = "{} %".format("{:.0f}".format(difference0))

    if -10 <= difference0 <= 10:
        rang0 = {"color": "black", "background-color": "yellow"}
    elif difference0 > 10:
        rang0 = {"color": "white", "background-color": "red"}
    elif difference0 < -10:
        rang0 = {"color": "white", "background-color": "green"}

    difmsg = "{} %".format("{:.0f}".format(difference))

    if -10 <= difference <= 10:
        rang = {"color": "black", "background-color": "yellow"}
    elif difference > 10:
        rang = {"color": "white", "background-color": "red"}
    elif difference < -10:
        rang = {"color": "white", "background-color": "green"}

    difmsg2 = "{} %".format("{:.0f}".format(difference2))

    if -10 <= difference2 <= 10:
        rang2 = {"color": "black", "background-color": "yellow"}
    elif difference2 > 10:
        rang2 = {"color": "white", "background-color": "red"}
    elif difference2 < -10:
        rang2 = {"color": "white", "background-color": "green"}

    difmsg3 = "{} %".format("{:.0f}".format(difference3))
    if -10 <= difference3 <= 10:
        rang3 = {"color": "black", "background-color": "yellow"}
    elif difference3 > 10:
        rang3 = {"color": "white", "background-color": "red"}
    elif difference3 < -10:
        rang3 = {"color": "white", "background-color": "green"}

    difmsg4 = "{} %".format("{:.0f}".format(difference4))
    if -10 <= difference4 <= 10:
        rang4 = {"color": "black", "background-color": "yellow"}
    elif difference4 > 10:
        rang4 = {"color": "white", "background-color": "red"}
    elif difference4 < -10:
        rang4 = {"color": "white", "background-color": "green"}

    difmsg5 = "{} %".format("{:.0f}".format(difference5))
    if -10 <= difference5 <= 10:
        rang5 = {"color": "black", "background-color": "yellow"}
    elif difference5 > 10:
        rang5 = {"color": "white", "background-color": "red"}
    elif difference5 < -10:
        rang5 = {"color": "white", "background-color": "green"}

    difmsg6 = "{} %".format("{:.0f}".format(difference6))

    if -10 <= difference6 <= 10:
        rang6 = {"color": "black", "background-color": "yellow"}
    elif difference6 > 10:
        rang6 = {"color": "white", "background-color": "red"}
    elif difference6 < -10:
        rang6 = {"color": "white", "background-color": "green"}

    sum = (vastable.iloc[1,1]) + (vastable.iloc[1,3]) + (abs(vastable.iloc[1,2])) +\
          (vastable.iloc[1,7]) + (vastable.iloc[1,9]) + (vastable.iloc[1,8]) +\
          (vastable.iloc[1,13]) + (vastable.iloc[1,15]) + (vastable.iloc[1,14]) + \
          (vastable.iloc[1, 19]) + (vastable.iloc[1, 21]) + (vastable.iloc[1, 20]) + \
          (vastable.iloc[1, 25]) + (vastable.iloc[1, 27]) + (vastable.iloc[1, 26]) + \
          (vastable.iloc[1, 31]) + (vastable.iloc[1, 33]) + (vastable.iloc[1, 32])

    sum2 =  (vastable.iloc[1,4]) + (vastable.iloc[1,6]) + (abs(vastable.iloc[1,5])) + \
            (vastable.iloc[1, 10]) + (vastable.iloc[1, 12]) + (vastable.iloc[1, 11]) + \
            (vastable.iloc[1, 16]) + (vastable.iloc[1, 18]) + (vastable.iloc[1, 17]) + \
            (vastable.iloc[1,22]) + (vastable.iloc[1,24]) + (vastable.iloc[1,23]) +\
            (vastable.iloc[1,28]) + (vastable.iloc[1,30]) + (vastable.iloc[1,29]) +\
            (vastable.iloc[1,34]) + (vastable.iloc[1,36]) + (vastable.iloc[1,35])
    sum3 = vasprez+ padprez+ topprez+ botprez+ supprez+ bustaprez
    sum4 = vasprezb+ padprezb+ topprezb+ botprezb+ supprezb+ bustaprezb

    #print(tavolo1, tavolo2)
    if ((tavolo1 == True) & (tavolo2 == False) & ((input_1b == True) or (input_21b == True) or (input_31b == True) or (input_41b == True) or (input_51b == True) or (input_61b == True))) or (((input_1 == False) & (input_21 == False) & (input_31 == False) & (input_41 == False) & (input_51 == False) & (input_61 == False)) &(tavolo1 == False) & (tavolo2 == False)& ((input_1b == True) or (input_21b == True) or (input_31b == True) or (input_41b == True) or (input_51b == True) or (input_61b == True))):
        jiwooli = pd.DataFrame({
            "Solutions": ["Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A",
                          "Soluzione A",
                          "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A",
                          "Soluzione A",
                          "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A",
                          "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B",
                          "Soluzione B",
                          "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B",
                          "Soluzione B",
                          "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B"],
            "Componente": ["Vassoio preformato", "Vassoio preformato", "Vassoio preformato", "Pad assorbente",
                           "Pad assorbente", "Pad assorbente", "Top flessibile", "Top flessibile",
                           "Top flessibile", "Bottom flessibile", "Bottom flessibile",
                           "Bottom flessibile",
                           "Supporto in cellulosa", "Supporto in cellulosa", "Supporto in cellulosa", "Busta", "Busta",
                           "Busta", "Vassoio preformato", "Vassoio preformato", "Vassoio preformato", "Pad assorbente",
                           "Pad assorbente", "Pad assorbente", "Top flessibile", "Top flessibile",
                           "Top flessibile", "Bottom flessibile", "Bottom flessibile",
                           "Bottom flessibile",
                           "Supporto in cellulosa", "Supporto in cellulosa", "Supporto in cellulosa", "Busta", "Busta",
                           "Busta"],
            "GHG (kg CO2)": [
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,

                (vastable.iloc[1, 4]), (vastable.iloc[1, 6]), abs((vastable.iloc[1, 5])),
                (vastable.iloc[1, 10]), (vastable.iloc[1, 12]), (vastable.iloc[1, 11]),
                (vastable.iloc[1, 16]), (vastable.iloc[1, 18]), (vastable.iloc[1, 17]),
                (vastable.iloc[1, 22]), (vastable.iloc[1, 24]), (vastable.iloc[1, 23]),
                (vastable.iloc[1, 28]), (vastable.iloc[1, 30]), (vastable.iloc[1, 29]),
                (vastable.iloc[1, 34]), (vastable.iloc[1, 36]), (vastable.iloc[1, 35])],
            "Contributo % ": [0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                              round(100 * (vastable.iloc[1, 4]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 6]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 5]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 10]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 12]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 11]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 16]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 18]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 17]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 22]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 24]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 23]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 28]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 30]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 29]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 34]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 36]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 35]) / sum2, 1)],

            "LCS": [" Materie prime e produzione", "Trasporto", "Fine vita", " Materie prime e produzione", "Trasporto",
                    "Fine vita", " Materie prime e produzione", "Trasporto", "Fine vita", " Materie prime e produzione",
                    "Trasporto", "Fine vita", " Materie prime e produzione", "Trasporto", "Fine vita",
                    " Materie prime e produzione", "Trasporto", "Fine vita",
                    " Materie prime e produzione", "Trasporto", "Fine vita", " Materie prime e produzione", "Trasporto",
                    "Fine vita", " Materie prime e produzione", "Trasporto", "Fine vita", " Materie prime e produzione",
                    "Trasporto", "Fine vita", " Materie prime e produzione", "Transport", "Fine vita",
                    " Materie prime e produzione", "Trasporto", "Fine vita"]
        })
        jiwooli2 = pd.DataFrame({
            "Solutions": ["Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A",
                          "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B"],
            "Componente2": ["Vassoio preformato", "Pad assorbente", "Top flessibile", "Bottom flessibile",
                            "Supporto in cellulosa", "Busta",
                            "Vassoio preformato", "Pad assorbente", "Top flessibile", "Bottom flessibile",
                            "Supporto in cellulosa", "Busta"],
            "Costo (€)": [0, 0,0,0,0,0, vasprezb, padprezb, topprezb,
                          botprezb, supprezb, bustaprezb],
            "Contributo % ": [0, 0,0,0,0,0, vasprezb * 100 / sum4,
                              padprezb * 100 / sum4,
                              topprezb * 100 / sum4, botprezb * 100 / sum4, supprezb * 100 / sum4,
                              bustaprezb * 100 / sum4]

        })
    elif ((tavolo1 == False) & (tavolo2 == True) & ((input_1 == True) or (input_21 == True) or (input_31 == True) or (input_41 == True) or (input_51 == True) or (input_61 == True))) or (((input_1b == False) & (input_21b == False) & (input_31b == False) & (input_41b == False) & (input_51b == False) & (input_61b == False)) &(tavolo1 == False) & (tavolo2 == False)& ((input_1 == True) or (input_21 == True) or (input_31 == True) or (input_41 == True) or (input_51 == True) or (input_61 == True))):
        jiwooli = pd.DataFrame({
            "Solutions": ["Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A",
                          "Soluzione A",
                          "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A",
                          "Soluzione A",
                          "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A",
                          "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B",
                          "Soluzione B",
                          "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B",
                          "Soluzione B",
                          "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B"],
            "Componente": ["Vassoio preformato", "Vassoio preformato", "Vassoio preformato", "Pad assorbente",
                           "Pad assorbente", "Pad assorbente", "Top flessibile", "Top flessibile",
                           "Top flessibile", "Bottom flessibile", "Bottom flessibile",
                           "Bottom flessibile",
                           "Supporto in cellulosa", "Supporto in cellulosa", "Supporto in cellulosa", "Busta", "Busta",
                           "Busta", "Vassoio preformato", "Vassoio preformato", "Vassoio preformato", "Pad assorbente",
                           "Pad assorbente", "Pad assorbente", "Top flessibile", "Top flessibile",
                           "Top flessibile", "Bottom flessibile", "Bottom flessibile",
                           "Bottom flessibile",
                           "Supporto in cellulosa", "Supporto in cellulosa", "Supporto in cellulosa", "Busta", "Busta",
                           "Busta"],
            "GHG (kg CO2)": [
                (vastable.iloc[1, 1]), (vastable.iloc[1, 3]), (abs(vastable.iloc[1, 2])),
                (vastable.iloc[1, 7]), (vastable.iloc[1, 9]), (vastable.iloc[1, 8]),
                (vastable.iloc[1, 13]), (vastable.iloc[1, 15]), (vastable.iloc[1, 14]),
                (vastable.iloc[1, 19]), (vastable.iloc[1, 21]), (vastable.iloc[1, 20]),
                (vastable.iloc[1, 25]), (vastable.iloc[1, 27]), (vastable.iloc[1, 26]),
                (vastable.iloc[1, 31]), (vastable.iloc[1, 33]), (vastable.iloc[1, 32]),

                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0],
            "Contributo % ": [round(100 * (vastable.iloc[1, 1]) / sum, 1), round(100 * (vastable.iloc[1, 3]) / sum, 1),
                              round(100 * (vastable.iloc[1, 2]) / sum, 1), round(100 * (vastable.iloc[1, 7]) / sum, 1),
                              round(100 * (vastable.iloc[1, 9]) / sum, 1),
                              round(100 * (vastable.iloc[1, 8]) / sum, 1), round(100 * (vastable.iloc[1, 13]) / sum, 1),
                              round(100 * (vastable.iloc[1, 15]) / sum, 1),
                              round(100 * (vastable.iloc[1, 14]) / sum, 1),
                              round(100 * (vastable.iloc[1, 19]) / sum, 1),
                              round(100 * (vastable.iloc[1, 21]) / sum, 1),
                              round(100 * (vastable.iloc[1, 20]) / sum, 1),
                              round(100 * (vastable.iloc[1, 25]) / sum, 1),
                              round(100 * (vastable.iloc[1, 27]) / sum, 1),
                              round(100 * (vastable.iloc[1, 26]) / sum, 1),
                              round(100 * (vastable.iloc[1, 31]) / sum, 1),
                              round(100 * (vastable.iloc[1, 33]) / sum, 1),
                              round(100 * (vastable.iloc[1, 32]) / sum, 1),
                              0, 0, 0,
                              0, 0, 0,
                              0, 0, 0,
                              0, 0, 0,
                              0, 0, 0,
                              0, 0, 0],

            "LCS": [" Materie prime e produzione", "Trasporto", "Fine vita", " Materie prime e produzione", "Trasporto",
                    "Fine vita", " Materie prime e produzione", "Trasporto", "Fine vita", " Materie prime e produzione",
                    "Trasporto", "Fine vita", " Materie prime e produzione", "Trasporto", "Fine vita",
                    " Materie prime e produzione", "Trasporto", "Fine vita",
                    " Materie prime e produzione", "Trasporto", "Fine vita", " Materie prime e produzione", "Trasporto",
                    "Fine vita", " Materie prime e produzione", "Trasporto", "Fine vita", " Materie prime e produzione",
                    "Trasporto", "Fine vita", " Materie prime e produzione", "Transport", "Fine vita",
                    " Materie prime e produzione", "Trasporto", "Fine vita"]
        })
        jiwooli2 = pd.DataFrame({
            "Solutions": ["Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A",
                          "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B"],
            "Componente2": ["Vassoio preformato", "Pad assorbente", "Top flessibile", "Bottom flessibile",
                            "Supporto in cellulosa", "Busta",
                            "Vassoio preformato", "Pad assorbente", "Top flessibile", "Bottom flessibile",
                            "Supporto in cellulosa", "Busta"],
            "Costo (€)": [vasprez, padprez, topprez, botprez, supprez, bustaprez, 0, 0,0,0,0,0],
            "Contributo % ": [vasprez * 100 / sum3, padprez * 100 / sum3, topprez * 100 / sum3, botprez * 100 / sum3,
                              supprez * 100 / sum3, bustaprez * 100 / sum3, 0, 0,0,0,0,0]

        })
    elif ((tavolo1 == True) & (tavolo2 == True)) or ((input_1 == False) & (input_21 == False) &(input_31 == False) &(input_41 == False) &(input_51 == False) &(input_61 == False) & (input_1b == False)& (tavolo1 == False) & (tavolo2 == False)& (input_21b == False) &(input_31b == False) &(input_41b == False) &(input_51b == False) &(input_61b == False)):
        jiwooli = pd.DataFrame({
            "Solutions": ["Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A",
                          "Soluzione A",
                          "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A",
                          "Soluzione A",
                          "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A",
                          "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B",
                          "Soluzione B",
                          "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B",
                          "Soluzione B",
                          "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B"],
            "Componente": ["Vassoio preformato", "Vassoio preformato", "Vassoio preformato", "Pad assorbente",
                           "Pad assorbente", "Pad assorbente", "Top flessibile", "Top flessibile",
                           "Top flessibile", "Bottom flessibile", "Bottom flessibile",
                           "Bottom flessibile",
                           "Supporto in cellulosa", "Supporto in cellulosa", "Supporto in cellulosa", "Busta", "Busta",
                           "Busta", "Vassoio preformato", "Vassoio preformato", "Vassoio preformato", "Pad assorbente",
                           "Pad assorbente", "Pad assorbente", "Top flessibile", "Top flessibile",
                           "Top flessibile", "Bottom flessibile", "Bottom flessibile",
                           "Bottom flessibile",
                           "Supporto in cellulosa", "Supporto in cellulosa", "Supporto in cellulosa", "Busta", "Busta",
                           "Busta"],
            "GHG (kg CO2)": [
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,

                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0],
            "Contributo % ": [0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
                              0, 0, 0,
                              0, 0, 0,
                              0, 0, 0,
                              0, 0, 0,
                              0, 0, 0,
                              0, 0, 0],

            "LCS": [" Materie prime e produzione", "Trasporto", "Fine vita", " Materie prime e produzione", "Trasporto",
                    "Fine vita", " Materie prime e produzione", "Trasporto", "Fine vita", " Materie prime e produzione",
                    "Trasporto", "Fine vita", " Materie prime e produzione", "Trasporto", "Fine vita",
                    " Materie prime e produzione", "Trasporto", "Fine vita",
                    " Materie prime e produzione", "Trasporto", "Fine vita", " Materie prime e produzione", "Trasporto",
                    "Fine vita", " Materie prime e produzione", "Trasporto", "Fine vita", " Materie prime e produzione",
                    "Trasporto", "Fine vita", " Materie prime e produzione", "Transport", "Fine vita",
                    " Materie prime e produzione", "Trasporto", "Fine vita"]
        })
        jiwooli2 = pd.DataFrame({
            "Solutions": ["Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A",
                          "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B"],
            "Componente2": ["Vassoio preformato", "Pad assorbente", "Top flessibile", "Bottom flessibile",
                            "Supporto in cellulosa", "Busta",
                            "Vassoio preformato", "Pad assorbente", "Top flessibile", "Bottom flessibile",
                            "Supporto in cellulosa", "Busta"],
            "Costo (€)": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Contributo % ": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        })
    elif (tavolo1 == False) & (tavolo2 == False) & ((input_1 == True) or (input_21 == True) or (input_31 == True) or (input_41 == True) or (input_51 == True) or (input_61 == True)) & ((input_1b == True) or (input_21b == True) or (input_31b == True) or (input_41b == True) or (input_51b == True) or (input_61b == True)):
        jiwooli = pd.DataFrame({
            "Solutions": ["Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A",
                          "Soluzione A",
                          "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A",
                          "Soluzione A",
                          "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A",
                          "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B",
                          "Soluzione B",
                          "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B",
                          "Soluzione B",
                          "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B"],
            "Componente": ["Vassoio preformato", "Vassoio preformato", "Vassoio preformato", "Pad assorbente",
                           "Pad assorbente", "Pad assorbente", "Top flessibile", "Top flessibile",
                           "Top flessibile", "Bottom flessibile", "Bottom flessibile",
                           "Bottom flessibile",
                           "Supporto in cellulosa", "Supporto in cellulosa", "Supporto in cellulosa", "Busta", "Busta",
                           "Busta", "Vassoio preformato", "Vassoio preformato", "Vassoio preformato", "Pad assorbente",
                           "Pad assorbente", "Pad assorbente", "Top flessibile", "Top flessibile",
                           "Top flessibile", "Bottom flessibile", "Bottom flessibile",
                           "Bottom flessibile",
                           "Supporto in cellulosa", "Supporto in cellulosa", "Supporto in cellulosa", "Busta", "Busta",
                           "Busta"],
            "GHG (kg CO2)": [
                (vastable.iloc[1, 1]), (vastable.iloc[1, 3]), (abs(vastable.iloc[1, 2])),
                (vastable.iloc[1, 7]), (vastable.iloc[1, 9]), (vastable.iloc[1, 8]),
                (vastable.iloc[1, 13]), (vastable.iloc[1, 15]), (vastable.iloc[1, 14]),
                (vastable.iloc[1, 19]), (vastable.iloc[1, 21]), (vastable.iloc[1, 20]),
                (vastable.iloc[1, 25]), (vastable.iloc[1, 27]), (vastable.iloc[1, 26]),
                (vastable.iloc[1, 31]), (vastable.iloc[1, 33]), (vastable.iloc[1, 32]),

                (vastable.iloc[1, 4]), (vastable.iloc[1, 6]), (abs(vastable.iloc[1, 5])),
                (vastable.iloc[1, 10]), (vastable.iloc[1, 12]), (vastable.iloc[1, 11]),
                (vastable.iloc[1, 16]), (vastable.iloc[1, 18]), (vastable.iloc[1, 17]),
                (vastable.iloc[1, 22]), (vastable.iloc[1, 24]), (vastable.iloc[1, 23]),
                (vastable.iloc[1, 28]), (vastable.iloc[1, 30]), (vastable.iloc[1, 29]),
                (vastable.iloc[1, 34]), (vastable.iloc[1, 36]), (vastable.iloc[1, 35])],
            "Contributo % ": [round(100 * (vastable.iloc[1, 1]) / sum, 1), round(100 * (vastable.iloc[1, 3]) / sum, 1),
                              round(100 * (vastable.iloc[1, 2]) / sum, 1), round(100 * (vastable.iloc[1, 7]) / sum, 1),
                              round(100 * (vastable.iloc[1, 9]) / sum, 1),
                              round(100 * (vastable.iloc[1, 8]) / sum, 1), round(100 * (vastable.iloc[1, 13]) / sum, 1),
                              round(100 * (vastable.iloc[1, 15]) / sum, 1),
                              round(100 * (vastable.iloc[1, 14]) / sum, 1),
                              round(100 * (vastable.iloc[1, 19]) / sum, 1),
                              round(100 * (vastable.iloc[1, 21]) / sum, 1),
                              round(100 * (vastable.iloc[1, 20]) / sum, 1),
                              round(100 * (vastable.iloc[1, 25]) / sum, 1),
                              round(100 * (vastable.iloc[1, 27]) / sum, 1),
                              round(100 * (vastable.iloc[1, 26]) / sum, 1),
                              round(100 * (vastable.iloc[1, 31]) / sum, 1),
                              round(100 * (vastable.iloc[1, 33]) / sum, 1),
                              round(100 * (vastable.iloc[1, 32]) / sum, 1),
                              round(100 * (vastable.iloc[1, 4]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 6]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 5]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 10]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 12]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 11]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 16]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 18]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 17]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 22]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 24]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 23]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 28]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 30]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 29]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 34]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 36]) / sum2, 1),
                              round(100 * (vastable.iloc[1, 35]) / sum2, 1)],

            "LCS": [" Materie prime e produzione", "Trasporto", "Fine vita", " Materie prime e produzione", "Trasporto",
                    "Fine vita", " Materie prime e produzione", "Trasporto", "Fine vita", " Materie prime e produzione",
                    "Trasporto", "Fine vita", " Materie prime e produzione", "Trasporto", "Fine vita",
                    " Materie prime e produzione", "Trasporto", "Fine vita",
                    " Materie prime e produzione", "Trasporto", "Fine vita", " Materie prime e produzione", "Trasporto",
                    "Fine vita", " Materie prime e produzione", "Trasporto", "Fine vita", " Materie prime e produzione",
                    "Trasporto", "Fine vita", " Materie prime e produzione", "Transport", "Fine vita",
                    " Materie prime e produzione", "Trasporto", "Fine vita"]
        })
        jiwooli2 = pd.DataFrame({
            "Solutions": ["Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A", "Soluzione A",
                          "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B", "Soluzione B"],
            "Componente2": ["Vassoio preformato", "Pad assorbente", "Top flessibile", "Bottom flessibile",
                            "Supporto in cellulosa", "Busta",
                            "Vassoio preformato", "Pad assorbente", "Top flessibile", "Bottom flessibile",
                            "Supporto in cellulosa", "Busta"],
            "Costo (€)": [vasprez, padprez, topprez, botprez, supprez, bustaprez, vasprezb, padprezb, topprezb,
                          botprezb, supprezb, bustaprezb],
            "Contributo % ": [vasprez * 100 / sum3, padprez * 100 / sum3, topprez * 100 / sum3, botprez * 100 / sum3,
                              supprez * 100 / sum3, bustaprez * 100 / sum3, vasprezb * 100 / sum4,
                              padprezb * 100 / sum4,
                              topprezb * 100 / sum4, botprezb * 100 / sum4, supprezb * 100 / sum4,
                              bustaprezb * 100 / sum4]

        })

    fig = px.bar(jiwooli, x="Solutions", y="GHG (kg CO2)", color="Componente", title="Carbon Footprint", text="LCS",
                 labels={'Solutions': " ", 'GHG (kg CO2)': 'Carbon Footprint (kg CO2 eq.)'}, hover_name="Componente",
                 hover_data={"Contributo % "}, custom_data=[jiwooli['Contributo % ']])

    fig2 = px.bar(jiwooli2, x="Solutions", y="Costo (€)", color="Componente2", title="Carbon Footprint",
                  labels={'Solutions': " ", 'Costo (€)': 'Costo (€)'}, hover_name="Componente2",
                  hover_data={"Componente2": False, 'Costo (€)': True, "Solutions": False},
                  custom_data=[jiwooli2['Contributo % ']])
    fig.update_layout(
        title_text="", paper_bgcolor='#DAF0AD', showlegend=True, margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='#DAF0AD', font_family="Arial",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title_text=None
        ), legend_font=dict(size=11),

    )
    fig.update_traces(
        hovertemplate='<b>CF</b>: %{y:,.2e} kg C02 eq.<br>' + '<b>LCS</b>: %{text}<br>' + '<b>Contributo sul totale</b>: %{customdata[0]} %<br>',
        textfont_size=12, textangle=0, textposition="inside")
    fig2.update_traces(
        hovertemplate='<b>Costo</b>: %{y:,.2f} €<br>' + '<b>Contributo sul totale</b>: %{customdata[0]:,.2f} %<br>',
        textfont_size=12, textangle=45, textposition="inside")
    fig2.update_layout(
        title_text="", paper_bgcolor='#DAF0AD', showlegend=True, margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='#DAF0AD', font_family="Arial",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title_text=None
        ), legend_font=dict(size=11),

    )


    return maintable, Inputexcel.to_dict('records'), [{'name': i, 'id': i} for i in Inputexcel.columns], msg1, msg2, msg3,msg1b, msg2b, msg3b, msg4, rang0, GWPtotA0, difmsg0, rang, GWPtotA, difmsg ,rang2, GWPtotA2, difmsg2 ,rang3, GWPtotA3, difmsg3 ,rang4, GWPtotA4, difmsg4 ,rang5, GWPtotA5, difmsg5,rang6, GWPtotA6, difmsg6, fig, fig2, maintable, vastable.to_dict('records'), [{'name': i, 'id': i} for i in vastable.columns], pwb, pestot, pestotb, colorresult

#----------------------- DUPLICATE -----------------

@callback(
    Output(component_id='tavol2', component_property='style'),
    [
     Input(component_id='tavolo2', component_property='value')])
def show_hide_table(input2):
    if input2 == False:
        return {'display': 'block'}
    if input2 == True:
        return {'display': 'none'}


@callback(

    Output(component_id='tavol1', component_property='style'),

    [Input(component_id='tavolo1', component_property='value'),
])
def show_hide_table(input1):
    if input1 == False:
        return {'display': 'block'}
    if input1 == True:
        return {'display': 'none'}


# --------------------------Call backs for switch on/off---------------------------------------

@callback(
    Output(component_id='dd1', component_property='style'),
    Output(component_id='alert1', component_property='style'),
    Output(component_id='input1', component_property='style'),
    Output(component_id='input11', component_property='style'),
    Output(component_id='dd11', component_property='style'),
    Output(component_id='unit11', component_property='style'),
    Output(component_id='unit1', component_property='style'),
    Output(component_id='unit111', component_property='style'),
    [Input(component_id='check1', component_property='value')])
def show_hide_element(visibility_state):
    if visibility_state == True:
        return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {
            'display': 'block'},  {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    if visibility_state == False:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {
            'display': 'none'},  {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


@callback(
    Output(component_id='dd2', component_property='style'),
    Output(component_id='alert2', component_property='style'),
    Output(component_id='input2', component_property='style'),
    Output(component_id='input22', component_property='style'),
    Output(component_id='dd22', component_property='style'),
    Output(component_id='unit22', component_property='style'),
    Output(component_id='unit2', component_property='style'),
    Output(component_id='unit222', component_property='style'),
    [Input(component_id='check2', component_property='value')])
def show_hide_element2(visibility_state):
    if visibility_state == True:
        return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {
            'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    if visibility_state == False:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {
            'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


@callback(
    Output(component_id='input3', component_property='style'),
    Output(component_id='input33', component_property='style'),
    Output(component_id='dd33', component_property='style'),
    Output(component_id='unit33', component_property='style'),
    Output(component_id='unit3', component_property='style'),
    Output(component_id='unit333', component_property='style'),
    Output(component_id='polym3', component_property='style'),
    Output(component_id='row31', component_property='style'),
    Output(component_id='row32', component_property='style'),
    Output(component_id='row33', component_property='style'),
    Output(component_id='row34', component_property='style'),
    [Input(component_id='check3', component_property='value')])
def show_hide_element3(visibility_state):
    if visibility_state == True:
        return {'display': 'block'}, {'display': 'block'}, {
            'display': 'block'},  {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    if visibility_state == False:
        return {'display': 'none'}, {'display': 'none'}, {
            'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


@callback(

    Output(component_id='input4', component_property='style'),
    Output(component_id='input44', component_property='style'),
    Output(component_id='dd44', component_property='style'),
    Output(component_id='unit44', component_property='style'),
    Output(component_id='unit4', component_property='style'),
    Output(component_id='unit444', component_property='style'),
    Output(component_id='polym4', component_property='style'),
    Output(component_id='row41', component_property='style'),
    Output(component_id='row42', component_property='style'),
    Output(component_id='row43', component_property='style'),
    Output(component_id='row44', component_property='style'),
    [Input(component_id='check4', component_property='value')])
def show_hide_element4(visibility_state):
    if visibility_state == True:
        return {'display': 'block'}, {'display': 'block'}, {
            'display': 'block'},  {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    if visibility_state == False:
        return {'display': 'none'}, {'display': 'none'}, {
            'display': 'none'},  {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


@callback(
    Output(component_id='dd5', component_property='style'),
    Output(component_id='alert5', component_property='style'),
    Output(component_id='input5', component_property='style'),
    Output(component_id='input55', component_property='style'),
    Output(component_id='dd55', component_property='style'),
    Output(component_id='unit55', component_property='style'),
    Output(component_id='unit5', component_property='style'),
    Output(component_id='unit555', component_property='style'),
    Output(component_id='areadis3', component_property='style'),
    [Input(component_id='check5', component_property='value')])
def show_hide_element5(visibility_state):
    if visibility_state == True:
        return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {
            'display': 'block'},  {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    if visibility_state == False:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {
            'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


@callback(
    Output(component_id='dd6', component_property='style'),
    Output(component_id='alert6', component_property='style'),
    Output(component_id='input6', component_property='style'),
    Output(component_id='input66', component_property='style'),
    Output(component_id='dd66', component_property='style'),
    Output(component_id='unit66', component_property='style'),
    Output(component_id='unit6', component_property='style'),
    Output(component_id='unit666', component_property='style'),
    Output(component_id='areadis4', component_property='style'),
    [Input(component_id='check6', component_property='value')])
def show_hide_element6(visibility_state):
    if visibility_state == True:
        return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {
            'display': 'block'},  {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    if visibility_state == False:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {
            'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


# ----------------------------- DUPLICATE-----------------------------------------

@callback(
    Output(component_id='dd1b', component_property='style'),
    Output(component_id='alert1b', component_property='style'),
    Output(component_id='input1b', component_property='style'),
    Output(component_id='input11b', component_property='style'),
    Output(component_id='dd11b', component_property='style'),
    Output(component_id='unit11b', component_property='style'),
    Output(component_id='unit1b', component_property='style'),
    Output(component_id='unit111b', component_property='style'),
    [Input(component_id='check1b', component_property='value')])
def show_hide_element(visibility_state):
    if visibility_state == True:
        return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {
            'display': 'block'},  {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    if visibility_state == False:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {
            'display': 'none'},  {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


@callback(
    Output(component_id='dd2b', component_property='style'),
    Output(component_id='alert2b', component_property='style'),
    Output(component_id='input2b', component_property='style'),
    Output(component_id='input22b', component_property='style'),
    Output(component_id='dd22b', component_property='style'),
    Output(component_id='unit22b', component_property='style'),
    Output(component_id='unit2b', component_property='style'),
    Output(component_id='unit222b', component_property='style'),
    [Input(component_id='check2b', component_property='value')])
def show_hide_element2(visibility_state):
    if visibility_state == True:
        return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {
            'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    if visibility_state == False:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {
            'display': 'none'},  {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


@callback(

    Output(component_id='areadisb', component_property='style'),
    Output(component_id='row31b', component_property='style'),
    Output(component_id='row32b', component_property='style'),
    Output(component_id='row33b', component_property='style'),
    Output(component_id='row34b', component_property='style'),
    [Input(component_id='check3b', component_property='value')])
def show_hide_element3(visibility_state):
    if visibility_state == True:
        return  {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {
            'display': 'block'}, {'display': 'block'}
    if visibility_state == False:
        return  {'display': 'none'}, {
            'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


@callback(


    Output(component_id='areadis2b', component_property='style'),
    Output(component_id='row41b', component_property='style'),
    Output(component_id='row42b', component_property='style'),
    Output(component_id='row43b', component_property='style'),
    Output(component_id='row44b', component_property='style'),
    [Input(component_id='check4b', component_property='value')])
def show_hide_element4(visibility_state):
    if visibility_state == True:
        return  {'display': 'block'}, {
            'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    if visibility_state == False:
        return  {'display': 'none'}, {
            'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


@callback(
    Output(component_id='dd5b', component_property='style'),
    Output(component_id='alert5b', component_property='style'),
    Output(component_id='input5b', component_property='style'),
    Output(component_id='input55b', component_property='style'),
    Output(component_id='dd55b', component_property='style'),
    Output(component_id='unit55b', component_property='style'),
    Output(component_id='unit5b', component_property='style'),
    Output(component_id='unit555b', component_property='style'),

    Output(component_id='areadis3b', component_property='style'),

    [Input(component_id='check5b', component_property='value')])
def show_hide_element5(visibility_state):
    if visibility_state == True:
        return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {
            'display': 'block'},  {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    if visibility_state == False:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {
            'display': 'none'},  {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


@callback(
    Output(component_id='dd6b', component_property='style'),
    Output(component_id='alert6b', component_property='style'),
    Output(component_id='input6b', component_property='style'),
    Output(component_id='input66b', component_property='style'),
    Output(component_id='dd66b', component_property='style'),
    Output(component_id='unit66b', component_property='style'),
    Output(component_id='unit6b', component_property='style'),
    Output(component_id='unit666b', component_property='style'),

    Output(component_id='areadis4b', component_property='style'),

    [Input(component_id='check6b', component_property='value')])
def show_hide_element6(visibility_state):
    if visibility_state == True:
        return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {
            'display': 'block'},  {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    if visibility_state == False:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {
            'display': 'none'},  {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}




# ------------------------------- Call backs for alert messages ------------------

#
@callback(
    Output(component_id='alert1', component_property='children'),
    Output(component_id='alert2', component_property='children'),

    Output(component_id='alert5', component_property='children'),
    Output(component_id='alert6', component_property='children'),
    [Input(component_id='dd1', component_property='value'),
     Input(component_id='dd2', component_property='value'),
     Input(component_id='dd5', component_property='value'),
     Input(component_id='dd6', component_property='value')])
def show_specification(specifiche1, specifiche2,  specifiche5, specifiche6):
    spe1 = df.loc[(df['Composizione'] == specifiche1) & (df['Componente'] == "Vassoio preformato")]['Specifiche']
    spe2 = df.loc[(df['Composizione'] == specifiche2) & (df['Componente'] == "Pad assorbente")]['Specifiche']
    spe5 = df.loc[(df['Composizione'] == specifiche5) & (df['Componente'] == "Supporto in cellulosa")]['Specifiche']
    spe6 = df.loc[(df['Composizione'] == specifiche6) & (df['Componente'] == "Busta")]['Specifiche']

    return spe1, spe2,  spe5, spe6

# ----------------------------- DUPLICATE ----------------------------------------------

@callback(
    Output(component_id='alert1b', component_property='children'),
    Output(component_id='alert2b', component_property='children'),
    Output(component_id='alert5b', component_property='children'),
    Output(component_id='alert6b', component_property='children'),
    [Input(component_id='dd1b', component_property='value'),
     Input(component_id='dd2b', component_property='value'),
     Input(component_id='dd5b', component_property='value'),
     Input(component_id='dd6b', component_property='value')])
def show_specification(specifiche1, specifiche2,  specifiche5, specifiche6):
    spe1 = df.loc[(df['Composizione'] == specifiche1) & (df['Componente'] == "Vassoio preformato")]['Specifiche']
    spe2 = df.loc[(df['Composizione'] == specifiche2) & (df['Componente'] == "Pad assorbente")]['Specifiche']
    spe5 = df.loc[(df['Composizione'] == specifiche5) & (df['Componente'] == "Supporto in cellulosa")]['Specifiche']
    spe6 = df.loc[(df['Composizione'] == specifiche6) & (df['Componente'] == "Busta")]['Specifiche']

    return spe1, spe2,  spe5, spe6

# ------------recycle rate input---------------------------------------------------------

@callback(
    Output(component_id='rtext', component_property='style'),
    Output(component_id='rinput', component_property='style'),
    Output(component_id='stype', component_property='style'),
    Output(component_id='stype2', component_property='style'),
    Output(component_id='stype3', component_property='style'),
    Output(component_id='stype4', component_property='style'),
    Output(component_id='tablehide', component_property='style'),
    [Input(component_id='dd1', component_property='value'),
     Input(component_id='check1', component_property='value')])
def show_hide_row(visibility_state, switch_state):
    if (switch_state == True) & ((visibility_state == 'PET') or (visibility_state == 'PET/PE') or (visibility_state == 'XPS')):
        return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

#------------------------------ DUPLICATE ----------------------

@callback(
    Output(component_id='rtextb', component_property='style'),
    Output(component_id='rinputb', component_property='style'),
    Output(component_id='stypeb', component_property='style'),
    Output(component_id='stype2b', component_property='style'),
    Output(component_id='stype3b', component_property='style'),
    Output(component_id='stype4b', component_property='style'),
    Output(component_id='tablehideb', component_property='style'),
    [Input(component_id='dd1b', component_property='value'),
     Input(component_id='check1b', component_property='value')])
def show_hide_row(visibility_state, switch_state):
    if (switch_state == True) & ((visibility_state == 'PET') or (visibility_state == 'PET/PE') or (visibility_state == 'XPS')):
        return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

# ----------------scrap type input-----------------------------------

@callback(
    Output(component_id="alert8b", component_property='children'),
    Output(component_id="alert10b", component_property='children'),
    Input(component_id='dd1b', component_property='value'),
    prevent_initial_call=True,
    suppress_callback_exceptions=True

)
def note_jadid(input1):
    if input1 == "PET":
        return "Contenuto di PET riciclato", "Contenuto di PET riciclato postconsumo nell' r-PET. La restante parte viene considerata PET riciclato preconsumo"
    elif input1 == "PET/PE":
        return "Contenuto di PET riciclato con riferimento allo strato di PET", "Contenuto di PET riciclato postconsumo nell' r-PET. La restante parte viene considerata PET riciclato preconsumo"
    elif input1 == "XPS":
        return "Contenuto di XPS riciclato", "Contenuto di XPS riciclato postconsumo nell' r-XPS. La restante parte viene considerata XPS riciclato preconsumo"
    else:
        return None, None


@callback(
    Output(component_id="alert8", component_property='children'),
    Output(component_id="alert10", component_property='children'),
    Input(component_id='dd1', component_property='value'),
    prevent_initial_call=True,
    suppress_callback_exceptions=True

)
def note_jadid(input1):
    if input1 == "PET":
        return "Contenuto di PET riciclato", "Contenuto di PET riciclato postconsumo nell' r-PET. La restante parte viene considerata PET riciclato preconsumo"
    elif input1 == "PET/PE":
        return "Contenuto di PET riciclato con riferimento allo strato di PET", "Contenuto di PET riciclato postconsumo nell' r-PET. La restante parte viene considerata PET riciclato preconsumo"
    elif input1 == "XPS":
        return "Contenuto di XPS riciclato", "Contenuto di XPS riciclato postconsumo nell' r-XPS. La restante parte viene considerata XPS riciclato preconsumo"
    else:
        return None, None

