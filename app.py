import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd


from dash import Dash, html, dcc, html, Input, Output
from datetime import date


#Geospatial Data
ph_provinces = gpd.read_file('Geo Data/gadm41_PHL_shp/gadm41_PHL_1.shp')
ph_regions = gpd.read_file('Geo Data/gadm41_PHL_shp/Regions.shp')
token = open(".mapbox_token").read()

#datasets
df_province_origin = pd.read_csv('processed_data/df_place_origin_provinces.csv')
df_region_origin = pd.read_csv('processed_data/df_place_origin_region.csv')
df_all_countries = pd.read_csv('processed_data/df_all_countries.csv')

#SEX
df_sex = pd.read_excel('Emigrant Data/Emigrant-1988-2020-Sex-Modified-Provinces.xlsx')
df_sex = df_sex.dropna()   # drop rows with null values
df_sex = df_sex.loc[:, (df_sex != 0).any(axis=0)]   # drop columns with all zero values
df_sex = df_sex.dropna(how='all', axis=1)   # drop columns with all null values
df_sex = df_sex.loc[:, (df_sex != 0).any(axis=0)]   # drop columns with any zero values after dropping null columns
df_sex_no_ratio = df_sex.drop(columns="SEX RATIO")
df_sex_no_ratio.reset_index(drop=True, inplace=True)

sorted_dates = ['1988','1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997',
       '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006',
       '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015',
       '2016', '2017', '2018', '2019', '2020']
slider_marks = {1988: 'Year 1988',1992: 'Year 1992',1996 :'Year 1996', 2000:  'Year 2000', 2004:'Year 2004',2008:'Year 2008',2012:'Year 2012',2016:'Year 2016',2020: 'Year 2020'}

#MAIN APP RUNNING
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP])

#sideabr
SIDEBAR_STYLE = {
   # "position": "fixed",
   # "top": 0,
    #"left": 0,
    #"bottom": 0,
    "padding": "1rem 1rem",
    "background-color": "#011530",
    "font-size": "2rem",
    #"width": "5rem"
}

CARD_STYLE1 = {
    "background": "#f8f9fa",
    "margin": "1rem",
    "width": "50rem"
}

CARD_STYLE2 = {
    "background": "#032047",
    "color": "white",
    "margin": "1rem",
    "width": "30rem",
}

DROPBOX_STYLE = {
    "display": "inline-block",
    "width": 200,
    "margin-left": 10,
    "color": "black"
}

sidebar = dbc.Col(
    [
        dbc.Nav(
            [
                dbc.NavLink(html.I(className="bi bi-house"), href="/",active="exact"),
                dbc.NavLink(html.I(className="bi bi-globe-americas"), href="/page-1", active="exact"),
            ],
            vertical=True,
        ),
    ],
    width = 1,
    style = SIDEBAR_STYLE,
)

line_graph = dbc.Card([
    dbc.CardHeader([
        html.H4('LINE GRAPH by', style={'display': 'inline-block'}),
        dcc.Dropdown(
            ['TOTAL EMIGRANTS', 'Province','Municipalities'],
            id='line_drop',
            value = 'TOTAL EMIGRANTS',
            style=DROPBOX_STYLE
        ),
    ]),
    dbc.CardBody([
        dcc.Loading(dcc.Graph(id='line_graph'))])],
    style=CARD_STYLE1
)

choropleth_origin_graph = dbc.Card([
    dbc.CardHeader([
        html.H4('PHILLIPPINE EMIGRANTS ORIGIN by', style={'display': 'inline-block'}),
        dcc.Dropdown(
            ['Region', 'Province','Municipalities'],
            id='origin_drop',
            value = 'Region',
            style=DROPBOX_STYLE
            ),
    ]),
    dbc.CardBody([
        dcc.Loading(dcc.Graph(id='choropleth_graph')),
        dcc.Slider(min=1988, max=2020, step=1, value=1988,
            marks=slider_marks,
            tooltip={"placement": "bottom", "always_visible": True}, #place slider at bottom of graph
            id='date_selected')])
        ],
    style=CARD_STYLE1
)

center = dbc.Col([
            dbc.Row(choropleth_origin_graph),
            dbc.Row(line_graph)],
            width = 7
        )


side =  dbc.Col([
            dbc.Row(
                dbc.Card([
                dbc.CardBody([
                    html.H4('Emmigrants by Sex', style={'display': 'inline-block'}),
                    dcc.Dropdown(
                        id='sex_chart_type', 
                        options=['Line Graph', 'Pie Chart'],
                        value='Pie Chart',
                        style=DROPBOX_STYLE),
                    dcc.Loading(dcc.Graph(id='pie_sex'))]
                )],
                style=CARD_STYLE2
                )),
            dbc.Row()
            ],
            style={"background": "#011530"},
            width = 4
        )

app.layout = dbc.Container(dbc.Row([sidebar,center,side],justify="center"),fluid=True)


@app.callback(
    Output('choropleth_graph', "figure"), 
    Input('date_selected', "value"),
    Input('origin_drop',"value"))
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
    if origin_drop == "Municipalities":
        #insert municipality
        pass

    fig = px.choropleth_mapbox(
        df,
        locations="NAME_1",
        featureidkey=featureid,
        geojson=geodata,
        hover_data=[year],
        color=year,
        mapbox_style="carto-positron",
        center={"lat": 12.879721, "lon": 121.774017},
        zoom = 5,
        color_continuous_scale="Viridis",
        )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

@app.callback(
    Output('line_graph', "figure"),
    Input('date_selected', "value"), 
    Input('line_drop', "value"))
def display_line_graph(date_selected, category):
    fig = px.line(
            df_all_countries,
            x = 'Year',
            y = 'Total'
        )
    return fig

@app.callback(
    Output('pie_sex', "figure"), 
    Input('date_selected', "value"),
    Input('sex_chart_type',"value"))
def display_pie_sex(date_selected,sex_chart_type):
    year = float(date_selected)
    filtered_data = df_sex_no_ratio.loc[df_sex_no_ratio['YEAR']==year].drop(columns=['YEAR','TOTAL'])

    if sex_chart_type == 'Pie Chart':
        fig = px.pie(
                template='plotly_dark', 
                names=['MALE','FEMALE'],
                labels=['Male','Female'],
                values=filtered_data.values.flatten().tolist(),
                hole=0.3,
                )
    else:
        fig = px.line(
            df_sex_no_ratio,
            template='plotly_dark',
            x='YEAR', 
            y= ['MALE', 'FEMALE', 'TOTAL']
        )
    return fig

app.run_server(debug=True)
