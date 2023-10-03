
from jupyter_plotly_dash import JupyterDash

import dash
import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table as dt
from dash.dependencies import Input, Output, State

import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from bson.json_util import dumps
import base64

#### FIX ME #####
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from SE_AnimalShelter import AnimalShelter


###########################
# Data Manipulation / Model
###########################
# FIX ME change for your username and password and CRUD Python module name
username = "aacuser"
password = "admin"
shelter = AnimalShelter(username, password)


# class read method must support return of cursor object
df = pd.DataFrame.from_records(shelter.read({}))


#########################
# Dashboard Layout / View
#########################
app = JupyterDash('SimpleExample')

#FIX ME Add in Grazioso Salvare logo
image_filename = 'Grazioso_Salvare_Logo.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#FIX ME Place the HTML image tag in the line below into the app.layout code according to your design
#FIX ME Also remember to include a unique identifier such as your name or date


#html.H3('SNHU CS-340 Dashboard'),

app.layout = html.Div([
#    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))),
    html.Center(html.B(html.H1('Steve Edmund - SNHU CS-340 Dashboard'))),
    html.Center(html.P('Select up to five from the table for the map')),
    html.Hr(),
    html.Div(
        #Radio Items to select the rescue filter options
        dcc.RadioItems(
            id='filter-type',
            # created the labels and keys based on the Grazioso requirements
            options=[
            {'label': 'Water Rescue', 'value': 'WR'},
            {'label': 'Mountain/Wilderness Rescue', 'value': 'MWR'},
            {'label': 'Disaster Rescue/Individual Tracking', 'value': 'DRIT'},
            {'label': 'Reset - returns unfiltered state', 'value': 'RESET'}
            ],
            value='RESET',
            labelStyle={'display': 'inline-block'}
        )
    ),
    html.Hr(),
    dt.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
#FIXME: Set up the features for your interactive data table to make it user-friendly for your client
#If you completed the Module Six Assignment, you can copy in the code you created here
        #made selectable 'multi' to allow map to work with several options
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable=False,
        row_selectable="multi",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Br(),
    html.Hr(),
#This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            #dcc.Graph(id='graph-id'),
            id='graph-id',
            className='col s12 m6',

            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################


@app.callback([Output('datatable-id','data'),
               Output('datatable-id','columns')],
              [Input('filter-type', 'value')])
def update_dashboard(filter_type):
### FIX ME Add code to filter interactive data table with MongoDB queries
        #adjusts the read request for the desired dog type and status
        if filter_type == 'WR':
            # complex queries used to compile - was not sure which "Newfoundland" they wanted
            # so I added all that came up in animals.distinct('breed') that used "Newfoundland"
            df = pd.DataFrame(list(shelter.read({'$and': [{'sex_upon_outcome': 'Intact Female'},
                                                          {'$or': [
                                                              {'breed': 'Labrador Retriever Mix'},
                                                              {'breed': 'Chesa Bay Retr Mix'},
                                                              {'breed': 'Newfoundland Mix'},
                                                              {'breed': 'Newfoundland/Labrador Retriever'},
                                                              {'breed': 'Newfoundland/Australian Cattle Dog'},
                                                              {'breed': 'Newfoundland/Great Pyrenees'}]
                                                          },
                                                          {'$and': [{'age_upon_outcome_in_weeks': {'$gte': 26}},
                                                                    {'age_upon_outcome_in_weeks': {'$lte': 156}}]
                                                          }]
                                                })))
        #adjusts the read request for the desired dog type and status
        elif filter_type == 'MWR':
            # breeds and ages determined by Grazioso
            df = pd.DataFrame(list(shelter.read({'$and': [{'sex_upon_outcome': 'Intact Male'},
                                                          {'$or': [
                                                              {'breed': 'German Shepherd'},
                                                              {'breed': 'Alaskan Malamute'},
                                                              {'breed': 'Old English Sheepdog'},
                                                              {'breed': 'Rottweiler'},
                                                              {'breed': 'Siberian Husky'}]
                                                          },
                                                          {'$and': [{'age_upon_outcome_in_weeks': {'$gte': 26}},
                                                                    {'age_upon_outcome_in_weeks': {'$lte': 156}}]
                                                          }]
                                                })))
        #adjusts the read request for the desired dog type and status
        elif filter_type == 'DRIT':
            #breeds and ages determined by Grazioso
            df = pd.DataFrame(list(shelter.read({'$and': [{'sex_upon_outcome': 'Intact Male'},
                                                          {'$or': [
                                                              {'breed': 'Doberman Pinscher'},
                                                              {'breed': 'German Shepherd'},
                                                              {'breed': 'Golden Retriever'},
                                                              {'breed': 'Bloodhound'},
                                                              {'breed': 'Rottweiler'}]
                                                          },
                                                          {'$and': [{'age_upon_outcome_in_weeks': {'$gte': 20}},
                                                                    {'age_upon_outcome_in_weeks': {'$lte': 300}}]
                                                          }]
                                                })))
        #resets the search to nothing to allow all results to be displayed
        elif filter_type == 'RESET':
            df = pd.DataFrame.from_records(shelter.read({}))


        columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
        data=df.to_dict('records')

        return (data,columns)


@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

#function to update the pie chart
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_viewport_data")])
def update_graphs(viewData):
    ###FIX ME ####
    # imports the currently displayed data
    dff = pd.DataFrame.from_dict(viewData)
    #creates the values needed for the names (breed) and values (recurring counts)
    names = dff['breed'].value_counts().keys().tolist()
    values = dff['breed'].value_counts().tolist()
    #creates a pie chart based on the data above
    return [
        dcc.Graph(
            figure = px.pie(
                data_frame=dff,
                values = values,
                names = names,
                color_discrete_sequence=px.colors.sequential.RdBu,
                width=800,
                height=500
            )
        )
    ]

@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_viewport_data"),
     Input('datatable-id', 'selected_rows'),
     Input('datatable-id', 'selected_columns')])
