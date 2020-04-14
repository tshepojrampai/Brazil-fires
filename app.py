import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash.dependencies import Input, Output
app =  dash.Dash()
server =  app.server

df = pd.read_csv('data/amazon.csv',encoding='latin1')

#MONTHS TO ENGLISH
span_to_eng = {
    'Janeiro':'January',
    'Fevereiro': 'February',
    'Março':'March',
    'Abril':'April',
    'Maio':'May',
    'Junho':'June',
    'Julho':'July',
    'Agosto':'August',
    'Setembro':'September',
    'Outubro': 'October',
    'Novembro': 'November',
    'Dezembro':'December'    
}
df['month'] = df['month'].map(span_to_eng)

#grouped dataframe
df_max = pd.DataFrame(df.groupby(['year','state','month']).number.sum())

#total by state
df_sum_state = pd.DataFrame(df_max.groupby(['state']).number.sum())
df_sum_state = df_sum_state.sort_values(by=['number'], ascending=False)
df_sum_state = df_sum_state.reset_index(drop=False)

#total by year
df_sum_year = pd.DataFrame(df_max.groupby(['year']).number.sum())
df_sum_year = df_sum_year.sort_values(by=['number'],ascending=False)
df_sum_year = df_sum_year.reset_index(drop=False)

#total by month and year
df['key'] = df.month.map(str)+'-'+df.year.apply(str)
df_sum_yr_month = pd.DataFrame(df.groupby(['key']).number.sum())
df_sum_yr_month = df_sum_yr_month.sort_values(by=['number'], ascending=False)
df_sum_yr_month = df_sum_yr_month .reset_index(drop=False)

style_table = {
    'maxHeight': '50ex',
    'overflowY': 'scroll',
    'width': '30%',
    'minWidth': '30%',
}
style_cell = {
    'fontFamily': 'Open Sans',
    'textAlign': 'center',
    'height': '30px',
    'padding': '10px 22px',
    'whiteSpace': 'inherit',
    'overflow': 'hidden',
                'textOverflow': 'ellipsis',
}
style_cell_conditional = [
    {
        'if': {'column_id': 'State'},
        'textAlign': 'left'
    },
]
style_header = {
    'fontWeight': 'bold',
    'backgroundColor': "#3D9970",
    'fontSize': '16px'
}
style_data_conditional = [
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)'
    }]
style_table = {
    'maxHeight': '50ex',
    'overflowY': 'scroll',
    'width': '100%',
    'minWidth': '100%',
}


# Style sheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# layout
app.layout = html.Div(children=[
    html.H1(
        children='Brazil Forest Fires',
        style={
            'textAlign': 'center',
            'color': 'green'
        }
    ),
    dcc.Tabs(id='tabs-example', value='tab', children=[
        dcc.Tab(label='Fire per state', value='tab-1'),
        dcc.Tab(label='Fires per year', value='tab-2'),
        dcc.Tab(label='Fires per year and month', value='tab-3'),
    ]),
    html.Div(id='tabs-example-content')
])

# callback for the responsiveness of the tab

@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])

def render_content(tab):
    '''Display the table and the graph sideby
    side when the respective tab is selected'''

    if tab == 'tab-1':
        return html.Div([
            html.Div([
                html.Div([
                    html.H1(
                        children='Table',
                        style={
                            'textAlign': 'center',
                            'color': 'green'
                        }), dash_table.DataTable(
                        id='table',
                        data=df_sum_state.to_dict("rows"),
                        columns=[{"name": i, "id": i}
                                 for i in df_sum_state.columns],
                        style_table=style_table,
                        style_cell=style_cell,
                        style_data_conditional=style_data_conditional,
                        style_header=style_header,
                        style_cell_conditional=style_cell_conditional,
                    )
                ], className="four columns"),
                html.Div([
                    html.H3('Fires per state in Brazil',
                            style={
                                'textAlign': 'center',
                                'color': 'green'}),
                    dcc.Graph(
                        id='Graph1',
                        figure={
                            'data': [
                                {'x': df.state, 'y': df.number, 'type': 'bar', 'name': 'state', 'marker': {'color': [
                                    '#b50000', '#e63535', '#fa8989'], 'size': 9, 'line': {'width': 1, 'color': 'orange'}}},
                            ]
                        }
                    )
                ], className="eight columns"),
            ], className="row")
        ])

    elif tab == 'tab-2':
        return html.Div([
            html.Div([
                html.Div([
                    html.H1(
                        children='Table',
                        style={
                            'textAlign': 'center',
                            'color': 'green'
                        }), dash_table.DataTable(
                        id='table',
                        data=df_sum_year.to_dict("rows"),
                        columns=[{"name": i, "id": i}
                                 for i in df_sum_year.columns],
                        style_table=style_table,
                        style_cell=style_cell,
                        style_data_conditional=style_data_conditional,
                        style_header=style_header,
                        style_cell_conditional=style_cell_conditional,
                    )

                ], className="four columns"),

                html.Div([
                    html.H3('Fires in Brazil per year',
                            style={
                                'textAlign': 'center',
                                'color': 'green'}
                            ), dcc.Graph(
                        id='Graph1',
                        figure={
                            'data': [
                                {'x': df.year, 'y': df.number, 'type': 'bar', 'name': 'state', 'marker': {'color': [
                                    '#b50000', '#e63535', '#fa8989'], 'size': 9, 'line': {'width': 1, 'color': 'orange'}}},

                            ]

                        }

                    )
                ], className="eight columns"),
            ], className="row")
        ])

    else:

        return html.Div([
            html.Div([
                html.Div([
                    html.H1(
                        children='Table',
                        style={
                            'textAlign': 'center',
                            'color': 'green'
                        }), dash_table.DataTable(
                            id='table',
                            data=df_sum_yr_month.to_dict("rows"),
                            columns=[{"name": i, "id": i}
                                     for i in df_sum_yr_month.columns],
                            style_table=style_table,
                            style_cell=style_cell,
                            style_data_conditional=style_data_conditional,
                            style_header=style_header,
                            style_cell_conditional=style_cell_conditional,
                    )

                ], className="four columns"),

                html.Div([
                    html.H3('Forest fires per month and year', style={
                        'textAlign': 'center',
                        'color': 'green'}
                    ), dcc.Graph(
                        id='Graph1',
                        figure={
                            'data': [
                                {'x': df.key, 'y': df.number, 'type': 'bar', 'name': 'state', 'marker': {'color': [
                                    '#b50000', '#e63535', '#fa8989'], 'size': 9, 'line': {'width': 1, 'color': 'orange'}}},

                            ],

                        }
                    )
                ], className="eight columns"),
            ], className="row")
        ])


if __name__ == '__main__':
    app.run_server()
