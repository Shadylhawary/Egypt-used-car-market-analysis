import pandas as pd
from datetime import datetime


df = pd.read_csv("latest.csv")


def get_makes(df):
    """Returns all unique car makes.

    Args:
        df (dataframe): dataframe

    Returns:
        dataframe: unique car makes dataframe
    """
    return df['car_make'].unique()


def get_model(df, make):
    """function used to get all the available models for a certain car make

    Args:
        df (dataframe): dataset
        make (str): a certain car make

    Returns:
        list[str]: all car models belongs to the specified car make
    """
    return df['car_model'].loc[df['car_make'] == make].unique().tolist()


def get_groupyModels(df, make):
    """function used to get the [count-models] for a certain car make

    Args:
        df (dataframe): dataset
        make (str): a certain car make

    Returns:
        int: Count of all car models belongs to the specified car make
    """    
    return df['car_model'].groupby(df['car_model'].loc[(df['car_make'] == f'{make}')]).count()


def price_vs_km(df, make, model, year):
    """function used to generate the required data for Fig1.

    Args:
        df (dataframe): dataset
        make (str): the desired car make
        model (str): the desired car model
        year (int): the desired car year

    Returns:
        dataframe: a dataframe holds [price, kilometers, year] for a certain car model.
    """    
    if year is None:
        data = df[{'car_price', 'car_kilometer', 'car_year'}].loc[(
            df['car_make'] == f'{make}') & (df['car_model'] == f'{model}')]
        return data
    else:
        data = df[{'car_price', 'car_kilometer', 'car_year'}].loc[(df['car_make'] == f'{make}') & (
            df['car_model'] == f'{model}') & (df['car_year'] == year)]
        return data


def price_vs_year(df, make, model):
    """function used to generate the required data for Fig2.

    Args:
        df (dataframe): dataset
        make (str): the desired car make
        model (str): the desired car model

    Returns:
        dataframe: a dataframe holds [price, year] for a certain car model.
    """    
    return df[{'car_price', 'car_year'}].loc[(df['car_make'] == f'{make}') & (df['car_model'] == f'{model}')]


def get_sales_values(df):
    car_models = []
    car_makes = []
    car_price = []
    unique_carModels = df['car_model'].unique().tolist()
    for carModel in unique_carModels:
        sum_price = df['car_price'].loc[df['car_model'] == f'{carModel}'].sum()
        car_make = df['car_make'].loc[df['car_model'] == carModel]
        car_models.append(carModel)
        car_price.append(sum_price)
        car_makes.append(car_make)

    carMake_sum = {'Car Make': car_makes,
                   'Car Model': car_models, 'Price': car_price}
    return carMake_sum


def get_sales_values_beta(df):
    carMake_sum = pd.DataFrame(columns=['Car Make', 'Car Model', 'SUM'])

    unique_Carmodels = df['car_model'].unique().tolist()
    for carModel in unique_Carmodels:
        sum_price = df['car_price'].loc[df['car_model'] == f'{carModel}'].sum()
        carMake = df['car_make'].loc[df['car_model'] == f'{carModel}'].tolist()
        new_row = {'Car Make': carMake[0],
                   'Car Model': carModel, 'SUM': sum_price}
        carMake_sum = carMake_sum.append(new_row, ignore_index=True)
    return carMake_sum


def get_sales_value_model(df, make):
    """_summary_

    Args:
        df (_type_): _description_
        make (_type_): _description_

    Returns:
        _type_: _description_
    """    
    carModel_sum = pd.DataFrame(columns=['Car Model', 'SUM'])
    carModels = get_model(df, make)
    for carModel in carModels:
        sum_price = df['car_price'].loc[df['car_model'] == f'{carModel}'].sum()
        new_row = {'Car Model': carModel, 'SUM': sum_price}
        carModel_sum = carModel_sum.append(new_row, ignore_index=True)
    return carModel_sum


def get_sum_of_ads(df, carmake):
    """function used to generate the data used to plot Fig3

    Args:
        df (dataframe): dataset
        carmake (str): car make

    Returns:
        pandas dataframe: dataframe holds [car model - number of ads]
    """    
    carModel_sum_of_ads = pd.DataFrame(columns=['Car Model', 'Number of Ads'])
    unique_Carmodels = df['car_model'].loc[df['car_make']
                                           == f'{carmake}'].unique().tolist()
    for carModel in unique_Carmodels:
        count = len(df.loc[df['car_model'] == carModel])
        new_row = {'Car Model': carModel, 'Number of Ads': count}
        carModel_sum_of_ads = carModel_sum_of_ads.append(
            new_row, ignore_index=True)
    return carModel_sum_of_ads


def get_car_year(df, make, model):
    """function used to return all the available years for a certain car model

    Args:
        df (dataframe): dataset
        make (str): the desired car make
        model (str): the desired car model

    Returns:
        list: A list of all available car years.
    """    
    unique_years = df['car_year'].loc[(df['car_make'] == f'{make}') & (
        df['car_model'] == f'{model}')].unique().tolist()
    return unique_years


def get_car_info(df, model):
    """function to return car model count

    Args:
        df (dataframe): dataset
        model (str): car model
    """    
    model_count = len(df.loc[df['car_model'] == model])
    pass


def log_ip(ip):
    logfile = open('log.txt', 'a')
    logfile.write(f"[IP: {ip} ]  --- [DATE: {datetime.now()} ] \n")
    logfile.close()
