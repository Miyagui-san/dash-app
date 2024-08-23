import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Sample data
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Grapes12345"],
    "Amount": [4, 1, 2, 3],
    "City": ["SF", "SF", "SF", "SF"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
