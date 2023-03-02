import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash_table
from dash_table import DataTable
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

data = pd.read_csv('archive/players_22.csv')

#Dataset Processing
#data cleaning
nonusefulcolumns = ['sofifa_id','player_url','long_name','league_rank']
nonusefulattributes = data.loc[:,'player_traits':]

df = data.copy()
df = df[df['player_positions'] != 'GK'] #filtering all the goalkeepers
df1 = df[df['age'] > 25] #players over 25 dataset
df2 = df[df['age'] <= 25] #players under 25 dataset

#Variables lists for comparision
player_skills = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
player_info = ['short_name','nationality', 'club_name', 'age', 'height_cm', 'weight_kg']
labels = ['Player', 'Nationality', 'Club', 'Age', 'Height(cm)', 'Weight(kg)']
skills=['skill_curve','skill_dribbling','skill_fk_accuracy','skill_ball_control','skill_long_passing']
player_1 = 'Kevin De Bruyne'
player_2 = 'Erling Braut Haaland'

# choice of the players
players_over_25 = []
for i in df1.index:
    players_over_25.append({'label': df1['long_name'][i], 'value': df1['long_name'][i]})

players_under_25 = []
for i in df2.index:
    players_under_25.append({'label': df2['long_name'][i], 'value':  df2['long_name'][i]})

dropdown_lists_player_over_25 = dcc.Dropdown(
        id='player_1',
        options=players_over_25,
        value='Kevin De Bruyne'
    )

dropdown_lists_player_under_25 = dcc.Dropdown(
        id='player_2',
        options=players_under_25,
        value='Erling Braut Haaland'
    )

dashtable_player_over_25 = dash_table.DataTable(
        id='table_1',
        data=df[df['long_name'] == player_1].to_dict('records'),
        columns=[{"name": col, "id": player_info[idx]} for (idx, col) in enumerate(labels)],
        style_cell={'textAlign': 'left',
                    'font_size': '14px'},
        style_header={
            'backgroundColor': 'rgb(0,200,255)',
            'fontWeight': 'bold'
        }
    )

dashtable_player_under_25 = dash_table.DataTable(
        id='table_2',
        data=df[df['long_name'] == player_2].to_dict('records'),
        columns=[{"name": col, "id": player_info[::-1][idx]} for (idx, col) in enumerate(labels[::-1])],
        style_cell={'textAlign': 'right',
            'font_size': '14px'},
        style_header={
            'backgroundColor': 'rgb(157,255,0)',
            'fontWeight': 'bold'
        }
    )

data.drop(nonusefulcolumns, axis=1, inplace=True)
data.drop(nonusefulattributes, axis=1, inplace=True)
data['is_over_25'] = data['age'] > 25
data['is_over_25_text']=data['is_over_25'].map(lambda x: "Over 25" if x else "Under 25")

options = [{'label': 'Overall', 'value': 'overall'},
           {'label': 'Potential', 'value': 'potential'},
           {'label': 'Value', 'value': 'value_eur'},
           {'label': 'Wage', 'value': 'wage_eur'},
           {'label': 'Height', 'value': 'height_cm'},
           {'label': 'Weight', 'value': 'weight_kg'},
           {'label': 'Pace', 'value': 'pace'},
           {'label': 'Shooting', 'value': 'shooting'},
           {'label': 'Passing', 'value': 'passing'},
           {'label': 'Dribbling', 'value': 'dribbling'},
           {'label': 'Defending', 'value': 'defending'},
           {'label': 'Physic', 'value': 'physic'}]

top_leagues = ['Spain Primera Division', 'Italian Serie A', 'German 1. Bundesliga', 'French Ligue 1', 'English Premier League',
                'Portuguese Liga ZON SAGRES', 'Belgian Jupiler Pro League', 'Holland Eredivisie', 'Russian Premier League']

