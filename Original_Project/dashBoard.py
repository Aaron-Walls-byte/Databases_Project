import pprint
import base64
import dash
import dash_leaflet as dl
from dash import dcc as dcc
from dash import html as html
from dash import dash_table as dt
from dash.dependencies import Input, Output, State
import plotly.express as px
import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from bson.json_util import dumps
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from MongoCRUD import MongoCRUD

username = "shipUser"
password = "password"
ships = MongoCRUD(username, password);

df = pd.DataFrame.from_records(ships.read({}))


#########################
# Dashboard Layout / View
#########################
image_filename = 'sw.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app = dash.Dash("Shipwrecks")


app.layout = html.Div([

    html.Center(html.B(html.H1('78487AaronsUniqueIdentifierThing78487'))),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode())),

    dcc.RadioItems(
        id='radio',
        options=[

        ],
        value='Water Rescue',
        labelStyle={'display': 'inline-block'}
    ),
    html.Hr(),
    html.Div(id='datatable-id-container', children = [
            dt.DataTable(
                id='datatable-id',
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
                ])]),
    html.Hr(),

    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
                html.Div(
                    id = 'graph-id',
                    className='col s12 m6',
                    children=[
                        html.Div()
                    ]
                ),
                html.Div(
                    id='map-id',
                    className='col s12 m6',
                )
        ])
    #html.Div(id='map-id'),
    #html.Hr(),
    #html.Div([
    #         dcc.Graph(id = 'graph-id')
    #         ])
    ])


if __name__ == "__main__":
    app.run_server(debug=True)
#############################################
# Interaction Between Components / Controller
#############################################
@app.callback(
    Output('datatable-id-container', 'children'),
    [Input('radio', 'value')]
    )
def update_output(value):
    df = pd.DataFrame.from_records(ships.read({}))
    #if value == 'Water Rescue':

    #if value == 'Mountain or Wilderness Rescue':

    #if value == 'Disaster Rescue or Individual Tracking':

    return [
            dt.DataTable(
                id='datatable-id',
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
                ],
                data=df.to_dict('records'),
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_selectable="multi",
                row_deletable=True,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current= 0,
                page_size= 10,

        )
    ]

@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')])

def update_styles(selected_columns):
        return [{
            'if': { 'column_id': i },
            'background_color': '#D2F3FF'
        } for i in selected_columns
    ]


@app.callback(
    Output('graph-id','children'),
    [Input('datatable-id', "derived_viewport_data")])

def update_graph(viewData):
     ###FIX ME ####
    # add code for chart of your choice (e.g. pie chart) #
    dff = pd.DataFrame.from_dict(viewData)
    fig = px.pie(
        dff['animal_type'],
       #labels = dff['animal_type'],
       title='Figure 1',
   )
    return [
        dcc.Graph(
            figure = fig
        )
    ]
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_viewport_data")])

def update_map(viewData):
#FIXME Add in the code for your geolocation chart
    dff = pd.DataFrame.from_dict(viewData)
    # Austin TX is at [30.75,-97.48]
    return [
         dl.Map(style={'width': '500px', 'height': '500px'}, center=[dff.location_lat[0],dff.location_long[0]], zoom=10, children=[
           dl.TileLayer(id="base-layer-id"),
           # Marker with tool tip and popup
           dl.Marker(position=[dff.location_lat[0],dff.location_long[0]], children=[
                dl.Tooltip(dff.iloc[0,4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[0,10]),
                    html.H3("Animal ID"),
                    html.P(dff.iloc[0,2]),

                ])
           ])
        ])
    ]
