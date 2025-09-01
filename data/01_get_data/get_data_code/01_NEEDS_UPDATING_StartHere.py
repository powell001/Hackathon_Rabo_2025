######
# remove files
######
import os
import glob

#############################################
# Remove previous files !!!! 
#############################################

def remove_files(file_folder):

    files = glob.glob(os.path.abspath(file_folder) + "/*")
    for f in files:
        print(f)
        if f != "__init__.py":
            os.remove(f)

output_files_mo = r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/mo_data/"
output_files_qt = r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/qt_data/"
remove_files(output_files_mo)
remove_files(output_files_qt)

######
# Python
######

import a01_cbs_data_seasons_removed_english
# import a01_cbs_data_withseasons_dutch
# import a01_cbs_data_withseasons_english
import a01_cbs_data
import a01_cpb
import a01_dnb_fed
import a01_eurostat
import a01_worldbank
# import a01_yfinance
import a01_cbs_data_construction
import a01_cbs_data_employment
import a01_cbs_data_household_consumption
import a01_cbs_data_nationalAccounts

######
# R
######

import rpy2.robjects as robjects
r = robjects.r
r.source("C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/get_data_code/a01_oecd.R")

######
# Must be last file
######

import a02_combine
