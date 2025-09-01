import os

######
# R (Run in Python)
######

import rpy2.robjects as robjects
r = robjects.r

file_path = r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/src/01_ets_extend_data/" 

r.source(file_path + 'a01_1_forecast_month_ETS_v2.R')
r.source(file_path + 'a01_2_analyses_month_ETS.R')
r.source(file_path + 'a02_1_forecast_quarter_ETS_v2.R')
r.source(file_path + 'a02_2_analyses_quarter_ETS.R')
r.source(file_path + 'a03_month_quarter_auto_arima.R')
r.source(file_path + 'a04_convertGDPToMonthlyData.R')
r.source(file_path + 'a04_convertQuarterlytoMonthly.R')






























