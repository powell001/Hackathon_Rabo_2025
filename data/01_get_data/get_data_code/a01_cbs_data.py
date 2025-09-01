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

###################################
# https://cbsodata.readthedocs.io/en/latest/readme_link.html
# chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://www.cpb.nl/sites/default/files/publicaties/download/cpb-technical-background-document-bvar-models-used-cpb.pdf
###################################

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

#### Where to save data and figures
output_data_main_data_file_mo = r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/mo_data//"
output_data_main_data_file_qt = r"C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/01_get_data/qt_data//"

############################
############################

def price_cbs(identifier = '83131NED', verbose = False):
    print("price_cbs")
 
    data = pd.DataFrame(cbsodata.get_data(identifier))

    data = data[data['Bestedingscategorieen'] == '000000 Alle bestedingen']
    data = data[(data['Perioden'].str.len()) > 4]

    if verbose:
        print(data)
        print(data.Perioden)
    ######################
    # Set data index
    ######################
    data.index = pd.date_range(start='01/01/1996', periods = data.shape[0], freq="M").to_period('M')
    cpi1 = data[['CPI_1', 'CPIAfgeleid_2', 'MaandmutatieCPI_3', 'MaandmutatieCPIAfgeleid_4']]

    # this adds one day, so end jan becomes first feb
    cpi1.index = pd.PeriodIndex(cpi1.index, freq='M').to_timestamp() #+ datetime.timedelta(days=1) #pd.offsets.MonthEnd()

    return cpi1

cpi_mo = price_cbs(verbose = False)
cpi_mo.to_csv(output_data_main_data_file_mo + "cbs_cpi_mo.csv")
cpi_mo[['MaandmutatieCPI_3', 'MaandmutatieCPIAfgeleid_4']]

############################
############################

def wage_cbs(identifier = '85917NED', verbose = False):
    print("wage_cbs, STOPPED, now using 85917NED")
    start_date = '01/01/1995'

    data = pd.DataFrame(cbsodata.get_data(identifier))

    if verbose:
        print(data)
        print(data.Perioden)

    data = data[data['BedrijfstakkenBranchesSBI2008'] == 'A-U Alle economische activiteiten']
    data = data[(data['Perioden'].str.len()) > 4]

    ######################
    # Set data index
    ######################
    data.index = pd.date_range(start=start_date, periods = data.shape[0], freq="Q").to_period('Q')

    # this adds one day, so end jan becomes first feb
    data.index = pd.PeriodIndex(data.index,freq='Q').to_timestamp()  # + datetime.timedelta(days=1) #pd.offsets.QuarterEnd()

    data = data[['BeloningSeizoengecorrigeerd_2', 'Loonkosten_7', 'BeloningVanWerknemers_8']]

    return data

wages_qt = wage_cbs(verbose = False)
wages_qt.to_csv(output_data_main_data_file_qt + "/cbs_wages_qt.csv")

############################
############################

def consumer_confidence_cbs(identifier = '83693NED', verbose = False):
    print("cbs_consumer_conf")
    
    data = pd.DataFrame(cbsodata.get_data(identifier))

    if verbose:
        print(data)
        data.to_csv("consumer_vertrouw.csv")

    data = data[(data['Perioden'].str.len()) > 4]
    data = data[['Consumentenvertrouwen_1', 'EconomischKlimaat_2', 'Koopbereidheid_3', 'EconomischeSituatieLaatste12Maanden_4', 'EconomischeSituatieKomende12Maanden_5', 'FinancieleSituatieLaatste12Maanden_6', 'FinancieleSituatieKomende12Maanden_7', 'GunstigeTijdVoorGroteAankopen_8']]

    ######################
    # Set data index
    ######################
    data.index = pd.date_range(start='04/01/1986', periods = data.shape[0], freq="M").to_period('M')

    # this adds one day, so end jan becomes first feb
    data.index = pd.PeriodIndex(data.index, freq='M').to_timestamp()  # + datetime.timedelta(days=1) #pd.offsets.MonthEnd()

    return data

