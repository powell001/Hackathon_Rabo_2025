import pandas as pd
import cbsodata
import matplotlib.pyplot as plt
import numpy as np
import functools as ft
from datetime import datetime
import os

import warnings
warnings.filterwarnings("ignore")

# https://opendata.cbs.nl/#/CBS/en/dataset/85937ENG/table


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
#
###################################

#### Where to save data and figures
output_data_main_data_file = r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/mo_data//"

print("household consumption data english")

def macro_data_cbs(identifier, verbose = False):
    start_date = '01/01/2000'

    # get data
    data = pd.DataFrame(cbsodata.get_data(identifier))

    if verbose:
        info = cbsodata.get_info(identifier)
        print(info)
        tables = pd.DataFrame(cbsodata.get_table_list())
        #tables.to_csv(output_data_mo + "cbs_table_list.csv")
        #data.to_csv(output_data_mo + "unprocessed_mo_data.csv")
        columns_unprocessed = data.columns
        print("Columns unprocessed: ", len(columns_unprocessed))
        print(data.Periods)

    # subsetting data rows data = data[data["TypeOfData"] == 'Prices of 2021 seasonally adjusted']

    # dont want quarters
    data = data[~data['Periods'].str.contains('quarter')]
    # dont want years
    data = data[~data['Periods'].str.isnumeric()]

    # rename columns
    data.rename(columns = {"Indices_1": "Volume_Index",
                           "VolumeChanges_2": "Volume_Changes_Index",
                           "VolumeChangesShoppingdayAdjusted_3": "Volume_Changes_Shoppingday_Adjusted_Index",
                           "Indices_4": "Value_Index",
                           "ValueChanges_5": "Value_Changes_Index",
                           "PriceChanges_6": "Price_Changes_Index"
    })

    data.drop(columns = ['ID','Periods'], inplace = True)
    
    all_categories = []
    for i in data['ConsumptionByHouseholds'].unique():
        category1 = data[data['ConsumptionByHouseholds'] == i]
        category1.index = pd.date_range(start = start_date, periods = category1.shape[0], freq = "M").to_period('M')
        category1.index = pd.PeriodIndex(category1.index, freq='M').to_timestamp()
        
        category1.drop(columns = ['ConsumptionByHouseholds'], inplace = True)

        category1.columns = [i + "_" + col for col in category1.columns]
        category1.columns = [col.replace(" ", "_") for col in category1.columns]

        all_categories.append(category1)

    all_data = pd.concat(all_categories, axis=1)

    # save to main data file to be combined with all other monthly data (note the _mo suffix)
    all_data.to_csv(output_data_main_data_file + "cbs_consumerConsumption_mo.csv")

    return all_data

consumerConsumption = NLD_basic_macro_data = macro_data_cbs(identifier = '85937ENG', verbose = False)