import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Database connection configuration
DATABASE_URL = "postgresql://postgres:asdfghj@postgresql/paraguaiot"

# Create an engine
engine = create_engine(DATABASE_URL)

# Function to get data from the database
def fetch_data():
    query = """
    SELECT
        identifier,
        DATE(timestamp) as day,
        AVG(weight) as avg_weight
    FROM
        weight_measurements
    GROUP BY
        identifier, day
    ORDER BY
        day
    """

    # Fetch the data into a DataFrame
    df = pd.read_sql(query, engine)

    return df

# Fetch the data
df = fetch_data()

# Create a plot for each identifier
figures = []
for identifier in df['identifier'].unique():
    fig = px.line(
        df[df['identifier'] == identifier],
        x="day", y="avg_weight", title=f"Weight over Time for {identifier}",
        labels={'avg_weight': 'Average Weight', 'day': 'Date'}
    )
    figures.append(fig)

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Weight Measurements Dashboard'),

    html.Div(children='''
        A dashboard displaying weight measurements over time.
    '''),

    # Add a graph for each identifier
    *[dcc.Graph(id=f'graph-{identifier}', figure=fig) for identifier, fig in zip(df['identifier'].unique(), figures)]
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
