import pandas as pd
# import plotly.express as px


""" df = pd.read_csv("Hatalaee.csv")
NaN_values_count = df.isna().sum()
df.dropna(inplace=True)
df.drop(columns=['car_img', 'car_link'], inplace=True)


df['car_year'] = [int(i) for i in df.car_year]
df['car_kilometer'] = [int(i) for i in df.car_kilometer]
df['car_price'] = [int(i) for i in df.car_price] 


Car_makes_count = df.groupby('car_make')['car_make'].count()  """

df = pd.read_csv("latest.csv")


def get_makes(df):
    """
    :return: all unique makes of our dataset
    """
    return df['car_make'].unique()


def get_model(df, make):
    """
    :param make: car make
    :return: return all unique models for this car make
    """
    return df['car_model'].loc[df['car_make'] == make].unique().tolist()


def get_groupyModels(df, make):
    """
    :param make: car make
    :return: return a unique groups of car models for this existing car make.
    """
    return df['car_model'].groupby(df['car_model'].loc[(df['car_make'] == f'{make}')]).count()


def price_vs_km(df, make, model, year):
    print(make, model, year)
    if year is None:
        data = df[{'car_price', 'car_kilometer', 'car_year'}].loc[(df['car_make'] == f'{make}') & (df['car_model'] == f'{model}')]
        return data
    else:
        data = df[{'car_price', 'car_kilometer', 'car_year'}].loc[(df['car_make'] == f'{make}') & (df['car_model'] == f'{model}') & (df['car_year'] == year)]
        return data
    


def price_vs_year(df, make, model):
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
    carModel_sum = pd.DataFrame(columns=['Car Model', 'SUM'])
    carModels = get_model(df, make)
    for carModel in carModels:
        sum_price = df['car_price'].loc[df['car_model'] == f'{carModel}'].sum()
        new_row = {'Car Model': carModel, 'SUM': sum_price}
        carModel_sum = carModel_sum.append(new_row, ignore_index=True)
    return carModel_sum


def get_sum_of_ads(df, carmake):
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
    unique_years = df['car_year'].loc[(df['car_make'] == f'{make}') & (
        df['car_model'] == f'{model}')].unique().tolist()
    return unique_years


def get_car_info(df, make, model):
    model_count = len(df.loc[df['car_model'] == model])
    pass
