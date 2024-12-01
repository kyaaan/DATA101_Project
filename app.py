import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import geopandas as gpd
import numpy as np

from dash import Dash, html, dcc, html, Input, Output, ctx, State
from datetime import date


# Geospatial Data
ph_provinces = gpd.read_file('Geo Data/gadm41_PHL_shp/gadm41_PHL_1.shp')
ph_regions = gpd.read_file('Geo Data/gadm41_PHL_shp/Regions.shp')
# world_geo = gpd.read_file('Geo Data/World Shapefile/ne_10m_admin_0_countries.shp')
world_geo = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# datasets
df_province_origin = pd.read_csv(
    'processed_data/df_place_origin_provinces.csv')
df_region_origin = pd.read_csv('processed_data/df_place_origin_region.csv')
df_all_countries = pd.read_csv('processed_data/df_all_countries.csv')
df_occupation = pd.read_csv('processed_data/df_occupation.csv')
df_civil_status = pd.read_csv('processed_data/df_civil_status.csv')
df_education = pd.read_excel(
    'Emigrant Data/Emigrant-1988-2020-Educ.xlsx').fillna(0)
df_age = pd.read_excel('Emigrant Data/Emigrant-1981-2020-Age.xlsx').fillna(0)

# Log transformed data
df_province_origin_log = df_province_origin
df_province_origin_log[df_province_origin_log.columns[1:]
                       ] = df_province_origin_log[df_province_origin_log.columns[1:]].replace(0, 0.000001)
df_province_origin_log[df_province_origin_log.columns[1:]] = np.log(
    df_province_origin_log[df_province_origin_log.columns[1:]])

df_region_origin_log = df_region_origin
df_region_origin_log[df_region_origin_log.columns[1:]
                     ] = df_region_origin_log[df_region_origin_log.columns[1:]].replace(0, 0.000001)
df_region_origin_log[df_region_origin_log.columns[1:]] = np.log(
    df_region_origin_log[df_region_origin_log.columns[1:]])


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

# sideabar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "6.5rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 0.2rem",
    "background-color": "#011530",
    "font-size": "1.5rem",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "6.5rem",
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

CARD_STYLE_HIDDEN = {
    'display': 'none'
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
    # "background-color": "#f9f9f9",
    "min-width": "160px",
    # "box-shadow": "0px 8px 16px 0px rgba(0,0,0,0.1)"
}


# pop-up box
modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("FEATURES TO SHOW")),
        dbc.ModalBody(dcc.Checklist(
            [{"label": html.Div(['Sex'], style={'font-size': 20}), "value": 'Sex'},
             {"label": html.Div(['Civil Status'], style={
                                'font-size': 20}), "value": 'Civil Status'},
             {"label": html.Div(['Educational Attainment'], style={'font-size': 20}),
              "value": 'Educational Attainment'},
             {"label": html.Div(['Major Occupation'], style={'font-size': 20}),
              "value": 'Major Occupation'},
             {"label": html.Div(['Age Group'], style={
                                'font-size': 20}), "value": 'Age Group'},
             ], value=['Sex'],
            id="checklist",
            inline=False,
            labelStyle={"display": "flex", "align-items": "center"},
        )),
        dbc.ModalFooter(
            dbc.Button(
                "SUBMIT", id="close", className="ms-auto", n_clicks=0
            )
        ),
    ],
    id="modal",
    is_open=False,
)


