import pandas as pd
import cbsodata
import matplotlib.pyplot as plt
import numpy as np
import functools as ft
from datetime import datetime
import os
import warnings
warnings.filterwarnings("ignore")

todayDate = datetime.today().strftime('%Y_%m_%d')
pd.set_option('display.max_columns', 40)

#  https://opendata.cbs.nl/#/CBS/en/dataset/85881ENG/table


todayDate = datetime.today().strftime('%Y_%m_%d')
pd.set_option('display.max_columns', 40)

settings = {'figure.figsize':(14,4),
            'figure.dpi':144,
            'figure.facecolor':'w',
            'axes.spines.top':False,
            'axes.spines.bottom':False,
            'axes.spines.left':False,
            'axes.spines.right':False,
            'axes.grid':True,
            'grid.linestyle':'--',
            'grid.linewidth':0.5}
plt.rcParams.update(settings)

###################################
# Want consumer disposable income data
###################################

#### Where to save data and figures
output_data_main_data_file = r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/mo_data/"

print("employment data english")

def macro_data_cbs(identifier, verbose = False):
    start_date = '01/01/2003'

    # get data
    data = pd.DataFrame(cbsodata.get_data(identifier))

    if verbose:
        info = cbsodata.get_info(identifier)
        print(info)
        tables = pd.DataFrame(cbsodata.get_table_list())
        columns_unprocessed = data.columns
        print("Columns unprocessed: ", len(columns_unprocessed))
        print(data.Periods)

    # dont want quarters
    data = data[~data['Periods'].str.isnumeric()]
    data = data[~data['Periods'].str.contains('quarter')]
    data = data[~data['Periods'].str.contains('quater')] ########################### CBS

    # drop unnecessary columns
    data.drop(columns = ['ID','Periods'], inplace = True)

    # per gender
    data_allGenders = data[data['Sex'] == 'Total sex']
    data_male = data[data['Sex'] == 'Men']
    data_female = data[data['Sex'] == 'Women']

    categories = ['Labor_Force', 'Employed_Labor_Force', 'Unemployed_Labor_Force', "UnemplyRate", "Not_in_Labor_Force", "Gross_Labor_Particp", "Net_Labor_Particp"]
    allBranches = []
    for age in data_allGenders['Age'].unique():
        data_age = data_allGenders[data_allGenders['Age'] == age]
        data_age = data_age.set_index(pd.date_range(start = start_date, periods = data_age.shape[0], freq = "M").to_period('M'))
        data_age.index = pd.PeriodIndex(data_age.index, freq='M').to_timestamp()
        wantThese = [col for col in data_age.columns if "Not" not in col]
        data_age = data_age[wantThese]
        data_age.drop(columns = ['Sex', 'Age'], inplace = True)
        data_age.columns = ["Employment_" + "allGenders_" + age + "_" + col for col in data_age.columns]
        data_age.columns = [x + "_" + y for x, y in zip(data_age.columns, categories)]
       
        allBranches.append(data_age)

    data_all = pd.concat(allBranches, axis=1)

    data_all.to_csv(output_data_main_data_file + "cbs_employment_all_genders_mo.csv")

    #############################################
    #############################################

    categories = ['Labor_Force', 'Employed_Labor_Force', 'Unemployed_Labor_Force', "UnemplyRate", "Not_in_Labor_Force", "Gross_Labor_Particp", "Net_Labor_Particp"]
    allBranches = []
    for age in data_male['Age'].unique():
        data_age = data_male[data_male['Age'] == age]
        data_age = data_age.set_index(pd.date_range(start = start_date, periods = data_age.shape[0], freq = "M").to_period('M'))
        data_age.index = pd.PeriodIndex(data_age.index, freq='M').to_timestamp()
        wantThese = [col for col in data_age.columns if "Not" not in col]
        data_age = data_age[wantThese]
        data_age.drop(columns = ['Sex', 'Age'], inplace = True)
        data_age.columns = ["Employment_" + "male_" + age + "_" + col for col in data_age.columns]
        data_age.columns = [x + "_" + y for x, y in zip(data_age.columns, categories)]
       
        allBranches.append(data_age)

    data_all = pd.concat(allBranches, axis=1)

    data_all.to_csv(output_data_main_data_file + "cbs_employment_males_mo.csv")


    #############################################
    #############################################

    categories = ['Labor_Force', 'Employed_Labor_Force', 'Unemployed_Labor_Force', "UnemplyRate", "Not_in_Labor_Force", "Gross_Labor_Particp", "Net_Labor_Particp"]
    allBranches = []
    for age in data_female['Age'].unique():
        data_age = data_female[data_female['Age'] == age]
        data_age = data_age.set_index(pd.date_range(start = start_date, periods = data_age.shape[0], freq = "M").to_period('M'))
        data_age.index = pd.PeriodIndex(data_age.index, freq='M').to_timestamp()
        wantThese = [col for col in data_age.columns if "Not" not in col]
        data_age = data_age[wantThese]
        data_age.drop(columns = ['Sex', 'Age'], inplace = True)
        data_age.columns = ["Employment_" + "female_" + age + "_" + col for col in data_age.columns]
        data_age.columns = [x + "_" + y for x, y in zip(data_age.columns, categories)]
       
        allBranches.append(data_age)

    data_all = pd.concat(allBranches, axis=1)

    data_all.to_csv(output_data_main_data_file + "cbs_employment_females_mo.csv")

    return None

macro_data_cbs(identifier = '80590eng', verbose = False)