# --------------------------------------------------
# --------------Imports Section---------------------
# --------------------------------------------------

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from dash import Dash, html, dcc
import queries

# --------------------------------------------------
# --------------Data wrangling Section--------------
# --------------------------------------------------


df = pd.read_csv('latest.csv')

""" NaN_values_count = df.isna().sum()
df.dropna(inplace=True)
df.drop(columns=['car_img', 'car_link'], inplace=True)
df = df[~df.car_price.str.contains('|'.join('-'))]

df['car_year'] = [int(i) for i in df.car_year]
df['car_kilometer'] = [int(i) for i in df.car_kilometer]
df['car_price'] = [int(i) for i in df.car_price]
 """

dataset_size = len(df)

Car_makes_count = df.groupby('car_make')['car_make'].count()


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{'name': 'viewport',
                                                                              'content': 'width=device-width, initial-scale=1'}])

# --------------------------------------------------
# --------------Figures Section---------------------
# --------------------------------------------------

# Pie chart shows number of ads for each car make


def number_of_ads_carmake():
    fig = go.Figure()
    fig = px.pie(Car_makes_count, values=Car_makes_count.values,
                 names=Car_makes_count.index, hole=0.4)
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide', )
    return fig


def bar1(df):
    sales_value = queries.get_sales_values_beta(df)
    fig = go.Figure()
    Unique_makes = sales_value.loc[(sales_value['Car Make'] == 'Hyundai') | (sales_value['Car Make'] == 'Kia') | (sales_value['Car Make'] == 'Toyota') | (
        sales_value['Car Make'] == 'Chevrolet') | (sales_value['Car Make'] == 'Renault') | (sales_value['Car Make'] == 'Mitsubishi') | (sales_value['Car Make'] == 'Opel')]
    fig = px.bar(Unique_makes, x='Car Make', y='SUM', color='Car Model')
    fig.update_layout(barmode='stack', xaxis={
                      'categoryorder': 'total descending'})
    return fig

# Pie chart shows number of ads for each model


def number_of_ads_carmodel(df):
    sum_of_ads = queries.get_sum_of_ads(df)
    fig = go.Figure()
    fig = px.pie(sum_of_ads, values='No. Of Ads', names='Car Model', hole=0.4)
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide', )
    return fig


# --------------------------------------------------
# --------------APP Layout Section------------------
# --------------------------------------------------
app.layout = dbc.Container([
    dbc.Row([

        html.Content("Last Update: 15/01/2023",
                     className='text-info text-right'),
        html.H1("Egypt Used Cars' Market Analysis",
                className='text-center mt-4 font-weight-bolder text-danger'),
        html.H5(f"Our dataset contains {dataset_size} ad of the available online ads",
                className='text-center text-secondary mb-5')

    ]),

    dbc.Row([
        dbc.Col(html.H4(["Hyundai occupies the first place for the most Selling Car in the Egyptian market, Hyundai Obsses more than 10% of the available ads over the Internet. ", html.Br(), "While BMW cars comes in the 14th place!."],
                className='text-center text-secondary shadow-sm text-monospace text-justify mt-5')),
        dbc.Col(html.Div([dcc.Graph(figure=number_of_ads_carmake())])
                ),


    ]),

    dbc.Row([
        html.Hr(style={'borderWidth': "0.3vh",
                "width": "6", "color": "#190404"})
    ]),

    dbc.Row([
        html.H3(f"Specify Car Parameters to perform the analysis.",
                className='text-center text-secondary mb-4 mt-2')

    ]),

    dbc.Row([
        dbc.Col(dcc.Dropdown(queries.get_makes(df), value=None,
                placeholder='Car Make', id='car_make_dropdown')),
        dbc.Col(dcc.Dropdown(id='car_models',
                value=None, placeholder='Car Models')),
        dbc.Col(dcc.Dropdown(id='car_years',
                value=None, placeholder='Car Year'))
    ]),

    html.Br(),
    dbc.Row([
        dcc.Graph(id='line_kmvsprice'),
        dcc.Graph(id='line_yearvsprice')
    ]),


    html.Br(),
    dbc.Row([
        dcc.Graph(id='models_num_ads')
    ]),


])


# --------------------------------------------------
# --------------Callback Section---------------------
# --------------------------------------------------

##      DROPDOWN SECTION