leagues_dict = [{'label':'Premier League', 'value':'English Premier League'},          
        {'label':'Bundesliga', 'value':'German 1. Bundesliga'},
        {'label':'Serie A', 'value':'Italian Serie A'},
        {'label':'Liga ZON SAGRES', 'value':'Portuguese Liga ZON SAGRES'},
        {'label':'La Liga', 'value':'Spain Primera Division'},
        {'label':'Ligue 1', 'value':'French Ligue 1'},
        {'label':'Jupiler Pro League', 'value':'Belgian Jupiler Pro League'},
        {'label':'Eredivisie', 'value':'Holland Eredivisie'},
        {'label':'Russian Premier League', 'value':'Russian Premier League'}]

skills_dict = [{'label': 'Overall', 'value': 'overall'},
            {'label': 'Potential', 'value': 'potential'},
            {'label': 'Value', 'value': 'value_eur'},
            {'label': 'Wage', 'value': 'wage_eur'},
            {'label': 'Height', 'value': 'height_cm'},
            {'label': 'Weight', 'value': 'weight_kg'},
            {'label': 'Pace', 'value': 'pace'},
            {'label': 'Shooting', 'value': 'shooting'},
            {'label': 'Passing', 'value': 'passing'},
            {'label': 'Dribbling', 'value': 'dribbling'},
            {'label': 'Defending', 'value': 'defending'},
            {'label': 'Physic', 'value': 'physic'}]

first_skills_dropdown = dcc.Dropdown(id='first_skills_dropdown', options=options, value='overall')
second_skills_dropdown = dcc.Dropdown(id='second_skills_dropdown', options=options, value='potential')
third_skills_dropdown = dcc.Dropdown(id='third_skills_dropdown', options=options, value='value_eur')
club_lists_dropdown = dcc.Dropdown(id='club_lists_dropdown', options=leagues_dict, value='English Premier League')
attribute_x_dropdown = dcc.Dropdown(id='attribute_x_dropdown', options=skills_dict, value='value_eur')
attribute_y_dropdown = dcc.Dropdown(id='attribute_y_dropdown', options=skills_dict, value='wage_eur')  

players_age_slider = dcc.RangeSlider(
                            id='players_age_slider',
                            min=data['age'].min(),
                            max=data['age'].max(),
                            value=[data['age'].min(), data['age'].max()],
                            step=1,
                            marks={16: '16',
                                20: '20',
                                24: '24',
                                28: '28',
                                32: '32',
                                36: '36',
                                40: '40',
                                44: '44',
                                48: '48',   
                                52: '52'})

#Dashapp layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
navbar = dbc.Navbar([
    html.A(
        dbc.Row([
            dbc.Col(html.Img(src='/assets/fifaa22.png', height="100px"),width=2.6),
            dbc.Col([html.Label("ANALYTICS DASHBOARD",id = "label_1"),
                    html.Label("Created by: Aashraya Pokhrel & Dikesh Shrestha",className = "label_2",style={'margin-bottom':'.5rem'})],width=8)],
            align="between"))])

players_above_25_card = dbc.Card([
    dbc.FormGroup([
        html.Label('Choose a Player Over Age 25:'),
        html.Br(),
        dropdown_lists_player_over_25])],
body=True,
className="players_over_25_card")

players_under_25_card = dbc.Card([
    dbc.FormGroup([
        html.Label('Choose a Player Under Age 25:'),
        html.Br(),
        dropdown_lists_player_under_25])],
body=True,
className="players_under_25_card")

league_card = dbc.Card([
    dbc.FormGroup([
        html.Label('Choose an Attribute:'),
        html.Br(),
        first_skills_dropdown]),

    dbc.FormGroup([
        html.Label('Choose an Attribute:'),
        html.Br(),
        second_skills_dropdown]),

    dbc.FormGroup([
        html.Label('Choose an Attribute:'),
        html.Br(),
        third_skills_dropdown])],
    body=True,
    className="attribute_selection_card")

club_card = dbc.Card([
    dbc.FormGroup([
        html.Label('Choose a League:'),
        html.Br(),
        club_lists_dropdown]),

    dbc.FormGroup([
        html.Label('Choose an attribute for x:'),
        html.Br(),
        attribute_x_dropdown]),

    dbc.FormGroup([
        html.Label('Choose an attribute for y:'),
        html.Br(),
        attribute_y_dropdown])],
    body=True,
    className="attribute_selection_card")

