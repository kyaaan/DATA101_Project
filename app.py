import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import geopandas as gpd
import numpy as np

from dash import Dash, html, dcc, Input, Output, State
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
    ],
    style = CONTENT_BODY_STYLE
)

references_modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("References")),
        dbc.ModalBody(dcc.Markdown("""
            Acemoneytransfer. (n.d.). 10 things every overseas Filipino worker in Germany must know in 2024. Retrieved from https://acemoneytransfer.com/blog/10-things-every-overseas-filipino-worker-in-germany-must-know-in-2024

            Acemoneytransfer. (n.d.). Top 10 job fields for Filipinos in Italy: Everything to know. Retrieved from https://acemoneytransfer.com/blog/top-10-job-fields-for-filipinos-in-italy-everything-to-know

            Archium Ateneo. (n.d.). Faculty publications on Korean studies. Retrieved from https://archium.ateneo.edu/cgi/viewcontent.cgi?article=1003&context=korean-stud-faculty-pubs

            CANAM Group. (2024, January 24). The United States of America is considered to be a land of opportunities. CANAM Group. Retrieved November 26, 2024, from https://www.canamgroup.com/blog/the-united-states-of-america-is-considered-to-be-a-land-of-opportunities#:~:text=The%20United%20States%20of%20America,vast%20landscapes%2C%20attracting%20souls%20worldwide

            CIFAL Philippines. (2018). Korean migration to the Philippines. Retrieved from https://cifal.up.edu.ph/wp-content/uploads/2018/07/Korean-Migration-to-PH-09182018.pdf

            Commission on Filipinos Overseas (CFO). (2024). To a better life: Filipino migration through the years. Commission on Filipinos Overseas. Retrieved November 26, 2024, from https://cfo.gov.ph/to-a-better-life-filipino-migration-through-the-years/

            Distance From To. (n.d.). Distance from South Korea to the Philippines. Retrieved from https://www.distancefromto.net/distance-from-south-korea-to-philippines

            Econstor. (2024). Overseas Filipino workers and their remittances: New evidence on migration and development. Retrieved November 26, 2024, from https://www.econstor.eu/bitstream/10419/284616/1/pidsdps2317.pdf

            Educatly. (n.d.). Top 20 most in-demand jobs in Spain. Retrieved from https://www.educatly.com/blog/343/top-20-most-in-demand-jobs-in-spain

            Figure NZ. (n.d.). Industry statistics in New Zealand. Retrieved from https://figure.nz/chart/WRpSmBftC60lEu2q

            Globaledge. (n.d.). Germany country overview. Retrieved from https://globaledge.msu.edu/countries/germany#:~:text=Germany%20is%20a%20country%20located,Sea%2C%20and%20the%20Baltic%20Sea

            Ipass Processing. (n.d.). The ultimate guide: Top 10 in-demand jobs in Canada by 2024. Retrieved from https://ipassprocessing.com/the-ultimate-guide-top-10-in-demand-jobs-in-canada-by-2024/

            Korean Culture and Information Service. (n.d.). Korean culture and the arts. Retrieved from https://www.koreanculture.org/korea-information-culture-and-the-arts

            Migration Policy Institute. (2024). The Philippines and migration: The next generation of OFWs. Migration Policy Institute. Retrieved November 26, 2024, from https://www.migrationpolicy.org/article/philippines-migration-next-generation-ofws

            Migration Workers Office. (n.d.). MWO Madrid, Spain. Retrieved from https://migrantworkersoffice.com/mwo-madrid-spain/

            Nationwide Visas. (n.d.). Average salary in Germany. Retrieved from https://www.nationwidevisas.com/germany-immigration/average-salary-in-germany/

            Philippine Go. (2024, July 27). 25,000 job opportunities in Japan await Filipinos. Retrieved from https://filipinotimes.net/latest-news/2024/07/27/25000-job-opportunities-in-japan-await-filipinos-dmw/

            Philippine Institute for Development Studies (PIDS). (2024). Migrant workers and their families: Challenges and opportunities. Philippine Institute for Development Studies. Retrieved November 26, 2024, from https://serp-p.pids.gov.ph/feature/public/index-view?feauredtype_id=1&slug=migrant-workers-and-their-families#:~:text=OFWs%20face%20numerous%20challenges%2C%20including,workers%20in%20the%20Middle%20East

            Placement International. (n.d.). Why is Spain a good destination for Filipino professionals? Retrieved from https://placement-international.com/blog/why-is-spain-a-good-destination-for-filipino-professionals

            POEA Online. (n.d.). Filipino jobs in South Korea. Retrieved from https://poeaonline.com/filipino-jobs-south-korea/

            POEA Online. (n.d.). Search DMW jobs in South Korea. Retrieved from https://poeaonline.com/search-dmw-jobs-south-korea/

            PSS Removals. (n.d.). New Zealand's most in-demand jobs. Retrieved from https://www.pssremovals.com/blog/new-zealand-most-in-demand-jobs

            Remote. (n.d.). New Zealand employee benefits and compensation. Retrieved from https://remote.com/blog/new-zealand-employee-benefits-compensation

            ResumeCoach. (n.d.). Jobs in demand in the USA. Retrieved November 26, 2024, from https://www.resumecoach.com/jobs-in-demand-usa/

            Signal Hire. (n.d.). 10 in-demand jobs in the UK in 2024. Retrieved from https://www.signalhire.com/blog/10-in-demand-jobs-in-the-uk-in-2024/

            Spain Info. (n.d.). Facts about Spain: Geography and landscape. Retrieved from https://www.spain.info/en/discover-spain/facts-spain-geography-landscape/#:~:text=Where%20is%20Spain%3F,also%20has%20two%20large%20archipelagos

            Stats NZ. (n.d.). Industries in New Zealand. Retrieved from https://www.stats.govt.nz/topics/industries

            The Canada Guide. (n.d.). What is Canada known for? Retrieved from https://travel2next.com/what-is-canada-known-for/

            The Travelobiz. (n.d.). UK shortage occupation list jobs for skilled worker visas. Retrieved from https://travelobiz.com/uk-shortage-occupation-list-jobs-requirements-for-skilled-worker-visa/

            Trade.gov. (n.d.). New Zealand market overview. Retrieved from https://www.trade.gov/country-commercial-guides/new-zealand-market-overview#:~:text=The%20foundation%20of%20New%20Zealand's,totaled%20approximately%20US%2413%20billion

            UIS Australia. (2024, May 12). 5 top reasons to work in Australia. UIS Australia. Retrieved November 26, 2024, from https://www.uisaustralia.com/blog/5-top-reasons-to-work-in-australia/

            Victoria University. (n.d.). The 10 most in-demand jobs in Australia right now. Victoria University. Retrieved November 26, 2024, from https://www.vu.edu.au/about-vu/news-events/study-space/the-10-most-in-demand-jobs-in-australia-right-now

            Webapps. (n.d.). Germany work permits and immigration. Retrieved from https://www.germany-visa.org/immigration/working-germany-getting-german-work-permit/
        """), style={
            "white-space": "pre-wrap",
            "text-align": "justify",
            "overflow-wrap": "break-word",
            "word-wrap": "break-word",
            "word-break": "break-word"
        }),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-references", className="ml-auto")
        )
    ], id="references-modal", is_open=False, size="lg", style={"max-width": "100%"})
])

