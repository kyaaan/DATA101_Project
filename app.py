import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import geopandas as gpd

from dash import Dash, html, dcc, html, Input, Output, ctx
from datetime import date


# Geospatial Data
ph_provinces = gpd.read_file('Geo Data/gadm41_PHL_shp/gadm41_PHL_1.shp')
ph_regions = gpd.read_file('Geo Data/gadm41_PHL_shp/Regions.shp')
#world_geo = gpd.read_file('Geo Data/World Shapefile/ne_10m_admin_0_countries.shp')
world_geo = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# datasets
df_province_origin = pd.read_csv('processed_data/df_place_origin_provinces.csv')
df_region_origin = pd.read_csv('processed_data/df_place_origin_region.csv')
df_all_countries = pd.read_csv('processed_data/df_all_countries.csv')
df_occupation = pd.read_csv('processed_data/df_occupation.csv')
df_civil_status = pd.read_csv('processed_data/df_civil_status.csv')


# SEX
# TODO: PROCESS THIS INTO A CSV FILE
df_sex = pd.read_excel(
    'Emigrant Data/Emigrant-1988-2020-Sex-Modified-Provinces.xlsx')
df_sex = df_sex.dropna()   # drop rows with null values
# drop columns with all zero values
df_sex = df_sex.loc[:, (df_sex != 0).any(axis=0)]
df_sex = df_sex.dropna(how='all', axis=1)   # drop columns with all null values
# drop columns with any zero values after dropping null columns
df_sex = df_sex.loc[:, (df_sex != 0).any(axis=0)]
df_sex_no_ratio = df_sex.drop(columns="SEX RATIO")
df_sex_no_ratio.reset_index(drop=True, inplace=True)


sorted_dates = ['1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997',
                '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006',
                '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015',
                '2016', '2017', '2018', '2019', '2020']
slider_marks = {1988: 'Year 1988', 1992: 'Year 1992', 1996: 'Year 1996', 2000:  'Year 2000',
                2004: 'Year 2004', 2008: 'Year 2008', 2012: 'Year 2012', 2016: 'Year 2016', 2020: 'Year 2020'}

# MAIN APP RUNNING
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

# sideabr
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "5rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#011530",
    "font-size": "1.5rem",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "5rem",
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    "width": "70%",
}