player_over_25_card_deck = dbc.CardDeck([
    dbc.Card(
        dbc.CardBody([
            html.Div("Position", className="card_title_over_25"),
            html.Div(id="Player_over_25_position",className="card_info_over_25")]),
        className='attributes_card_over_25'),
        
    dbc.Card(
        dbc.CardBody([
            html.Div("Value", className="card_title_over_25"),
            html.Div(id="Player_over_25_value",className="card_info_over_25")]),
        className='attributes_card_over_25'),  

    dbc.Card(
        dbc.CardBody([
            html.Div("Skill moves", className="card_title_over_25"),
            html.Div(id="Player_over_25_skill",className="card_info_over_25")]),
        className='attributes_card_over_25'),

    dbc.Card(
        dbc.CardBody([
            html.Div("Prefer foot", className="card_title_over_25"),
            html.Div(id="Player_over_25_foot",className="card_info_over_25")]),
        className='attributes_card_over_25')])

player_under_25_card_deck = dbc.CardDeck([
    dbc.Card(
        dbc.CardBody([
            html.Div("Prefer foot", className="card_title_under_25"),
            html.Div(id="Player_under_25_foot",className="card_info_under_25")]),
        className='attributes_card_under_25'), 

    dbc.Card(
        dbc.CardBody([
            html.Div("Skill moves", className="card_title_under_25"),
            html.Div(id="Player_under_25_skill",className="card_info_under_25")]),
        className='attributes_card_under_25'), 

    dbc.Card(
        dbc.CardBody([
            html.Div("Value", className="card_title_under_25"),
            html.Div(id="Player_under_25_value",className="card_info_under_25")]),
        className='attributes_card_under_25'), 

    dbc.Card(
        dbc.CardBody([
            html.Div("Position", className="card_title_under_25"),
            html.Div(id="Player_under_25_position",className="card_info_under_25")]),
        className='attributes_card_under_25')])

over_25_plot_card_deck = dbc.CardDeck([
    dbc.Card(
        dbc.CardBody([
            html.Div("Potential", className="card_title_over_25"),
            dcc.Graph(id='range_meter_over_25')]),
        className='attributes_card_over_25'),

    dbc.Card(
        dbc.CardBody([
            html.Div("Skills", className="card_title_over_25"),
            dcc.Graph(id='skills_bar_chart_over_25')]),
        className='attributes_card_over_25')])

under_25_plot_card_deck = dbc.CardDeck([
    dbc.Card(
        dbc.CardBody([
            html.Div("Skills", className="card_title_under_25"),
            dcc.Graph(id='skills_bar_chart_under_25')]),
        className='attributes_card_under_25'), 

        dbc.Card(
            dbc.CardBody([
                html.Div("Potential", className="card_title_under_25"),
                dcc.Graph(id='range_meter_under_25')]),
            className='attributes_card_under_25')])

tab_player_comparison = html.Div([
    dbc.Card(
        dbc.CardBody([

                    html.H1('Player Comparison'),
                    html.Hr(),

                    dbc.Row([
                        dbc.Col([
                            dbc.Row(players_above_25_card),
                            dbc.Row(html.Img(src='/assets/player_o25.png',className="player_img"))
                        ],sm=3),
                        dbc.Col(dcc.Graph(id='scatterpolar_chart'), sm=5, align = 'center'),
                        dbc.Col([
                            dbc.Row(players_under_25_card),
                            dbc.Row(html.Img(src='/assets/player_u25.png',className="player_img"))
                        ],sm=3),
                    ],justify="between"),

                    dbc.Row([
                        dbc.Col(
                            [dashtable_player_over_25,
                            html.Br(),
                            player_over_25_card_deck,
                            html.Br(),
                            over_25_plot_card_deck],sm=6),
                        dbc.Col(
                            [dashtable_player_under_25,
                            html.Br(),
                            player_under_25_card_deck,
                            html.Br(),
                           under_25_plot_card_deck],sm=6),
                    ]),
                ]
            )
        )
    ]
),