rationale_modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Rationale and Purpose of this Website")),
        dbc.ModalBody(dcc.Markdown("""
            **Rationale:**
            Migration has long been a part of the Philippines' history and is deeply embedded in Filipino culture. Overseas Filipino Workers (OFWs) have been celebrated by the Philippine government as “New Heroes” (Uy-Tioco, 2007) for their significant contributions to the nation’s economy and society. According to Opiniano and Ang (2024), the enactment of the 1974 Labor Code (Presidential Decree 442) marked a turning point in the country's migration history, introducing measures to regulate and promote labor migration. Since then, emigration has played a crucial role in driving economic growth, with millions of Filipino workers remitting billions of dollars annually. This continuous flow of remittances has created a feedback loop, where emigration fuels national development, making overseas migration increasingly appealing.

            Today, an estimated 10 million Filipino emigrants (Opiniano and Ang, 2024) are spread across more than 200 countries, working in a wide range of occupations and skill levels (United Nations, n.d.). Despite these successes, OFWs face numerous challenges. Before migrating, many encounter issues such as illegal recruitment and contract substitution. Once abroad, they may endure excessive work hours, maltreatment from employers, particularly among migrant domestic workers, and other labor-related abuses (Yap, 2024). These problems are not new; challenges such as illegal placement fees, irregular migration (often referred to as "tago nang tago" or "TNT"), long working hours, and lack of rest days for domestic workers have persisted since the 1970s (Ramon et al., 2023). Addressing these longstanding issues remains critical to improving the welfare of OFWs and ensuring that migration continues to be a positive force for both workers and the nation.

            **Purpose:**
            This website is designed to help Filipinos make informed decisions about migrating to different countries. It provides essential details about each destination, including a brief description of the country’s cultural, social, and economic environment. It highlights what makes the destination attractive or challenging for Filipinos, along with information about its geographical location to help users understand how far it is from the Philippines. The site also includes details about available jobs, such as in-demand roles for Filipinos in industries like healthcare, IT, construction, or domestic work. Salary expectations are clearly outlined, showing the average salary ranges for common migrant jobs. Additionally, the website provides information on benefits, such as healthcare, paid leave, housing allowances, and educational opportunities for dependents. Finally, it lists the requirements for migration, including visa types, work permits, educational qualifications, language requirements, and any specific certifications needed.
        """), style={
            "white-space": "pre-wrap",
            "text-align": "justify",
            "overflow-wrap": "break-word",
            "word-wrap": "break-word",
            "word-break": "break-word"
        }),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-rationale", className="ml-auto")
        )
    ], id="rationale-modal", is_open=False, size="lg", style={"max-width": "100%"})
])



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

