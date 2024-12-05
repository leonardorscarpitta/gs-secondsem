import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import requests
from datetime import datetime
import pytz

# Constants for IP and port
IP_ADDRESS = "localhost"
PORT_STH = 8666
DASH_HOST = "0.0.0.0"  # Set this to "0.0.0.0" to allow access from any IP

# Function to fetch data from the API
def get_data(attribute, lastN):
    url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/type/Iot/id/urn:ngsi-ld:Iot:001/attributes/{attribute}?lastN={lastN}"
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            values = data['contextResponses'][0]['contextElement']['attributes'][0]['values']
            return values
        except KeyError as e:
            print(f"Key error for {attribute}: {e}")
            return []
    else:
        print(f"Error accessing {url}: {response.status_code}")
        return []

# Function to convert UTC timestamps to Lisbon time
def convert_to_lisbon_time(timestamps):
    utc = pytz.utc
    lisbon = pytz.timezone('Europe/Lisbon')
    converted_timestamps = []
    for timestamp in timestamps:
        try:
            timestamp = timestamp.replace('T', ' ').replace('Z', '')
            converted_time = utc.localize(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')).astimezone(lisbon)
        except ValueError:
            converted_time = utc.localize(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')).astimezone(lisbon)
        converted_timestamps.append(converted_time)
    return converted_timestamps

# Set lastN value
lastN = 10  # Get 10 most recent points at each interval

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Efficiency Dashboard'),
    # Combined graph for East and West
    html.Div([
        html.H2('East and West Data'),
        dcc.Graph(id='east-west-graph'),
        dcc.Store(id='east-west-data-store', data={'timestamps': [], 'east_values': [], 'west_values': []}),
    ]),
    # Separate graph for Efficiency
    html.Div([
        html.H2('Efficiency Data'),
        dcc.Graph(id='efficiency-graph'),
        dcc.Store(id='efficiency-data-store', data={'timestamps': [], 'efficiency_values': []}),
    ]),
    # Interval for periodic updates
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # in milliseconds (10 seconds)
        n_intervals=0
    )
])

# Generalized data update callback
def update_data_store(attribute, stored_data, key):
    data = get_data(attribute, lastN)
    if data:
        values = [float(entry['attrValue']) for entry in data]
        timestamps = [entry['recvTime'] for entry in data]
        timestamps = convert_to_lisbon_time(timestamps)
        stored_data['timestamps'] = timestamps
        stored_data[key] = values
    return stored_data

# Callback for updating the East-West store
@app.callback(
    Output('east-west-data-store', 'data'),
    Input('interval-component', 'n_intervals'),
    State('east-west-data-store', 'data')
)
def update_east_west_store(n, stored_data):
    stored_data = update_data_store('east', stored_data, 'east_values')
    stored_data = update_data_store('west', stored_data, 'west_values')
    return stored_data

# Callback for updating the Efficiency store
@app.callback(
    Output('efficiency-data-store', 'data'),
    Input('interval-component', 'n_intervals'),
    State('efficiency-data-store', 'data')
)
def update_efficiency_store(n, stored_data):
    return update_data_store('efficiency', stored_data, 'efficiency_values')

# Callback for updating the East-West graph
@app.callback(
    Output('east-west-graph', 'figure'),
    Input('east-west-data-store', 'data')
)
def update_east_west_graph(stored_data):
    if stored_data['timestamps']:
        east_trace = go.Scatter(
            x=stored_data['timestamps'],
            y=stored_data['east_values'],
            mode='lines+markers',
            name='East',
            line=dict(color='orange')
        )
        west_trace = go.Scatter(
            x=stored_data['timestamps'],
            y=stored_data['west_values'],
            mode='lines+markers',
            name='West',
            line=dict(color='green')
        )
        fig = go.Figure(data=[east_trace, west_trace])
        fig.update_layout(
            title='East and West Over Time',
            xaxis_title='Timestamp',
            yaxis_title='Value',
            hovermode='closest'
        )
        return fig
    return {}

# Callback for updating the Efficiency graph
@app.callback(
    Output('efficiency-graph', 'figure'),
    Input('efficiency-data-store', 'data')
)
def update_efficiency_graph(stored_data):
    if stored_data['timestamps']:
        efficiency_trace = go.Scatter(
            x=stored_data['timestamps'],
            y=stored_data['efficiency_values'],
            mode='lines+markers',
            name='Efficiency',
            line=dict(color='blue')
        )
        fig = go.Figure(data=[efficiency_trace])
        fig.update_layout(
            title='Efficiency Over Time',
            xaxis_title='Timestamp',
            yaxis_title='Efficiency',
            hovermode='closest'
        )
        return fig
    return {}

if __name__ == '__main__':
    app.run_server(debug=True, host=DASH_HOST, port=8050)
