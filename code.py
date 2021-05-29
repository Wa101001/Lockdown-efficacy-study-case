import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CERULEAN],
)
df = pd.read_excel("owid-covid-data.xlsx", parse_dates=True, index_col="date")
df.fillna(0)
cols = [
    "date",
    "total_cases",
    "total_deaths",
    "new_cases",
    "new_deaths",
]
num=df._get_numeric_data()
num[num < 0]=0
# sweden dataset
df_sw = df.loc[df["location"] == "Sweden"]
df_sw = df_sw.reindex(columns=cols)
# UAE dataset
df_AE = df.loc[df["location"] == "United Arab Emirates"]
df_AE = df_AE.reindex(columns=cols)
#---statistics----

#max cases
maxc_sw=df_sw['new_cases'].max()
print("Maximum cases in one day Sweden:",maxc_sw)
print('\n')
maxc_AE=df_AE['new_cases'].max()
print("Maximum cases in one day UAE:",maxc_AE)
print('\n')
#max deaths
maxd_sw=df_sw['new_deaths'].max()
print("Maximum new deaths in one day Sweden :",maxd_sw)
print('\n')
maxd_AE=df_AE['new_deaths'].max()
print("Maximum new deaths in one day UAE :",maxd_AE)
print('\n')


# Average cases
meanc_sw=df_sw['new_cases'].resample('M').mean()
meanc_AE=df_AE['new_cases'].resample('M').mean()
print('Average cases per month for Sweden',meanc_sw)
print('\n')
print('Average cases per month for UAE',meanc_AE)
print('\n')

# Average deaths
meand_sw=df_sw['new_deaths'].resample('M').mean()
print('Average deaths per month for Sweden :',meand_sw)
print('\n')
meand_AE=df_AE['new_deaths'].resample('M').mean()
print('Average  deaths per month for UAE',meand_AE)
print('\n')
total_cases_sweden=df_sw['new_cases'].sum()
print('total cases Sweden : ',total_cases_sweden)
print('\n')
total_cases_UAE=df_AE['new_cases'].sum()
print('total cases UAE: ',total_cases_UAE)
print('\n')
total_deaths_sweden=df_sw['new_deaths'].sum()
print('total deaths Sweden',total_deaths_sweden)
print('\n')
total_deaths_AE=df_AE['new_deaths'].sum()
print("total deaths UAE",total_deaths_AE)




# dashboard
options = {
    "new_cases": "New Cases",
    "new_deaths": "New Deaths",
    "total_cases": "Total Cases",
    "total_deaths": "Total Deaths"
}
app.layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.H3("COVID-19 comparaison between Sweden and UAE"),
                width={"size": 8, "offset": 3},
            ),
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(html.H5("SWEDEN SECTION"), width={"size": 4, "offset": 1},),
                dbc.Col(html.H5("UAE SECTION"), width={"size": 4, "offset": 2},),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="UAE",
                        placeholder="Choose the statistics",
                        options=[{"label": v, "value": k} for k, v in options.items()],
                    ),
                    width={"size": 4, "offset": 2, "order": 2},
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="Sweden",
                        placeholder="Choose the statistics",
                        options=[{"label": v, "value": k} for k, v in options.items()],
                    ),
                    width={"size": 4, "offset": 1, "order": 1},
                ),
            ],
            no_gutters=True,
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="sw_line", figure={}),
                    width=8,
                    lg={"size": 6, "offset": 0, "order": "first"},
                ),
                dbc.Col(
                    dcc.Graph(id="uae_line", figure={}),
                    width=4,
                    lg={"size": 6, "offset": 0, "order": "last"},
                ),
            ]
            ),
        dbc.Row([
            html.Br()
            ]),
        dbc.Row(
            [
            dbc.Col(
               dcc.Markdown('''
                * Total cases : 1 068 473
                * Total deaths : 14 451 
                * Maximum cases in a day : 324 850
                * Maximum deaths in a day : 474
                * Mortality rate : 1.352%
                 
                  ''') 
                  , width={"size": 4, "offset": 1},
                ),
            dbc.Col(
               dcc.Markdown('''
                * Total cases : 565 451
                * Total deaths : 1 668
                * Maximum cases in a day :  3977
                * Maximum deaths in a day : 20
                * Mortality rate : 0.358%
                  
                  ''') 
                  , width={"size": 4, "offset": 2},
                )
               
                  ],
                 ),
          
        
    
    ]
)


@app.callback(
    [Output("sw_line", "figure"), Output("uae_line", "figure")],
    [Input("Sweden", "value"), Input("UAE", "value")],
)
def build_graph(Sweden, UAE):
    return (
        px.line(df_sw, y=Sweden, title=options[Sweden]),
        px.line(df_AE, y=UAE, title=options[UAE]),
    )


if __name__ == "__main__":
    app.run_server()