tab_league_analysis = html.Div(
    [
        dbc.Card(    
            dbc.CardBody(
                [
                    html.H1("League Analysis"),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(league_card,sm=3),

                            dbc.Col(
                                dcc.Graph(id='league_attribute_bar_plot_1',className="league_analysis_bar_plot"),sm=3
                                ),

                            dbc.Col(
                                dcc.Graph(id='league_attribute_bar_plot_2',className="league_analysis_bar_plot"),sm=3
                                ),

                            dbc.Col(
                                dcc.Graph(id='league_attribute_bar_plot_3',className="league_analysis_bar_plot"),sm=3
                                ),
                        ],
                        align="center",
                    ),
                    
                    dbc.Row([
                        dbc.Label("Select Age:", style={'margin-left' : '5%', 'font-size': '20px'}),
                        dbc.Col(players_age_slider,align = "center")
                    ]),
                ]
            ),
        ),
        html.Br(),
        dbc.Card(    
            dbc.CardBody(
                [
                    html.H1("Club Analysis"),
                    html.Hr(),  
                    dbc.Row(
                        [
                        dbc.Col(club_card,sm=2),

                        dbc.Col(
                            dcc.Graph(id='scatter_plot',className="league_analysis_bar_plot"),sm=5
                        ),
                        dbc.Col(
                            dcc.Graph(id='side_comparison_bar_chart',className="league_analysis_bar_plot"),sm=5
                        )
                        ],
                        align="center",
                    ),     
                ]
            ),
            className=" mt-3"
        )
    ]
)    

app.layout = dbc.Container([
    
        navbar,

        dbc.Tabs(
            [
                dbc.Tab(tab_player_comparison, label="Players Comparison"),
                dbc.Tab(tab_league_analysis, label="League & Club Analysis"),
            ], 
        ),
    ],
    fluid=True,
)


@app.callback(
    [Output(component_id='league_attribute_bar_plot_1', component_property='figure'),
     Output(component_id='league_attribute_bar_plot_2', component_property='figure'),
     Output(component_id='league_attribute_bar_plot_3', component_property='figure')],
     
    [Input(component_id='first_skills_dropdown', component_property='value'),
     Input(component_id='second_skills_dropdown', component_property='value'),
     Input(component_id='third_skills_dropdown', component_property='value'), 
     Input(component_id="players_age_slider", component_property="value")]
)

#BARPLOT
def league_analysis_plots(first_attribute_value, second_attribute_value, third_attribute_value, age):

    filter_by_age_data = data[(data['age'] >= age[0]) & (data['age'] <= age[1])]

    first_attribute_bar_data = dict(
        type='bar',
        y=filter_by_age_data.groupby('league_name').median()[first_attribute_value].sort_values(ascending=False).head(5),
        x=filter_by_age_data['league_name'].unique()
    )

    second_attribute_bar_data = dict(
        type='bar',
        y=filter_by_age_data.groupby('league_name').median()[second_attribute_value].sort_values(ascending=False).head(5),
        x=filter_by_age_data['league_name'].unique()
    )

    third_attribute_bar_data = dict(
        type='bar',
        y=filter_by_age_data.groupby('league_name').median()[third_attribute_value].sort_values(ascending=False).head(5),
        x=filter_by_age_data['league_name'].unique()
    ),

    first_attribute_bar_layout = dict(xaxis=dict(title='Leagues', tickangle=45))
    second_attribute_bar_layout = dict(xaxis=dict(title='Leagues',tickangle=45))
    third_attribute_bar_layout = dict(xaxis=dict(title='Leagues',tickangle=45))

    first_attribute_bar_plot = go.Figure(data = first_attribute_bar_data, layout=first_attribute_bar_layout)
    first_attribute_bar_plot.update_traces(marker_color='rgb(0,200,255)', marker_line_color='rgb(160,252,4)', marker_line_width=1.0, opacity=1.0)
    first_attribute_bar_plot.update_layout(title_text=first_attribute_value.capitalize(),
                                            title_x=0.5,
                                            margin=dict(l=70, r=40, t=60, b=40),
                                            plot_bgcolor = 'rgba(0, 0, 0, 0)',
                                            paper_bgcolor = 'rgba(0, 0, 0, 0)',
                                            xaxis = dict(gridcolor= "#e5e6dc",gridwidth= 0.5),
                                            yaxis = dict(gridcolor= "#e5e6dc",gridwidth= 0.5))
    
    second_attribute_bar_plot = go.Figure(data=second_attribute_bar_data, layout=second_attribute_bar_layout)
    second_attribute_bar_plot.update_traces(marker_color='rgb(160,252,4)', marker_line_color='rgb(0,200,255)', marker_line_width=0.8, opacity=0.9)
    second_attribute_bar_plot.update_layout(title_text=second_attribute_value.capitalize(),title_x=0.5,
                                            margin=dict(l=70, r=40, t=60, b=40),
                                            plot_bgcolor = 'rgba(0, 0, 0, 0)',
                                            paper_bgcolor = 'rgba(0, 0, 0, 0)',
                                            xaxis = dict(gridcolor= "#e5e6dc",gridwidth= 0.5),
                                            yaxis = dict(gridcolor= "#e5e6dc",gridwidth= 0.5))

    third_attribute_bar_plot = go.Figure(data=third_attribute_bar_data, layout=third_attribute_bar_layout)
    third_attribute_bar_plot.update_traces(marker_color='rgb(80, 226, 130)', marker_line_color='rgb(138, 236, 171)', marker_line_width=0.8, opacity=0.9)
    third_attribute_bar_plot.update_layout(title_text=third_attribute_value.capitalize(),title_x=0.5,
                                            margin=dict(l=70, r=40, t=60, b=40),
                                            plot_bgcolor = 'rgba(0, 0, 0, 0)',
                                            paper_bgcolor = 'rgba(0, 0, 0, 0)',
                                            xaxis = dict(gridcolor= "#e5e6dc",gridwidth= 0.5),
                                            yaxis = dict(gridcolor= "#e5e6dc",gridwidth= 0.5))

    return first_attribute_bar_plot,second_attribute_bar_plot, third_attribute_bar_plot
           
