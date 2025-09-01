######
# remove files
######
import os
import glob

####
# Remove files
####
output_files = r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/02_processed_data/test//"

files = glob.glob(os.path.abspath(output_files))

for f in files:
    print(f)
    if f != "__init__.py":
        os.remove(f)

######
# Python
######

import a01_cbs_data_seasons_removed_english
#import a01_cbs_data_withseasons_dutch
import a01_cbs_data_withseasons_english
import a01_cbs_data
import a01_cpb
import a01_dnb_fed
import a01_eurostat
import a01_worldbank
import a01_yfinance

######
# R
######

import rpy2.robjects as robjects
r = robjects.r
r.source("C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/get_data_code/a01_oecd.R")

# ######
# # Must be last file
# ######

import a02_combine