SIDE_STYLE = {
    "background": "#011530",
    "width": "30%",
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

CARD_STYLE3 = {
    "background": "#f8f9fa",
    "margin": "1rem",
    'display':'none'
}

CARD_STYLE4 = {
    "background": "#032047",
    "color": "white",
    "margin": "1rem",
    "display": "none",
}


# TODO: FIX DROPBOX

DROPBOX_STYLE2 = {
    "display": "inline-block",
    "width": 200,
    "margin-left": 10,
    "color": "black",
    "radius": 50,
    "background-color": "#85A5CF",
    "min-width": "160px",
    "box-shadow": "0px 8px 16px 0px rgba(0,0,0,0.1)"
}

DROPBOX_STYLE1 = {
    "display": "inline-block",
    "width": 200,
    "margin-left": 10,
    "color": "black",
    "radius": 50,
    "background-color": "#f9f9f9",
    "min-width": "160px",
    "box-shadow": "0px 8px 16px 0px rgba(0,0,0,0.1)"
}


sidebar = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink(html.I(className="bi bi-house"), id="btn-origin", n_clicks=0),
                dbc.NavLink(html.I(className="bi bi-globe-americas"), id="btn-destination", n_clicks=0),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

line_graph = dbc.Card([
    dbc.CardHeader([
        html.H4('LINE GRAPH by', style={'display': 'inline-block'}),
        dcc.Dropdown(
            ['TOTAL EMIGRANTS', 'Province'],
            id='line_drop',
            value='TOTAL EMIGRANTS',
            style=DROPBOX_STYLE1
        ),
    ]),
    dbc.CardBody([
        dcc.Loading(dcc.Graph(id='line_graph'))])],
    style=CARD_STYLE1
)

choropleth_origin_graph = dbc.Card([
    dbc.CardHeader([
        html.H4('PHILLIPPINE EMIGRANTS ORIGIN by',
                style={'display': 'inline-block'}),
        dcc.Dropdown(
            ['Region', 'Province', 'Municipalities'],
            id='origin_drop',
            value='Region',
            style=DROPBOX_STYLE1
        ),
    ]),
    dbc.CardBody([
        dcc.Loading(dcc.Graph(id='choropleth_graph')),
        dcc.Slider(min=1988, max=2020, step=1, value=1988,
                   marks=slider_marks,
                   # place slider at bottom of graph
                   tooltip={"placement": "bottom", "always_visible": True},
                   id='date_selected')])
],
    style=CARD_STYLE1,
    id = 'origin-graph'
)

choropleth_destination_graph = dbc.Card([
    dbc.CardHeader([
        html.H4('PHILLIPPINE EMIGRANTS DESTINATION',
                style={'display': 'inline-block'}),
    ]),
    dbc.CardBody([
        dcc.Loading(dcc.Graph(id='choropleth_graph_destination')),
        dcc.Slider(min=1988, max=2020, step=1, value=1988,
                   marks=slider_marks,
                   # place slider at bottom of graph
                   tooltip={"placement": "bottom", "always_visible": True},
                   id='date_selected_destination')])
],
    style=CARD_STYLE3,
    id="destination-graph"
)

center = html.Div([
    html.Div(choropleth_origin_graph),
    html.Div(choropleth_destination_graph),
    html.Div(line_graph)],
    style=CONTENT_STYLE,
)


side = html.Div([

    dbc.Card(
                id='geninfo_card',
                style=CARD_STYLE2),

    dbc.Card(
                id='geninfo_destination_card',
                style=CARD_STYLE4),

    dbc.Card([
        dbc.CardBody([
            html.H4('Emmigrants by Sex', style={
                'display': 'inline-block'}),
            dcc.Dropdown(
                id='sex_chart_type',
                options=['Line Graph', 'Pie Chart'],
                value='Pie Chart',
                style=DROPBOX_STYLE2),
            dcc.Loading(dcc.Graph(id='pie_sex'))]
        )],
        style=CARD_STYLE2),

    dbc.Card([
        dbc.CardBody([
            html.H4('Major Occupation Group', style={
                'display': 'inline-block'}),
            dcc.Loading(dcc.Graph(id='bar_occupation'))]
        )],
        style=CARD_STYLE2),

    dbc.Card([
        dbc.CardBody([
            html.H4('Civil Status', style={'display': 'inline-block'}),
            dcc.Loading(dcc.Graph(id='bar_civil'))]
        )],
        style=CARD_STYLE2),
],

    style=SIDE_STYLE,
)

content = html.Div([center, side], className="d-flex align-items-stretch")

app.layout = html.Div([sidebar, content])


isOrigin = True #For Swapping Maptypes

@app.callback(Output('destination-graph', 'style'),
              Output('origin-graph', 'style'),
              Output('geninfo_card', 'style'),
              Output('geninfo_destination_card','style'),
              Input('btn-destination','n_clicks'),
              Input('btn-origin','n_clicks'),)
def hide_graph(btnDest,btnOrigin):
    if "btn-destination" == ctx.triggered_id:
         return {'display':'block'},{'display':'none'},{'display':'none'},{'display':'block',"background": "#032047","color": "white","margin": "1rem",}
    if "btn-origin" == ctx.triggered_id:
        return {'display':'none'},{'display':'block'},{'display':'block',"background": "#032047","color": "white","margin": "1rem",},{'display':'none'}
    
    
        
@app.callback(
    Output('choropleth_graph', "figure"),
    Input('date_selected', "value"),
    Input('origin_drop', "value"))
def display_choropleth(date_selected, origin_drop):
    year = str(date_selected)

    if origin_drop == "Province":
        df = df_province_origin
        geodata = ph_provinces
        featureid = "properties.NAME_1"
    if origin_drop == "Region":
        df = df_region_origin
        geodata = ph_regions
        featureid = "properties.REGION"

    fig = px.choropleth_mapbox(
        df,
        locations="NAME_1",
        featureidkey=featureid,
        geojson=geodata,
        hover_data=[year],
        color=year,
        mapbox_style="carto-positron",
        center={"lat": 12.879721, "lon": 121.774017},
        zoom=4,
        color_continuous_scale="Viridis",
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

@app.callback(
    Output('choropleth_graph_destination', "figure"),
    Input('date_selected_destination', "value"),)
def display_choropleth_destination(date_selected):
    
    year = str(date_selected)
    df=df_all_countries
    fig = px.choropleth_mapbox(
        df,
        locations="ISO_A3",
        featureidkey="properties.iso_a3",
        geojson=world_geo,
        hover_data=[year],
        color=year,
        zoom=1,
        mapbox_style="carto-positron",
        color_continuous_scale=[
                     [0, 'rgb(239,243,255)'],
                      [0.001, 'rgb(189,215,231)'],
                      [0.005, 'rgb(107,174,214)'],
                      [1, 'rgb(33,113,181,0.5)']],
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


@app.callback(
    Output('geninfo_card', 'children'),
    Input('date_selected', "value"),
    [Input('choropleth_graph', 'clickData')])
def display_info(date_selected, clickData):

    try:
        region = clickData['points'][0]['location']
    except:
        region = 'None Selected'
    try:
        count = clickData['points'][0]['customdata'][0]
    except:
        count = 0

    year = date_selected
    total = df_sex_no_ratio.loc[df_sex_no_ratio['YEAR'] == int(
        date_selected)]['TOTAL'].values[0]
    percentage = count/total

    fig = go.Figure(go.Bar(x=[count], name='Region Selected', text=[
                    count], marker_color='#FFBD59', orientation='h'))
    fig.add_bar(x=[total-count], name='Rest of the PH',
                text=[total-count], marker_color='#2B3660',)
    fig.update_layout(barmode='stack',
                      template='plotly_dark',
                      paper_bgcolor="#032047",
                      plot_bgcolor="#032047",
                      margin=dict(
                          l=10,
                          r=10,
                          b=10,
                          t=10,
                          pad=4
                      ),
                      height=100)
    fig.update_yaxes(visible=False)

    output = dbc.CardBody([
        dcc.Loading(dcc.Graph(figure=fig)),
        html.H4('General Information', style={'display': 'inline-block'}),
        html.P('Year: ' + str(year)),
        html.P('Region: ' + region),
        html.P('Percentage: ' + str(round(percentage*100, 2)) + '%'),])
    return output

@app.callback(
    Output('geninfo_destination_card', 'children'),
    Input('date_selected', "value"),
    [Input('choropleth_graph_destination', 'clickData')])
def display_destination_info(date_selected, clickData):

    try:
        region = clickData['points'][0]['location']
    except:
        region = 'None Selected'
    try:
        count = clickData['points'][0]['customdata'][0]
    except:
        count = 0

    year = date_selected
    total = df_sex_no_ratio.loc[df_sex_no_ratio['YEAR'] == int(
        date_selected)]['TOTAL'].values[0]
    percentage = count/total

    fig = go.Figure(go.Bar(x=[count], name='Region Selected', text=[
                    count], marker_color='#FFBD59', orientation='h'))
    fig.add_bar(x=[total-count], name='Rest of the World',
                text=[total-count], marker_color='#2B3660',)
    fig.update_layout(barmode='stack',
                      template='plotly_dark',
                      paper_bgcolor="#032047",
                      plot_bgcolor="#032047",
                      margin=dict(
                          l=10,
                          r=10,
                          b=10,
                          t=10,
                          pad=4
                      ),
                      height=100)
    fig.update_yaxes(visible=False)
    
    output = dbc.CardBody([
        dcc.Loading(dcc.Graph(figure=fig)),
        html.H4('General Information', style={'display': 'inline-block'}),
        html.P('Year: ' + str(year)),
        html.P('Country: ' + df_all_countries.loc[df_all_countries['ISO_A3'] == region]['COUNTRY'].values[0]),
        html.P('Percentage: ' + str(round(percentage*100, 2)) + '%'),])
    return output


@app.callback(
    Output('line_graph', "figure"),
    Input('date_selected', "value"),
    Input('line_drop', "value"))
def display_line_graph(date_selected, category):
    year = str(date_selected)
    fig = px.line(
        df_all_countries,
        x=year,
        y='Total'
    )
    return fig


@app.callback(
    Output('pie_sex', "figure"),
    Input('date_selected', "value"),
    Input('sex_chart_type', "value"))
def display_pie_sex(date_selected, sex_chart_type):
    year = float(date_selected)
    filtered_data = df_sex_no_ratio.loc[df_sex_no_ratio['YEAR'] == year].drop(
        columns=['YEAR', 'TOTAL'])

    if sex_chart_type == 'Pie Chart':
        fig = px.pie(
            names=['MALE', 'FEMALE'],
            labels=['Male', 'Female'],
            values=filtered_data.values.flatten().tolist(),
            hole=0.3,
        )
    else:
        fig = px.line(
            df_sex_no_ratio,
            x='YEAR',
            y=['MALE', 'FEMALE', 'TOTAL'])

    fig.update_layout(
        paper_bgcolor="#032047",
        plot_bgcolor="#032047",
        font_color="#E6E6E6",
        margin=dict(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=4
        ),
        height=300)

    return fig


@app.callback(
    Output('bar_occupation', "figure"),
    Input('date_selected', "value"))
def display_bar_occupation(date_selected):
    year = str(date_selected)

    fig = px.bar(
        df_occupation,
        x='MAJOR OCCUPATION GROUP',
        y=year)

    fig.update_layout(
        paper_bgcolor="#032047",
        plot_bgcolor="#032047",
        font_color="#E6E6E6",
        margin=dict(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=4
        ),
        height=300)

    return fig


@app.callback(
    Output('bar_civil', "figure"),
    Input('date_selected', "value"))
def display_bar_civil(date_selected):
    year = float(date_selected)

    fig = px.bar(
        df_civil_status,
        y=['Single', 'Married', 'Widower',
            'Separated', 'Divorced', 'Not Reported'],
        x='YEAR')

    fig.update_layout(
        paper_bgcolor="#032047",
        plot_bgcolor="#032047",
        font_color="#E6E6E6",
        margin=dict(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=4
        ),
        width=450,
        height=300)

    return fig


app.run_server(debug=True)