@app.callback(
    [Output(component_id='scatter_plot', component_property='figure'),
     Output(component_id='side_comparison_bar_chart', component_property='figure')],
    [Input(component_id='club_lists_dropdown', component_property='value'),
    Input(component_id='attribute_x_dropdown', component_property='value'),
    Input(component_id='attribute_y_dropdown', component_property='value')]
)

def club_analysis_plots(league,x_attribute,y_attribute):

    scatter_plot_df = data[data['league_name'] == league].sort_values('overall',ascending = False).head(100)
    scatter_plot_fig = px.scatter(data_frame  = scatter_plot_df, x=x_attribute, y=y_attribute,color="is_over_25_text",
                        color_discrete_sequence=['rgb(0,200,255)','rgb(160,252,4)'], hover_name ='short_name',
                        hover_data={"is_over_25_text":False,'age':True,'club_name':True,'overall':True,'potential':True,'player_positions':True},
                        title = ('Top 100 players with highest overall rating in '+league))    
    scatter_plot_fig.update_layout(
        title = dict(font = dict(size =16)),
        legend=dict(title = dict(text ="Age of players"),
                    orientation="h",
                    yanchor="bottom",
                    y=1,
                    xanchor="right",
                    x=1),
        margin=dict(l=70, r=30, t=100, b=70),
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        xaxis = dict(gridcolor= "#e5e6dc",gridwidth= 0.5),
        yaxis = dict(gridcolor= "#e5e6dc",gridwidth= 0.5)
    )  
    scatter_plot_fig.update_traces(marker=dict(size=10, line=dict(width=1.5, color='rgb(149, 139, 114)')))

    # Bar plot
    bar_plot_df = data[data['league_name'] == league].groupby(['club_name','is_over_25']).count()['short_name'].reset_index()
    bar_plot_df = pd.pivot_table(bar_plot_df, values='short_name', index=['club_name'], columns=['is_over_25'], aggfunc=np.sum).reset_index()
    x = bar_plot_df['club_name']
    y = bar_plot_df.iloc[:,-2:].div(bar_plot_df.iloc[:,-2:].sum(axis=1), axis=0)
    bar_plot_fig = go.Figure()
    bar_plot_fig.add_traces(go.Bar(y=x,x=y[True],name='Over 25',orientation='h', marker=dict(color='rgb(0,200,255)',line=dict(color='rgb(149, 139, 114)', width=1.0))))
    bar_plot_fig.add_traces(go.Bar(y=x,x=y[False],name='Under 25',orientation='h', marker=dict(color='rgb(160,252,4)',line=dict(color='rgb(149, 139, 114)', width=1.0))))

    bar_plot_fig.update_yaxes(tickfont = dict(size=10))
    bar_plot_fig.update_layout(barmode='stack', title = dict(text ='Players over 25 and under 25 years old by club',font = dict(size =14)),
                        plot_bgcolor = 'rgba(0, 0, 0, 0)',
                        paper_bgcolor = 'rgba(0, 0, 0, 0)',    
                        legend=dict(title = dict(text ="Age of players"),orientation="h",yanchor="bottom",y=1,xanchor="right",x=1),
                        margin=dict(r=30, t=100, b=70),)
    return scatter_plot_fig,bar_plot_fig



