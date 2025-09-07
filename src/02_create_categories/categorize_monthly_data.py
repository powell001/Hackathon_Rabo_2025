import pandas as pd
import itertools

# The idea is to create component categories.  First establish general categories based on the data, 
# run PCA to determine the principal components for each category, and then use those components in
# further analyses.  Let's see what happens.

output_file = r"C:\Users\jpark\vscode\Hackathon_Rabo_2025\src\02_create_categories\data\monthly_data_categorized.csv"


###################
# Create Categories
###################

####
# Monthly data
####

monthData = pd.read_csv(r"C:\Users\jpark\vscode\Hackathon_Rabo_2025\data\02_processed_data\a0_combinedMonthly_use_this.csv", index_col=0, parse_dates=True)
monthData_categorized = monthData.copy()

# Bankruptcies
Bankruptcies = ["Bankruptcies"]

# Consumer Consumption
ConsumerConsumption = ["Domestic_consumption_by_households_VolumeChangesShoppingdayAdjusted_3",
'Consumption_of_goods_by_households_VolumeChangesShoppingdayAdjusted_3',
'Foodproducts,_beverages_and_tabacco_VolumeChangesShoppingdayAdjusted_3',
'Durable_consumer_goods_VolumeChangesShoppingdayAdjusted_3',
'Textiles_and_clothing_VolumeChanges_2',
'Leather_goods_and_footwear_VolumeChanges_2',
'Home_furnishing_and_home_decoration_VolumeChanges_2',
'Electrical_equipment_VolumeChanges_2',
'Vehicles_VolumeChanges_2',
'Other_goods_VolumeChangesShoppingdayAdjusted_3',
'Electricity,_gas,_water_and_motor_fuels_VolumeChanges_2',
'Personal_care_and_other_goods_VolumeChanges_2',
'Consumption_of_services_by_households_VolumeChangesShoppingdayAdjusted_3']

# Consumer confidence
ConsumerConfidence = ['Consumentenvertrouwen_1',
'EconomischKlimaat_2',
 'Koopbereidheid_3',
 'EconomischeSituatieLaatste12Maanden_4',
 'EconomischeSituatieKomende12Maanden_5',
 'FinancieleSituatieLaatste12Maanden_6',
 'FinancieleSituatieKomende12Maanden_7',
 'GunstigeTijdVoorGroteAankopen_8']

# CPI
CPI = ['CPI_1']

# Employment
Employment = ['Employment_allGenders_15 to 74 years_SeasonallyAdjusted_8_UnemplyRate',
 'Employment_allGenders_15 to 74 years_SeasonallyAdjusted_12_Gross_Labor_Particp',
 'Employment_allGenders_15 to 74 years_SeasonallyAdjusted_14_Net_Labor_Particp',
 'Employment_allGenders_15 to 24 years_SeasonallyAdjusted_8_UnemplyRate',
 'Employment_allGenders_25 to 44 years_SeasonallyAdjusted_8_UnemplyRate',
 'Employment_allGenders_45 to 74 years_SeasonallyAdjusted_8_UnemplyRate',
 'Employment_allGenders_45 to 74 years_SeasonallyAdjusted_12_Gross_Labor_Particp',
 'Employment_allGenders_45 to 74 years_SeasonallyAdjusted_14_Net_Labor_Particp',
 'Employment_female_15 to 74 years_SeasonallyAdjusted_8_UnemplyRate',
 'Employment_female_15 to 74 years_SeasonallyAdjusted_12_Gross_Labor_Particp',
 'Employment_female_15 to 74 years_SeasonallyAdjusted_14_Net_Labor_Particp',
 'Employment_female_15 to 24 years_SeasonallyAdjusted_6_Unemployed_Labor_Force',
 'Employment_female_15 to 24 years_SeasonallyAdjusted_8_UnemplyRate',
 'Employment_female_25 to 44 years_SeasonallyAdjusted_8_UnemplyRate',
 'Employment_female_45 to 74 years_SeasonallyAdjusted_6_Unemployed_Labor_Force',
 'Employment_female_45 to 74 years_SeasonallyAdjusted_8_UnemplyRate',
 'Employment_female_45 to 74 years_SeasonallyAdjusted_12_Gross_Labor_Particp',
 'Employment_female_45 to 74 years_SeasonallyAdjusted_14_Net_Labor_Particp']

# Producer Confidence
ProducerConfidence = ['ProducerConfidence_1',
 'ExpectedActivity_2']

# Business Interest Rates
BusinessInterestRates = ['BigBusinessInterestRate',
 'Deposit rate',
 'Main refinancing operations: Variable rate tenders weighted average interest rate',
 'Marginal lending rate',
 'Main refinancing operations: Variable rate tenders marginal interest rate',
 'Main refinancing operations: Fixed rate tenders',
 'Main refinancing operations: Variable rate tenders minimum bid rate',
 'Rente op uitstaande bedragen (percentages)',
 'HousingInterestRatesNLD']

# Money supply
MoneySupply = ['M3_1',
 'M3_2',
 'M1']

# Net Savings
NetSavings = ['NetSavings']

# International Construction Confidence
InternationalConstructionConfidence = ['BE_Construction_confidence',
 'DE_Construction_confidence',
 'EE_Construction_confidence',	
 'ES_Construction_confidence',	
 'FR_Construction_confidence',
 'IT_Construction_confidence',
 'NL_Construction_confidence']

