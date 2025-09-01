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
# https://cbsodata.readthedocs.io/en/latest/readme_link.html
# chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://www.cpb.nl/sites/default/files/publicaties/download/cpb-technical-background-document-bvar-models-used-cpb.pdf
###################################

#### Where to save data and figures
output_data_qt = r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/qt_data//"
output_data_mo = r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/mo_data//"
output_figures = r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/output/figures/rawdata//"

print("cbs with seasons removed data english")

# https://opendata.cbs.nl/statline#/CBS/nl/dataset/85879NED/table?ts=1696490590802

def macro_data_cbs(identifier, verbose = False):
    start_date = '01/01/1995'

    # get data
    data = pd.DataFrame(cbsodata.get_data(identifier))

    if verbose:
        info = cbsodata.get_info(identifier)
        print(info)
        tables = pd.DataFrame(cbsodata.get_table_list())
        tables.to_csv(output_data_qt + "cbs_table_list.csv")
        data.to_csv(output_data_qt + "unprocessed_qt_data.csv")
        columns_unprocessed = data.columns
        print("Columns unprocessed: ", len(columns_unprocessed))
        print(data.Periods)

    # subsetting data rows
    data = data[data["TypeOfData"] == 'Prices of 2021 seasonally adjusted']
    data = data[data['Periods'].str.contains('quarter')]
    data.index = pd.date_range(start = start_date, periods = data.shape[0], freq = "Q").to_period('Q')

    all_data = data
    # remove ID column
    all_data.drop(columns = ['ID','TypeOfData','Periods'], inplace = True)

    ######################
    # Set data index
    ######################
    all_data.index = pd.date_range(start=start_date, periods = all_data.shape[0], freq="Q").to_period('Q')
    all_data.index = pd.PeriodIndex(all_data.index, freq='Q').to_timestamp() 

    ######################
    # Adjust column names for later processing
    ######################
    all_data.columns = [col + "_seasonCorrected" for col in all_data.columns]

    # Have columns been added or removed?
    if verbose:
        assert len(columns_unprocessed) == len(all_data.columns) + 3 #three columns dropped above

    return all_data

NLD_basic_macro_data = macro_data_cbs(identifier = '85879ENG', verbose = False)

print("NLD_basic_macro_data shape: ", NLD_basic_macro_data.shape)

a1 = NLD_basic_macro_data.columns[0:17] + "_expenditure"
a2 = NLD_basic_macro_data.columns[17:63] + "_production"
a3 = NLD_basic_macro_data.columns[63:71] + "_income"
a4 = NLD_basic_macro_data.columns[71:100] + "_balance"
a5 = NLD_basic_macro_data.columns[100:] + "_additional"

newcolumns = a1.to_list() + a2.to_list() + a3.to_list() + a4.to_list() + a5.to_list()
NLD_basic_macro_data.columns = newcolumns

NLD_basic_macro_data.to_csv(output_data_qt + "/cbs_basic_macro_SEASONCORRECTED_english_qt.csv")

###################################
###################################