consumer_confd_mo = consumer_confidence_cbs(verbose = False)
consumer_confd_mo.to_csv(output_data_main_data_file_mo +"cbs_consumer_confd_mo.csv")

############################
############################

def bankrupt_cbs(identifier = '82242NED', verbose = False):
    print("bankrupt_cbs")
    
    data = pd.DataFrame(cbsodata.get_data(identifier))

    if verbose:
        print(data)

    # remove jaardata
    data = data[(data['Perioden'].str.len()) > 4]
    # remove kwarteldata
    filter = data['Perioden'].str.contains('kwartaal')
    data = data[~filter]

    data = data[data['TypeGefailleerde'] == 'Totaal rechtsvormen Nederland/buitenland']
    data.drop(columns=['ID'], inplace=True)

    data = data[['UitgesprokenFaillissementen_1']]
    data.columns = ['Bankruptcies']

    ######################
    # Set data index
    ######################
    data.index = pd.date_range(start='01/01/1981', periods=data.shape[0], freq="M").to_period('M')

    # this adds one day, so end jan becomes first feb
    data.index = pd.PeriodIndex(data.index, freq='M').to_timestamp()  # + datetime.timedelta(days=1) #pd.offsets.MonthEnd()

    return data

bankrupt_mo = bankrupt_cbs(verbose = False)
bankrupt_mo.to_csv(output_data_main_data_file_mo + "cbs_bankrupt_mo.csv")

############################
############################

def producer_confidence( identifier = '81234eng', verbose = False):
    print("producer_confidence")
   
    data = pd.DataFrame(cbsodata.get_data(identifier))

    if verbose:
        print(data)

    data = data[data['SectorBranchesSIC2008'] =='C Manufacturing']
    data = data[data['Margins'] == 'Value']
    data = data[['Periods', 'ProducerConfidence_1', 'ExpectedActivity_2']]

    ######################
    # Set data index
    ######################
    data.index = pd.date_range(start='01/01/1985', periods=data.shape[0], freq="M").to_period('M')

    # this adds one day, so end jan becomes first feb
    data.index = pd.PeriodIndex(data.index, freq='M').to_timestamp()  # + datetime.timedelta(days=1) #pd.offsets.MonthEnd()
    data.drop(columns = ['Periods'], inplace = True)

    return data

producer_confd_mo = producer_confidence(verbose = False)
producer_confd_mo.to_csv(output_data_main_data_file_mo + "cbs_producer_confd_mo.csv")

############################
############################

def producer_confidence_2():

    print("producer_confidence_2")

    identifier = '85612ENG'
    data = pd.DataFrame(cbsodata.get_data(identifier))
    all_sectors1 = data['SectorBranchesSBI2008'].unique()

    all_sect_bc_1 = []
    for sec in all_sectors1:
        data = pd.DataFrame(cbsodata.get_data(identifier))
        data = data[data['SectorBranchesSBI2008'] == sec]
        data.index = pd.date_range(start='01/01/2012', periods=data.shape[0], freq="M").to_period('M').to_timestamp()
        data = data[data['Margins'] == "Value"]
        bus_conf_1 = data.loc[:,"BusinessConfidence_1"]
        bus_conf_1.dropna()
        all_sect_bc_1.append(bus_conf_1)

    bc_1 = pd.concat(all_sect_bc_1, axis=1)
    bc_1.columns = all_sectors1


    qt_data = ['All enterprises (no finance or energy)',
                'A Agriculture, forestry and fishing',
                'B Mining and quarrying',
                'C Industry, H-S services and 45+47',
                'C Manufacturing',
                'F Construction',	
                'G Wholesale and retail trade',	
                '45 Sale and repair of motor vehicles',
                '46 Wholesale trade (no motor vehicles)',	
                '47 Retail trade (not in motor vehicles)']

    mo_data = ['H-S Sevices',
                'H Transportation and storage',
                'I Accommodation and food serving',
                'J Information and communication',	
                'L Renting, buying, selling real estate',	
                'M-N Business services',
                'R Culture, sports and recreation',	
                'S Other service activities']



    bc_1_qt = bc_1[qt_data]
    bc_1_qt.dropna(inplace = True)
    # make columns unique
    bc_1_qt.columns = [col + "_BusinessConfidence" for col in bc_1_qt.columns]
    bc_1_qt.to_csv(output_data_main_data_file_qt + "cbs_BusinessConfidence_qt.csv")

    bc_1_mo = bc_1[mo_data]
    bc_1_mo.columns = [col + "_BusinessConfidence" for col in bc_1_mo.columns]
    bc_1_mo.to_csv(output_data_main_data_file_mo + "cbs_BusinessConfidence_mo.csv")


