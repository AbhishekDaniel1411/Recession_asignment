#Importing Libraries
import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')


# Initialize the Dash app
app = dash.Dash(__name__)

#dict of options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Rescession Period Satistics'}
]

# List of years
year_list = [i for i in range(1980, 2024, 1)]

#Creating the app layout
app.layout = html.Div([
    html.H1("Automobile Statistics Dashboard", style={'textAlign':'center', 'color': '#503D36', 'font-size':24}),
    html.Div([
        html.Label('Select Report:'),
        dcc.Dropdown(id = 'dropdown-statistics', options = dropdown_options, value='Select Report', placeholder='Select a report type')
    ]),
    html.Div(dcc.Dropdown(id = 'select-year', options = [{'label': i, 'value' : i} for i in year_list], value = 'select the year')),
    html.Div(id = 'output-container', className = 'chart-grid', style = {'display': 'flex'})
])

# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

#Callback for plotting
@app.callback(
    Output(component_id='output-container', component_property='children'),
     [Input(component_id='dropdown-statistics', component_property='value'),Input(component_id='select-year', component_property='value')])

def update_output_container(selected_statistics, input_year):
  if selected_statistics == 'Recession Period Statistics':
    recession_data = data[data['Recession'] == 1] #creating a new df
    #plot1: Average Automobile Sales fluctuation over Recession Period
    yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
    R_chart1 = dcc.Graph(figure=px.line(yearly_rec,x='Year', y='Automobile_Sales', title="Average Automobile Sales fluctuation over Recession Period"))
    #plot2: Average number of vehicles sold by each vehicle type
    average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
    R_chart2  = dcc.Graph(figure=px.bar(average_sales, x = 'Vehicle_Type', y = 'Automobile_Sales', title = 'Average number of vehicles sold by each vehicle type'))
    #plot3: Proportions of Advertising expenditure for each Vehicle type during Recession
    exp_rec= recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
    R_chart3 = dcc.Graph(figure = px.pie(exp_rec, values = 'Advertising_Expenditure', names = 'Vehicle_Type', title = 'Proportions of Advertising expenditure for each Vehicle type during Recession'))
    #plot4: Effect of unemployment rate on vehicle type and sales
    unemp1 = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].mean().reset_index()
    R_chart4 = dcc.Graph(figure = px.bar(unemp1, x = 'unemployment_rate', y = 'Automobile_Sales', color = 'Vehicle_Type',title = 'Effect of unemployment rate on vehicle type and sales'))
    return [
        html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)], style={'display': 'flex'}),
        html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)], style={'display': 'flex'})
    ]
  elif (input_year and selected_statistics=='Yearly Statistics') :
    yearly_data = data[data['Year'] == int(input_year)] #creating a new df
    #plot1: Yearly Automobile sales
    yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
    Y_chart1 = dcc.Graph(figure=px.line(yas, x = 'Year', y= 'Automobile_Sales', title = 'Yearly Automobile sales'))
    #plot2: Total Monthly Automobile sales in the selected year
    yms = yearly_data.groupby('Month')['Automobile_Sales'].mean().reset_index()
    Y_chart2 = dcc.Graph(figure = px.line(yms, x = 'Month', y = 'Automobile_Sales', title = 'Total Monthly Automobile sales in the year {}'.format(input_year)))
    #plot3: Average Vehicles Sold by Vehicle Type in the selected year
    avr_vdata=yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
    Y_chart3 = dcc.Graph( figure = px.bar(avr_vdata, x = 'Vehicle_Type', y = 'Automobile_Sales', title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))
    #plot4: Total Advertisement Expenditure for each vehicle in the selected year
    y_exp = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
    Y_chart4 = dcc.Graph(figure = px.pie(y_exp, values = 'Advertising_Expenditure', names = 'Vehicle_Type', title = 'Total Advertisement Expenditure for each vehicle in the year {}'.format(input_year)))
    return [
        html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)],style={'display':'flex'}),
        html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)],style={'display':'flex'})
    ]

if __name__ == '__main__':
    app.run_server(debug=True)