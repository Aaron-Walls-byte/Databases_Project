import pprint
import base64
import dash
import dash_auth
import dash_leaflet as dl
import dash_leaflet.express as dlx
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State
import plotly.express as px
import os
os.environ['PROJ_LIB'] = 'C:/Users/dynat/anaconda3/Lib/site-packages/mpl_toolkits/basemap'

import numpy as np
import pandas as pd
from shapely import wkt
from IPython.display import display
from pymongo import MongoClient
from bson.json_util import dumps
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from MongoCRUD import MongoCRUD

######################~~~~~~~~~~~~~~~~~######################
#                   Credentials For MongoDB
######################~~~~~~~~~~~~~~~~~######################


VALID_USERNAME_PASSWORD_PAIRS = {
    'shipUser':'password'
}

ships = MongoCRUD()

app=dash.Dash("Shipwrecks!")
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
######################~~~~~~~~~~~~~~~~~######################
#                     Data From MongoDB
######################~~~~~~~~~~~~~~~~~######################
df = pd.DataFrame.from_records(ships.read({}))


#coords = df[["latdec","londec"]]
waterlevels = df['watlev'].unique()
print(df.head())



######################~~~~~~~~~~~~~~~~~######################
#                        Main Page
######################~~~~~~~~~~~~~~~~~######################
image_filename = 'sw.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


app.layout = html.Div(
    children=[
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode())),
        html.Center(html.B(html.H1(children="Shipwreck Locations"))),
        html.Div([
            dcc.Dropdown(
                id='watlev',
                options=[{'label':i, 'value':i}for i in waterlevels],
                value = 'always dry'
            ),
            dcc.Graph(id = 'map_plot'
            )
        ], style={'display':'inline-block'}, id='container')
    ]
)

@app.callback(
    Output('map_plot','figure'),
    Input('watlev','value'))
#Watlev contains user selected data
def ships_map(watlev):
    #copy orginal data frame
    coord = df.copy()
    #filter selection based on Watlev
    if(watlev == "always dry"):
        coord.query('watlev == "always dry"', inplace = True)
    if(watlev == "always under water/submerged"):
        coord.query('watlev == "always under water/submerged"', inplace = True)
    if(watlev == "covers and uncovers"):
        coord.query('watlev == "covers and uncovers"', inplace = True)
    if(watlev == "partly submerged at high water"):
        coord.query('watlev == "partly submerged at high water"', inplace = True)
    if(watlev == "awash"):
        coord.query('watlev == "awash"', inplace = True)
    #create plots based on filtered data (coord)
    fig = px.scatter_mapbox(coord, lat="latdec", lon="londec", hover_data=["watlev", "depth"])
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b":0})
    #return and populate dash graph
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