producer_confidence_2()

############################
############################

def producer_confidence_3():

    print("producer_confidence_3")

    identifier = '85612ENG'
    data = pd.DataFrame(cbsodata.get_data(identifier))
    all_sectors1 = data['SectorBranchesSBI2008'].unique()

    all_sect_bc_1 = []
    for sec in all_sectors1:
        data = pd.DataFrame(cbsodata.get_data(identifier))
        data = data[data['SectorBranchesSBI2008'] == sec]
        data.index = pd.date_range(start='01/01/2012', periods=data.shape[0], freq="M").to_period('M').to_timestamp()
        data = data[data['Margins'] == "Value"]
        bus_conf_1 = data.loc[:,"BusinessSituationPastThreeMonths_2"]
        bus_conf_1.dropna()
        all_sect_bc_1.append(bus_conf_1)

    bc_1 = pd.concat(all_sect_bc_1, axis=1)
    bc_1.columns = all_sectors1

    qt_data = ['All enterprises (no finance or energy)',
                'A Agriculture, forestry and fishing',
                'B Mining and quarrying',
                'C Industry, H-S services and 45+47',
                'C Manufacturing',
                'F Construction',	
                'G Wholesale and retail trade',	
                '45 Sale and repair of motor vehicles',
                '46 Wholesale trade (no motor vehicles)',	
                '47 Retail trade (not in motor vehicles)']

    mo_data = ['H-S Sevices',
                'H Transportation and storage',
                'I Accommodation and food serving',
                'J Information and communication',	
                'L Renting, buying, selling real estate',	
                'M-N Business services',
                'R Culture, sports and recreation',	
                'S Other service activities']			

    bc_1_qt = bc_1[qt_data]
    bc_1_qt.dropna(inplace = True)
    # make columns unique
    bc_1_qt.columns = [col + "BusinessSituationPastThreeMonths" for col in bc_1_qt.columns]
    bc_1_qt.to_csv(output_data_main_data_file_qt + "cbs_BusinessSituationPastThreeMonths_qt.csv")

    bc_1_mo = bc_1[mo_data]
    bc_1_mo.columns = [col + "BusinessSituationPastThreeMonths" for col in bc_1_mo.columns]
    bc_1_mo.to_csv(output_data_main_data_file_mo + "cbs_BusinessSituationPastThreeMonths_mo.csv")

producer_confidence_3()

############################
############################

