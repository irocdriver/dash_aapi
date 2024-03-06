import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from sqlalchemy import create_engine
from dash import Dash, html, dcc, callback, Output, Input


engine = create_engine('sqlite:///aapi_dash.db', echo = False)


# if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'

asian_groups_ug = '''
select trim(asian_group) asian_group,
year_term,
trim(semester) semester,
total
from asian_group_counts
'''

pacific_islander_groups_ug = '''
select trim(pacific_islander_group) pacific_islander_group,
year_term,
trim(semester) semester,
total
from pacific_islander_group_counts 
'''

FTF_ASIAN = '''
select trim(asian_group) asian_group,
cohort_year_term,
cohort_semester,
"#ENTERING_COHORT",
retention_1yr,
retention_2yr,
retention_4yr,
retention_6yr
from ftf_asian_rtn
'''

FTF_PACIFIC_ISLANDER =  '''
select trim(pacific_islander_group) pacific_islander_group,
cohort_year_term,
cohort_semester,
"#ENTERING_COHORT",
retention_1yr,
retention_2yr,
retention_4yr,
retention_6yr
from ftf_pi_rtn
'''

TRANSFER_ASIAN =  '''
select trim(asian_group) asian_group,
cohort_year_term,
cohort_semester,
"#ENTERING_COHORT",
retention_1yr,
retention_2yr,
retention_4yr,
retention_6yr from trf_asian_rtn
'''

TRANSFER_PACIFIC_ISLANDER = '''
select trim(pacific_islander_group) pacific_islander_group,
cohort_year_term,
cohort_semester,
"#ENTERING_COHORT",
retention_1yr,
retention_2yr,
retention_4yr,
retention_6yr from tfr_pi_rtn
'''

asian_standing = '''
select trim(asian_group) asian_group,
standing, 
year_term,
semester,
total_enroll,
standing_count,
standing_pct
from asian_standing where total_enroll >= 5
order by 3, 6 desc, 5 desc, 1 
'''

pi_standing = '''
select trim(pacific_islander_group) pacific_islander_group,
standing, 
year_term,
semester,
total_enroll,
standing_count,
standing_pct
from pi_standing where total_enroll >= 5
order by 3, 6 desc, 5 desc, 1 
'''

#enrollment counts
asian_group_counts_ug_frame = pd.read_sql_query(asian_groups_ug, engine)
asian_group_counts_columns = asian_group_counts_ug_frame.transpose().values.tolist()

pacific_islander_group_counts_ug_frame = pd.read_sql_query(pacific_islander_groups_ug, engine)
pacific_islander_group_counts_columns = pacific_islander_group_counts_ug_frame.transpose().values.tolist()

#retention
ftf_asian_frame = pd.read_sql_query(FTF_ASIAN, engine)
ftf_pacific_islander_frame = pd.read_sql_query(FTF_PACIFIC_ISLANDER, engine)
transfer_asian_frame = pd.read_sql_query(TRANSFER_ASIAN, engine)
transfer_pacific_islander_frame = pd.read_sql_query(TRANSFER_PACIFIC_ISLANDER, engine)

ftf_asian_frame.drop(ftf_asian_frame.columns[1], axis = 1, inplace = True)
ftf_pacific_islander_frame.drop(ftf_pacific_islander_frame.columns[1], axis = 1, inplace = True)
transfer_asian_frame.drop(transfer_asian_frame.columns[1], axis = 1, inplace = True)
transfer_pacific_islander_frame.drop(transfer_pacific_islander_frame.columns[1], axis = 1, inplace = True)

ftf_asian_frame.fillna("", inplace = True)
ftf_pacific_islander_frame.fillna("", inplace = True)
transfer_asian_frame.fillna("", inplace = True)
transfer_pacific_islander_frame.fillna("", inplace = True)

ftf_asian_frame.columns = ['Asian Group', 'Cohort Semester', '#Entering Cohort', 'Retention 1Yr', 'Retention 2Yr', 'Retention 4Yr', 'Retention 6Yr']
transfer_asian_frame.columns = ['Asian Group', 'Cohort Semester', '#Entering Cohort', 'Retention 1Yr', 'Retention 2Yr', 'Retention 4Yr', 'Retention 6Yr']
ftf_pacific_islander_frame.columns = ['Pacific Islander Group', 'Cohort Semester', '#Entering Cohort', 'Retention 1Yr', 'Retention 2Yr', 'Retention 4Yr', 'Retention 6Yr']
transfer_pacific_islander_frame.columns = ['Pacific Islander Group', 'Cohort Semester', '#Entering Cohort', 'Retention 1Yr', 'Retention 2Yr', 'Retention 4Yr', 'Retention 6Yr']

