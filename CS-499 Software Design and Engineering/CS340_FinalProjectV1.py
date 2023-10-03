
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
import logging

#importing AnimalShelter_CRUD File
from AnimalShelter_CRUD import AnimalShelter


###########################
#Configuring Logging Feature
###########################

logging.basicConfig(
    filename='Application.log',  # Specify the log file name
    level=logging.INFO,  # Set the logging level to INFO (you can change it)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Define log message format
)

###########################
# Data Manipulation / Model
###########################

username = "aacuser"
password = "admin"
shelter = AnimalShelter(username, password)


# class read method must support return of cursor object
df = pd.DataFrame.from_records(shelter.read({}))


#########################
# Dashboard Layout / View
#########################
app = JupyterDash('SimpleExample')

# Add in Grazioso Salvare logo
image_filename = 'Grazioso_Salvare_Logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Place the HTML image tag in the line below into the app.layout code according to your design
# Also remember to include a unique identifier such as your name or date


#html.H3('SNHU CS-499 Dashboard'),

app.layout = html.Div([
#    html.Div(id='hidden-div', style={'display':'none'}),
    # Display an image
    html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))),
    # Display a title
    html.Center(html.B(html.H1('Steve Edmund - SNHU CS-340 Dashboard'))),
    # Display a description
    html.Center(html.P('Select up to five from the table for the map')),
   # Add a horizontal line
    html.Hr(),
   # Radio Items to select the rescue filter options
    html.Div(
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
    # Add another horizontal line
    html.Hr(),
    # Data table component
    dt.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        
        data=df.to_dict('records'),
        
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
   
   # Add line break and horizontal line
    html.Br(),
    html.Hr(),

#This sets up the dashboard so that the chart and geolocation chart are side-by-side
   
    # Div to hold charts and map
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        # Chart component
        html.Div(
            #dcc.Graph(id='graph-id'),
            id='graph-id',
            className='col s12 m6',

            ),
        # Map component
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
    try:
        logging.info(f"Updating dashboard with filter type: {filter_type}")

        if filter_type == 'WR':
            # Filter criteria for intact female dogs of specific breeds and ages
            filter_criteria = {
                '$and': [
                    {'sex_upon_outcome': 'Intact Female'},
                    {'$or': [
                        {'breed': 'Labrador Retriever Mix'},
                        {'breed': 'Chesa Bay Retr Mix'},
                        {'breed': 'Newfoundland Mix'},
                        {'breed': 'Newfoundland/Labrador Retriever'},
                        {'breed': 'Newfoundland/Australian Cattle Dog'},
                        {'breed': 'Newfoundland/Great Pyrenees'}
                    ]},
                    {'$and': [
                        {'age_upon_outcome_in_weeks': {'$gte': 26}},
                        {'age_upon_outcome_in_weeks': {'$lte': 156}}
                    ]}
                ]
            }
            df = pd.DataFrame(list(shelter.read(filter_criteria)))

        elif filter_type == 'MWR':
            # Filter criteria for intact male dogs of specific breeds and ages
            filter_criteria = {
                '$and': [
                    {'sex_upon_outcome': 'Intact Male'},
                    {'$or': [
                        {'breed': 'German Shepherd'},
                        {'breed': 'Alaskan Malamute'},
                        {'breed': 'Old English Sheepdog'},
                        {'breed': 'Rottweiler'},
                        {'breed': 'Siberian Husky'}
                    ]},
                    {'$and': [
                        {'age_upon_outcome_in_weeks': {'$gte': 26}},
                        {'age_upon_outcome_in_weeks': {'$lte': 156}}
                    ]}
                ]
            }
            df = pd.DataFrame(list(shelter.read(filter_criteria)))

        elif filter_type == 'DRIT':
            # Filter criteria for intact male dogs of specific breeds and ages
            filter_criteria = {
                '$and': [
                    {'sex_upon_outcome': 'Intact Male'},
                    {'$or': [
                        {'breed': 'Doberman Pinscher'},
                        {'breed': 'German Shepherd'},
                        {'breed': 'Golden Retriever'},
                        {'breed': 'Bloodhound'},
                        {'breed': 'Rottweiler'}
                    ]},
                    {'$and': [
                        {'age_upon_outcome_in_weeks': {'$gte': 20}},
                        {'age_upon_outcome_in_weeks': {'$lte': 300}}
                    ]}
                ]
            }
            df = pd.DataFrame(list(shelter.read(filter_criteria)))

        elif filter_type == 'RESET':
            # Reset the search to display all results
            df = pd.DataFrame.from_records(shelter.read({}))

        # Define columns for the DataTable
        columns = [{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]

        # Convert DataFrame to dictionary records
        data = df.to_dict('records')

        return (data, columns)

    except Exception as e:
        # Handle exceptions and provide an error message
        logging.error(f"An error occurred in update_dashboard: {str(e)}")
        error_message = str(e)
        return ([], []), [{'name': 'Error', 'id': 'error'}]  # Return an error message as a single-column DataTable
    

@app.callback(
    Output('datatable-id', 'style_data_conditional'), # Output component to update (conditional styling)
    [Input('datatable-id', 'selected_columns')] # Input component (selected columns)
)
def update_styles(selected_columns):
    """
    Callback function to update the conditional styling of a DataTable based on selected columns.

    Args:
    - selected_columns (list): A list of selected column IDs in the DataTable.

    Returns:
    - list of dict: A list of dictionaries specifying conditional styling rules for columns.
    """
    # This callback function is triggered when the user selects columns in the DataTable.

    # Define conditional styling rules for selected columns.
    # Each rule is specified as a dictionary in a list comprehension.
    try:
        if isinstance(selected_columns, list):
            logging.info(f"Updating styles for selected columns: {selected_columns}")
            return [{
                'if': { 'column_id': i }, # Apply the style if the condition is met for column 'i'
                'background_color': '#D2F3FF' # Set the background color for the selected columns
            } for i in selected_columns]
        else:
            # Handle the case where 'selected_columns' is not a list
            raise ValueError("Input 'selected_columns' must be a list.")
    except Exception as e:
        logging.error(f"An error occurred in update_styles: {str(e)}")
        # Handle any unexpected exceptions
        return []  # Return an empty list if an error occurs


#function to update the pie chart
@app.callback(
    Output('graph-id', "children"), # Output component to update with new content (a graph)
    [Input('datatable-id', "derived_viewport_data")]) # Input component for data (from a DataTable)

def update_graphs(viewData):
    try:
        
        # Log the function call
        logging.info("Updating pie chart")
        
        # Check if viewData is not None and is a dictionary
        if viewData is not None and isinstance(viewData, dict):
            
            # Import the currently displayed data from the DataTable into a DataFrame (dff)
            dff = pd.DataFrame.from_dict(viewData)
            
            # Check if 'breed' column exists in the DataFrame
            if 'breed' in dff.columns:
                # Calculate values needed for the pie chart: names (breed) and values (recurring counts)
                names = dff['breed'].value_counts().keys().tolist()
                values = dff['breed'].value_counts().tolist()

                # Create a pie chart based on the calculated data
                pie_chart = dcc.Graph(
                    figure=px.pie(
                        data_frame=dff,
                        values=values,
                        names=names,
                        color_discrete_sequence=px.colors.sequential.RdBu,
                        width=800,
                        height=500
                    )

          )

                logging.error("Error: 'breed' column not found in the data.")
                # Return the pie chart as a list, which will be used to update the output component
                return [pie_chart]
            else:
                # Handle the case where 'breed' column is missing
                logging.error("Error: 'breed' column not found in the data.")
                return ["Error: 'breed' column not found in the data."]
        else:
            # Handle the case where viewData is not a dictionary
            logging.error("Error: Invalid data format.")
            return ["Error: Invalid data format."]

    except Exception as e:
        # Handle any other unexpected exceptions
        logging.error(f"An error occurred in update_graphs: {str(e)}")
        return ["Error: An unexpected error occurred."]


# This is a Dash callback decorator that specifies the output and inputs for the callback function.
@app.callback(
    Output('map-id', "children"), # Output component to update with new content
    [Input('datatable-id', "derived_viewport_data"), # Input component for data
     Input('datatable-id', 'selected_rows'), # Input component for selected rows
     Input('datatable-id', 'selected_columns')]) # Input component for selected columns

def add_marker_with_popup(selected_row, dff):
    #"""
    #Add a marker with a popup to a map based on the selected row's data.

    #Args:
    #- selected_row (int): Index of the selected row.
    #- dff (pd.DataFrame): The DataFrame containing the data.

    #Returns:
    #- str: HTML code for the marker and popup.
    #"""
    try:
        if selected_row < len(dff):
            
            # Log the function call
            logging.info(f"Adding marker for selected row: {selected_row}")

            marker_html = f"""
                dl.Marker(position=({dff.iloc[selected_row, 13]}, {dff.iloc[selected_row, 14]}), children=[
                    dl.Tooltip("{dff.iloc[selected_row, 4]}"),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P("{dff.iloc[selected_row, 9]}"),
                        html.H4("Sex"),
                        html.P("{dff.iloc[selected_row, 12]}"),
                        html.H4("Breed"),
                        html.P("{dff.iloc[selected_row, 4]}"),
                        html.H4("Age"),
                        html.P("{dff.iloc[selected_row, 15]}")
                    ])
                ])
            """
            return marker_html
        else:
            raise IndexError("Selected row index is out of range.")
    except KeyError as e:
        # Handle missing key error
        logging.error(f"Error: Missing key - {str(e)}")
        return f"Error: Missing key - {str(e)}"
    except ValueError as e:
        # Handle value error
        logging.error(f"Error: Value error - {str(e)}")
        return f"Error: Value error - {str(e)}"
    except IndexError as e:
        # Handle index out of range error
        logging.error(f"Error: Index out of range - {str(e)}")
        return f"Error: Index out of range - {str(e)}"


def update_map(viewData, selected_rows, selected_columns):

   #"""
    #Updates Map with with pop up Markers
    #Args:
    #- viewData(Dictionary): Data stored in the form of dictionary in Database.
    #- selected_row (int): Index of the selected row.

    #Returns:
    #- map_html: HTML code for the map.
    #""" 
    try:
    # Log the function call
        logging.info("Updating map")
        
        dff = pd.DataFrame.from_dict(viewData)

        if selected_rows == []:
            selected_rows = [0]

        # Create a map object
        map_html = """
            dl.Map(style={'width':'1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
                dl.TileLayer(id="base-layer-id"),
        """

        # Add markers to the map based on the selected rows
        for index in selected_rows:
            try:
                marker_html = add_marker_with_popup(index, dff)
                map_html += marker_html
            except Exception as e:
                # Handle any exceptions that may occur during marker addition
                logging.error(f"Error adding marker: {str(e)}")
                map_html += f"Error adding marker: {str(e)}"

        # Close the map object
        map_html += "])"

        return [map_html]
    except Exception as e:
        # Log the exception
        logging.error(f"An error occurred in update_map: {str(e)}")
app
 