def producer_confidence_4():

    print("producer_confidence_4")

    identifier = '85612ENG'
    data = pd.DataFrame(cbsodata.get_data(identifier))
    all_sectors1 = data['SectorBranchesSBI2008'].unique()

    all_sect_bc_1 = []
    for sec in all_sectors1:
        data = pd.DataFrame(cbsodata.get_data(identifier))
        data = data[data['SectorBranchesSBI2008'] == sec]
        data.index = pd.date_range(start='01/01/2012', periods=data.shape[0], freq="M").to_period('M').to_timestamp()
        data = data[data['Margins'] == "Value"]
        bus_conf_1 = data.loc[:,"BusinessSituationNextThreeMonths_3"]
        bus_conf_1.dropna()
        all_sect_bc_1.append(bus_conf_1)

    bc_1 = pd.concat(all_sect_bc_1, axis=1)
    bc_1.columns = all_sectors1

    qt_data = ['All enterprises (no finance or energy)',
                'A Agriculture, forestry and fishing',
                'B Mining and quarrying',
                'C Industry, H-S services and 45+47',
                'C Manufacturing',
                'F Construction',	
                'G Wholesale and retail trade',	
                '45 Sale and repair of motor vehicles',
                '46 Wholesale trade (no motor vehicles)',	
                '47 Retail trade (not in motor vehicles)']

    mo_data = ['H-S Sevices',
                'H Transportation and storage',
                'I Accommodation and food serving',
                'J Information and communication',	
                'L Renting, buying, selling real estate',	
                'M-N Business services',
                'R Culture, sports and recreation',	
                'S Other service activities']


    bc_1_qt = bc_1[qt_data]
    bc_1_qt.dropna(inplace = True)
    # make columns unique
    bc_1_qt.columns = [col + "BusinessSituationNextThreeMonths" for col in bc_1_qt.columns]
    bc_1_qt.to_csv(output_data_main_data_file_qt + "cbs_BusinessSituationNextThreeMonths_qt.csv")

    bc_1_mo = bc_1[mo_data]
    bc_1_mo.columns = [col + "BusinessSituationNextThreeMonths" for col in bc_1_mo.columns]
    bc_1_mo.to_csv(output_data_main_data_file_mo + "cbs_BusinessSituationNextThreeMonths_mo.csv")


producer_confidence_4()


############################
############################

def producer_confidence_5():

    print("producer_confidence_5")

    identifier = '85612ENG'
    data = pd.DataFrame(cbsodata.get_data(identifier))
    all_sectors1 = data['SectorBranchesSBI2008'].unique()

    all_sect_bc_1 = []
    for sec in all_sectors1:
        data = pd.DataFrame(cbsodata.get_data(identifier))
        data = data[data['SectorBranchesSBI2008'] == sec]
        data.index = pd.date_range(start='01/01/2012', periods=data.shape[0], freq="M").to_period('M').to_timestamp()
        data = data[data['Margins'] == "Value"]
        bus_conf_1 = data.loc[:,"UncertaintyIndicatorBusinessClimate_4"]
        bus_conf_1.dropna()
        all_sect_bc_1.append(bus_conf_1)

    bc_1 = pd.concat(all_sect_bc_1, axis=1)
    bc_1.columns = all_sectors1


    qt_data = ['A Agriculture, forestry and fishing',
            'B Mining and quarrying',
            'G Wholesale and retail trade',	
            '46 Wholesale trade (no motor vehicles)']
                

    mo_data = [
                'C Industry, H-S services and 45+47',
                'C Manufacturing',
                '45 Sale and repair of motor vehicles',
                '47 Retail trade (not in motor vehicles)',
                'H-S Sevices',
                'H Transportation and storage',
                'I Accommodation and food serving',
                'J Information and communication',	
                'L Renting, buying, selling real estate',	
                'M-N Business services',
                'R Culture, sports and recreation',	
                'S Other service activities']						

    bc_1_qt = bc_1[qt_data]
    bc_1_qt.dropna(inplace = True)
    # make columns unique
    bc_1_qt.columns = [col + "_UncertaintyIndicatorBusinessClimate" for col in bc_1_qt.columns]
    bc_1_qt.to_csv(output_data_main_data_file_qt + "cbs_UncertaintyIndicatorBusinessClimate_qt.csv")

    bc_1_mo = bc_1[mo_data]
    bc_1_mo.columns = [col + "_UncertaintyIndicatorBusinessClimate" for col in bc_1_mo.columns]
    bc_1_mo.to_csv(output_data_main_data_file_mo + "cbs_UncertaintyIndicatorBusinessClimate_mo.csv")

producer_confidence_5()


