# # Run this app with `python app.py` and
# # visit http://127.0.0.1:8050/ in your web browser.



from datetime import datetime
from pathlib import Path
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np 
from scipy import stats
import plotly.graph_objects as go





current_datetime =  datetime.now()
current_date_str = str(current_datetime.date()).replace('-','_')

current_directory = Path.cwd()
model_outputs_directory = current_directory / 'data/model_outputs' 

forwards_filename = current_date_str + '_forward_predictions.csv'
forwards_filepath = model_outputs_directory / forwards_filename

defense_filename = current_date_str + '_defense_predictions.csv'
defense_filepath = model_outputs_directory / defense_filename


# Load in the model dataframes and combine them 
forwards_df = pd.read_csv(forwards_filepath)
forwards_df = forwards_df.drop(columns=['Unnamed: 0'])
forwards_df['Position'] = 'F'
defense_df = pd.read_csv(defense_filepath)
defense_df = defense_df.drop(columns=['Unnamed: 0'])
defense_df['Position'] = 'D'
model_output_df = pd.concat([forwards_df, defense_df] )

# Load in the player data again 
player_data_directory = current_directory / 'data/processed/player_data'
player_data_filename = current_date_str + '_clean_player_data.csv'
player_data_filepath = player_data_directory / player_data_filename

player_data_df = pd.read_csv(player_data_filepath)
player_data_df = player_data_df.drop(columns=['Unnamed: 0'])

# Clean the player data df 
player_data_df = player_data_df[player_data_df['Pos'] != 'G']
drop_columns = ['Team', 'specific_pos', 'Cap%', 'Salary','S/C', 'Ht', 'Wt', 'TOI', 'FO%']
player_data_df = player_data_df.drop(columns=drop_columns)
player_data_df = player_data_df.dropna()
def prep_atoi(atoi_string):
    list = atoi_string.split(':')
    minutes = int(list[0])
    seconds = int(list[1])

    return minutes + (seconds/60)



player_data_df['ATOI'] = player_data_df['ATOI'].apply(prep_atoi)

# combine the model and statistics dataframes into one master df 
df = player_data_df.merge(model_output_df, on='Player', how='inner')



dropdown_features = [ 'Age', 'GP', 'G', 'A', 'PTS', '+/-', 'PIM',  'ATOI', 'BLK', 'HIT',  'Exp']


initial_range = (np.min(df['difference']), np.max(df['difference']))


# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H3('Select a feature:'),
    dcc.Dropdown(
            id='feature-dropdown',
            options=[{'label': feat, 'value': feat} for feat in dropdown_features],
            value='A'),

    html.Div([
    html.H3(f'Select a range of values')]),  
    dcc.RangeSlider(id='feature-slider',value=initial_range),
    dcc.Graph(id='graph-with-slider'),
    html.Div(id='mean-std-output')
])


@app.callback(
    Output('feature-slider', 'min'),
    Output('feature-slider', 'max'),
    Output('feature-slider', 'step'),
    Input('feature-dropdown', 'value')
)
def update_slider_options(feature):
    min_val = np.floor(np.min(df[feature]))
    max_val = np.floor(np.max(df[feature]))
    if max_val > 100:
        step_val = 3
    else:
        step_val = 1 
    return min_val, max_val, step_val


@app.callback(
    Output('graph-with-slider', 'figure'),
    Output('mean-std-output', 'children'),
    Input('feature-dropdown', 'value'),
    Input('feature-slider', 'value'),

)
def update_figure(feature, range):
    if feature is None or range is None:
        # Return a default figure or None to display nothing initially
        return {}


    filtered_df = df[(df[feature] >= range[0]) & (df[feature] <= range[1])]

    fig = px.histogram(filtered_df, x="difference")




    # fig.update_layout(transition_duration=500)

    mean_val = np.mean(filtered_df['difference'])
    std_val = np.std(filtered_df['difference'])

    mean_std_text = f"Mean: {mean_val:.2f}, Standard Deviation: {std_val:.2f}"


    return fig, mean_std_text




# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