intro = dcc.Markdown("""
## WELCOME!

Migration has been deeply woven into the fabric of the Philippines' history, profoundly influencing Filipino culture. This website offers an insightful look into the destinations where Filipinos migrate and provides detailed information about each country.

Click on a country on the map to view more details. Use the slider below the map to explore emigration patterns over time.

We hope this platform helps you in making informed decisions about migration!
""", style={'text-align': 'justify', 'color': 'white', 'padding': '1em'})


side = html.Div([
    intro,
    dbc.Card(id='geninfo_destination_card', children=[
        dbc.CardBody([
            html.H4('General Information'),
            html.H4("Select a country to see details", style={'text-align': 'center', 'color': '#E6E6E6', 'margin-top': 10}),
        ])
    ], style=CARD_STYLE2),
    html.Div([
        dbc.Button("References", id="open-references", color="primary", style={"width": "100%", "margin-top": "1rem"}),
        dbc.Button("Rationale and Purpose", id="open-rationale", color="primary", style={"width": "100%", "margin-top": "1rem"})
    ], style={'padding': '1rem'})
], style=SIDE_STYLE)


content = html.Div([center, side], className="d-flex align-items-stretch")

rationale_modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Rationale and Purpose of this Website")),
        dbc.ModalBody(dcc.Markdown("""
            This website aims to provide detailed information on migration destinations for Filipinos. It offers insights into the countries where Filipinos migrate, including job opportunities, living conditions, and cultural aspects. The goal is to help Filipinos make informed decisions about migration and prepare them for their new life abroad. By providing comprehensive data and resources, we strive to support the Filipino community in achieving a better future through migration.
        """), style={
            "white-space": "pre-wrap",
            "text-align": "justify",
            "overflow-wrap": "break-word",
            "word-wrap": "break-word",
            "word-break": "break-word"
        }),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-rationale", className="ml-auto")
        )
    ], id="rationale-modal", is_open=False, size="lg", style={"max-width": "100%"})
])

app.layout = html.Div([
    sidebar, 
    content, 
    body_content,
    references_modal
])

@app.callback(
    Output("references-modal", "is_open"),
    [Input("open-references", "n_clicks"), Input("close-references", "n_clicks")],
    [State("references-modal", "is_open")],
)
def toggle_references_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("rationale-modal", "is_open"),
    [Input("open-rationale", "n_clicks"), Input("close-rationale", "n_clicks")],
    [State("rationale-modal", "is_open")],
)
def toggle_rationale_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


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
