import os
import pandas as pd
import functools as ft

print("Combining data")

#############################
# Monthly data
#############################

def mo_data():

    input_path_mo =  r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/mo_data//"
    input_path_qt =  r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/qt_data//"
    output_path =    r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/02_processed_data//"

    filesall = os.listdir(input_path_mo)

    listoffiles = []
    for enum, i in enumerate(filesall):
        if "_mo" in i:
            data = pd.read_csv(input_path_mo + i,  index_col=[0])
            data.index.name = ''
            listoffiles.append(data)

    df_final_mo = ft.reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how = 'outer'), listoffiles)

    df_final_mo = df_final_mo.loc['1995-01-01':, :]  

    df_final_mo = df_final_mo.interpolate(limit_direction='both', limit_area='inside') 

    df_final_mo.interpolate(method='linear', limit_direction='forward', axis=0)
    cols_before_removing = df_final_mo.columns

    # remove empty columns or columns with little data
    print("Number of month columns, rows, before removing: ", len(df_final_mo.columns), df_final_mo.shape[0])
   
    df_final_mo.to_csv(output_path + "a0_alldata_combinedMonthly.csv")

    
    # drop data
    uptoXemptyrows = 250
    df_final_mo.dropna(thresh = uptoXemptyrows, axis=1, inplace=True) #########################################################
    col_after_removing = df_final_mo.columns

    print("Number of month columns, rows, after removing: ", len(col_after_removing), df_final_mo.shape[0])

    df_final_mo.to_csv(output_path + "a0_combinedMonthly_use_this.csv")

mo_data()

###########################################
###########################################
###########################################


#############################
# Quarterly data
#############################

def qt_data():

    input_path_mo =  r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/mo_data//"
    input_path_qt =  r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/qt_data//"
    output_path =    r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/02_processed_data//"


    filesall = os.listdir(input_path_qt)

    listoffiles = []
    for enum, i in enumerate(filesall):
        if "_qt" in i:
            data = pd.read_csv(input_path_qt + i,  index_col=[0])
            data.index.name = ''
            listoffiles.append(data)


    df_final_qt = ft.reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how = 'outer'), listoffiles)

    df_final_qt = df_final_qt.loc['1995-01-01':, :]  ##############

    df_final_qt = df_final_qt.interpolate(limit_direction='both', limit_area='inside') ##############
    col_before_removing = df_final_qt.columns


    # remove empty columns or columns with little data
    print("Number of quarter columns, rows, before removing: ", len(df_final_qt.columns), df_final_qt.shape[0])
    df_final_qt.to_csv(output_path + "a0_alldata_combinedQuarterly.csv")

    # drop data
    uptoXemptyrows = 100
    df_final_qt.dropna(thresh=len(df_final_qt) - uptoXemptyrows, axis=1, inplace=True)
    col_after_removing = df_final_qt.columns

    #print("Columns removed: ", set(col_before_removing) - set(col_after_removing))
    print("Number of quarter columns, rows, after removing: ", len(col_after_removing), df_final_qt.shape[0])

    df_final_qt.to_csv(output_path + "a0_combinedQuarterly_use_this.csv")

qt_data()