sidebar = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink([html.I(className="bi bi-house"), html.Br(), html.P("ORIGIN", style={"font-size": 10, 'font-weight': 'bold'})],
                            id="btn-origin", n_clicks=0, style={'text-align': 'center', 'color': 'white'}),
                dbc.NavLink([html.I(className="bi bi-globe-americas"), html.Br(), html.P("DESTINATION", style={"font-size": 10, 'font-weight': 'bold'})],
                            id="btn-destination", n_clicks=0, style={'text-align': 'center', 'color': 'white'}),
                dbc.NavLink([html.I(className="bi bi-plus-square"), html.Br(), html.P("FEATURES", style={"font-size": 10, 'font-weight': 'bold'})],
                            id="open", n_clicks=0, style={'text-align': 'center', 'color': 'white'}),
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
            ['TOTAL EMIGRANTS', 'SEX', 'MAJOR OCCUPATION',
                'CIVIL STATUS', 'EDUCATION', 'AGE GROUP'],
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
            ['Region', 'Province'],
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
    id='origin-graph'
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
    style=CARD_STYLE_HIDDEN,
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
        style=CARD_STYLE_HIDDEN),

    dbc.Card([
        dbc.CardBody([
            html.H4('Emmigrants by Sex', style={
                'display': 'inline-block'}),
            dcc.Loading(dcc.Graph(id='pie_sex'))]
        )],
        id='sex_card',
        style=CARD_STYLE2),

    dbc.Card([
        dbc.CardBody([
            html.H4('Major Occupation Group', style={
                'display': 'inline-block'}),
            dcc.Loading(dcc.Graph(id='bar_occupation'))]
        )],
        id='occupation_card',
        style=CARD_STYLE_HIDDEN),

    dbc.Card([
        dbc.CardBody([
            html.H4('Civil Status', style={'display': 'inline-block'}),
            dcc.Loading(dcc.Graph(id='bar_civil'))]
        )],
        id='civil_card',
        style=CARD_STYLE_HIDDEN),

    dbc.Card([
        dbc.CardBody([
            html.H4('Educational Attainment', style={
                    'display': 'inline-block'}),
            dcc.Loading(dcc.Graph(id='bar_educ'))]
        )],
        id='educ_card',
        style=CARD_STYLE_HIDDEN),

    dbc.Card([
        dbc.CardBody([
            html.H4('Age Group', style={
                    'display': 'inline-block'}),
            dcc.Loading(dcc.Graph(id='bar_age'))]
        )],
        id='age_card',
        style=CARD_STYLE_HIDDEN),
],

    style=SIDE_STYLE,
)

content = html.Div([center, side, modal],
                   className="d-flex align-items-stretch")

app.layout = html.Div([sidebar, content])

# This is for pop-up


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Code to Show and Hide Cards


@app.callback(Output('destination-graph', 'style'),
              Output('origin-graph', 'style'),
              Output('geninfo_card', 'style'),
              Output('geninfo_destination_card', 'style'),
              Output('sex_card', 'style'),
              Output('occupation_card', 'style'),
              Output('civil_card', 'style'),
              Output('educ_card', 'style'),
              Output('age_card', 'style'),
              Input('btn-destination', 'n_clicks'),
              Input('btn-origin', 'n_clicks'),
              Input('checklist', 'value'),
              Input('close', 'n_clicks'),)
def hide_graph(btnDest, btnOrigin, checklist, btnClose):

    sexStyle = CARD_STYLE_HIDDEN
    civilStyle = CARD_STYLE_HIDDEN
    educStyle = CARD_STYLE_HIDDEN
    occuStyle = CARD_STYLE_HIDDEN
    ageStyle = CARD_STYLE_HIDDEN

    if "btn-destination" == ctx.triggered_id:
        return {'display': 'block'}, {'display': 'none'}, CARD_STYLE_HIDDEN, CARD_STYLE2, CARD_STYLE_HIDDEN, CARD_STYLE_HIDDEN, CARD_STYLE_HIDDEN, CARD_STYLE_HIDDEN, CARD_STYLE_HIDDEN
    if ("btn-origin" == ctx.triggered_id) or ("close" == ctx.triggered_id):
        for option in checklist:
            if option == 'Sex':
                sexStyle = CARD_STYLE2
            if option == 'Civil Status':
                civilStyle = CARD_STYLE2
            if option == 'Educational Attainment':
                educStyle = CARD_STYLE2
            if option == 'Major Occupation':
                occuStyle = CARD_STYLE2
            if option == 'Age Group':
                ageStyle = CARD_STYLE2
        return {'display': 'none'}, {'display': 'block'}, CARD_STYLE2, CARD_STYLE_HIDDEN, sexStyle, occuStyle, civilStyle, educStyle, ageStyle


@app.callback(
    Output('choropleth_graph', "figure"),
    Input('date_selected', "value"),
    Input('origin_drop', "value"))
def display_choropleth(date_selected, origin_drop):
    year = str(date_selected)

    if origin_drop == "Province":
        df = df_province_origin_log
        geodata = ph_provinces
        featureid = "properties.NAME_1"
    if origin_drop == "Region":
        df = df_region_origin_log
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
    df = df_all_countries
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
        region = 'No Region'
    try:
        count = round(np.exp(clickData['points'][0]['customdata'][0]))
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
        html.H4('General Information'),
        dcc.Loading(dcc.Graph(figure=fig)),
        html.H4(region, style={'text-align': 'center',
                'color': '#E6E6E6', 'margin-top': 10}),
        html.H3(str(round(percentage*100, 2)) + '%', style={'text-align': 'center', 'color': '#FF914D'}),])
    return output


@app.callback(
    Output('geninfo_destination_card', 'children'),
    Input('date_selected', "value"),
    [Input('choropleth_graph_destination', 'clickData')])
