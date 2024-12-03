import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import geopandas as gpd
import numpy as np

from dash import Dash, html, dcc, Input, Output
from datetime import date

# Geospatial Data
world_geo = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Datasets
df_all_countries = pd.read_csv('processed_data/df_all_countries.csv')
df_sex_no_ratio = pd.read_excel('Emigrant Data/Emigrant-1988-2020-Sex-Modified-Provinces.xlsx').fillna(0)
df_country_details = pd.read_csv('processed_data/country_details.csv')

df_sex_no_ratio = df_sex_no_ratio.dropna(how='all', axis=1).loc[:, (df_sex_no_ratio != 0).any(axis=0)]
df_sex_no_ratio.reset_index(drop=True, inplace=True)

sorted_dates = [i for i in range(1988, 2020 + 1)]
slider_marks = {year: f'Year {year}' for year in sorted_dates[::4]}

# MAIN APP RUNNING
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

# Styles
SIDEBAR_STYLE = {
    "width": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 0.2rem",
    "background-color": "#011530",
    "font-size": "1.5rem",
}

CONTENT_STYLE = {
    "margin-top": "2rem",
    "margin-left": "1rem",
    "margin-right": "1rem",
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    "width": "60%",
}

SIDE_STYLE = {
    "margin-top": "2rem",
    "margin-right": "2rem",
    "background": "#011530",
    "width": "40%",
}

CARD_STYLE1 = {
    "background": "#f8f9fa",
    "margin": "1rem",
}

CARD_STYLE2 = {
    "background": "#032047",
    "color": "white",
    "margin": "1rem",
}

DROPBOX_STYLE1 = {
    "display": "inline-block",
    "width": 200,
    "margin-left": 10,
    "color": "black",
    "radius": 50,
    "min-width": "160px",
}

CONTENT_BODY_STYLE = {
    "margin-top": "2rem",
    "margin-left": "1rem",
    "margin-right": "1rem",
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    "width": "100%",
}

body_content = html.Div([
    html.Div(id='country-details')
],style=CONTENT_BODY_STYLE)

sidebar = html.Div([
    html.H2('Migration Guide for Filipinos', style={'textAlign': 'center', 'color': 'white'}),
], id="sidebar", style=SIDEBAR_STYLE)

line_graph = dbc.Card([
    dbc.CardHeader([
        html.H4('LINE GRAPH by', style={'display': 'inline-block'}),
        dcc.Dropdown(['TOTAL EMIGRANTS', 'SEX', 'MAJOR OCCUPATION', 'CIVIL STATUS', 'EDUCATION', 'AGE GROUP'],
                     id='line_drop', value='TOTAL EMIGRANTS', style=DROPBOX_STYLE1),
    ]),
    dbc.CardBody([dcc.Loading(dcc.Graph(id='line_graph'))]),
], style=CARD_STYLE1)

choropleth_destination_graph = dbc.Card([
    dbc.CardHeader([html.H4('Philippine Emigration', style={'display': 'inline-block'})]),
    dbc.CardBody([
        dcc.Loading(dcc.Graph(id='choropleth_graph_destination')),
        dcc.Slider(min=1988, max=2020, step=1, value=1988, marks=slider_marks,
                   tooltip={"placement": "bottom", "always_visible": True}, id='date_selected_destination')
    ]),
], style=CARD_STYLE1, id="destination-graph")

center = html.Div([html.Div(choropleth_destination_graph)], style=CONTENT_STYLE)

intro = html.Div([
    html.H2("WELCOME!"),
    html.P("Migration has been deeply woven into the fabric of the Philippines' history, profoundly influencing Filipino culture. This website offers an insightful look into the destinations where Filipinos migrate and provides detailed information about each country."),
    html.P("Click on a country on the map to view more details"),
], style={'textAlign': 'justify', 'color': 'white', 'padding': '0.5em'})

side = html.Div([
    intro,
    dbc.Card(id='geninfo_destination_card', children=[
        dbc.CardBody([
            html.H4('General Information'),
            html.H4("Select a country to see details", style={'text-align': 'center', 'color': '#E6E6E6', 'margin-top': 10}),
        ])
    ], style=CARD_STYLE2),
], style=SIDE_STYLE)

content = html.Div([center, side], className="d-flex align-items-stretch")

app.layout = html.Div([sidebar, content, body_content])

# Callbacks
@app.callback(
    Output('choropleth_graph_destination', "figure"),
    Input('date_selected_destination', "value"),
)
def display_choropleth_destination(date_selected):
    year = str(date_selected)
    df = df_all_countries
    fig = px.choropleth_mapbox(
        df, locations="ISO_A3", featureidkey="properties.iso_a3", geojson=world_geo,
        hover_data=[year], color=year, zoom=1, mapbox_style="carto-positron",
        color_continuous_scale=[
            [0, 'rgb(239,243,255)'],
            [0.001, 'rgb(189,215,231)'],
            [0.005, 'rgb(107,174,214)'],
            [1, 'rgb(33,113,181,0.5)']],
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

@app.callback(
    Output('geninfo_destination_card', 'children'),
    Input('date_selected_destination', "value"),
    [Input('choropleth_graph_destination', 'clickData')]
)
def display_destination_info(date_selected, clickData):
    if clickData:
        region = clickData['points'][0]['location']
        country_info = df_all_countries[df_all_countries['ISO_A3'] == region].iloc[0]
        country = country_info['COUNTRY']
        count = country_info[str(date_selected)]
    else:
        country = 'No Country'
        count = 0

    total = df_sex_no_ratio.loc[df_sex_no_ratio['YEAR'] == int(date_selected)]['TOTAL'].values[0]
    percentage = count / total if total != 0 else 0

    fig = go.Figure(go.Bar(x=[count], name='Region Selected', text=[count], marker_color='#FFBD59', orientation='h'))
    fig.add_bar(x=[total - count], name='Rest of the World', text=[total - count], marker_color='#2B3660')
    fig.update_layout(barmode='stack', template='plotly_dark', paper_bgcolor="#032047", plot_bgcolor="#032047",
                      margin=dict(l=10, r=10, b=10, t=10, pad=4), height=100)
    fig.update_yaxes(visible=False)

    output = dbc.CardBody([
        html.H4('General Information'),
        dcc.Loading(dcc.Graph(figure=fig)),
        html.H4(country, style={'text-align': 'center', 'color': '#E6E6E6', 'margin-top': 10}),
        html.H3(f"{round(percentage * 100, 2)}%", style={'text-align': 'center', 'color': '#FF914D'})
    ])
    return output

@app.callback(
    Output('country-details', 'children'),
    [Input('choropleth_graph_destination', 'clickData')]
)
def display_country_details(clickData):
    if clickData:
        region = clickData['points'][0]['location']
        country_details = df_country_details[df_country_details['Country'] == region]
        if not country_details.empty:
            country_details = country_details.iloc[0]
            country_name = country_details['Country']
            about = country_details['About Country']
            location = country_details['Location']
            jobs = country_details['Available Jobs and Salaries Expectations']
            benefits = country_details['Benefits']
            requirements = country_details['Requirements']
            
            benefits_list = '\n- '.join(benefits.split('. '))
            requirements_list = '\n- '.join(requirements.split('. '))
    
            return dcc.Markdown(
                "## Country: " + country_name + "\n\n" +
                "**About:** " + about + "\n\n" +
                "**Location:** " + location + "\n\n" +
                "**Available Jobs and Salaries Expectations:**\n- " + jobs.replace(', ', '\n- ') + "\n"
            )

app.run(debug=False, host="0.0.0.0", port=10000)
