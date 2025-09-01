import pandas as pd
import cbsodata
import matplotlib.pyplot as plt
import numpy as np
import functools as ft
import os
import warnings
warnings.filterwarnings("ignore")

##############################
# CPB World Trade
# https://www.cpb.nl/en/cpb-world-trade-monitor-february-2025
# trade weighted Euro Area
# DATA needs to be processed by hand, just over write: data/cpb_trade_data.csv
#############################

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

#### WHERE TO SAVE DATA
output_data = r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/mo_data//"
# Note that name of file must remain the same
data_input =  r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/data_by_hand/cpb_trade_data.csv"

##############################
# CPB World Trade
# Euro_Area_Exports_Imports_mo = pd.read_csv("https://www.cpb.nl/en/world-trade-monitor-december-2024")
# trade weighted Euro Area
# DATA needs to be processed by hand, just overwrite the data_input file above
#############################

print("cpb data")

def cpb_exports_imports(verbose = False):
   
    Euro_Area_Exports_Imports_mo = pd.read_csv(data_input)
    Euro_Area_Exports_Imports_mo = Euro_Area_Exports_Imports_mo.iloc[:,0:6]

    Euro_Area_Exports_Imports_mo.index = pd.date_range(start='01/01/2000', periods=Euro_Area_Exports_Imports_mo.shape[0], freq="M").to_period('M')

    Euro_Area_Exports_Imports_mo.index = pd.PeriodIndex(Euro_Area_Exports_Imports_mo.index, freq='M').to_timestamp()

    if verbose:
        print(Euro_Area_Exports_Imports_mo)

    Euro_Area_Exports_Imports_mo.to_csv(output_data + "cpb_Euro_Area_Exports_Imports_mo.csv")

cpb_exports_imports(False)