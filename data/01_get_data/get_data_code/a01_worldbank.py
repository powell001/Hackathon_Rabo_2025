#%pip install wbgapi
import pandas as pd
import requests
import wbgapi as wb
import io
import matplotlib.pyplot as plt
import openpyxl
import os
import warnings
warnings.filterwarnings("ignore")

settings = {'figure.figsize':(14,4),
            'figure.dpi':144,
            'figure.facecolor':'w',
            'axes.spines.top':False,
            'axes.spines.bottom':False,
            'axes.spines.left':False,
            'axes.spines.right':False,
            'axes.grid':True,
            'grid.linestyle':'--',
            'grid.linewidth':0.5, 
            'figure.constrained_layout.use':True}
plt.rcParams.update(settings)

#### WHERE TO SAVE DATA
output_data_monthly = r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/mo_data//"

print("world bank data")

wb.source.info()

myURL = 'https://thedocs.worldbank.org/en/doc/5d903e848db1d1b83e0ec8f744e55570-0350012021/related/CMO-Historical-Data-Monthly.xlsx'

s = requests.get(myURL).content
xl = pd.ExcelFile(io.BytesIO(s))
xl.sheet_names

data = xl.parse('Monthly Prices',skiprows=4)
data.drop(index=0,inplace=True)
data.drop(columns=["Unnamed: 0"], inplace=True)

data.index = pd.date_range("1960-01-01", periods=data.shape[0], freq="MS")

data = data.loc['1980-01-01':,:]
data_original = data.copy()

# data contains strings
cols1 = data_original.columns
data_original[cols1] = data_original[cols1].apply(pd.to_numeric,errors='coerce')

# barley sorghum bad data
data_original.drop(columns=["Barley","Sorghum"],inplace=True)

data_original.to_csv(output_data_monthly +"worldbank_commodityprices_mo.csv")