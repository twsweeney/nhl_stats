# # Run this app with `python app.py` and
# # visit http://127.0.0.1:8050/ in your web browser.



from datetime import datetime
from pathlib import Path
import dash
from dash import dcc, html
import pandas as pd

# app = dash.Dash(__name__)





current_datetime =  datetime.now()
current_date_str = str(current_datetime.date()).replace('-','_')

current_directory = Path.cwd()
model_outputs_directory = current_directory / 'data/model_outputs' 

forwards_filename = current_date_str + '_forward_predictions.csv'
forwards_filepath = model_outputs_directory / forwards_filename

defense_filename = current_date_str + '_defense_predictions.csv'
defense_filepath = model_outputs_directory / defense_filename



forwards_df = pd.read_csv(forwards_filepath)
forwards_df = forwards_df.drop(columns=['Unnamed: 0'])
forwards_df['Position'] = 'F'
defense_df = pd.read_csv(defense_filepath)
defense_df = defense_df.drop(columns=['Unnamed: 0'])
defense_df['Position'] = 'D'




df = pd.concat([forwards_df, defense_df] )


import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd



# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    # Dropdown for Team selection
    dcc.Dropdown(
        id='team-dropdown',
        options=[{'label': team, 'value': team} for team in df['Team'].unique()],
        value=df['Team'].unique()[0],  # Default value
        multi=True
    ),
    
    # Radio button for Overpaid/Underpaid selection
    dcc.RadioItems(
        id='overunder-radio',
        options=[
            {'label': 'Overpaid', 'value': 'overpaid'},
            {'label': 'Underpaid', 'value': 'underpaid'}
        ],
        value='overpaid',  # Default value
        labelStyle={'display': 'block'}
    ),
    # Radio button for Position selection
    dcc.RadioItems(
        id='position-radio',
        options=[
            {'label': 'Forward (F)', 'value': 'F'},
            {'label': 'Defense (D)', 'value': 'D'},
            {'label': 'Show Both', 'value': 'both'}
        ],
        value='both',  # Default value
        labelStyle={'display': 'block'}
    ),
    # Table to display data
    html.Table(id='table'),
])

# Callback to update the table based on dropdown and radio button selection
@app.callback(
    Output('table', 'children'),
    [Input('team-dropdown', 'value'),
     Input('overunder-radio', 'value'),
     Input('position-radio', 'value')]
)
def update_table(selected_teams, overunder_value, position_value):
 # Check if only one team is selected, if so make it a list so isin works as expected 
    if isinstance(selected_teams, str): 
        selected_teams = [selected_teams]


    if position_value == 'both':
        filtered_df = df[(df['Team'].isin(selected_teams)) & (df['Position'].isin(['F', 'D']))]
    else:
        filtered_df = df[(df['Team'].isin(selected_teams)) & (df['Position'] == position_value)]
    
    if overunder_value == 'overpaid':
        filtered_df = filtered_df[filtered_df['difference'] > 0]
    else:
        filtered_df = filtered_df[filtered_df['difference'] < 0]

    filtered_df = round(filtered_df)
    
    table_rows = [html.Tr([html.Th(col) for col in filtered_df.columns])] + [
        html.Tr([html.Td(filtered_df.iloc[i][col]) for col in filtered_df.columns]) for i in range(len(filtered_df))
    ]
    return table_rows

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
