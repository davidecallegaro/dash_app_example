#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv("nama_10_gdp_1_Data.csv")

# Only absolute value are relevant, so UNIT column has to be filtered
df = df[df["UNIT"] == 'Current prices, million euro']

# Value column transformed to numeric
df["Value"] = df["Value"].str.replace(",",".")
df["Value"] = df["Value"].str.replace(".","")
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

# Options for dropdowns
available_indicators = df["NA_ITEM"].unique()
available_countries = df["GEO"].unique()


tab1 = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ],
    style={'marginBottom': 20}),
    dcc.Graph(id='indicator-graphic'),
    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    )
])


tab2 = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='country-column-2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='European Union - 28 countries'
            ),
        ],
        style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='yaxis-column-2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='yaxis-type-2',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ],
    style={'marginBottom': 20, 'marginTop': 100}),
    dcc.Graph(id='indicator-graphic-2'),
])


app.layout = html.Div([html.H1('Dashboard of Davide Callegaro'), tab1, tab2],
                     style={'marginLeft': 30, 'marginRight': 30})


@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]
    return {
        'data': [go.Scatter(
            x=dff[dff["NA_ITEM"] == xaxis_column_name]['Value'],
            y=dff[dff["NA_ITEM"] == yaxis_column_name]['Value'],
            text=dff[dff["NA_ITEM"] == yaxis_column_name]["GEO"],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 50, 'b': 40, 't': 40, 'r': 10},
            hovermode='closest'
        )
    }


@app.callback(
    dash.dependencies.Output('indicator-graphic-2', 'figure'),
    [dash.dependencies.Input('yaxis-column-2', 'value'),
     dash.dependencies.Input('yaxis-type-2', 'value'),
     dash.dependencies.Input('country-column-2', 'value')])
def update_graph_2(yaxis_column_name_2,yaxis_type_2,country_column_2):
    dff_2 = df[df['GEO'] == country_column_2]
    dff_2 = dff_2[dff_2["NA_ITEM"] == yaxis_column_name_2]
    return {
        'data': [go.Scatter(
            x=dff_2["TIME"],
            y=dff_2['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': "Year",
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name_2,
                'type': 'linear' if yaxis_type_2 == 'Linear' else 'log'
            },
            margin={'l': 50, 'b': 50, 't': 40, 'r': 10},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()