# International Consumer Confidence
InternationalConsumerConfidence = ['BE_Consumer_confidence',
 'DE_Consumer_confidence',
 'EE_Consumer_confidence',
 'ES_Consumer_confidence',
 'FR_Consumer_confidence',
 'IT_Consumer_confidence',
 'NL_Consumer_confidence']

 # International Economic Sentiment
InternationalEconomicSentiment = ['BE_Economic_sentiment_confidence',
  'DE_Economic_sentiment_confidence',
  'EE_Economic_sentiment_confidence',
  'ES_Economic_sentiment_confidence',
  'FR_Economic_sentiment_confidence',
  'IT_Economic_sentiment_confidence',
  'NL_Economic_sentiment_confidence']

# International Industrial Confidence
InternationalIndustrialConfidence = ['BE_Industrial_confidence',
 'DE_Industrial_confidence',
 'EE_Industrial_confidence',
 'ES_Industrial_confidence',
 'FR_Industrial_confidence',
 'IT_Industrial_confidence',
 'NL_Industrial_confidence']

# International Retail Confidence
InternationalRetailConfidence = ['BE_Retail_confidence',
  'DE_Retail_confidence',
  'EE_Retail_confidence',
  'ES_Retail_confidence',
  'FR_Retail_confidence',
  'IT_Retail_confidence',
  'NL_Retail_confidence']

# International Services Confidence
InternationalServicesConfidence = ['BE_Service_confidence',
   'DE_Service_confidence',
   'EE_Service_confidence',
   'ES_Service_confidence',
   'FR_Service_confidence',
   'IT_Service_confidence',
   'NL_Service_confidence']

# International Inflation
InternationalInflation = ['BE_Inflation',
 'DE_Inflation',
 'EE_Inflation',
 'ES_Inflation',
 'FR_Inflation',
 'IT_Inflation',
 'NL_Inflation']

# International long term bond yields
InternationalLongTermBondYields = ['Belgium_longtermBondYield',
 'Germany_longtermBondYield',
 'Spain_longtermBondYield',
 'France_longtermBondYield',
 'Italy_longtermBondYield',
 'Netherlands_longtermBondYield']

# International MoneyMarketIntRates
InternationalMoneyMarketIntRates = ['EuropeanArea_MoneyMarketIntRates_Intr_M1',
 'EuropeanArea_MoneyMarketIntRates_Intr_M12',
 'EuropeanArea_MoneyMarketIntRates_Intr_M3',
 'EuropeanArea_MoneyMarketIntRates_Intr_M6']

# Leading economic indicators
LeadingEconomicIndicators = ['ConsumLeadIndicator_NLD',
 'BusinessLeadIndicator_NLD',
 'BusinessLeadIndicator_DEU',
 'ConsumLeadIndicator_DEU']

# International Unemployment Indicators
InternationalUnemploymentIndicators = ['Germany_unemply_F',
 'Germany_unemply_M',
 'France_unemply_F',
 'France_unemply_M',
 'Italy_unemply_F',
 'Italy_unemply_M',
 'Spain_unemply_F',
 'Spain_unemply_M',
 'Belgium_unemply_F',
 'Belgium_unemply_M',
 'Japan_unemply_F',
 'Japan_unemply_M',
 'United States_unemply_F',
 'United States_unemply_M']

# International Energy Indicators
InternationalEnergyIndicators = ['Crude oil, average',
 'Crude oil, Brent',
 'Crude oil, Dubai',
 'Crude oil, WTI',
 'Coal, Australian',
 'Coal, South African **',
 'Natural gas, US',
 'Natural gas, Europe',
 'Liquefied natural gas, Japan',
 'Natural gas index'
]

# International Metals
InternationalMetals = ['Aluminum',
 'Iron ore, cfr spot',
 'Copper',
 'Lead',
 'Tin',
 'Nickel',
 'Zinc',
 'Gold',
 'Platinum',
 'Silver']

categories       = [Bankruptcies, ConsumerConsumption, ConsumerConfidence, CPI, Employment, ProducerConfidence, BusinessInterestRates, MoneySupply, InternationalMoneyMarketIntRates, LeadingEconomicIndicators, InternationalUnemploymentIndicators, InternationalEnergyIndicators, InternationalMetals]
categories_names = ['Bankruptcies', 'ConsumerConsumption', 'ConsumerConfidence', 'CPI', 'Employment', 'ProducerConfidence', 'BusinessInterestRates', 'MoneySupply', 'InternationalMoneyMarketIntRates', 'LeadingEconomicIndicators', 'InternationalUnemploymentIndicators', 'InternationalEnergyIndicators', 'InternationalMetals']

# combine lists into one large list
categories_combine = itertools.chain(*categories)

# select relevant columns from monthData_categorized
monthData_categorized = monthData_categorized[categories_combine]

# add category name to columns
monthData_categorized_names = list()
for enum, cat1 in enumerate(categories):
    dt1 = monthData_categorized.loc[:,monthData_categorized.columns.isin(cat1)]
    dt1.columns = [categories_names[enum] + '_' + col for col in dt1.columns]
    monthData_categorized_names.append(dt1)

monthData_categorized = pd.concat(monthData_categorized_names, axis=1)
monthData_categorized.to_csv(output_file)