def update_map(viewData, selected_rows, selected_columns):
#FIXME: Add in the code for your geolocation chart
#If you completed the Module Six Assignment, you can copy in the code you created here.
    # imports the currently viewed data
    dff = pd.DataFrame.from_dict(viewData)
    #determines the default status
    if selected_rows == []:
        selected_rows = [0]
    # creats a map for a single selected row or the default
    if len(selected_rows) == 1:
        return [
            dl.Map(style={'width':'1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
                dl.TileLayer(id="base-layer-id"),

                #marker with tool tip and popup
                dl.Marker(position=[(dff.iloc[selected_rows[0],13]), (dff.iloc[selected_rows[0],14])], children=[
                    dl.Tooltip(dff.iloc[selected_rows[0],4]),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P(dff.iloc[selected_rows[0],9]),
                        html.H4("Sex"),
                        html.P(dff.iloc[selected_rows[0],12]),
                        html.H4("Breed"),
                        html.P(dff.iloc[selected_rows[0],4]),
                        html.H4("Age"),
                        html.P(dff.iloc[selected_rows[0],15])
                    ])
                ])
            ])
        ]
    #creats a map with 2 markers
    elif len(selected_rows) == 2:
        return [
            dl.Map(style={'width':'1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
                dl.TileLayer(id="base-layer-id"),

                #marker with tool tip and popup
                dl.Marker(position=[(dff.iloc[selected_rows[0],13]), (dff.iloc[selected_rows[0],14])], children=[
                    dl.Tooltip(dff.iloc[selected_rows[0],4]),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P(dff.iloc[selected_rows[0],9]),
                        html.H4("Sex"),
                        html.P(dff.iloc[selected_rows[0],12]),
                        html.H4("Breed"),
                        html.P(dff.iloc[selected_rows[0],4]),
                        html.H4("Age"),
                        html.P(dff.iloc[selected_rows[0],15])
                    ])
                ]),
                dl.Marker(position=[(dff.iloc[selected_rows[1],13]), (dff.iloc[selected_rows[1],14])], children=[
                    dl.Tooltip(dff.iloc[selected_rows[1],4]),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P(dff.iloc[selected_rows[1],9]),
                        html.H4("Sex"),
                        html.P(dff.iloc[selected_rows[1],12]),
                        html.H4("Breed"),
                        html.P(dff.iloc[selected_rows[1],4]),
                        html.H4("Age"),
                        html.P(dff.iloc[selected_rows[1],15])
                    ])
                ])
            ])
        ]
    #creats a map with 3 markers
    elif len(selected_rows) == 3:
        return [
            dl.Map(style={'width':'1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
                dl.TileLayer(id="base-layer-id"),

                #marker with tool tip and popup
                dl.Marker(position=[(dff.iloc[selected_rows[0],13]), (dff.iloc[selected_rows[0],14])], children=[
                    dl.Tooltip(dff.iloc[selected_rows[0],4]),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P(dff.iloc[selected_rows[0],9]),
                        html.H4("Sex"),
                        html.P(dff.iloc[selected_rows[0],12]),
                        html.H4("Breed"),
                        html.P(dff.iloc[selected_rows[0],4]),
                        html.H4("Age"),
                        html.P(dff.iloc[selected_rows[0],15])
                    ])
                ]),
                dl.Marker(position=[(dff.iloc[selected_rows[1],13]), (dff.iloc[selected_rows[1],14])], children=[
                    dl.Tooltip(dff.iloc[selected_rows[1],4]),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P(dff.iloc[selected_rows[1],9]),
                        html.H4("Sex"),
                        html.P(dff.iloc[selected_rows[1],12]),
                        html.H4("Breed"),
                        html.P(dff.iloc[selected_rows[1],4]),
                        html.H4("Age"),
                        html.P(dff.iloc[selected_rows[1],15])
                    ])
                ]),
                dl.Marker(position=[(dff.iloc[selected_rows[2],13]), (dff.iloc[selected_rows[2],14])], children=[
                    dl.Tooltip(dff.iloc[selected_rows[2],4]),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P(dff.iloc[selected_rows[2],9]),
                        html.H4("Sex"),
                        html.P(dff.iloc[selected_rows[2],12]),
                        html.H4("Breed"),
                        html.P(dff.iloc[selected_rows[2],4]),
                        html.H4("Age"),
                        html.P(dff.iloc[selected_rows[2],15])
                    ])
                ])
            ])
        ]
    #creats a map with 4 markers
    elif len(selected_rows) == 4:
        return [
            dl.Map(style={'width':'1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
                dl.TileLayer(id="base-layer-id"),

                #marker with tool tip and popup
                dl.Marker(position=[(dff.iloc[selected_rows[0],13]), (dff.iloc[selected_rows[0],14])], children=[
                    dl.Tooltip(dff.iloc[selected_rows[0],4]),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P(dff.iloc[selected_rows[0],9]),
                        html.H4("Sex"),
                        html.P(dff.iloc[selected_rows[0],12]),
                        html.H4("Breed"),
                        html.P(dff.iloc[selected_rows[0],4]),
                        html.H4("Age"),
                        html.P(dff.iloc[selected_rows[0],15])
                    ])
                ]),
                dl.Marker(position=[(dff.iloc[selected_rows[1],13]), (dff.iloc[selected_rows[1],14])], children=[
                    dl.Tooltip(dff.iloc[selected_rows[1],4]),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P(dff.iloc[selected_rows[1],9]),
                        html.H4("Sex"),
                        html.P(dff.iloc[selected_rows[1],12]),
                        html.H4("Breed"),
                        html.P(dff.iloc[selected_rows[1],4]),
                        html.H4("Age"),
                        html.P(dff.iloc[selected_rows[1],15])
                    ])
                ]),
                dl.Marker(position=[(dff.iloc[selected_rows[2],13]), (dff.iloc[selected_rows[2],14])], children=[
                    dl.Tooltip(dff.iloc[selected_rows[2],4]),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P(dff.iloc[selected_rows[2],9]),
                        html.H4("Sex"),
                        html.P(dff.iloc[selected_rows[2],12]),
                        html.H4("Breed"),
                        html.P(dff.iloc[selected_rows[2],4]),
                        html.H4("Age"),
                        html.P(dff.iloc[selected_rows[2],15])
                    ])
                ]),
                dl.Marker(position=[(dff.iloc[selected_rows[3],13]), (dff.iloc[selected_rows[3],14])], children=[
                    dl.Tooltip(dff.iloc[selected_rows[3],4]),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P(dff.iloc[selected_rows[3],9]),
                        html.H4("Sex"),
                        html.P(dff.iloc[selected_rows[3],12]),
                        html.H4("Breed"),
                        html.P(dff.iloc[selected_rows[3],4]),
                        html.H4("Age"),
                        html.P(dff.iloc[selected_rows[3],15])
                    ])
                ])
            ])
        ]
    #creats a map with 5 markers
    elif len(selected_rows) == 5:
        return [
            dl.Map(style={'width':'1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
                dl.TileLayer(id="base-layer-id"),

                #marker with tool tip and popup
                dl.Marker(position=[(dff.iloc[selected_rows[0],13]), (dff.iloc[selected_rows[0],14])], children=[
                    dl.Tooltip(dff.iloc[selected_rows[0],4]),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P(dff.iloc[selected_rows[0],9]),
                        html.H4("Sex"),
                        html.P(dff.iloc[selected_rows[0],12]),
                        html.H4("Breed"),
                        html.P(dff.iloc[selected_rows[0],4]),
                        html.H4("Age"),
                        html.P(dff.iloc[selected_rows[0],15])
                    ])
                ]),
                dl.Marker(position=[(dff.iloc[selected_rows[1],13]), (dff.iloc[selected_rows[1],14])], children=[
                    dl.Tooltip(dff.iloc[selected_rows[1],4]),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P(dff.iloc[selected_rows[1],9]),
                        html.H4("Sex"),
                        html.P(dff.iloc[selected_rows[1],12]),
                        html.H4("Breed"),
                        html.P(dff.iloc[selected_rows[1],4]),
                        html.H4("Age"),
                        html.P(dff.iloc[selected_rows[1],15])
                    ])
                ]),
                dl.Marker(position=[(dff.iloc[selected_rows[2],13]), (dff.iloc[selected_rows[2],14])], children=[
                    dl.Tooltip(dff.iloc[selected_rows[2],4]),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P(dff.iloc[selected_rows[2],9]),
                        html.H4("Sex"),
                        html.P(dff.iloc[selected_rows[2],12]),
                        html.H4("Breed"),
                        html.P(dff.iloc[selected_rows[2],4]),
                        html.H4("Age"),
                        html.P(dff.iloc[selected_rows[2],15])
                    ])
                ]),
                dl.Marker(position=[(dff.iloc[selected_rows[3],13]), (dff.iloc[selected_rows[3],14])], children=[
                    dl.Tooltip(dff.iloc[selected_rows[3],4]),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P(dff.iloc[selected_rows[3],9]),
                        html.H4("Sex"),
                        html.P(dff.iloc[selected_rows[3],12]),
                        html.H4("Breed"),
                        html.P(dff.iloc[selected_rows[3],4]),
                        html.H4("Age"),
                        html.P(dff.iloc[selected_rows[3],15])
                    ])
                ]),
                dl.Marker(position=[(dff.iloc[selected_rows[4],13]), (dff.iloc[selected_rows[4],14])], children=[
                    dl.Tooltip(dff.iloc[selected_rows[4],4]),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P(dff.iloc[selected_rows[4],9]),
                        html.H4("Sex"),
                        html.P(dff.iloc[selected_rows[4],12]),
                        html.H4("Breed"),
                        html.P(dff.iloc[selected_rows[4],4]),
                        html.H4("Age"),
                        html.P(dff.iloc[selected_rows[4],15])
                    ])
                ])
            ])
        ]



app
 