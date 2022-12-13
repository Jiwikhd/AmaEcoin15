import dash
from dash import html, dcc,State, callback, Input, Output
from dash import dash_table
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image
import pandas as pd
import sys
import sympy as smp
import base64
import numpy as np
import openpyxl
import xlsxwriter
from datetime import datetime


img_path = "assets/cc.jpg"
pil_image0 = Image.open("assets/acid.jpg")
pil_image = Image.open(img_path)
pil_image2 = Image.open("assets/landuse.jpg")
pil_image3 = Image.open("assets/ozone.jpg")
pil_image4 = Image.open("assets/risorse.jpg")
pil_image5 = Image.open("assets/particolo.jpg")
pil_image6 = Image.open("assets/wtr.jpg")
pil_image_sfrido = Image.open("assets/sfridopic.png")
pil_image_excel = Image.open("assets/excel2.png")



df = pd.read_csv('assets/Database.csv', encoding='unicode_escape')
dash.register_page(__name__)

colors = {
    'background': '#DAF0AD'
}
layout = html.Div([
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card([dbc.CardBody(html.P(id = "pesoprodotto"))],style={"margin-left": "10px", "height": "55px", "background-color": "#DAF0AD"})), dbc.Col([dbc.Row(dbc.Spinner(color="danger", type="grow", size="sm", id="spin1", spinner_style={"width": "2rem", "height": "2rem"}), style={"margin-top":"10px"})], id="redspinners")], style={"width":"35%"}),

    html.Br(),
    html.Div([
        dbc.ListGroupItem("C) IMBALLAGGIO TERZIARIO", active=False, style={"color": "white"}, color="#004e18"),
        html.Br(),

        dbc.Row([dbc.Col(html.P("Numero di imballaggi secondari per pallet : "), width=5),
                 dbc.Col(dbc.Input(type="number", value=1, size="sm", id="num2", min=1,persistence=True,persistence_type='memory'), width=2),
                 ],
                style={"margin-left": "5px", "font-size": "12px","margin-right": "5px"}),
       dbc.Row([
                 dbc.Col(html.P("Distanza di fornitura (km) : "), width=5),
                 dbc.Col(dbc.Input(type="number", value=0, size="sm", min=0, id="dis4",persistence=True,persistence_type='memory'), width=2)],
                style={"margin-left": "5px", "font-size": "12px","margin-right": "5px"}),
        html.Br(),
       dbc.Card([dbc.CardHeader("Si considerano:"),dbc.CardBody(html.H6(["Un pallet EPA di legno dal peso di 23 kg", html.Br(), "2,4 kg film estensibile LDPE", html.Br(), "2,5 kg di cartone"], className="card-title"))], style={"marigin-right":"30px", "width": "50%", "height":"30%", "background-color":"#DAF0AD"}),
    ], style={"float": "right", "width": "45%"}),
    dbc.ListGroupItem("B) IMBALLAGGIO SECONDARIO", active=False, style={"width": "54%","color":"white"}, color="#004e18"),

    dbc.Table([
                html.Thead(html.Tr(
                    [html.Th("Componente", style={'width': '35%'}), html.Th("Dimensioni", style={'width': '19%'}),
                     html.Th("Peso/unità", style={'width': '36%'}),
                     html.Th("Distanza di Fornitura", style={'width': '10%'}),
                     ])),
                html.Tr([
                    html.Td(dcc.Dropdown(df.loc[(df['Componente'] == 'Secondario')]['Composizione'], 'I01529 cassa cartone', id="2nddd",persistence=True,persistence_type='memory' )),
                    html.Td(html.P(id="2nddim")),
                    html.Td(html.P(id="2ndpeso")),
                    html.Td(dbc.Input(type="number", value=0, size="sm", min=0, id = "dis1",persistence=True,persistence_type='memory')),
                ]),
                html.Tr([
                    html.Td(dcc.Dropdown(df.loc[(df['Componente'] == 'Secondario2')]['Composizione'], 'I00625 coperchio anonimo ',
                                 id="2ndddb",persistence=True,persistence_type='memory')),
                    html.Td(html.P(id="2nddimb")),
                    html.Td(html.P(id="2ndpesob")),
                    html.Td(dbc.Input(type="number", value=0, size="sm", min=0, id = "dis2",persistence=True,persistence_type='memory')),
        ]),

               html.Tr([
                    html.Td(dbc.Checkbox(label="Cartene", id="checkcartene", style={"margin-left":"20px"},persistence=True,persistence_type='memory')),
                    html.Td(dbc.Row(
                        [dbc.Input(type="number",  value=0, min=0, size="sm", id= "2ndarea",persistence=True,persistence_type='memory'), html.P("Inserire l'area (m\u00b2)")])),
                    html.Td(dbc.Row(
                        [dbc.Input(type="number",  value=0, min=0, size="sm",id = "2ndg",persistence=True,persistence_type='memory'), html.P("g / m\u00b2")], style={"margin-left":"10px", "margin-right":"10px"})),
                    html.Td(dbc.Input(type="number", value=0, min=0, size="sm", id = "dis3",persistence=True,persistence_type='memory')),
        ])
    ], bordered=True, style= {"font-size":"12px", "width":"54%"}),
    html.Br(),
    dbc.Row([dbc.Col(html.P("Numero di imballaggi primari per scatola : "), width=4), dbc.Col(dbc.Input(type="number", value=1, min=0, size="sm", id="num1",persistence=True,persistence_type='memory'), width=2)], style= {"margin-left": "10px","font-size":"12px","width":"54%"}),
    html.Br(),
    html.Div([
        dbc.ListGroupItem("E) DISTRIBUZIONE", active=False,
                          style={"color": "white"}, color="#004e18"),
        html.Br(),
        dbc.Row([dbc.Col(html.P("Distanza di distribuzione (km) : "), width=5),
                 dbc.Col(dbc.Input(type="number", value=0, size="sm" , id="finaldis",persistence=True,persistence_type='memory', min=0), width=2)],
                style={"margin-left": "10px", "font-size": "12px"}),
        html.Br(),
        dbc.Card([dbc.CardBody(html.H6(["Trasporto dal sito produttivo di Amadori", html.Br(), "al punto vendita tramite bilico EURO 4", html.Br(), "con capacità \u2245 25 ton refrigerato"], className="card-title"),style={ "margin-left": "10px"})], style={ "width": "50%", "height":"30%", "background-color":"#DAF0AD"})
    ], style={"float": "right", "width": "45%", "margin-top": "25px"}),
    html.Br(),
    dbc.ListGroupItem("D) CONFEZIONAMENTO", active=False,
                      style={"width": "54%","color":"white"}, color="#004e18"),
    html.Br(),

    dbc.Row([dbc.Col([dbc.Row(html.P("Tipo di confezionamento : ")), dbc.Row(html.P("La percentuale di sfrido : "))], width=3),dbc.Col([dbc.Row(dcc.Dropdown(df.loc[(df['Componente'] == 'Confezionamento')]['Composizione'], 'packaging stretch',id="ddconf",persistence=True,persistence_type='memory')), dbc.Row(dbc.Input(type="number", value=0, size="sm",min=0,max=100, id = "sfrido",persistence=True,persistence_type='memory', style={"width":"91%", "margin-left":"12px"}))], width=4),dbc.Col("", width=8)],style= {"font-size":"12px"}),
    html.Br(),
    dbc.Card([dbc.CardBody(html.Img(src=pil_image_sfrido, height="53px", width="373px"))],
             style={"margin-left": "10px","width": "30%", "height": "30%", "background-color": "#DAF0AD"}),

    html.Br(),
    dbc.ListGroupItem(html.H4(id="fromstore"), style={"width":"67%","display":"none"}),
    html.Br(),
    dbc.Alert([dbc.Row(html.H4("Risultati per l'analisi del ciclo di vita del sistema packaging, inteso come imballaggio primario + secondario + terziario",
                              style={"color": "white", "text-align": "center", "margin-top":"10px"})), dbc.Button("Calcola i risultati",
            color="danger",
            className="position-absolute top-0 start-50 translate-middle", n_clicks=None, id = "submit-val2")], color="#004e18",
              style={"margin-left": "20px", "margin-right": "20px"},className="position-relative"),
    html.Div([
        dbc.Table([
            html.Thead(html.Tr(
                [html.Th("Indicatore", style={'width': '50%'}), html.Th("UdM", style={'width': '20%'}),
                 html.Th("Soluzione A", style={'width': '15%'}),
                 html.Th("Soluzione B", style={'width': '15%'}),

                 ])),


            html.Tr([

                         html.Td(dbc.Row([dbc.Col(html.Img(src = pil_image0, height="70px", width="70px"), width=2),dbc.Col(html.P('Acidificazione'))])),
                         html.Td(html.P("Mole of H+ eq.",style={"font-size":"16px"})),
                         html.Td(html.H5(id="GWPtotA0b")),
                         html.Td(html.H5(id="GWPdf0b"),id="colordf0b", style={"color":"white","background-color":"red"}),


                    ]),

            html.Tr([

                html.Td(dbc.Row([dbc.Col(html.Img(src=pil_image, height="70px", width="70px"), width=2),
                                 dbc.Col(html.P('Cambiamento climatico'))])),
                html.Td(html.P("kg CO2 eq.", style={"font-size": "16px"})),
                html.Td(html.H5(id="GWPtotAb")),
                html.Td(html.H5(id="GWPdfb"), id="colordfb", style={"color": "white", "background-color": "red"}),

            ]),
            html.Tr([

                html.Td(dbc.Row([dbc.Col(html.Img(src=pil_image2, height="70px", width="70px"), width=2),
                                 dbc.Col(html.P('Uso del suolo '))])),
                html.Td(html.P("Pt", style={"font-size": "16px"})),

                html.Td(html.H5(id="GWPtotA2b")),
                html.Td(html.H5(id="GWPdf2b"), id="colordf2b", style={"color": "white", "background-color": "red"}),

            ]),
            html.Tr([

                html.Td(dbc.Row([dbc.Col(html.Img(src=pil_image3, height="70px", width="70px"), width=2),
                                 dbc.Col(html.P('Formazione di ozono fotochimico, salute umana '))])),
                html.Td(html.P("kg NMVOC eq.", style={"font-size": "16px"})),

                html.Td(html.H5(id="GWPtotA3b")),
                html.Td(html.H5(id="GWPdf3b"), id="colordf3b", style={"color": "white", "background-color": "red"}),

            ]),
            html.Tr([

                html.Td(dbc.Row([dbc.Col(html.Img(src=pil_image4, height="70px", width="70px"), width=2),
                                 dbc.Col(html.P('Uso di risorse fossili'))])),
                html.Td(html.P("MJ", style={"font-size": "16px"})),

                html.Td(html.H5(id="GWPtotA4b")),
                html.Td(html.H5(id="GWPdf4b"), id="colordf4b", style={"color": "white", "background-color": "red"}),

            ]),
            html.Tr([

                html.Td(dbc.Row([dbc.Col(html.Img(src=pil_image5, height="70px", width="70px"), width=2),
                                 dbc.Col(html.P('Particolato'))])),
                html.Td(html.P("Disease incidences", style={"font-size": "16px"})),

                html.Td(html.H5(id="GWPtotA5b")),
                html.Td(html.H5(id="GWPdf5b"), id="colordf5b", style={"color": "white", "background-color": "red"}),

            ]),

            html.Tr([

                html.Td(dbc.Row([dbc.Col(html.Img(src=pil_image6, height="70px", width="70px"), width=2),
                                 dbc.Col(html.P('Uso acqua'))])),
                html.Td(html.P("m³ eq.", style={"font-size": "16px"})),

                html.Td(html.H5(id="GWPtotA6b")),
                html.Td(html.H5(id="GWPdf6b"), id="colordf6b", style={"color": "white", "background-color": "red"}),

            ]),
        ], style={"width": "70%", "margin-left": "15%", "margin-right": "15%", "font-size": "16px"}, bordered=True),]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Alert(dbc.Row([
        dbc.Col(html.H3("Soluzione A"))])
        , color="#A38000", style={'width': '100%'})),
        dbc.Col(dbc.Alert(dbc.Row([
            dbc.Col(html.H3("Soluzione B"))])
            , color="#D9AA00", style={'width': '100%', "color":"black"}))], style={"margin-left": "10px", "margin-right": "10px"}),
    html.Br(),
    dbc.Row([dbc.Col(dcc.Graph(id='indicator-graphicb')), dbc.Col(dcc.Graph(id='indicator-graphicb2'))], style={"margin-left": "10px", "margin-right": "10px"}),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Table([
                html.Thead(html.Tr(
                    [html.Th("Categorie impatto", style={'width': '10%'}), html.Th("Unità", style={'width': '10%'}), html.Th("Soluzione", style={'width': '8%'}),
                     html.Th("Prod. & trasp. imb. primario", style={'width': '8%'}),
                     html.Th("Prod. & trasp. imb. secondario", style={'width': '8%'}), html.Th("Prod. & trasp. imb. terziario", style={'width': '8%'}),
                     html.Th("Confezionamento", style={'width': '7%'}),html.Th("Distribuzione", style={'width': '8%'}),
                     html.Th("Fine vita imb. secondario", style={'width': '7%'}),
                     html.Th("Fine vita imb. terziario", style={'width': '7%'}),html.Th("Fine vita imb. primario", style={'width': '8%'}),html.Th("Totale", style={'width': '7%'}),
                     # html.Th("Contributo (g CO2 eq.)", style={'width': '2%'})
                     ])),

        html.Tr([
            html.Td(html.P("Acidificazione")),
            html.Td(html.P("Mole of H+ eq.")),
            html.Td(dbc.Row([dbc.Row(html.P("A")), dbc.Row(html.P("B"))])),
            html.Td(dbc.Row([dbc.Row(dbc.Button(id="00", size="sm", style={"font-size": "11px","margin-bottom":"1px"})),
                             dbc.Row(dbc.Button(id="00b", size="sm", style={"font-size": "11px","margin-top":"1px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="01", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="01b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="02", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="02b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="03", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="03b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="04", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="04b", style={"font-size": "12px"}))])),

            html.Td(dbc.Row([dbc.Row(html.P(id="06", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="06b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="07", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="07b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="05", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="05b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="08", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="08b", style={"font-size": "12px"}))])), ]),


        html.Tr([
            html.Td(html.P("Cambiamento climatico tot")),
            html.Td(html.P("kg CO2 eq.")),
            html.Td(dbc.Row([dbc.Row(html.P("A")),dbc.Row(html.P("B"))])),
            html.Td(dbc.Row([dbc.Row(dbc.Button( id="10", size="sm",style={"font-size":"11px","margin-bottom":"1px"})),dbc.Row(dbc.Button(id="10b", size="sm",style={"font-size":"11px","margin-top":"1px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="11", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="11b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="12", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="12b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="13", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="13b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="14", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="14b", style={"font-size": "12px"}))])),

            html.Td(dbc.Row([dbc.Row(html.P(id="16", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="16b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="17", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="17b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="15", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="15b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="18", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="18b", style={"font-size": "12px"}))])),]),

        html.Tr([
            html.Td(html.P("Uso del suolo")),
            html.Td(html.P("Pt")),
            html.Td(dbc.Row([dbc.Row(html.P("A")), dbc.Row(html.P("B"))])),

            html.Td(dbc.Row([dbc.Row(dbc.Button(id="20", size="sm", style={"font-size": "11px","margin-bottom":"1px"})),
                             dbc.Row(dbc.Button(id="20b", size="sm", style={"font-size": "11px","margin-top":"1px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="21", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="21b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="22", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="22b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="23", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="23b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="24", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="24b", style={"font-size": "12px"}))])),

            html.Td(dbc.Row([dbc.Row(html.P(id="26", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="26b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="27", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="27b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="25", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="25b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="28", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="28b", style={"font-size": "12px"}))])), ]),

        html.Tr([
            html.Td(html.P("Particolato")),
            html.Td(html.P("Disease incidences")),
            html.Td(dbc.Row([dbc.Row(html.P("A")), dbc.Row(html.P("B"))])),

            html.Td(dbc.Row([dbc.Row(dbc.Button(id="30", size="sm", style={"font-size": "11px","margin-bottom":"1px"})),
                             dbc.Row(dbc.Button(id="30b", size="sm", style={"font-size": "11px","margin-top":"1px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="31", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="31b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="32", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="32b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="33", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="33b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="34", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="34b", style={"font-size": "12px"}))])),

            html.Td(dbc.Row([dbc.Row(html.P(id="36", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="36b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="37", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="37b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="35", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="35b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="38", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="38b", style={"font-size": "12px"}))])), ]),
        html.Tr([
            html.Td(html.P("Formazione di ozono fotochimico, salute umana")),
            html.Td(html.P("kg NMVOC eq.")),
            html.Td(dbc.Row([dbc.Row(html.P("A")), dbc.Row(html.P("B"))])),

            html.Td(dbc.Row([dbc.Row(dbc.Button(id="40", size="sm", style={"font-size": "11px","margin-bottom":"1px"})),
                             dbc.Row(dbc.Button(id="40b", size="sm", style={"font-size": "11px","margin-top":"1px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="41", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="41b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="42", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="42b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="43", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="43b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="44", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="44b", style={"font-size": "12px"}))])),

            html.Td(dbc.Row([dbc.Row(html.P(id="46", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="46b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="47", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="47b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="45", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="45b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="48", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="48b", style={"font-size": "12px"}))])), ]),
        html.Tr([
            html.Td(html.P("Uso di risorse fossili")),
            html.Td(html.P("MJ")),
            html.Td(dbc.Row([dbc.Row(html.P("A")), dbc.Row(html.P("B"))])),

            html.Td(dbc.Row([dbc.Row(dbc.Button(id="50", size="sm", style={"font-size": "11px","margin-bottom":"1px"})),
                             dbc.Row(dbc.Button(id="50b", size="sm", style={"font-size": "11px","margin-top":"1px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="51", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="51b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="52", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="52b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="53", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="53b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="54", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="54b", style={"font-size": "12px"}))])),

            html.Td(dbc.Row([dbc.Row(html.P(id="56", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="56b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="57", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="57b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="55", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="55b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="58", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="58b", style={"font-size": "12px"}))])), ]),

        html.Tr([
            html.Td(html.P("Uso acqua")),
            html.Td(html.P("m³ equiv.")),
            html.Td(dbc.Row([dbc.Row(html.P("A")), dbc.Row(html.P("B"))])),

            html.Td(dbc.Row([dbc.Row(dbc.Button(id="60", size="sm", style={"font-size": "11px","margin-bottom":"1px"})),
                             dbc.Row(dbc.Button(id="60b", size="sm", style={"font-size": "11px","margin-top":"1px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="61", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="61b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="62", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="62b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="63", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="63b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="64", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="64b", style={"font-size": "12px"}))])),

            html.Td(dbc.Row([dbc.Row(html.P(id="66", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="66b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="67", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="67b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="65", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="65b", style={"font-size": "12px"}))])),
            html.Td(dbc.Row([dbc.Row(html.P(id="68", style={"font-size": "12px"})),
                             dbc.Row(html.P(id="68b", style={"font-size": "12px"}))])), ]),

    ], bordered=True, style= {"font-size":"11px"}))], style={"margin-left": "5px", "margin-right": "5px"}),
    dbc.Button(dbc.Row([dbc.Col(html.Img(src=pil_image_excel, height="30px", width="30px"), width=2), dbc.Col(html.P("Download", style={"margin-left":"10px"}))]), id="btn",n_clicks= 0, style={"float": "right", "margin-right":"30px", "height":"45px"}),
    dcc.Download(id="download"),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.P("© Ecoinnovazione srl 2022. Tutti i diritti riservati", style={"margin-left": "10px", "font-size": "11px"}),
    html.Br(),

    dbc.Popover([dcc.Graph(id='indicator-graphic9')], target="00",  trigger="click",style={"width":"600px","maxWidth":"600px"}),
    dbc.Popover([dcc.Graph(id='indicator-graphic9b')], target="00b", trigger="click",
                style={"width": "600px", "maxWidth": "600px"}),

    dbc.Popover([dcc.Graph(id='indicator-graphic3')], target="10",  trigger="click",style={"width":"600px","maxWidth":"600px"}),
    dbc.Popover([dcc.Graph(id='indicator-graphic3b')], target="10b", trigger="click",
                style={"width": "600px", "maxWidth": "600px"}),
    dbc.Popover([dcc.Graph(id='indicator-graphic4')], target="20", trigger="click",
                style={"width": "600px", "maxWidth": "600px"}),
    dbc.Popover([dcc.Graph(id='indicator-graphic4b')], target="20b", trigger="click",
                style={"width": "600px", "maxWidth": "600px"}),
    dbc.Popover([dcc.Graph(id='indicator-graphic5')], target="30", trigger="click",
                style={"width": "600px", "maxWidth": "600px"}),
    dbc.Popover([dcc.Graph(id='indicator-graphic5b')], target="30b", trigger="click",
                style={"width": "600px", "maxWidth": "600px"}),
    dbc.Popover([dcc.Graph(id='indicator-graphic6')], target="40", trigger="click",
                style={"width": "600px", "maxWidth": "600px"}),
    dbc.Popover([dcc.Graph(id='indicator-graphic6b')], target="40b", trigger="click",
                style={"width": "600px", "maxWidth": "600px"}),
    dbc.Popover([dcc.Graph(id='indicator-graphic7')], target="50", trigger="click",
                style={"width": "600px", "maxWidth": "600px"}),
    dbc.Popover([dcc.Graph(id='indicator-graphic7b')], target="50b", trigger="click",
                style={"width": "600px", "maxWidth": "600px"}),
    dbc.Popover([dcc.Graph(id='indicator-graphic8')], target="60", trigger="click",
                style={"width": "600px", "maxWidth": "600px"}),
    dbc.Popover([dcc.Graph(id='indicator-graphic8b')], target="60b", trigger="click",
                style={"width": "600px", "maxWidth": "600px"}),

    html.Div(id="dashtable2", style={"display":"None"}),
    dbc.Tooltip(id="alert2nd", target="2nddd"),
    dbc.Tooltip(id="alert2ndd", target="2ndddb"),



], style={'backgroundColor': colors['background']})


@callback(
    Output(component_id='sessionvolte', component_property='data'),
    Input(component_id="btn", component_property="n_clicks")
)
def showpeso(input1):

    return input1

@callback(
    Output(component_id='2ndddb', component_property='disabled'),
    Output(component_id='dis2', component_property='disabled'),
    Output(component_id='2ndarea', component_property='disabled'),
    Output(component_id='2ndg', component_property='disabled'),
    Output(component_id='dis3', component_property='disabled'),
    Input(component_id="checkcartene", component_property="value"),



)
def data_store(input1):
    if input1 == True:
        return True, True, False, False, False
    else:
        return False, False, True, True, True

@callback(
    Output(component_id='pesoprodotto', component_property='children'),
    Output(component_id='pesoprodotto', component_property='style'),
    Output(component_id='redspinners', component_property='style'),
    Output(component_id='spin1', component_property='color'),

    [Input(component_id="sessionweight", component_property="data")],
)
def showpeso(input1):
    if input1 == None:
        return "Peso netto / unità: {} g".format(input1), {"color":"red"}, {"display":"block"}, "danger"
    elif input1 > 0:
        return "Peso netto / unità: {} g".format(input1), {"color":"black"}, {"display":"block"},"#DAF0AD"
    else:
        return "Peso netto / unità: {} g".format(input1), {"color":"red"}, {"display":"block"}, "danger"


@callback(
    Output(component_id='alert2nd', component_property='children'),
    Output(component_id='alert2ndd', component_property='children'),
    [Input(component_id='2nddd', component_property='value'),
     Input(component_id='2ndddb', component_property='value')])
def show_specificationpage2(specifiche1, specifiche2):
    spe1 = df.loc[df['Composizione'] == specifiche1]['Ricic']
    spe2 = df.loc[df['Composizione'] == specifiche2]['Ricic']

    return spe1, spe2


@callback(
    Output(component_id='dashtable2', component_property='children'),
    Output(component_id='indicator-graphicb', component_property='figure'),
    Output(component_id='indicator-graphicb2', component_property='figure'),
    Output(component_id='indicator-graphic3', component_property='figure'),
    Output(component_id='indicator-graphic4', component_property='figure'),
    Output(component_id='indicator-graphic5', component_property='figure'),
    Output(component_id='indicator-graphic6', component_property='figure'),
    Output(component_id='indicator-graphic7', component_property='figure'),
    Output(component_id='indicator-graphic8', component_property='figure'),
    Output(component_id='indicator-graphic9', component_property='figure'),

    Output(component_id='indicator-graphic3b', component_property='figure'),
    Output(component_id='indicator-graphic4b', component_property='figure'),
    Output(component_id='indicator-graphic5b', component_property='figure'),
    Output(component_id='indicator-graphic6b', component_property='figure'),
    Output(component_id='indicator-graphic7b', component_property='figure'),
    Output(component_id='indicator-graphic8b', component_property='figure'),
    Output(component_id='indicator-graphic9b', component_property='figure'),
    Output(component_id='colordf0b', component_property='style'),
    Output(component_id='GWPtotA0b', component_property='children'),
    Output(component_id='GWPdf0b', component_property='children'),
    Output(component_id='colordfb', component_property='style'),
    Output(component_id='GWPtotAb', component_property='children'),
    Output(component_id='GWPdfb', component_property='children'),
    Output(component_id='colordf2b', component_property='style'),
    Output(component_id='GWPtotA2b', component_property='children'),
    Output(component_id='GWPdf2b', component_property='children'),
    Output(component_id='colordf3b', component_property='style'),
    Output(component_id='GWPtotA3b', component_property='children'),
    Output(component_id='GWPdf3b', component_property='children'),
    Output(component_id='colordf4b', component_property='style'),
    Output(component_id='GWPtotA4b', component_property='children'),
    Output(component_id='GWPdf4b', component_property='children'),
    Output(component_id='colordf5b', component_property='style'),
    Output(component_id='GWPtotA5b', component_property='children'),
    Output(component_id='GWPdf5b', component_property='children'),
    Output(component_id='colordf6b', component_property='style'),
    Output(component_id='GWPtotA6b', component_property='children'),
    Output(component_id='GWPdf6b', component_property='children'),

    Output(component_id='00', component_property='children'),
    Output(component_id='00b', component_property='children'),
    Output(component_id='01', component_property='children'),
    Output(component_id='01b', component_property='children'),
    Output(component_id='02', component_property='children'),
    Output(component_id='02b', component_property='children'),
    Output(component_id='03', component_property='children'),
    Output(component_id='03b', component_property='children'),
    Output(component_id='04', component_property='children'),
    Output(component_id='04b', component_property='children'),
    Output(component_id='05', component_property='children'),
    Output(component_id='05b', component_property='children'),
    Output(component_id='06', component_property='children'),
    Output(component_id='06b', component_property='children'),
    Output(component_id='07', component_property='children'),
    Output(component_id='07b', component_property='children'),
    Output(component_id='08', component_property='children'),
    Output(component_id='08b', component_property='children'),

    Output(component_id='10', component_property='children'),
    Output(component_id='10b', component_property='children'),
    Output(component_id='11', component_property='children'),
    Output(component_id='11b', component_property='children'),
    Output(component_id='12', component_property='children'),
    Output(component_id='12b', component_property='children'),
    Output(component_id='13', component_property='children'),
    Output(component_id='13b', component_property='children'),
    Output(component_id='14', component_property='children'),
    Output(component_id='14b', component_property='children'),
    Output(component_id='15', component_property='children'),
    Output(component_id='15b', component_property='children'),
    Output(component_id='16', component_property='children'),
    Output(component_id='16b', component_property='children'),
    Output(component_id='17', component_property='children'),
    Output(component_id='17b', component_property='children'),
    Output(component_id='18', component_property='children'),
    Output(component_id='18b', component_property='children'),

    Output(component_id='20', component_property='children'),
    Output(component_id='20b', component_property='children'),
    Output(component_id='21', component_property='children'),
    Output(component_id='21b', component_property='children'),
    Output(component_id='22', component_property='children'),
    Output(component_id='22b', component_property='children'),
    Output(component_id='23', component_property='children'),
    Output(component_id='23b', component_property='children'),
    Output(component_id='24', component_property='children'),
    Output(component_id='24b', component_property='children'),
    Output(component_id='25', component_property='children'),
    Output(component_id='25b', component_property='children'),
    Output(component_id='26', component_property='children'),
    Output(component_id='26b', component_property='children'),
    Output(component_id='27', component_property='children'),
    Output(component_id='27b', component_property='children'),
    Output(component_id='28', component_property='children'),
    Output(component_id='28b', component_property='children'),

    Output(component_id='30', component_property='children'),
    Output(component_id='30b', component_property='children'),
    Output(component_id='31', component_property='children'),
    Output(component_id='31b', component_property='children'),
    Output(component_id='32', component_property='children'),
    Output(component_id='32b', component_property='children'),
    Output(component_id='33', component_property='children'),
    Output(component_id='33b', component_property='children'),
    Output(component_id='34', component_property='children'),
    Output(component_id='34b', component_property='children'),
    Output(component_id='35', component_property='children'),
    Output(component_id='35b', component_property='children'),
    Output(component_id='36', component_property='children'),
    Output(component_id='36b', component_property='children'),
    Output(component_id='37', component_property='children'),
    Output(component_id='37b', component_property='children'),
    Output(component_id='38', component_property='children'),
    Output(component_id='38b', component_property='children'),

    Output(component_id='40', component_property='children'),
    Output(component_id='40b', component_property='children'),
    Output(component_id='41', component_property='children'),
    Output(component_id='41b', component_property='children'),
    Output(component_id='42', component_property='children'),
    Output(component_id='42b', component_property='children'),
    Output(component_id='43', component_property='children'),
    Output(component_id='43b', component_property='children'),
    Output(component_id='44', component_property='children'),
    Output(component_id='44b', component_property='children'),
    Output(component_id='45', component_property='children'),
    Output(component_id='45b', component_property='children'),
    Output(component_id='46', component_property='children'),
    Output(component_id='46b', component_property='children'),
    Output(component_id='47', component_property='children'),
    Output(component_id='47b', component_property='children'),
    Output(component_id='48', component_property='children'),
    Output(component_id='48b', component_property='children'),
    Output(component_id='50', component_property='children'),
    Output(component_id='50b', component_property='children'),
    Output(component_id='51', component_property='children'),
    Output(component_id='51b', component_property='children'),
    Output(component_id='52', component_property='children'),
    Output(component_id='52b', component_property='children'),
    Output(component_id='53', component_property='children'),
    Output(component_id='53b', component_property='children'),
    Output(component_id='54', component_property='children'),
    Output(component_id='54b', component_property='children'),
    Output(component_id='55', component_property='children'),
    Output(component_id='55b', component_property='children'),
    Output(component_id='56', component_property='children'),
    Output(component_id='56b', component_property='children'),
    Output(component_id='57', component_property='children'),
    Output(component_id='57b', component_property='children'),
    Output(component_id='58', component_property='children'),
    Output(component_id='58b', component_property='children'),
    Output(component_id='60', component_property='children'),
    Output(component_id='60b', component_property='children'),
    Output(component_id='61', component_property='children'),
    Output(component_id='61b', component_property='children'),
    Output(component_id='62', component_property='children'),
    Output(component_id='62b', component_property='children'),
    Output(component_id='63', component_property='children'),
    Output(component_id='63b', component_property='children'),
    Output(component_id='64', component_property='children'),
    Output(component_id='64b', component_property='children'),
    Output(component_id='65', component_property='children'),
    Output(component_id='65b', component_property='children'),
    Output(component_id='66', component_property='children'),
    Output(component_id='66b', component_property='children'),
    Output(component_id='67', component_property='children'),
    Output(component_id='67b', component_property='children'),
    Output(component_id='68', component_property='children'),
    Output(component_id='68b', component_property='children'),
    Output(component_id='download', component_property='data'),

    [Input("submit-val2", 'n_clicks'),
    Input("btn", 'n_clicks'),
    State(component_id='sessionvolte', component_property='data'),
    State(component_id="sessiondata", component_property="data"),
    State(component_id="sessioncolumn", component_property="data"),
    State(component_id="sessiondataexcel", component_property="data"),
    State(component_id="sessioncolumnexcel", component_property="data"),
    State(component_id="2nddd", component_property="value"),
    State(component_id="2ndddb", component_property="value"),
    State(component_id="2ndarea", component_property="value"),
    State(component_id="2ndg", component_property="value"),
    State(component_id="dis1", component_property="value"),
    State(component_id="dis2", component_property="value"),
    State(component_id="dis3", component_property="value"),
    State(component_id="dis4", component_property="value"),
    State(component_id="num1", component_property="value"),
    State(component_id="num2", component_property="value"),
    State(component_id="sfrido", component_property="value"),
    State(component_id="ddconf", component_property="value"),
    State(component_id="sessionweight", component_property="data"),
    State(component_id="sessionpeso", component_property="data"),
    State(component_id="sessionpesob", component_property="data"),
    State(component_id="finaldis", component_property="value"),
    State(component_id="checkcartene", component_property="value")],
    prevent_initial_call=True,
    suppress_callback_exceptions = True

)
def data_store(inputdokmeh2, dokmeexcel, volte, data, column,dataexcel, columnexcel, input1, input2, input3, input4, dis1, dis2, dis3, dis4, num1, num2, sfrido, ddconf, inputweight, peso, pesob, finaldis, checkcartene):
    schifosso = pd.DataFrame(data, columns=[c['name'] for c in column])
    Inputexcel = pd.DataFrame(dataexcel, columns=[c['name'] for c in columnexcel])

    Inputexcel2 = pd.DataFrame({

        "0": ["Secondario", "Secondario", "Secondario", "Secondario", "######", "Terziario", "######", "Confezionamento", "######", "Distribuzione"],
        "1": [input1, input2,"Cartene", "Numero di imballaggi primari per scatola : {}".format(num1),  "######", "Numero di imballaggi secondari per pallet : {}".format(num2), "######", "Tipo: {}".format(ddconf), "######", "######"],
        "2": ["Dimensioni: {}".format(df.loc[(df['Composizione'] == input1)]['Specifiche'].values[0]), "Dimensioni: {}".format(df.loc[(df['Composizione'] == input2)]['Specifiche'].values[0]),"area: {} m2".format(input3), "######", "######", "######",  "######", "Peso netto / unità: {} g".format(inputweight), "######", "######"],
        "3": ["Peso/unità: {}".format(df.loc[(df['Composizione'] == input1)]['More'].values[0]), "Peso/unità: {}".format(df.loc[(df['Composizione'] == input2)]['More'].values[0]), "Peso/unità: {} g/m2".format(input4), "######", "######", "######",  "######","La percentuale di sfrido : {} %".format(sfrido), "######", "######"],
        "4": ["Distanza: {} km".format(dis1),"Distanza: {} km".format(dis2),"Distanza: {} km".format(dis3), "######", "######", "Distanza: {} km".format(dis4),"######", "######", "######", "Distanza: {} km".format(finaldis)],


    })

    impacts = ["Acidificazione", "Cambiamento climatico tot"
        , "Uso del suolo", "Particolato",
               "Formazione di ozono fotochimico, salute umana", "Uso di risorse fossili",
               "Uso acqua"]
    if inputdokmeh2 != 0:
        secondario = []
        EoLsecond = []
        if checkcartene == True:
            secondpeso = ((df.loc[(df['Composizione'] == input1)]['Extra'].values[0]) + (
                        input3 * input4 * 0.001)) / num1
            for i in impacts:
                second = (df.loc[(df['Composizione'] == input1)]['Extra'].values[0]) * (
                    df.loc[(df['Composizione'] == input1)][i].values[0])

                second2 = (input3 * input4 * 0.001) * (
                df.loc[(df['Composizione'] == "Foglio plastico sfuso")][i].values[0])
                trasp = ((df.loc[(df['Composizione'] == input1)]['Extra'].values[0]) + (input3 * input4 * 0.001)) * (
                        dis1 + dis3) * (df.loc[(df['Componente'] == "Trasporto")][i].values[0])
                eolsecond = ((df.loc[(df['Composizione'] == input1)]['Extra'].values[0]) + (
                            input3 * input4 * 0.001)) * (
                            df.loc[(df['Composizione'] == "EoL second")][i].values[0]) / num1
                EoLsecond.append(eolsecond)
                tot = (second + second2 + trasp) / num1
                secondario.append(tot)

        else:
            secondpeso = ((df.loc[(df['Composizione'] == input1)]['Extra'].values[0]) + (
                df.loc[(df['Composizione'] == input2)]['Extra'].values[0])) / num1
            for i in impacts:
                second = (df.loc[(df['Composizione'] == input1)]['Extra'].values[0]) * (
                df.loc[(df['Composizione'] == input1)][i].values[0])
                second2 = (df.loc[(df['Composizione'] == input2)]['Extra'].values[0]) * (
                df.loc[(df['Composizione'] == input2)][i].values[0])
                trasp = ((df.loc[(df['Composizione'] == input1)]['Extra'].values[0]) + (
                    df.loc[(df['Composizione'] == input2)]['Extra'].values[0])) * (dis1 + dis2) * (
                            df.loc[(df['Componente'] == "Trasporto")][i].values[0])
                eolsecond = ((df.loc[(df['Composizione'] == input1)]['Extra'].values[0]) + (
                    df.loc[(df['Composizione'] == input2)]['Extra'].values[0])) * (
                            df.loc[(df['Composizione'] == "EoL second")][i].values[0]) / num1
                EoLsecond.append(eolsecond)
                tot = (second + second2 + trasp) / num1
                secondario.append(tot)
        terziario = []
        EoLter = []
        thirdpeso = 29.9 / (num1 * num2)
        for i in impacts:
            ter = ((df.loc[(df['Composizione'] == "pallet in legno")][i].values[0]) + (
            df.loc[(df['Composizione'] == "angolari in cartone")][i].values[0]) + (
                       df.loc[(df['Composizione'] == "film estensibile LDPE")][i].values[0])) / (num1 * num2)
            traspter = dis4 * (29.9 / (num1 * num2)) * (df.loc[(df['Componente'] == "Trasporto")][i].values[0])
            totter = ter + traspter
            terziario.append(totter)
            eolter = ((df.loc[(df['Composizione'] == "EoL pallet in legno")][i].values[0]) + (
            df.loc[(df['Composizione'] == "EoL angolari in cartone")][i].values[0]) + (
                          df.loc[(df['Composizione'] == "EoL film estensibile LDPE")][i].values[0])) / (num1 * num2)
            EoLter.append(eolter)

        if (schifosso["sum"].sum(axis=0) == 0) & (schifosso["sumb"].sum(axis=0) != 0):
            firsttwo = []
            for i in impacts:
                firstpart = df.loc[(df['Componente'] == ddconf)][i].values[0] * 1
                secondpart = (df.loc[(df['Componente'] == "part2")][i].values[0]) * (inputweight * 0.001)
                firstsecond = firstpart + secondpart
                firsttwo.append(firstsecond)

            if ddconf == "packaging skin":
                thirdpartb = [
                    ((x / (1 - (sfrido * 0.01))) * sfrido * 0.01) + ((y / (1 - (sfrido * 0.01))) * sfrido * 0.01)
                    for x, y in zip(schifosso["EoL Topb"], schifosso["EoL Bottomb"])]
                schifosso["Topb"] = [(x / (1 - (sfrido * 0.01))) for x in schifosso["Topb"]]
                schifosso["Bottomb"] = [(x / (1 - (sfrido * 0.01))) for x in schifosso["Bottomb"]]

            if (ddconf == "packaging stretch") or (ddconf == "packaging termosaldato"):
                thirdpartb = [((x / (1 - (sfrido * 0.01))) * sfrido * 0.01) for x in schifosso["EoL Topb"]]
                schifosso["Topb"] = [(x / (1 - (sfrido * 0.01))) for x in schifosso["Topb"]]

            if ddconf == "packaging sottovuoto":
                thirdpartb = [((x / (1 - (sfrido * 0.01))) * sfrido * 0.01) for x in schifosso["EoL Bustab"]]
                schifosso["Bustab"] = [(x / (1 - (sfrido * 0.01))) for x in schifosso["Bustab"]]

            confezionamneto = [0, 0, 0, 0, 0, 0, 0]
            confezionamentob = [x + y for x, y in zip(firsttwo, thirdpartb)]

        elif (schifosso["sum"].sum(axis=0) != 0) & (schifosso["sumb"].sum(axis=0) == 0):
            firsttwo = []
            for i in impacts:
                firstpart = df.loc[(df['Componente'] == ddconf)][i].values[0] * 1
                secondpart = (df.loc[(df['Componente'] == "part2")][i].values[0]) * (inputweight * 0.001)
                firstsecond = firstpart + secondpart
                firsttwo.append(firstsecond)

            if ddconf == "packaging skin":
                thirdpart = [
                    ((x / (1 - (sfrido * 0.01))) * sfrido * 0.01) + ((y / (1 - (sfrido * 0.01))) * sfrido * 0.01)
                    for x, y in zip(schifosso["EoL Top"], schifosso["EoL Bottom"])]
                schifosso["Top"] = [(x / (1 - (sfrido * 0.01))) for x in schifosso["Top"]]
                schifosso["Bottom"] = [(x / (1 - (sfrido * 0.01))) for x in schifosso["Bottom"]]

            if (ddconf == "packaging stretch") or (ddconf == "packaging termosaldato"):
                thirdpart = [((x / (1 - (sfrido * 0.01))) * sfrido * 0.01) for x in schifosso["EoL Top"]]
                schifosso["Top"] = [(x / (1 - (sfrido * 0.01))) for x in schifosso["Top"]]

            if ddconf == "packaging sottovuoto":
                thirdpart = [((x / (1 - (sfrido * 0.01))) * sfrido * 0.01) for x in schifosso["EoL Busta"]]
                schifosso["Busta"] = [(x / (1 - (sfrido * 0.01))) for x in schifosso["Busta"]]

            confezionamneto = [x + y for x, y in zip(firsttwo, thirdpart)]
            confezionamentob = [0, 0, 0, 0, 0, 0, 0]

        elif (schifosso["sum"].sum(axis=0) == 0) & (schifosso["sumb"].sum(axis=0) == 0):
            confezionamneto = [0, 0, 0, 0, 0, 0, 0]
            confezionamentob = [0, 0, 0, 0, 0, 0, 0]

        elif (schifosso["sum"].sum(axis=0) != 0) & (schifosso["sumb"].sum(axis=0) != 0):
            firsttwo = []
            for i in impacts:
                firstpart = df.loc[(df['Componente'] == ddconf)][i].values[0] * 1
                secondpart = (df.loc[(df['Componente'] == "part2")][i].values[0]) * (inputweight * 0.001)
                firstsecond = firstpart + secondpart
                firsttwo.append(firstsecond)

            if ddconf == "packaging skin":
                thirdpart = [
                    ((x / (1 - (sfrido * 0.01))) * sfrido * 0.01) + ((y / (1 - (sfrido * 0.01))) * sfrido * 0.01)
                    for x, y in zip(schifosso["EoL Top"], schifosso["EoL Bottom"])]
                thirdpartb = [
                    ((x / (1 - (sfrido * 0.01))) * sfrido * 0.01) + ((y / (1 - (sfrido * 0.01))) * sfrido * 0.01)
                    for x, y in zip(schifosso["EoL Topb"], schifosso["EoL Bottomb"])]
                schifosso["Top"] = [(x / (1 - (sfrido * 0.01))) for x in schifosso["Top"]]
                schifosso["Bottom"] = [(x / (1 - (sfrido * 0.01))) for x in schifosso["Bottom"]]
                schifosso["Topb"] = [(x / (1 - (sfrido * 0.01))) for x in schifosso["Topb"]]
                schifosso["Bottomb"] = [(x / (1 - (sfrido * 0.01))) for x in schifosso["Bottomb"]]

            if (ddconf == "packaging stretch") or (ddconf == "packaging termosaldato"):
                thirdpart = [((x / (1 - (sfrido * 0.01))) * sfrido * 0.01) for x in schifosso["EoL Top"]]
                thirdpartb = [((x / (1 - (sfrido * 0.01))) * sfrido * 0.01) for x in schifosso["EoL Topb"]]
                schifosso["Top"] = [(x / (1 - (sfrido * 0.01))) for x in schifosso["Top"]]
                schifosso["Topb"] = [(x / (1 - (sfrido * 0.01))) for x in schifosso["Topb"]]

            if ddconf == "packaging sottovuoto":
                thirdpart = [((x / (1 - (sfrido * 0.01))) * sfrido * 0.01) for x in schifosso["EoL Busta"]]
                thirdpartb = [((x / (1 - (sfrido * 0.01))) * sfrido * 0.01) for x in schifosso["EoL Bustab"]]
                schifosso["Busta"] = [(x / (1 - (sfrido * 0.01))) for x in schifosso["Busta"]]
                schifosso["Bustab"] = [(x / (1 - (sfrido * 0.01))) for x in schifosso["Bustab"]]

            confezionamneto = [x + y for x, y in zip(firsttwo, thirdpart)]
            confezionamentob = [x + y for x, y in zip(firsttwo, thirdpartb)]

        Distribution = []
        Distributionb = []
        for i in impacts:
            distribution = (df.loc[(df['Componente'] == "Distribution")][i].values[0] * 1) * (
                        secondpeso + thirdpeso + peso) * finaldis
            distributionb = (df.loc[(df['Componente'] == "Distribution")][i].values[0] * 1) * (
                        secondpeso + thirdpeso + pesob) * finaldis
            Distribution.append(distribution)
            Distributionb.append(distributionb)

    else:
        secondario = [0,0,0,0,0,0,0]
        EoLsecond = [0,0,0,0,0,0,0]
        terziario = [0,0,0,0,0,0,0]
        EoLter = [0,0,0,0,0,0,0]
        confezionamneto = [0,0,0,0,0,0,0]
        confezionamentob = [0,0,0,0,0,0,0]
        Distribution = [0,0,0,0,0,0,0]
        Distributionb = [0,0,0,0,0,0,0]

    schifosso["secondario"] = secondario
    schifosso["secondario EoL"] = EoLsecond
    schifosso["terziario"] = terziario
    schifosso["terziario EoL"] = EoLter
    schifosso["Confezionamento a"] = confezionamneto
    schifosso["Confezionamento b"] = confezionamentob
    schifosso["Distribution"] = Distribution
    schifosso["Distribution b"] = Distributionb

    primb = ["Vassoiob",  "Transport Vassoiob", "Padb",  "Transport Padb", "Topb",
                "Transport Topb", "Bottomb",  "Transport Bottomb",
                "Supportob",  "Transport Supportob", "Bustab", "Transport Bustab"]
    prim = ["Vassoio", "Transport Vassoio", "Pad", "Transport Pad", "Top",
             "Transport Top", "Bottom", "Transport Bottom",
             "Supporto", "Transport Supporto", "Busta", "Transport Busta"]
    Endprim = [ "EoL Vassoio",  "EoL Pad",  "EoL Top",
                 "EoL Bottom",  "EoL Supporto",  "EoL Busta"]
    Endprimb = [ "EoL Vassoiob",  "EoL Padb",  "EoL Topb",
                 "EoL Bottomb",  "EoL Supportob",  "EoL Bustab"]

    schifosso['Primariob'] = schifosso[primb].sum(axis=1)
    schifosso['Primario'] = schifosso[prim].sum(axis=1)
    schifosso['endprim'] = schifosso[Endprim].sum(axis=1)
    schifosso['endprimb'] = schifosso[Endprimb].sum(axis=1)

    Total = ['Primario', 'endprim', "secondario", "secondario EoL", "terziario", "terziario EoL", "Confezionamento a", "Distribution"  ]
    Totalb = ['Primariob', 'endprimb', "secondario", "secondario EoL", "terziario", "terziario EoL", "Confezionamento b", "Distribution b"]

    schifosso['Total'] = schifosso[Total].sum(axis=1)
    schifosso['Totalb'] = schifosso[Totalb].sum(axis=1)

    schifossoExcel = pd.DataFrame({

        "Indicatore": schifosso["Indicator"],
        "UdM": ["Mole of H+ eq.", "kg CO2 eq.", "Pt", "kg NMVOC eq.", "MJ", "Disease incidences", "m³ eq."],
        "Vassoio produzione (Soluzione A)": schifosso["Vassoio"],
        "Vassoio EoL (Soluzione A)": schifosso["EoL Vassoio"],
        "Vassoio Trasporto (Soluzione A)": schifosso["Transport Vassoio"],
        "Vassoio produzione (Soluzione B)": schifosso["Vassoiob"],
        "Vassoio EoL (Soluzione B)": schifosso["EoL Vassoiob"],
        "Vassoio Trasporto (Soluzione B)": schifosso["Transport Vassoiob"],
        "Pad assorbente produzione (Soluzione A)": schifosso["Pad"],
        "Pad assorbente EoL (Soluzione A)": schifosso["EoL Pad"],
        "Pad assorbente Trasporto (Soluzione A)": schifosso["Transport Pad"],
        "Pad assorbente produzione (Soluzione B)": schifosso["Padb"],
        "Pad assorbente EoL (Soluzione B)": schifosso["EoL Padb"],
        "Pad assorbente Trasporto (Soluzione B)": schifosso["Transport Padb"],

        "Top flessibile produzione (Soluzione A)": schifosso["Top"],
        "Top flessibile EoL (Soluzione A)": schifosso["EoL Top"],
        "Top flessibile Trasporto (Soluzione A)": schifosso["Transport Top"],
        "Top flessibile produzione (Soluzione B)": schifosso["Topb"],
        "Top flessibile EoL (Soluzione B)": schifosso["EoL Topb"],
        "Top flessibile Trasporto (Soluzione B)": schifosso["Transport Topb"],

        "Bottom flessibile produzione (Soluzione A)": schifosso["Bottom"],
        "Bottom flessibile EoL (Soluzione A)": schifosso["EoL Bottom"],
        "Bottom flessibile Trasporto (Soluzione A)": schifosso["Transport Bottom"],
        "Bottom flessibile produzione (Soluzione B)": schifosso["Bottomb"],
        "Bottom flessibile EoL (Soluzione B)": schifosso["EoL Bottomb"],
        "Bottom flessibile Trasporto (Soluzione B)": schifosso["Transport Bottomb"],

        "Supporto in cellulosa produzione (Soluzione A)": schifosso["Supporto"],
        "Supporto in cellulosa EoL (Soluzione A)": schifosso["EoL Supporto"],
        "Supporto in cellulosa Trasporto (Soluzione A)": schifosso["Transport Supporto"],
        "Supporto in cellulosa produzione (Soluzione B)": schifosso["Supportob"],
        "Supporto in cellulosa EoL (Soluzione B)": schifosso["EoL Supportob"],
        "Supporto in cellulosa Trasporto (Soluzione B)": schifosso["Transport Supportob"],

        "Busta produzione (Soluzione A)": schifosso["Busta"],
        "Busta EoL (Soluzione A)": schifosso["EoL Busta"],
        "Busta Trasporto (Soluzione A)": schifosso["Transport Busta"],
        "Busta produzione (Soluzione B)": schifosso["Bustab"],
        "Busta EoL (Soluzione B)": schifosso["EoL Bustab"],
        "Busta Trasporto (Soluzione B)": schifosso["Transport Bustab"],



        "Imballaggio Primario produzione & trasporto (Soluzione A)": schifosso["Primario"],
        "Imballaggio Primario produzione & trasporto (Soluzione B)": schifosso["Primariob"],

        "Imballaggio Primario EoL (Soluzione A)": schifosso["endprim"],
        "Imballaggio Primario EoL (Soluzione B)": schifosso["endprimb"],

        "Imballaggio Secondario produzione & trasporto (Soluzione A/B)": schifosso["secondario"],
        "Imballaggio Secondario EoL (Soluzione A/B)": schifosso["secondario EoL"],

        "Imballaggio Terziario produzione & trasporto (Soluzione A/B)": schifosso["terziario"],
        "Imballaggio Terziario EoL (Soluzione A/B)": schifosso["terziario EoL"],

        "Confezionamento (Soluzione A)": schifosso["Confezionamento a"],
        "Confezionamento (Soluzione B)": schifosso["Confezionamento b"],

        "Distribuzione (Soluzione A/B)": schifosso["Distribution"],

        "Total (Soluzione A)": schifosso["Total"],
        "Total (Soluzione B)": schifosso["Totalb"],


    })

    if dokmeexcel > volte:
        name = datetime.now().strftime('%d%H%M')
        writer = pd.ExcelWriter('Amadori_'+name+'.xlsx', engine='xlsxwriter')
        workbook = writer.book
        worksheet = workbook.add_worksheet('General')
        worksheet.write('A1',
                         'This result is created on  ' + datetime.now().strftime('%d %b %Y %H:%M') + ' through CF tool.',
                         workbook.add_format({'bold': True, 'color': '#E26B0A', 'size': 14}))

        Inputexcel.to_excel(writer, sheet_name='Input Primario')
        Inputexcel2.to_excel(writer, sheet_name='Input Secondario&Terziario')
        schifossoExcel.to_excel(writer, sheet_name='Results')

        writer.save()
        dl = dcc.send_file('Amadori_'+name+'.xlsx')
    else:
        dl = None


    difference0 = ((schifosso.iloc[0, 52] - schifosso.iloc[0, 51]) / (schifosso.iloc[0, 51])) * 100
    difmsg0 = "{} %".format("{:.0f}".format(difference0))
    GWPtotA0 = "{}".format("{:.2e}".format(schifosso.iloc[0, 51]))

    if -10 <= difference0 <= 10:
        rang0 = {"color": "black", "background-color": "yellow"}
    elif difference0 > 10:
        rang0 = {"color": "white", "background-color": "red"}
    elif difference0 < -10:
        rang0 = {"color": "white", "background-color": "green"}

    difference = ((schifosso.iloc[1, 52] - schifosso.iloc[1, 51]) / (schifosso.iloc[1, 51])) * 100
    difmsg = "{} %".format("{:.0f}".format(difference))
    GWPtotA = "{}".format("{:.2e}".format(schifosso.iloc[1, 51]))

    if -10 <= difference <= 10:
        rang = {"color": "black", "background-color": "yellow"}
    elif difference > 10:
        rang = {"color": "white", "background-color": "red"}
    elif difference < -10:
        rang = {"color": "white", "background-color": "green"}

    difference2 = ((schifosso.iloc[2, 52] - schifosso.iloc[2, 51]) / (schifosso.iloc[2, 51])) * 100
    difmsg2 = "{} %".format("{:.0f}".format(difference2))
    GWPtotA2 = "{}".format("{:.2e}".format(schifosso.iloc[2, 51]))

    if -10 <= difference2 <= 10:
        rang2 = {"color": "black", "background-color": "yellow"}
    elif difference2 > 10:
        rang2 = {"color": "white", "background-color": "red"}
    elif difference2 < -10:
        rang2 = {"color": "white", "background-color": "green"}

    difference3 = ((schifosso.iloc[3, 52] - schifosso.iloc[3, 51]) / (schifosso.iloc[3, 51])) * 100
    difmsg3 = "{} %".format("{:.0f}".format(difference3))
    GWPtotA3 = "{}".format("{:.2e}".format(schifosso.iloc[3, 51]))
    if -10 <= difference3 <= 10:
        rang3 = {"color": "black", "background-color": "yellow"}
    elif difference3 > 10:
        rang3 = {"color": "white", "background-color": "red"}
    elif difference3 < -10:
        rang3 = {"color": "white", "background-color": "green"}

    difference4 = ((schifosso.iloc[4, 52] - schifosso.iloc[4, 51]) / (schifosso.iloc[4, 51])) * 100
    difmsg4 = "{} %".format("{:.0f}".format(difference4))
    GWPtotA4 = "{}".format("{:.2e}".format(schifosso.iloc[4, 51]))
    if -10 <= difference4 <= 10:
        rang4 = {"color": "black", "background-color": "yellow"}
    elif difference4 > 10:
        rang4 = {"color": "white", "background-color": "red"}
    elif difference4 < -10:
        rang4 = {"color": "white", "background-color": "green"}

    difference5 = ((schifosso.iloc[5, 52] - schifosso.iloc[5, 51]) / (schifosso.iloc[5, 51])) * 100
    difmsg5 = "{} %".format("{:.0f}".format(difference5))
    GWPtotA5 = "{}".format("{:.2e}".format(schifosso.iloc[5, 51]))
    if -10 <= difference5 <= 10:
        rang5 = {"color": "black", "background-color": "yellow"}
    elif difference5 > 10:
        rang5 = {"color": "white", "background-color": "red"}
    elif difference5 < -10:
        rang5 = {"color": "white", "background-color": "green"}

    difference6 = ((schifosso.iloc[6, 52] - schifosso.iloc[6, 51]) / (schifosso.iloc[6, 51])) * 100
    difmsg6 = "{} %".format("{:.0f}".format(difference6))
    GWPtotA6 = "{}".format("{:.2e}".format(schifosso.iloc[6, 51]))

    if -10 <= difference6 <= 10:
        rang6 = {"color": "black", "background-color": "yellow"}
    elif difference6 > 10:
        rang6 = {"color": "white", "background-color": "red"}
    elif difference6 < -10:
        rang6 = {"color": "white", "background-color": "green"}

    schifosso2 = schifosso[Total].abs()
    schifosso3 = schifosso[Totalb].abs()

    schifosso2['Totalabs'] = schifosso2[Total].sum(axis=1)
    schifosso3['Totalbabs'] = schifosso3[Totalb].sum(axis=1)


    prod1 = [round(100 * abs(x) / y,1) for x,y in zip(schifosso["Primario"], schifosso2['Totalabs'])]
    prod2 = [round(100 * abs(x) / y,1) for x,y in zip(schifosso["secondario"], schifosso2['Totalabs'])]
    prod3 = [round(100 * abs(x) / y,1) for x,y in zip(schifosso["terziario"], schifosso2['Totalabs'])]
    conf = [round(100 * abs(x) / y,1) for x,y in zip(schifosso["Confezionamento a"], schifosso2['Totalabs'])]
    dist = [round(100 * abs(x) / y,1) for x,y in zip(schifosso["Distribution"], schifosso2['Totalabs'])]
    fine1 = [round(100 * abs(x) / y,1) for x,y in zip(schifosso["endprim"], schifosso2['Totalabs'])]
    fine2 = [round(100 * abs(x) / y,1) for x,y in zip(schifosso["secondario EoL"], schifosso2['Totalabs'])]
    fine3 = [round(100 * abs(x) / y,1) for x,y in zip(schifosso["terziario EoL"], schifosso2['Totalabs'])]

    prod1b = [round(100 * abs(x) / y,1) for x,y in zip(schifosso["Primariob"], schifosso3['Totalbabs'])]
    prod2b = [round(100 * abs(x) / y,1) for x,y in zip(schifosso["secondario"], schifosso3['Totalbabs'])]
    prod3b = [round(100 * abs(x) / y,1) for x,y in zip(schifosso["terziario"], schifosso3['Totalbabs'])]
    confb = [round(100 * abs(x) / y,1) for x,y in zip(schifosso["Confezionamento b"], schifosso3['Totalbabs'])]
    distb = [round(100 * abs(x) / y,1) for x,y in zip(schifosso["Distribution b"], schifosso3['Totalbabs'])]
    fine1b = [round(100 * abs(x) / y,1) for x,y in zip(schifosso["endprimb"], schifosso3['Totalbabs'])]
    fine2b = [round(100 * abs(x) / y,1) for x,y in zip(schifosso["secondario EoL"], schifosso3['Totalbabs'])]
    fine3b = [round(100 * abs(x) / y,1) for x,y in zip(schifosso["terziario EoL"], schifosso3['Totalbabs'])]

    if ((schifosso["Primario"].sum(axis=0) == 0) and (schifosso["Primariob"].sum(axis=0) != 0)):
        vasprod = [0, 0, 0, 0, 0, 0,0]
        padprod = [0, 0, 0, 0, 0, 0,0]
        topprod = [0, 0, 0, 0, 0, 0,0]
        botprod = [0, 0, 0, 0, 0, 0,0]
        supprod = [0, 0, 0, 0, 0, 0,0]
        busprod = [0, 0, 0, 0, 0, 0,0]

        vasprodb = [round(100 * (x + y) / z, 1) for x, y, z in
                    zip(schifosso["Vassoiob"], schifosso['Transport Vassoiob'], schifosso["Primariob"])]
        padprodb = [round(100 * (x + y) / z, 1) for x, y, z in
                    zip(schifosso["Padb"], schifosso['Transport Padb'], schifosso["Primariob"])]
        topprodb = [round(100 * (x + y) / z, 1) for x, y, z in
                    zip(schifosso["Topb"], schifosso['Transport Topb'], schifosso["Primariob"])]
        botprodb = [round(100 * (x + y) / z, 1) for x, y, z in
                    zip(schifosso["Bottomb"], schifosso['Transport Bottomb'], schifosso["Primariob"])]
        supprodb = [round(100 * (x + y) / z, 1) for x, y, z in
                    zip(schifosso["Supportob"], schifosso['Transport Supportob'], schifosso["Primariob"])]
        busprodb = [round(100 * (x + y) / z, 1) for x, y, z in
                    zip(schifosso["Bustab"], schifosso['Transport Bustab'], schifosso["Primariob"])]
    elif ((schifosso["Primario"].sum(axis=0) != 0) and (schifosso["Primariob"].sum(axis=0) == 0)):
        vasprod = [round(100 * (x + y) / z, 1) for x, y, z in
                   zip(schifosso["Vassoio"], schifosso['Transport Vassoio'], schifosso["Primario"])]
        padprod = [round(100 * (x + y) / z, 1) for x, y, z in
                   zip(schifosso["Pad"], schifosso['Transport Pad'], schifosso["Primario"])]
        topprod = [round(100 * (x + y) / z, 1) for x, y, z in
                   zip(schifosso["Top"], schifosso['Transport Top'], schifosso["Primario"])]
        botprod = [round(100 * (x + y) / z, 1) for x, y, z in
                   zip(schifosso["Bottom"], schifosso['Transport Bottom'], schifosso["Primario"])]
        supprod = [round(100 * (x + y) / z, 1) for x, y, z in
                   zip(schifosso["Supporto"], schifosso['Transport Supporto'], schifosso["Primario"])]
        busprod = [round(100 * (x + y) / z, 1) for x, y, z in
                   zip(schifosso["Busta"], schifosso['Transport Busta'], schifosso["Primario"])]

        vasprodb = [0, 0, 0, 0, 0, 0,0]
        padprodb = [0, 0, 0, 0, 0, 0,0]
        topprodb = [0, 0, 0, 0, 0, 0,0]
        botprodb = [0, 0, 0, 0, 0, 0,0]
        supprodb = [0, 0, 0, 0, 0, 0,0]
        busprodb = [0, 0, 0, 0, 0, 0,0]
    elif ((schifosso["Primario"].sum(axis=0) == 0) and (schifosso["Primariob"].sum(axis=0) == 0)):
        vasprod = [0, 0, 0, 0, 0, 0,0]
        padprod = [0, 0, 0, 0, 0, 0,0]
        topprod = [0, 0, 0, 0, 0, 0,0]
        botprod = [0, 0, 0, 0, 0, 0,0]
        supprod = [0, 0, 0, 0, 0, 0,0]
        busprod = [0, 0, 0, 0, 0, 0,0]

        vasprodb = [0, 0, 0, 0, 0, 0,0]
        padprodb = [0, 0, 0, 0, 0, 0,0]
        topprodb = [0, 0, 0, 0, 0, 0,0]
        botprodb = [0, 0, 0, 0, 0, 0,0]
        supprodb = [0, 0, 0, 0, 0, 0,0]
        busprodb = [0, 0, 0, 0, 0, 0,0]
    elif ((schifosso["Primario"].sum(axis=0) != 0) and (schifosso["Primariob"].sum(axis=0) != 0)):
        vasprod = [round(100 * (x + y) / z, 1) for x, y, z in
                   zip(schifosso["Vassoio"], schifosso['Transport Vassoio'], schifosso["Primario"])]
        padprod = [round(100 * (x + y) / z, 1) for x, y, z in
                   zip(schifosso["Pad"], schifosso['Transport Pad'], schifosso["Primario"])]
        topprod = [round(100 * (x + y) / z, 1) for x, y, z in
                   zip(schifosso["Top"], schifosso['Transport Top'], schifosso["Primario"])]
        botprod = [round(100 * (x + y) / z, 1) for x, y, z in
                   zip(schifosso["Bottom"], schifosso['Transport Bottom'], schifosso["Primario"])]
        supprod = [round(100 * (x + y) / z, 1) for x, y, z in
                   zip(schifosso["Supporto"], schifosso['Transport Supporto'], schifosso["Primario"])]
        busprod = [round(100 * (x + y) / z, 1) for x, y, z in
                   zip(schifosso["Busta"], schifosso['Transport Busta'], schifosso["Primario"])]

        vasprodb = [round(100 * (x + y) / z, 1) for x, y, z in
                    zip(schifosso["Vassoiob"], schifosso['Transport Vassoiob'], schifosso["Primariob"])]
        padprodb = [round(100 * (x + y) / z, 1) for x, y, z in
                    zip(schifosso["Padb"], schifosso['Transport Padb'], schifosso["Primariob"])]
        topprodb = [round(100 * (x + y) / z, 1) for x, y, z in
                    zip(schifosso["Topb"], schifosso['Transport Topb'], schifosso["Primariob"])]
        botprodb = [round(100 * (x + y) / z, 1) for x, y, z in
                    zip(schifosso["Bottomb"], schifosso['Transport Bottomb'], schifosso["Primariob"])]
        supprodb = [round(100 * (x + y) / z, 1) for x, y, z in
                    zip(schifosso["Supportob"], schifosso['Transport Supportob'], schifosso["Primariob"])]
        busprodb = [round(100 * (x + y) / z, 1) for x, y, z in
                    zip(schifosso["Bustab"], schifosso['Transport Bustab'], schifosso["Primariob"])]


    pie1 = pd.DataFrame({
        "Componente" : ["Vassoio preformato","Pad assorbente","Top flessibile", "Bottom flessibile", "Supporto in cellulosa", "Busta"],
        "Footprint9": [vasprod[0], padprod[0], topprod[0], botprod[0], supprod[0], busprod[0]],
        "Footprint1" : [vasprod[1],padprod[1],topprod[1],botprod[1],supprod[1],busprod[1]],
        "Footprint2": [vasprod[2], padprod[2], topprod[2], botprod[2], supprod[2], busprod[2]],
        "Footprint3": [vasprod[3], padprod[3], topprod[3], botprod[3], supprod[3], busprod[3]],
        "Footprint4": [vasprod[4], padprod[4], topprod[4], botprod[4], supprod[4], busprod[4]],
        "Footprint5": [vasprod[5], padprod[5], topprod[5], botprod[5], supprod[5], busprod[5]],
        "Footprint6": [vasprod[6], padprod[6], topprod[6], botprod[6], supprod[6], busprod[6]],
        "Footprint9b": [vasprodb[0], padprodb[0], topprodb[0], botprodb[0], supprodb[0], busprodb[0]],
        "Footprint1b": [vasprodb[1], padprodb[1], topprodb[1], botprodb[1], supprodb[1], busprodb[1]],
        "Footprint2b": [vasprodb[2], padprodb[2], topprodb[2], botprodb[2], supprodb[2], busprodb[2]],
        "Footprint3b": [vasprodb[3], padprodb[3], topprodb[3], botprodb[3], supprodb[3], busprodb[3]],
        "Footprint4b": [vasprodb[4], padprodb[4], topprodb[4], botprodb[4], supprodb[4], busprodb[4]],
        "Footprint5b": [vasprodb[5], padprodb[5], topprodb[5], botprodb[5], supprodb[5], busprodb[5]],
        "Footprint6b": [vasprodb[6], padprodb[6], topprodb[6], botprodb[6], supprodb[6], busprodb[6]],

    })
    jiwooli = pd.DataFrame({
        "Categorie impatto" : [ "Acidificazione", "Acidificazione", "Acidificazione", "Acidificazione", "Acidificazione", "Acidificazione", "Acidificazione", "Acidificazione",
                       "Cambiamento climatico tot", "Cambiamento climatico tot", "Cambiamento climatico tot", "Cambiamento climatico tot", "Cambiamento climatico tot", "Cambiamento climatico tot", "Cambiamento climatico tot", "Cambiamento climatico tot",
                       "Uso del suolo","Uso del suolo","Uso del suolo","Uso del suolo","Uso del suolo","Uso del suolo","Uso del suolo","Uso del suolo",
                       "Particolato","Particolato","Particolato","Particolato","Particolato","Particolato","Particolato","Particolato",
                       "Formazione di ozono fotochimico, salute umana","Formazione di ozono fotochimico, salute umana","Formazione di ozono fotochimico, salute umana","Formazione di ozono fotochimico, salute umana","Formazione di ozono fotochimico, salute umana","Formazione di ozono fotochimico, salute umana","Formazione di ozono fotochimico, salute umana","Formazione di ozono fotochimico, salute umana",
                       "Uso di risorse fossili", "Uso di risorse fossili","Uso di risorse fossili","Uso di risorse fossili","Uso di risorse fossili","Uso di risorse fossili","Uso di risorse fossili","Uso di risorse fossili",
                       "Uso acqua", "Uso acqua","Uso acqua","Uso acqua","Uso acqua","Uso acqua","Uso acqua","Uso acqua"],
        "Faso" : ["Prod. & trasporto dell'imb. primario","Prod. & trasporto dell'imb. secondario",
                  "Prod. & trasporto dell'imb. terziario", "Confezionamento","Distribuzione",
                  "Fine vita imb. primario","Fine vita imb. secondario","Fine vita imb. terziario",
                  "Prod. & trasporto dell'imb. primario","Prod. & trasporto dell'imb. secondario",
                  "Prod. & trasporto dell'imb. terziario", "Confezionamento","Distribuzione",
                  "Fine vita imb. primario","Fine vita imb. secondario","Fine vita imb. terziario",
                        "Prod. & trasporto dell'imb. primario", "Prod. & trasporto dell'imb. secondario",
                        "Prod. & trasporto dell'imb. terziario", "Confezionamento", "Distribuzione",
                        "Fine vita imb. primario", "Fine vita imb. secondario", "Fine vita imb. terziario",
                        "Prod. & trasporto dell'imb. primario", "Prod. & trasporto dell'imb. secondario",
                        "Prod. & trasporto dell'imb. terziario", "Confezionamento", "Distribuzione",
                        "Fine vita imb. primario", "Fine vita imb. secondario", "Fine vita imb. terziario",
                        "Prod. & trasporto dell'imb. primario", "Prod. & trasporto dell'imb. secondario",
                        "Prod. & trasporto dell'imb. terziario", "Confezionamento", "Distribuzione",
                        "Fine vita imb. primario", "Fine vita imb. secondario", "Fine vita imb. terziario",
                        "Prod. & trasporto dell'imb. primario", "Prod. & trasporto dell'imb. secondario",
                        "Prod. & trasporto dell'imb. terziario", "Confezionamento", "Distribuzione",
                        "Fine vita imb. primario", "Fine vita imb. secondario", "Fine vita imb. terziario",
                        "Prod. & trasporto dell'imb. primario", "Prod. & trasporto dell'imb. secondario",
                        "Prod. & trasporto dell'imb. terziario", "Confezionamento", "Distribuzione",
                        "Fine vita imb. primario", "Fine vita imb. secondario", "Fine vita imb. terziario"

                        ],
        "Contributo delle fasi del ciclo di vita %": [prod1[0], prod2[0], prod3[0], conf[0], dist[0], fine1[0], fine2[0], fine3[0],
                                                      prod1[1], prod2[1], prod3[1], conf[1], dist[1], fine1[1], fine2[1], fine3[1],
                                                      prod1[2], prod2[2], prod3[2], conf[2], dist[2], fine1[2], fine2[2], fine3[2],
                                                      prod1[3], prod2[3], prod3[3], conf[3], dist[3], fine1[3], fine2[3], fine3[3],
                                                      prod1[4], prod2[4], prod3[4], conf[4], dist[4], fine1[4], fine2[4], fine3[4],
                                                      prod1[5], prod2[5], prod3[5], conf[5], dist[5], fine1[5], fine2[5], fine3[5],
                                                      prod1[6], prod2[6], prod3[6], conf[6], dist[6], fine1[6], fine2[6], fine3[6]

                                                      ],
        "Contributo delle fasi del ciclo di vita(b) %": [prod1b[0], prod2b[0], prod3b[0], confb[0], distb[0], fine1b[0],
                                                      fine2b[0], fine3b[0],
                                                      prod1b[1], prod2b[1], prod3b[1], confb[1], distb[1], fine1b[1],
                                                      fine2b[1], fine3b[1],
                                                      prod1b[2], prod2b[2], prod3b[2], confb[2], distb[2], fine1b[2],
                                                      fine2b[2], fine3b[2],
                                                      prod1b[3], prod2b[3], prod3b[3], confb[3], distb[3], fine1b[3],
                                                      fine2b[3], fine3b[3],
                                                      prod1b[4], prod2b[4], prod3b[4], confb[4], distb[4], fine1b[4],
                                                      fine2b[4], fine3b[4],
                                                      prod1b[5], prod2b[5], prod3b[5], confb[5], distb[5], fine1b[5],
                                                      fine2b[5], fine3b[5],
                                                      prod1b[6], prod2b[6], prod3b[6], confb[6], distb[6], fine1b[6],
                                                      fine2b[6], fine3b[6]

                                                      ],

    })
    fig = px.bar(jiwooli, x="Categorie impatto", y="Contributo delle fasi del ciclo di vita %", color="Faso", title="Solution 1", labels={'Categorie impatto': " "}, hover_name="Faso", hover_data={"Faso":False,"Contributo delle fasi del ciclo di vita %":True, "Categorie impatto":True})
    fig2 = px.bar(jiwooli, x="Categorie impatto", y="Contributo delle fasi del ciclo di vita(b) %", color="Faso", title="Solution 2", labels={'Categorie impatto': " "}, hover_name="Faso", hover_data={"Faso":False,"Contributo delle fasi del ciclo di vita %":True, "Categorie impatto":True})

    fig9 = px.pie(pie1, values='Footprint9', names='Componente',  hole=.3, labels={'Footprint9':'Contribution',"Componente":"Componente"})
    fig3 = px.pie(pie1, values='Footprint1', names='Componente',  hole=.3, labels={'Footprint1':'Contribution',"Componente":"Componente"})
    fig4 = px.pie(pie1, values='Footprint2', names='Componente',  hole=.3, labels={'Footprint2':'Contribution',"Componente":"Componente"})
    fig5 = px.pie(pie1, values='Footprint3', names='Componente',  hole=.3, labels={'Footprint3':'Contribution',"Componente":"Componente"})
    fig6 = px.pie(pie1, values='Footprint4', names='Componente',  hole=.3, labels={'Footprint4':'Contribution',"Componente":"Componente"})
    fig7 = px.pie(pie1, values='Footprint5', names='Componente',  hole=.3, labels={'Footprint5':'Contribution',"Componente":"Componente"})
    fig8 = px.pie(pie1, values='Footprint6', names='Componente',  hole=.3, labels={'Footprint6':'Contribution',"Componente":"Componente"})

    fig9b = px.pie(pie1, values='Footprint9b', names='Componente',  hole=.3, labels={'Footprint9b':'Contribution',"Componente":"Componente"})
    fig3b = px.pie(pie1, values='Footprint1b', names='Componente',  hole=.3, labels={'Footprint1b':'Contribution',"Componente":"Componente"})
    fig4b = px.pie(pie1, values='Footprint2b', names='Componente',  hole=.3, labels={'Footprint2b':'Contribution',"Componente":"Componente"})
    fig5b = px.pie(pie1, values='Footprint3b', names='Componente',  hole=.3, labels={'Footprint3b':'Contribution',"Componente":"Componente"})
    fig6b = px.pie(pie1, values='Footprint4b', names='Componente',  hole=.3, labels={'Footprint4b':'Contribution',"Componente":"Componente"})
    fig7b = px.pie(pie1, values='Footprint5b', names='Componente',  hole=.3, labels={'Footprint5b':'Contribution',"Componente":"Componente"})
    fig8b = px.pie(pie1, values='Footprint6b', names='Componente',  hole=.3, labels={'Footprint6b':'Contribution',"Componente":"Componente"})

    #
    fig9.update_layout(
         title_text="Acidificazione - Soluzione A", paper_bgcolor='#DAF0AD', showlegend=True,  plot_bgcolor='#DAF0AD', title_font_family="Times New Roman",
     )
    fig3.update_layout(
         title_text="Cambiamento climatico tot - Soluzione A", paper_bgcolor='#DAF0AD', showlegend=True,  plot_bgcolor='#DAF0AD', title_font_family="Times New Roman",
     )
    fig4.update_layout(
        title_text="Uso del suolo - Soluzione A", paper_bgcolor='#DAF0AD', showlegend=True,
        plot_bgcolor='#DAF0AD', title_font_family="Times New Roman",
    )
    fig5.update_layout(
        title_text="Particolato - Soluzione A", paper_bgcolor='#DAF0AD', showlegend=True,
        plot_bgcolor='#DAF0AD', title_font_family="Times New Roman",
    )
    fig6.update_layout(
        title_text="Formazione di ozono fotochimico, salute umana - Soluzione A", paper_bgcolor='#DAF0AD', showlegend=True,
        plot_bgcolor='#DAF0AD', title_font_family="Times New Roman",
    )
    fig7.update_layout(
        title_text="Uso di risorse fossili - Soluzione A", paper_bgcolor='#DAF0AD', showlegend=True,
        plot_bgcolor='#DAF0AD', title_font_family="Times New Roman",
    )
    fig8.update_layout(
        title_text="Uso acqua - Soluzione A", paper_bgcolor='#DAF0AD', showlegend=True,
        plot_bgcolor='#DAF0AD', title_font_family="Times New Roman",
    )
    fig9b.update_layout(
         title_text="Acidificazione - Soluzione B", paper_bgcolor='#DAF0AD', showlegend=True,  plot_bgcolor='#DAF0AD', title_font_family="Times New Roman",
     )

    fig3b.update_layout(
        title_text="Cambiamento climatico tot - Soluzione B", paper_bgcolor='#DAF0AD', showlegend=True,
        plot_bgcolor='#DAF0AD', title_font_family="Times New Roman",
    )
    fig4b.update_layout(
        title_text="Uso del suolo - Soluzione B", paper_bgcolor='#DAF0AD', showlegend=True,
        plot_bgcolor='#DAF0AD', title_font_family="Times New Roman",
    )
    fig5b.update_layout(
        title_text="Particolato - Soluzione B", paper_bgcolor='#DAF0AD', showlegend=True,
        plot_bgcolor='#DAF0AD', title_font_family="Times New Roman",
    )
    fig6b.update_layout(
        title_text="Formazione di ozono fotochimico, salute umana - Soluzione B", paper_bgcolor='#DAF0AD',
        showlegend=True,
        plot_bgcolor='#DAF0AD', title_font_family="Times New Roman",
    )
    fig7b.update_layout(
        title_text="Uso di risorse fossili - Soluzione B", paper_bgcolor='#DAF0AD', showlegend=True,
        plot_bgcolor='#DAF0AD', title_font_family="Times New Roman",
    )
    fig8b.update_layout(
        title_text="Uso acqua - Soluzione B", paper_bgcolor='#DAF0AD', showlegend=True,
        plot_bgcolor='#DAF0AD', title_font_family="Times New Roman",
    )


    fig.update_layout(
        title_text="", paper_bgcolor='#DAF0AD', showlegend=True, xaxis_tickangle=-30, height=800, plot_bgcolor='#DAF0AD', font_family="Arial",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title_text=None
        ), legend_font=dict(size=13),


    )
    fig.update_traces(hovertemplate='<b>Contributo sul totale</b>: %{y:,.2f} %<br>'+ '<b>Categorie impatto</b>: %{x}<br>',textposition='inside')
    fig2.update_traces(hovertemplate='<b>Contributo sul totale</b>: %{y:,.2f} %<br>'+ '<b>Categorie impatto</b>: %{x}<br>',textposition='inside')
    fig3.update_traces(hovertemplate='<b>Contributo sul totale</b>: %{value} %<br>'+ '<b>Componente</b>: %{label}<br>',textposition='inside')
    fig4.update_traces(hovertemplate='<b>Contributo sul totale</b>: %{value} %<br>'+ '<b>Componente</b>: %{label}<br>',textposition='inside')
    fig5.update_traces(hovertemplate='<b>Contributo sul totale</b>: %{value} %<br>'+ '<b>Componente</b>: %{label}<br>',textposition='inside')
    fig6.update_traces(hovertemplate='<b>Contributo sul totale</b>: %{value} %<br>'+ '<b>Componente</b>: %{label}<br>',textposition='inside')
    fig7.update_traces(hovertemplate='<b>Contributo sul totale</b>: %{value} %<br>'+ '<b>Componente</b>: %{label}<br>',textposition='inside')
    fig8.update_traces(hovertemplate='<b>Contributo sul totale</b>: %{value} %<br>'+ '<b>Componente</b>: %{label}<br>',textposition='inside')
    fig9.update_traces(hovertemplate='<b>Contributo sul totale</b>: %{value} %<br>'+ '<b>Componente</b>: %{label}<br>',textposition='inside')
    fig3b.update_traces(hovertemplate='<b>Contributo sul totale</b>: %{value} %<br>'+ '<b>Componente</b>: %{label}<br>',textposition='inside')
    fig4b.update_traces(hovertemplate='<b>Contributo sul totale</b>: %{value} %<br>'+ '<b>Componente</b>: %{label}<br>',textposition='inside')
    fig5b.update_traces(hovertemplate='<b>Contributo sul totale</b>: %{value} %<br>'+ '<b>Componente</b>: %{label}<br>',textposition='inside')
    fig6b.update_traces(hovertemplate='<b>Contributo sul totale</b>: %{value} %<br>'+ '<b>Componente</b>: %{label}<br>',textposition='inside')
    fig7b.update_traces(hovertemplate='<b>Contributo sul totale</b>: %{value} %<br>'+ '<b>Componente</b>: %{label}<br>',textposition='inside')
    fig8b.update_traces(hovertemplate='<b>Contributo sul totale</b>: %{value} %<br>'+ '<b>Componente</b>: %{label}<br>',textposition='inside')
    fig9b.update_traces(hovertemplate='<b>Contributo sul totale</b>: %{value} %<br>'+ '<b>Componente</b>: %{label}<br>',textposition='inside')



    fig2.update_layout(
        title_text="", paper_bgcolor='#DAF0AD', showlegend=True, xaxis_tickangle=-30, height=800, plot_bgcolor='#DAF0AD', font_family="Arial",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title_text=None
        ), legend_font=dict(size=13),


    )


    return  dash_table.DataTable(schifosso.to_dict('records'),[{'name': i, 'id': i} for i in schifosso.columns]), fig, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig3b, fig4b, fig5b, fig6b, fig7b, fig8b, fig9b,rang0, GWPtotA0, difmsg0 ,rang, GWPtotA, difmsg ,rang2, GWPtotA2, difmsg2 ,rang3, GWPtotA3, difmsg3 ,rang4, GWPtotA4, difmsg4 ,rang5, GWPtotA5, difmsg5,rang6, GWPtotA6, difmsg6, \
            "{:.2e}".format(schifosso.iloc[0, 48]), "{:.2e}".format(schifosso.iloc[0, 47]), "{:.2e}".format(schifosso.iloc[0, 39]), "{:.2e}".format(schifosso.iloc[0, 39]), "{:.2e}".format(schifosso.iloc[0, 41]), "{:.2e}".format(schifosso.iloc[0, 41]), "{:.2e}".format(schifosso.iloc[0, 43]), "{:.2e}".format(schifosso.iloc[0, 44]), "{:.2e}".format(schifosso.iloc[0, 45]), "{:.2e}".format(schifosso.iloc[0, 46]), "{:.2e}".format(schifosso.iloc[0, 49]), "{:.2e}".format(schifosso.iloc[0, 50]), "{:.2e}".format(schifosso.iloc[0, 40]), "{:.2e}".format(schifosso.iloc[0, 40]), "{:.2e}".format(schifosso.iloc[0, 42]), "{:.2e}".format(schifosso.iloc[0, 42]), "{:.2e}".format(schifosso.iloc[0, 51]), "{:.2e}".format(schifosso.iloc[0, 52]), \
            "{:.2e}".format(schifosso.iloc[1, 48]), "{:.2e}".format(schifosso.iloc[1, 47]), "{:.2e}".format(schifosso.iloc[1, 39]), "{:.2e}".format(schifosso.iloc[1, 39]),"{:.2e}".format(schifosso.iloc[1, 41]),"{:.2e}".format(schifosso.iloc[1, 41]),"{:.2e}".format(schifosso.iloc[1, 43]),"{:.2e}".format(schifosso.iloc[1, 44]),"{:.2e}".format(schifosso.iloc[1, 45]),"{:.2e}".format(schifosso.iloc[1, 46]),"{:.2e}".format(schifosso.iloc[1, 49]),"{:.2e}".format(schifosso.iloc[1, 50]),"{:.2e}".format(schifosso.iloc[1, 40]),"{:.2e}".format(schifosso.iloc[1, 40]),"{:.2e}".format(schifosso.iloc[1, 42]),"{:.2e}".format(schifosso.iloc[1, 42]),"{:.2e}".format(schifosso.iloc[1, 51]),"{:.2e}".format(schifosso.iloc[1, 52]),\
            "{:.2e}".format(schifosso.iloc[2, 48]), "{:.2e}".format(schifosso.iloc[2, 47]), "{:.2e}".format(schifosso.iloc[2, 39]), "{:.2e}".format(schifosso.iloc[2, 39]),"{:.2e}".format(schifosso.iloc[2, 41]),"{:.2e}".format(schifosso.iloc[2, 41]),"{:.2e}".format(schifosso.iloc[2, 43]),"{:.2e}".format(schifosso.iloc[2, 44]),"{:.2e}".format(schifosso.iloc[2, 45]),"{:.2e}".format(schifosso.iloc[2, 46]),"{:.2e}".format(schifosso.iloc[2, 49]),"{:.2e}".format(schifosso.iloc[2, 50]),"{:.2e}".format(schifosso.iloc[2, 40]),"{:.2e}".format(schifosso.iloc[2, 40]),"{:.2e}".format(schifosso.iloc[2, 42]),"{:.2e}".format(schifosso.iloc[2, 42]),"{:.2e}".format(schifosso.iloc[2, 51]),"{:.2e}".format(schifosso.iloc[2, 52]),\
            "{:.2e}".format(schifosso.iloc[3, 48]), "{:.2e}".format(schifosso.iloc[3, 47]), "{:.2e}".format(schifosso.iloc[3, 39]), "{:.2e}".format(schifosso.iloc[3, 39]),"{:.2e}".format(schifosso.iloc[3, 41]),"{:.2e}".format(schifosso.iloc[3, 41]),"{:.2e}".format(schifosso.iloc[3, 43]),"{:.2e}".format(schifosso.iloc[3, 44]),"{:.2e}".format(schifosso.iloc[3, 45]),"{:.2e}".format(schifosso.iloc[3, 46]),"{:.2e}".format(schifosso.iloc[3, 49]),"{:.2e}".format(schifosso.iloc[3, 50]),"{:.2e}".format(schifosso.iloc[3, 40]),"{:.2e}".format(schifosso.iloc[3, 40]),"{:.2e}".format(schifosso.iloc[3, 42]),"{:.2e}".format(schifosso.iloc[3, 42]),"{:.2e}".format(schifosso.iloc[3, 51]),"{:.2e}".format(schifosso.iloc[3, 52]),\
            "{:.2e}".format(schifosso.iloc[4, 48]), "{:.2e}".format(schifosso.iloc[4, 47]), "{:.2e}".format(schifosso.iloc[4, 39]), "{:.2e}".format(schifosso.iloc[4, 39]),"{:.2e}".format(schifosso.iloc[4, 41]),"{:.2e}".format(schifosso.iloc[4, 41]),"{:.2e}".format(schifosso.iloc[4, 43]),"{:.2e}".format(schifosso.iloc[4, 44]),"{:.2e}".format(schifosso.iloc[4, 45]),"{:.2e}".format(schifosso.iloc[4, 46]),"{:.2e}".format(schifosso.iloc[4, 49]),"{:.2e}".format(schifosso.iloc[4, 50]),"{:.2e}".format(schifosso.iloc[4, 40]),"{:.2e}".format(schifosso.iloc[4, 40]),"{:.2e}".format(schifosso.iloc[4, 42]),"{:.2e}".format(schifosso.iloc[4, 42]),"{:.2e}".format(schifosso.iloc[4, 51]),"{:.2e}".format(schifosso.iloc[4, 52]),\
            "{:.2e}".format(schifosso.iloc[5, 48]), "{:.2e}".format(schifosso.iloc[5, 47]), "{:.2e}".format(schifosso.iloc[5, 39]), "{:.2e}".format(schifosso.iloc[5, 39]),"{:.2e}".format(schifosso.iloc[5, 41]),"{:.2e}".format(schifosso.iloc[5, 41]),"{:.2e}".format(schifosso.iloc[5, 43]),"{:.2e}".format(schifosso.iloc[5, 44]),"{:.2e}".format(schifosso.iloc[5, 45]),"{:.2e}".format(schifosso.iloc[5, 46]),"{:.2e}".format(schifosso.iloc[5, 49]),"{:.2e}".format(schifosso.iloc[5, 50]),"{:.2e}".format(schifosso.iloc[5, 40]),"{:.2e}".format(schifosso.iloc[5, 40]),"{:.2e}".format(schifosso.iloc[5, 42]),"{:.2e}".format(schifosso.iloc[5, 42]),"{:.2e}".format(schifosso.iloc[5, 51]),"{:.2e}".format(schifosso.iloc[5, 52]),\
            "{:.2e}".format(schifosso.iloc[6, 48]), "{:.2e}".format(schifosso.iloc[6, 47]), "{:.2e}".format(schifosso.iloc[6, 39]), "{:.2e}".format(schifosso.iloc[6, 39]),"{:.2e}".format(schifosso.iloc[6, 41]),"{:.2e}".format(schifosso.iloc[6, 41]),"{:.2e}".format(schifosso.iloc[6, 43]),"{:.2e}".format(schifosso.iloc[6, 44]),"{:.2e}".format(schifosso.iloc[6, 45]),"{:.2e}".format(schifosso.iloc[6, 46]),"{:.2e}".format(schifosso.iloc[6, 49]),"{:.2e}".format(schifosso.iloc[6, 50]),"{:.2e}".format(schifosso.iloc[6, 40]),"{:.2e}".format(schifosso.iloc[6, 40]),"{:.2e}".format(schifosso.iloc[6, 42]),"{:.2e}".format(schifosso.iloc[6, 42]), "{:.2e}".format(schifosso.iloc[6, 51]),"{:.2e}".format(schifosso.iloc[6, 52]), dl

@callback(
    Output(component_id='2nddim', component_property='children'),
    Output(component_id='2ndpeso', component_property='children'),
    Output(component_id='2nddimb', component_property='children'),
    Output(component_id='2ndpesob', component_property='children'),
    Input(component_id="2nddd", component_property="value"),
    Input(component_id="2ndddb", component_property="value")
)

def second(input1, input2):
    dim = df.loc[(df['Composizione'] == input1)]['Specifiche']
    peso = df.loc[(df['Composizione'] == input1)]['More']
    dim2= df.loc[(df['Composizione'] == input2)]['Specifiche']
    peso2 = df.loc[(df['Composizione'] == input2)]['More']
    return dim, peso, dim2, peso2