ftf_asian_frame_columns = ftf_asian_frame.transpose().values.tolist()
transfer_asian_frame_columns = transfer_asian_frame.transpose().values.tolist()
ftf_pacific_islander_frame_columns = ftf_pacific_islander_frame.transpose().values.tolist()
transfer_pacific_islander_frame_columns = transfer_pacific_islander_frame.transpose().values.tolist()

#standing
asian_standing_frame = pd.read_sql_query(asian_standing, engine)

asian_standing_frame.columns = ['Asian Group', 'Academic Standing', 'Term Code', 'Semester', 'Total Enrollment', 'Standing Total', 'Standing %']

asian_standing_columns =  asian_standing_frame.transpose().values.tolist()


pi_standing_frame = pd.read_sql_query(pi_standing, engine)

pi_standing_frame.columns = ['Pacific Islander Group', 'Academic Standing', 'Term Code', 'Semester', 'Total Enrollment', 'Standing Total', 'Standing %']

pi_standing_columns =  pi_standing_frame.transpose().values.tolist()


app = Dash(__name__)

app.layout = html.Div([
    html.Div(children = 'Student Enrollment by Ethnic Sub-groups: Asian Groups'),
    dcc.Dropdown(options= asian_group_counts_columns[0], value = 'Filipino',  id = 'controls-and-drop', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph'), 
    
    html.Div(children = 'Student Enrollment by Ethnic Sub-groups: Pacific Islander Groups'),
    dcc.Dropdown(options= pacific_islander_group_counts_columns[0], value = 'Other Pac.Islander',  id = 'controls-and-drop_pi', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_pi'),

    html.Div(children = 'Student Enrollment by Ethnic Sub-groups: Asian Groups'),
    dcc.Dropdown(options= asian_group_counts_ug_frame.semester.unique(), value = 'Fall   2019',  id = 'controls-and-drop_pie', placeholder = 'Select semester from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_pie'),

    html.Div(children = 'Student Enrollment by Ethnic Sub-groups: Pacific Islander Groups'),
    dcc.Dropdown(options= pacific_islander_group_counts_ug_frame.semester.unique(), value = 'Fall   2019',  id = 'controls-and-drop_pi_pie', placeholder = 'Select semester from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_pi_pie'),

    #ftf asian
    html.Div(children = 'FTF 1-Year Student Retention by Ethnic Sub-groups: Asian Groups'),
    dcc.Dropdown(options= ftf_asian_frame_columns[0], value = 'Filipino',  id = 'controls-and-drop_rtn_asian', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_asian'),

    html.Div(children = 'FTF 2-Year Student Retention by Ethnic Sub-groups: Asian Groups'),
    dcc.Dropdown(options= ftf_asian_frame_columns[0], value = 'Filipino',  id = 'controls-and-drop_rtn_asian_2', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_asian_2'),

    html.Div(children = 'FTF 4-Year Student Retention by Ethnic Sub-groups: Asian Groups'),
    dcc.Dropdown(options= ftf_asian_frame_columns[0], value = 'Filipino',  id = 'controls-and-drop_rtn_asian_4', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_asian_4'),

    html.Div(children = 'FTF 6-Year Student Retention by Ethnic Sub-groups: Asian Groups'),
    dcc.Dropdown(options= ftf_asian_frame_columns[0], value = 'Filipino',  id = 'controls-and-drop_rtn_asian_6', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_asian_6'),

    #pacific ialander ftf
    html.Div(children = 'FTF 1-Year Student Retention by Ethnic Sub-groups: Pacific Islander Groups'),
    dcc.Dropdown(options= ftf_pacific_islander_frame_columns[0], value = 'Other Pac.Islander', id = 'controls-and-drop_rtn_pi', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_pi'),

    html.Div(children = 'FTF 2-Year Student Retention by Ethnic Sub-groups: Pacific Islander Groups'),
    dcc.Dropdown(options= ftf_pacific_islander_frame_columns[0], value = 'Other Pac.Islander', id = 'controls-and-drop_rtn_pi_2', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_pi_2'),

    html.Div(children = 'FTF 4-Year Student Retention by Ethnic Sub-groups: Pacific Islander Groups'),
    dcc.Dropdown(options= ftf_pacific_islander_frame_columns[0], value = 'Other Pac.Islander', id = 'controls-and-drop_rtn_pi_4', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_pi_4'),

    html.Div(children = 'FTF 6-Year Student Retention by Ethnic Sub-groups: Pacific Islander Groups'),
    dcc.Dropdown(options= ftf_pacific_islander_frame_columns[0], value = 'Other Pac.Islander', id = 'controls-and-drop_rtn_pi_6', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_pi_6'),

    #transfer asian
    html.Div(children = 'Transfer 1-Year Student Retention by Ethnic Sub-groups: Asian Groups'),
    dcc.Dropdown(options= transfer_asian_frame_columns[0], value = 'Filipino',  id = 'controls-and-drop_rtn_asian_trf', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_asian_trf'),

    html.Div(children = 'Transfer 2-Year Student Retention by Ethnic Sub-groups: Asian Groups'),
    dcc.Dropdown(options= transfer_asian_frame_columns[0], value = 'Filipino',  id = 'controls-and-drop_rtn_asian_trf_2', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_asian_trf_2'),

    html.Div(children = 'Transfer 4-Year Student Retention by Ethnic Sub-groups: Asian Groups'),
    dcc.Dropdown(options= transfer_asian_frame_columns[0], value = 'Filipino',  id = 'controls-and-drop_rtn_asian_trf_4', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_asian_trf_4'),

    html.Div(children = 'Transfer 6-Year Student Retention by Ethnic Sub-groups: Asian Groups'),
    dcc.Dropdown(options= transfer_asian_frame_columns[0], value = 'Filipino',  id = 'controls-and-drop_rtn_asian_trf_6', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_asian_trf_6'),

#transfer pacific islander
    html.Div(children = 'Transfer 1-Year Student Retention by Ethnic Sub-groups: Pacific Islander Groups'),
    dcc.Dropdown(options= transfer_pacific_islander_frame_columns[0], value = 'Other Pac.Islander',  id = 'controls-and-drop_rtn_pi_trf', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_pi_trf'),

    html.Div(children = 'Transfer 2-Year Student Retention by Ethnic Sub-groups: Pacific Islander Groups'),
    dcc.Dropdown(options= transfer_pacific_islander_frame_columns[0], value = 'Other Pac.Islander',  id = 'controls-and-drop_rtn_pi_trf_2', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_pi_trf_2'),

    html.Div(children = 'Transfer 4-Year Student Retention by Ethnic Sub-groups: Pacific Islander Groups'),
    dcc.Dropdown(options= transfer_pacific_islander_frame_columns[0], value = 'Other Pac.Islander',  id = 'controls-and-drop_rtn_pi_trf_4', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_pi_trf_4'),

    html.Div(children = 'Transfer 6-Year Student Retention by Ethnic Sub-groups: Pacific Islander Groups'),
    dcc.Dropdown(options= transfer_pacific_islander_frame_columns[0], value = 'Other Pac.Islander',  id = 'controls-and-drop_rtn_pi_trf_6', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_pi_trf_6'),

#ftf retention asian chart
    html.Div(children = 'FTF Student Retention by Ethnic Sub-groups: Asian Groups'),
    dcc.Dropdown(options= ftf_asian_frame_columns[0], value = 'Filipino',  id = 'controls-and-drop_rtn_asian_ftf_chart', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_asian_ftf_chart'),

#ftf retention pacific islander chart
    html.Div(children = 'FTF Student Retention by Ethnic Sub-groups: Pacific Islander Groups'),
    dcc.Dropdown(options= ftf_pacific_islander_frame_columns[0], value = 'Other Pac.Islander',  id = 'controls-and-drop_rtn_pi_ftf_chart', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_pi_ftf_chart'),

#transfer retention asian chart
    html.Div(children = 'Transfer Student Retention by Ethnic Sub-groups: Asian Groups'),
    dcc.Dropdown(options= transfer_asian_frame_columns[0], value = 'Filipino',  id = 'controls-and-drop_rtn_asian_trf_chart', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_asian_trf_chart'),

#transfer retention pacific islander chart
    html.Div(children = 'Transfer Student Retention by Ethnic Sub-groups: Pacific Islander Groups'),
    dcc.Dropdown(options= transfer_pacific_islander_frame_columns[0], value = 'Other Pac.Islander', id = 'controls-and-drop_rtn_pi_trf_chart', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_rtn_pi_trf_chart'),

#asian standing chart
    html.Div(children = 'Academic Standing by Ethnic Sub-groups: Asian Groups'),
    dcc.Dropdown(options= asian_standing_frame['Asian Group'].unique(), value = 'Filipino',  id = 'controls-and-drop_stndg_asian_chart', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_stndg_asian_chart'),

#pi standing chart
    html.Div(children = 'Academic Standing by Ethnic Sub-groups: Pacific Islander Groups'),
    dcc.Dropdown(options= pi_standing_frame['Pacific Islander Group'].unique(), value = 'Other Pac.Islander',  id = 'controls-and-drop_stndg_pi_chart', placeholder = 'Select group from list below' ),
    dcc.Graph(figure = {}, id = 'controls-and-graph_stndg_pi_chart'),

    ])

@callback(
    Output(component_id = 'controls-and-graph', component_property = 'figure'),
    Input(component_id = 'controls-and-drop', component_property = 'value')
        )
def update_graph_asian(ethnic_select):
    fig = px.line(asian_group_counts_ug_frame.loc[asian_group_counts_ug_frame['asian_group'] == ethnic_select], x = 'semester', y = 'total', color = 'asian_group', height = 600, width = 1200) 
    return fig


@callback(
    Output(component_id = 'controls-and-graph_pi', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_pi', component_property = 'value')
        )
def update_graph_pacific_islander(ethnic_select):
    fig = px.line(pacific_islander_group_counts_ug_frame.loc[pacific_islander_group_counts_ug_frame['pacific_islander_group'] == ethnic_select], x = 'semester', y = 'total', color = 'pacific_islander_group', height = 600, width = 1200) 
    return fig

@callback(
    Output(component_id = 'controls-and-graph_pie', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_pie', component_property = 'value')
        )
def update_graph_asian_pie(term_select):
    fig = px.pie(asian_group_counts_ug_frame.loc[asian_group_counts_ug_frame['semester'] == term_select], values = 'total', names = 'asian_group', height = 600, width = 1200) 
    return fig

@callback(
    Output(component_id = 'controls-and-graph_pi_pie', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_pi_pie', component_property = 'value')
        )
def update_graph_pi_pie(term_select):
    fig = px.pie(pacific_islander_group_counts_ug_frame.loc[pacific_islander_group_counts_ug_frame['semester'] == term_select], values = 'total', names = 'pacific_islander_group', height = 600, width = 1200) 
    return fig


#asian ftf callbacks
@callback(
    Output(component_id = 'controls-and-graph_rtn_asian', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_asian', component_property = 'value')
        )
def update_graph_asian_rtn_line(ethnic_select):
    fig = px.line(ftf_asian_frame.loc[ftf_asian_frame['Asian Group'] == ethnic_select], x = 'Cohort Semester', y = 'Retention 1Yr', color = 'Asian Group', height = 600, width = 1200) 
    return fig

@callback(
    Output(component_id = 'controls-and-graph_rtn_asian_2', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_asian_2', component_property = 'value')
        )
def update_graph_asian_rtn_line2(ethnic_select):
    fig = px.line(ftf_asian_frame.loc[ftf_asian_frame['Asian Group'] == ethnic_select], x = 'Cohort Semester', y = 'Retention 2Yr', color = 'Asian Group', height = 600, width = 1200) 
    return fig

@callback(
    Output(component_id = 'controls-and-graph_rtn_asian_4', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_asian_4', component_property = 'value')
        )
def update_graph_asian_rtn_line4(ethnic_select):
    fig = px.line(ftf_asian_frame.loc[ftf_asian_frame['Asian Group'] == ethnic_select], x = 'Cohort Semester', y = 'Retention 4Yr', color = 'Asian Group', height = 600, width = 1200) 
    return fig

@callback(
    Output(component_id = 'controls-and-graph_rtn_asian_6', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_asian_6', component_property = 'value')
        )
def update_graph_asian_rtn_line6(ethnic_select):
    fig = px.line(ftf_asian_frame.loc[ftf_asian_frame['Asian Group'] == ethnic_select], x = 'Cohort Semester', y = 'Retention 6Yr', color = 'Asian Group', height = 600, width = 1200) 
    return fig

#pacific islander ftf callbacks
@callback(
    Output(component_id = 'controls-and-graph_rtn_pi', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_pi', component_property = 'value')
        )
def update_graph_pi_rtn_line(ethnic_select):
    fig = px.line(ftf_pacific_islander_frame.loc[ftf_pacific_islander_frame['Pacific Islander Group'] == ethnic_select], x = 'Cohort Semester', y = 'Retention 1Yr', color = 'Pacific Islander Group', height = 600, width = 1200) 
    return fig

@callback(
    Output(component_id = 'controls-and-graph_rtn_pi_2', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_pi_2', component_property = 'value')
        )
def update_graph_pi_rtn_line2(ethnic_select):
    fig = px.line(ftf_pacific_islander_frame.loc[ftf_pacific_islander_frame['Pacific Islander Group'] == ethnic_select], x = 'Cohort Semester', y = 'Retention 2Yr', color = 'Pacific Islander Group', height = 600, width = 1200) 
    return fig

@callback(
    Output(component_id = 'controls-and-graph_rtn_pi_4', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_pi_4', component_property = 'value')
        )
def update_graph_pi_rtn_line4(ethnic_select):
    fig = px.line(ftf_pacific_islander_frame.loc[ftf_pacific_islander_frame['Pacific Islander Group'] == ethnic_select], x = 'Cohort Semester', y = 'Retention 4Yr', color = 'Pacific Islander Group', height = 600, width = 1200) 
    return fig

@callback(
    Output(component_id = 'controls-and-graph_rtn_pi_6', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_pi_6', component_property = 'value')
        )
def update_graph_pi_rtn_line6(ethnic_select):
    fig = px.line(ftf_pacific_islander_frame.loc[ftf_pacific_islander_frame['Pacific Islander Group'] == ethnic_select], x = 'Cohort Semester', y = 'Retention 6Yr', color = 'Pacific Islander Group', height = 600, width = 1200) 
    return fig

#asian transfer callbacks
@callback(
    Output(component_id = 'controls-and-graph_rtn_asian_trf', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_asian_trf', component_property = 'value')
        )
def update_graph_asian_rtn_line_trf(ethnic_select):
    fig = px.line(transfer_asian_frame.loc[transfer_asian_frame['Asian Group'] == ethnic_select], x = 'Cohort Semester', y = 'Retention 1Yr', color = 'Asian Group', height = 600, width = 1200) 
    return fig

@callback(
    Output(component_id = 'controls-and-graph_rtn_asian_trf_2', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_asian_trf_2', component_property = 'value')
        )
def update_graph_asian_rtn_line2_trf(ethnic_select):
    fig = px.line(transfer_asian_frame.loc[transfer_asian_frame['Asian Group'] == ethnic_select], x = 'Cohort Semester', y = 'Retention 2Yr', color = 'Asian Group', height = 600, width = 1200) 
    return fig

@callback(
    Output(component_id = 'controls-and-graph_rtn_asian_trf_4', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_asian_trf_4', component_property = 'value')
        )
def update_graph_asian_rtn_line4_trf(ethnic_select):
    fig = px.line(transfer_asian_frame.loc[transfer_asian_frame['Asian Group'] == ethnic_select], x = 'Cohort Semester', y = 'Retention 4Yr', color = 'Asian Group', height = 600, width = 1200) 
    return fig

@callback(
    Output(component_id = 'controls-and-graph_rtn_asian_trf_6', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_asian_trf_6', component_property = 'value')
        )
def update_graph_asian_rtn_line6_trf(ethnic_select):
    fig = px.line(transfer_asian_frame.loc[transfer_asian_frame['Asian Group'] == ethnic_select], x = 'Cohort Semester', y = 'Retention 6Yr', color = 'Asian Group', height = 600, width = 1200) 
    return fig

#pacific islander transfer callbacks
@callback(
    Output(component_id = 'controls-and-graph_rtn_pi_trf', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_pi_trf', component_property = 'value')
        )
def update_graph_pi_rtn_line_trf(ethnic_select):
    fig = px.line(transfer_pacific_islander_frame.loc[transfer_pacific_islander_frame['Pacific Islander Group'] == ethnic_select], x = 'Cohort Semester', y = 'Retention 1Yr', color = 'Pacific Islander Group', height = 600, width = 1200) 
    return fig

@callback(
    Output(component_id = 'controls-and-graph_rtn_pi_trf_2', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_pi_trf_2', component_property = 'value')
        )
def update_graph_pi_rtn_line2_trf(ethnic_select):
    fig = px.line(transfer_pacific_islander_frame.loc[transfer_pacific_islander_frame['Pacific Islander Group'] == ethnic_select], x = 'Cohort Semester', y = 'Retention 2Yr', color = 'Pacific Islander Group', height = 600, width = 1200) 
    return fig

@callback(
    Output(component_id = 'controls-and-graph_rtn_pi_trf_4', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_pi_trf_4', component_property = 'value')
        )
def update_graph_pi_rtn_line4_trf(ethnic_select):
    fig = px.line(transfer_pacific_islander_frame.loc[transfer_pacific_islander_frame['Pacific Islander Group'] == ethnic_select], x = 'Cohort Semester', y = 'Retention 4Yr', color = 'Pacific Islander Group', height = 600, width = 1200) 
    return fig

@callback(
    Output(component_id = 'controls-and-graph_rtn_pi_trf_6', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_pi_trf_6', component_property = 'value')
        )
def update_graph_pi_rtn_line6_trf(ethnic_select):
    fig = px.line(transfer_pacific_islander_frame.loc[transfer_pacific_islander_frame['Pacific Islander Group'] == ethnic_select], x = 'Cohort Semester', y = 'Retention 6Yr', color = 'Pacific Islander Group', height = 600, width = 1200) 
    return fig 

@callback(
    Output(component_id = 'controls-and-graph_rtn_asian_ftf_chart', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_asian_ftf_chart', component_property = 'value')
        )
def update_graph_asian_ftf_chart(ethnic_select):
    fig = go.Figure(data = [go.Table(header = dict(values = list(ftf_asian_frame.columns),
    fill_color = 'lavender',
    align = 'left'),
    cells = dict(values = ftf_asian_frame.loc[ftf_asian_frame['Asian Group'] == ethnic_select].transpose().values.tolist()))
    ])
    return fig

@callback(
    Output(component_id = 'controls-and-graph_rtn_pi_ftf_chart', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_pi_ftf_chart', component_property = 'value')
        )
def update_graph_pi_ftf_chart(ethnic_select):
    fig = go.Figure(data = [go.Table(header = dict(values = list(ftf_pacific_islander_frame.columns),
    fill_color = 'lavender',
    align = 'left'),
    cells = dict(values = ftf_pacific_islander_frame.loc[ftf_pacific_islander_frame['Pacific Islander Group'] == ethnic_select].transpose().values.tolist()))
    ])
    return fig

@callback(
    Output(component_id = 'controls-and-graph_rtn_asian_trf_chart', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_asian_trf_chart', component_property = 'value')
        )
def update_graph_asian_trf_chart(ethnic_select):
    fig = go.Figure(data = [go.Table(header = dict(values = list(transfer_asian_frame.columns),
    fill_color = 'lavender',
    align = 'left'),
    cells = dict(values = transfer_asian_frame.loc[transfer_asian_frame['Asian Group'] == ethnic_select].transpose().values.tolist()))
    ])
    return fig

@callback(
    Output(component_id = 'controls-and-graph_rtn_pi_trf_chart', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_rtn_pi_trf_chart', component_property = 'value')
        )
def update_graph_pi_trf_chart(ethnic_select):
    fig = go.Figure(data = [go.Table(header = dict(values = list(transfer_pacific_islander_frame.columns),
    fill_color = 'lavender',
    align = 'left'),
    cells = dict(values = transfer_pacific_islander_frame.loc[transfer_pacific_islander_frame['Pacific Islander Group'] == ethnic_select].transpose().values.tolist()))
    ])
    return fig

@callback(
    Output(component_id = 'controls-and-graph_stndg_asian_chart', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_stndg_asian_chart', component_property = 'value')
        )
def update_graph_asian_standing_chart(ethnic_select):
    fig = go.Figure(data = [go.Table(header = dict(values = list(asian_standing_frame.columns),
    fill_color = 'lavender',
    align = 'left'),
    cells = dict(values = asian_standing_frame.loc[asian_standing_frame['Asian Group'] == ethnic_select].transpose().values.tolist()))
    ])
    return fig

@callback(
    Output(component_id = 'controls-and-graph_stndg_pi_chart', component_property = 'figure'),
    Input(component_id = 'controls-and-drop_stndg_pi_chart', component_property = 'value')
        )
def update_graph_pi_standing_chart(ethnic_select):
    fig = go.Figure(data = [go.Table(header = dict(values = list(pi_standing_frame.columns),
    fill_color = 'lavender',
    align = 'left'),
    cells = dict(values = pi_standing_frame.loc[pi_standing_frame['Pacific Islander Group'] == ethnic_select].transpose().values.tolist()))
    ])
    return fig


if __name__ == '__main__':
    app.run(debug = True)



