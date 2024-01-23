# # Run this app with `python app.py` and
# # visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from datetime import datetime
from pathlib import Path

# app = Dash(__name__)




current_datetime =  datetime.now()
current_date_str = str(current_datetime.date()).replace('-','_')

current_directory = Path.cwd()
model_outputs_directory = current_directory / 'data/model_outputs' 

forwards_filename = current_date_str + '_forward_predictions.csv'
forwards_filepath = model_outputs_directory / forwards_filename

defense_filename = current_date_str + '_defense_predictions.csv'
defense_filepath = model_outputs_directory / defense_filename



forwards_df = pd.read_csv(forwards_filepath)
defense_df = pd.read_csv(defense_filepath)





# fig.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
# )

# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),

#     html.Div(children='''
#         Dash: A web application framework for your data.
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ])

# if __name__ == '__main__':
#     app.run(debug=True)






# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

app = Dash(__name__)



fig = px.scatter(forwards_df, x="Predicted_Salary", y='Actual_Salary')



# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc

app = Dash(__name__)

markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

app.layout = html.Div([
    dcc.Markdown(children=markdown_text),
    dcc.Graph(
            id='example-graph',
            figure=fig
        )])



if __name__ == '__main__':
    app.run(debug=True)
