from dash import dcc, html
import dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import pymysql
from flask import Flask
from flask_socketio import SocketIO, emit

# Initialize Flask and Flask-SocketIO
app = dash.Dash(__name__)
server = app.server
#server = Flask(__name__)
#app = dash.Dash(__name__, server=server)
socketio = SocketIO(server)

# Database connection configuration
db_config = {
    "host": "mariadb",
    "user": "root",
    "password": "asdfghj",
    "database": "paraguaiot"
}

def fetch_data():
    connection = pymysql.connect(**db_config)
    query = """
    SELECT identifier, DATE(timestamp) as day, AVG(weight) as avg_weight
    FROM weight_measurements
    GROUP BY identifier, day
    ORDER BY day
    """
    df = pd.read_sql(query, connection)
    connection.close()
    return df

@app.callback(
    Output('live-graph', 'figure'),
    [Input('identifier-dropdown', 'value')]
)
def update_graph(selected_identifier):
    df = fetch_data()
    filtered_df = df[df['identifier'] == selected_identifier]
    fig = px.line(filtered_df, x="day", y="avg_weight", title=f"Weight over Time for {selected_identifier}")
    return fig

app.layout = html.Div([
    html.H1("Weight Measurements Dashboard"),
    dcc.Dropdown(id='identifier-dropdown', options=[], value=None),
    dcc.Graph(id='live-graph')
])

@socketio.on('connect')
def handle_connect():
    df = fetch_data()
    identifiers = df['identifier'].unique().tolist()
    socketio.emit('update-dropdown', identifiers)

@socketio.on('refresh-data')
def handle_refresh_data():
    df = fetch_data()
    identifiers = df['identifier'].unique().tolist()
    socketio.emit('update-dropdown', identifiers)

if __name__ == "__main__":
    socketio.run(server, host='0.0.0.0', debug=True, allow_unsafe_werkzeug=True)
