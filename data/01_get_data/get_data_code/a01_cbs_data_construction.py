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
output_data_main_data_file = r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/mo_data//"

print("construction data english")

def macro_data_cbs(identifier, verbose = False):
    start_date = '01/01/2005'

    # get data
    data = pd.DataFrame(cbsodata.get_data(identifier))

    if verbose:
        info = cbsodata.get_info(identifier)
        print(info)
        tables = pd.DataFrame(cbsodata.get_table_list())
        columns_unprocessed = data.columns
        print("Columns unprocessed: ", len(columns_unprocessed))
        print(data.Periods)

    # want quarters
    data = data[~data['Periods'].str.isnumeric()]
    data = data[~data['Periods'].str.contains('quarter')]
    data = data[data['EnterpriseSize'] == 'Total 1 or more employed persons']

    # drop unnecessary columns
    data.drop(columns = ['ID','Periods', 'EnterpriseSize'], inplace = True)

    allBranches = []
    for brnch in data['SectorBranchesSIC2008'].unique():
        data_brnch = data[data['SectorBranchesSIC2008'] == brnch]
        data_brnch = data_brnch.drop(columns = ['SectorBranchesSIC2008'])
        data_brnch = data_brnch.set_index(pd.date_range(start = start_date, periods = data_brnch.shape[0], freq = "M").to_period('M'))
        data_brnch.index = pd.PeriodIndex(data_brnch.index, freq='M').to_timestamp()
        data_brnch.columns = ["Construction_" + brnch + "_" + col for col in data_brnch.columns]
        allBranches.append(data_brnch)
        
    data = pd.concat(allBranches, axis=1)

    return data

construction = NLD_basic_macro_data = macro_data_cbs(identifier = '85809ENG', verbose = False)

construction.to_csv(output_data_main_data_file + "cbs_construction_mo.csv") 