#update car model dropdown menu
@app.callback(
    Output('car_models', 'options'),
    Input('car_make_dropdown', 'value')
)
def update_dropdown(input_value):
    return queries.get_model(df, input_value)

#update car year dropdown menu
@app.callback(
    Output('car_years', 'options'),
    Input('car_make_dropdown', 'value'),
    Input('car_models', 'value')
)
def update_dropdown(make, model):
    return queries.get_car_year(df, make, model)


##      FIGURE UPDATE SECTION


# Callback for figure1 > Price VS Km
@app.callback(
    Output('line_kmvsprice', 'figure'),
    State('car_make_dropdown', 'value'),
    State('car_models', 'value'),
    Input('car_years', 'value')
)
def update_figure1(make, model, year):
    if year is None:
        data = queries.price_vs_km(df, make, model, year)
        fig = go.Figure()
        fig = px.scatter(data_frame=data, x=data.car_kilometer,
                        y=data.car_price, trendline='ols', trendline_scope='overall', labels={"car_kilometer": "Kilomitrage(KM)", "car_price": "Price(EGP)", "car_year": "Car Year"}, color='car_year')

        # print(px.get_trendline_results(fig))
        return fig
    else:
        data = queries.price_vs_km(df, make, model, year)
        fig = go.Figure()
        fig = px.scatter(data_frame=data, x=data.car_kilometer,
                        y=data.car_price, trendline='ols', trendline_scope='overall', labels={"car_kilometer": "Kilomitrage(KM)", "car_price": "Price(EGP)"})

        # print(px.get_trendline_results(fig))
        return fig


# callback for figure2 > Price VS Year
@app.callback(
    Output('line_yearvsprice', 'figure'),
    Input('car_make_dropdown', 'value'),
    Input('car_models', 'value')
)
def update_figure2(make, model):
    data = queries.price_vs_year(df, make, model)
    fig = go.Figure()
    fig = px.scatter(data_frame=data, x=data.car_year,
                     y=data.car_price, trendline='ols', trendline_scope='overall', labels={"car_year": "Year", "car_price": "Price(EGP)"})
    return fig


@app.callback(
    Output('models_num_ads', 'figure'),
    Input('car_make_dropdown', 'value')
)
def model_num_ads(make):
    num_ads = queries.get_sum_of_ads(df, make)
    fig = go.Figure()
    fig = px.bar(num_ads, x='Car Model', y='Number of Ads')
    fig.update_layout(barmode='stack', xaxis={
                      'categoryorder': 'total descending'})
    return fig

# update the car status


@app.callback(
    Output('car_status', 'children'),
    Input('car_make_dropdown', 'value'),
    Input('car_models', 'value')
)
def car_info(make, model):
    pass

##          SHOW&HIDE SECTION


@app.callback(
    Output(component_id='line_kmvsprice', component_property='style'),
    Input(component_id='car_models', component_property='value'),
    Input(component_id='car_make_dropdown', component_property='value'))
def show_hide_element(carmodel, carmake):
    # print(visibility_state)
    if carmake == None or carmodel == None:
        return {'display': 'none'}
    else:
        return {'display': 'block'}


@app.callback(
    Output(component_id='line_yearvsprice', component_property='style'),
    Input(component_id='car_models', component_property='value'),
    Input(component_id='car_make_dropdown', component_property='value'))
def show_hide_element(carmodel, carmake):
    # print(visibility_state)
    if carmake == None or carmodel == None:
        return {'display': 'none'}
    else:
        return {'display': 'block'}


@app.callback(
    Output(component_id='models_num_ads', component_property='style'),
    Input(component_id='car_models', component_property='value'),
    Input(component_id='car_make_dropdown', component_property='value'))
def show_hide_element(carmodel, carmake):
    # print(carmake, carmodel)
    if carmake == None or carmodel == None:
        return {'display': 'none'}
    else:
        return {'display': 'block'}


@app.callback(
    Output(component_id='test', component_property='style'),
    Input(component_id='car_models', component_property='value'),
    Input(component_id='car_make_dropdown', component_property='value'))
def show_hide_element(carmodel, carmake):
    # print(carmake, carmodel)
    if carmake == None or carmodel == None:
        return {'display': 'none'}
    else:
        return {'display': 'block'}


if __name__ == "__main__":
    app.run_server(host='192.168.1.28', port=5000)