@app.callback(
    [   
        Output('scatterpolar_chart', 'figure'),
        Output('table_1', 'data'),
        Output('range_meter_over_25', 'figure'),
        Output('skills_bar_chart_over_25', 'figure'),
        Output('table_2', 'data'),
        Output('range_meter_under_25', 'figure'),
        Output('skills_bar_chart_under_25', 'figure'),
        Output("Player_over_25_position","children"),
        Output("Player_over_25_value",'children'),
        Output("Player_over_25_skill",'children'),
        Output("Player_over_25_foot",'children'),
        Output("Player_under_25_position","children"),
        Output("Player_under_25_value",'children'),
        Output("Player_under_25_skill",'children'),
        Output("Player_under_25_foot",'children')
    ],
    [
        Input('player_1', 'value'),
        Input('player_2', 'value')
    ]
)

def players_comparison_function(player_1, player_2):
    #Scatterpolar
    player_over_25_plot = pd.DataFrame(df1[df1['long_name'] == player_1][player_skills].iloc[0])
    player_over_25_plot.columns = ['score']
    player_under_25_plot = pd.DataFrame(df2[df2['long_name'] == player_2][player_skills].iloc[0])
    player_under_25_plot.columns = ['score']
    list_scores = [player_over_25_plot.index[i].capitalize() +' = ' + str(player_over_25_plot['score'][i]) for i in range(len(player_over_25_plot))]
    text_scores_1 = player_1
    for i in list_scores:
        text_scores_1 += '<br>' + i

    list_scores = [player_under_25_plot.index[i].capitalize() +' = ' + str(player_under_25_plot['score'][i]) for i in range(len(player_over_25_plot))]
    text_scores_2 = player_2
    for i in list_scores:
        text_scores_2 += '<br>' + i

    scatterpolar_fig = go.Figure(data=go.Scatterpolar(
        r=player_over_25_plot['score'],
        theta=player_over_25_plot.index,
        fill='toself', 
        marker_color = 'rgb(0, 200, 255)', 
        opacity =1, 
        hoverinfo = "text" ,
        name = text_scores_1,
        text  = [player_over_25_plot.index[i] +' = ' + str(player_over_25_plot['score'][i]) for i in range(len(player_over_25_plot))]
    ))
    scatterpolar_fig.add_traces(go.Scatterpolar(
        r=player_under_25_plot['score'],
        theta=player_under_25_plot.index,
        fill='toself',
        marker_color = 'rgb(160, 252, 4)',
        hoverinfo = "text" ,
        name= text_scores_2,
        text  = [player_under_25_plot.index[i] +' = ' + str(player_under_25_plot['score'][i]) for i in range(len(player_under_25_plot))]
    ))

    scatterpolar_fig.update_layout(
        polar=dict(
            hole=0,
            bgcolor="white",
            radialaxis=dict(
                visible=True,
                type='linear',
                autotypenumbers='strict',
                autorange=False,
                range=[0, 100],
                showline=True,
                showticklabels=False, ticks='',
                gridcolor='black'),
                ),
        width = 550,
        height = 550,
        margin=dict(l=80, r=80, t=20, b=20),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        font_color="black",
        font_size= 15
    )


    # table 1
    updated_table_1 = df[df['long_name'] == player_1].to_dict('records')

    # gauge plot 1
    player_over_25_plot = pd.DataFrame(df1[df1['long_name'] == player_1]['potential'])
    player_over_25_plot['name'] = player_1
    gauge_plot_over_25 = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=player_over_25_plot.potential.iloc[0],
        mode="gauge+number",
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "rgb(0, 200, 255)"}}))

    gauge_plot_over_25.update_layout(
        height = 300,
        margin=dict(l=7, r=7, t=40, b=10),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        font_color="black",
        font_size= 15
    )
    # barplot over 25
    player_over_25_plot = pd.DataFrame(df1[df1['long_name'] == player_1][skills].iloc[0].reset_index())
    player_over_25_plot.rename(columns={player_over_25_plot.columns[1]: 'counts'}, inplace=True)
    player_over_25_plot.rename(columns={player_over_25_plot.columns[0]: 'skills'}, inplace=True)
    barplot_over_25 = px.bar(player_over_25_plot, x='skills', y='counts')
    barplot_over_25.update_traces(marker_color='rgb(0, 200, 255)')
    barplot_over_25.update_layout(
        height = 300,
        margin=dict(l=10, r=10, t=20, b=0),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        font_color="black",
        font_size= 10
    )
    barplot_over_25.update_yaxes(range=[0,100])
    # table 2
    updated_table_2 = df[df['long_name'] == player_2].to_dict('records')

    # gauge plot under 25
    player_under_25_plot = pd.DataFrame(df2[df2['long_name'] == player_2]['potential'])
    player_under_25_plot['name'] = player_2
    gauge_plot_under_25 = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=player_under_25_plot.potential.iloc[0],
        mode="gauge+number",
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "rgb(160, 252, 4)"}}))

    gauge_plot_under_25.update_layout(
        height = 300,
        margin=dict(l=7, r=7, t=40, b=10),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        font_color="black",
        font_size= 15
    )
    # bar plot under 25
    player_under_25_plot = pd.DataFrame(df2[df2['long_name'] == player_2][skills].iloc[0].reset_index())
    player_under_25_plot.rename(columns={player_under_25_plot.columns[1]:'counts'}, inplace=True )
    player_under_25_plot.rename(columns={player_under_25_plot.columns[0]:'skills'}, inplace=True )
    barplot_under_25 = px.bar(player_under_25_plot,x='skills',y='counts')
    barplot_under_25.update_traces(marker_color='rgb(160, 252, 4)')
    barplot_under_25.update_layout(
    height = 300,
    margin=dict(l=10, r=10, t=20, b=0),
    showlegend=False,
    template="plotly_dark",
    plot_bgcolor = 'rgba(0, 0, 0, 0)',
    paper_bgcolor = 'rgba(0, 0, 0, 0)',
    font_color="black",
    font_size= 10
    )
    barplot_under_25.update_yaxes(range=[0,100])
    # cards
    player_over_25_pos = df1[df1['long_name'] == player_1]["team_position"]
    player_over_25_value = str(df1[df1['long_name'] == player_1]["value_eur"].values[0] / 1000000) +" M Euro"
    player_over_25_skill = df1[df1['long_name'] == player_1]["skill_moves"]
    player_over_25_foot =  df1[df1['long_name'] == player_1]["preferred_foot"]

    player_under_25_pos = df2[df2['long_name'] == player_2]["team_position"]
    player_under_25_value = str(df2[df2['long_name'] == player_2]["value_eur"].values[0] / 1000000) +" M Euro"
    player_under_25_skill = df2[df2['long_name'] == player_2]["skill_moves"]
    player_under_25_foot =  df2[df2['long_name'] == player_2]["preferred_foot"]

    # outputs
    return scatterpolar_fig, updated_table_1, gauge_plot_over_25, barplot_over_25, updated_table_2, gauge_plot_under_25, barplot_under_25,player_over_25_pos, player_over_25_value, player_over_25_skill, player_over_25_foot, player_under_25_pos, player_under_25_value, player_under_25_skill, player_under_25_foot



if __name__ == '__main__':
    app.run_server(debug=True)