def display_destination_info(date_selected, clickData):

    try:
        region = clickData['points'][0]['location']
    except:
        region = 'No Country'
    try:
        count = clickData['points'][0]['customdata'][0]
        country = df_all_countries.loc[df_all_countries['ISO_A3']
                                       == region]['COUNTRY'].values[0]
    except:
        count = 0
        country = 'No Country'

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
        html.H4('General Information'),
        dcc.Loading(dcc.Graph(figure=fig)),
        html.H4(country, style={'text-align': 'center',
                'color': '#E6E6E6', 'margin-top': 10}),
        html.H3(str(round(percentage*100, 2)) + '%', style={'text-align': 'center', 'color': '#FF914D'})])

    return output


@app.callback(
    Output('line_graph', "figure"),
    Input('date_selected', "value"),
    Input('line_drop', "value"))
def display_line_graph(date_selected, category):
    year = str(date_selected)
    df3 = df_occupation
    df3 = df3.set_index('MAJOR OCCUPATION GROUP').drop(
        columns=["TOTAL"]).T.reset_index().rename(columns={'index': 'YEAR'})
    df4 = df_education
    df4 = df4.set_index('EDUCATIONAL ATTAINMENT').drop(
        columns=["TOTAL"]).T.reset_index().rename(columns={'index': 'YEAR'})
    df5 = df_age
    df5 = df5.set_index('AGE GROUP').drop(
        columns=["TOTAL"]).T.reset_index().rename(columns={'index': 'YEAR'})

    if category == 'TOTAL EMIGRANTS':
        fig = px.line(
            df_sex_no_ratio,
            x='YEAR',
            y=['TOTAL']
        )

    if category == 'SEX':
        fig = px.line(
            df_sex_no_ratio,
            x='YEAR',
            y=['MALE', 'FEMALE'])

    if category == 'MAJOR OCCUPATION':
        fig = px.line(
            df3,
            x='YEAR',
            y=df3.columns[1:-1])

    if category == 'CIVIL STATUS':
        fig = px.line(
            df_civil_status,
            x='YEAR',
            y=['Single', 'Married', 'Widower', 'Separated', 'Divorced'])

    if category == 'EDUCATION':
        fig = px.line(
            df4,
            x='YEAR',
            y=df4.columns[1:-1])

    if category == 'AGE GROUP':
        fig = px.line(
            df5,
            x='YEAR',
            y=df5.columns[1:-1])

    return fig


@app.callback(
    Output('pie_sex', "figure"),
    Input('date_selected', "value"))
def display_pie_sex(date_selected):
    year = float(date_selected)
    filtered_data = df_sex_no_ratio.loc[df_sex_no_ratio['YEAR'] == year].drop(
        columns=['YEAR', 'TOTAL'])

    fig = px.pie(
        names=['MALE', 'FEMALE'],
        labels=['Male', 'Female'],
        values=filtered_data.values.flatten().tolist(),
        hole=0.3,
    )

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
        y='MAJOR OCCUPATION GROUP',
        x=year,
        orientation='h')

    fig.update_layout(
        paper_bgcolor="#032047",
        plot_bgcolor="#032047",
        font_color="#E6E6E6",
        yaxis={'categoryorder': 'total ascending'},
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
    year = int(date_selected)

    df = df_civil_status
    df = df.drop(columns=["TOTAL"]).T.reset_index()
    df = df.rename(columns=df.iloc[0]).drop(df.index[0])

    fig = px.bar(
        df,
        y=year,
        x=['Single', 'Married', 'Widower', 'Separated', 'Divorced', 'Not Reported'])

    fig.update_layout(
        paper_bgcolor="#032047",
        plot_bgcolor="#032047",
        font_color="#E6E6E6",
        xaxis_title="CIVIL STATUS",
        xaxis={'categoryorder': 'total descending'},
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
    Output('bar_educ', "figure"),
    Input('date_selected', "value"))
def display_bar_educ(date_selected):
    year = int(date_selected)
    fig = px.bar(
        df_education,
        x=year,
        y='EDUCATIONAL ATTAINMENT',
        orientation='h')

    fig.update_layout(
        paper_bgcolor="#032047",
        plot_bgcolor="#032047",
        font_color="#E6E6E6",
        yaxis={'categoryorder': 'total ascending'},
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
    Output('bar_age', "figure"),
    Input('date_selected', "value"))
def display_bar_educ(date_selected):
    year = str(date_selected)
    fig = px.bar(
        df_age,
        y=year,
        x='AGE GROUP',)

    fig.update_layout(
        paper_bgcolor="#032047",
        plot_bgcolor="#032047",
        font_color="#E6E6E6",
        xaxis={'categoryorder': 'total descending'},
        margin=dict(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=4
        ),
        height=300)

    return fig


if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run_server(debug=False, host="0.0.0.0", port=port)
