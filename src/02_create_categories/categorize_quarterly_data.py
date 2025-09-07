import pandas as pd
import itertools

# The idea is to create component categories.  First establish general categories based on the data, 
# run PCA to determine the principal components for each category, and then use those components in
# further analyses.  Let's see what happens.

output_file = r"C:\Users\jpark\vscode\Hackathon_Rabo_2025\src\02_create_categories\data\quarterly_toMonthlydata_categorized.csv"


###################
# Create Categories
###################

####
# Quarterly data
####

quarterlyData = pd.read_csv(r"C:\Users\jpark\vscode\Hackathon_Rabo_2025\final_forecasts\gdp_QuarterlyData_to_MonthlyData.csv", index_col='X', parse_dates=True)
quarterlyData_categorized = quarterlyData.copy()

quarterlyData_categorized.columns = [col for col in quarterlyData_categorized.columns.str.replace('.', ' ')]
quarterlyData_categorized.columns = [col for col in quarterlyData_categorized.columns.str.replace(',', ' ')]
quarterlyData_categorized.columns = [col for col in quarterlyData_categorized.columns.str.replace('+', ' ')]

print(quarterlyData_categorized.columns.tolist())

#quarterlyData_categorized.to_csv("tmp122121.csv")

# NonFinancialCorporations
NonFinancialCorporations = ["GrossValueAdded_12", 
                            "GrossOperatingSurplus_13", 
                            "GrossProfitsBeforeTaxes_14", 
                            "ProfitsFromForeignSubsidiaries_15"]

NonFinancialCorporations_ratios = ["ProfitRatio_16", "CapitalFormationRatio_17"]

# FinancialCorporations
FinancialCorporations = ["GrossValueAdded_19", 
                         "GrossProfitsBeforeTaxes_20", 
                         "ProfitsFromForeignSubsidiaries_21", 
                         "FinancialNetWorth_22", 
                         "PropertyIncomeReceived_23", 
                         "PropertyIncomePaid_24",
                         "FinancialAssetsOfPensionFunds_26"]

# Macro Components
MarcoComponents = ["GrossDomesticProduct_2_seasonCorrected_expenditure", # GDP
 "Total_3_seasonCorrected_expenditure", # total imports
 "ImportsOfGoods_4_seasonCorrected_expenditure", # imports of goods
 "ImportsOfServices_5_seasonCorrected_expenditure", # imports of services
 "HouseholdsIncludingNPISHs_9_seasonCorrected_expenditure", # households including NPISHs
 "GeneralGovernment_10_seasonCorrected_expenditure", # general government
 "Total_11_seasonCorrected_expenditure", # total investments
 "EnterprisesAndHouseholds_12_seasonCorrected_expenditure", # investments enterprises and households
 "GeneralGovernment_13_seasonCorrected_expenditure", # investment government
 "ChangesInInventoriesInclValuables_14_seasonCorrected_expenditure", # changes in inventories
 "ExportsOfGoods_16_seasonCorrected_expenditure", # exports of goods
 "ExportsOfServices_17_seasonCorrected_expenditure" # exports of services
]

# Sector production
SectorProduction = ["AAgricultureForestryAndFishing_20_seasonCorrected_production", 
 "BMiningAndQuarrying_22_seasonCorrected_production",  
 "DElectricityAndGasSupply_35_seasonCorrected_production", 
 "EWaterSupplyAndWasteManagement_36_seasonCorrected_production", 
 "FConstruction_37_seasonCorrected_production", 
 "JInformationAndCommunication_43_seasonCorrected_production", 
 "KFinancialInstitutions_44_seasonCorrected_production", 
 "LRentingBuyingSellingRealEstate_45_seasonCorrected_production", 
 "RUCultureRecreationOtherServices_59_seasonCorrected_production", 
 "TaxesLessSubsidiesOnProducts_60_seasonCorrected_production", 
 "TaxesOnProducts_61_seasonCorrected_production"]

# Business Confidence
BusinessConfidence = ["All enterprises  no finance or energy _BusinessConfidence", 
                      "A Agriculture  forestry and fishing_BusinessConfidence", 
                      "B Mining and quarrying_BusinessConfidence", 
                      "C Industry  H S services and 45 47_BusinessConfidence", 
                      "C Manufacturing_BusinessConfidence", 
                      "F Construction_BusinessConfidence", 
                      "G Wholesale and retail trade_BusinessConfidence", 
                      "X45 Sale and repair of motor vehicles_BusinessConfidence", 
                      "X46 Wholesale trade  no motor vehicles _BusinessConfidence", 
                      "X47 Retail trade  not in motor vehicles _BusinessConfidence"]


# Business Situation Next Three Months


BusinessSituationNextThreeMonths = ["All enterprises  no finance or energy BusinessSituationNextThreeMonths",
 "A Agriculture  forestry and fishingBusinessSituationNextThreeMonths",
 "B Mining and quarryingBusinessSituationNextThreeMonths",
 "C Industry  H S services and 45 47BusinessSituationNextThreeMonths",
 "C ManufacturingBusinessSituationNextThreeMonths",
 "F ConstructionBusinessSituationNextThreeMonths",
 "G Wholesale and retail tradeBusinessSituationNextThreeMonths",
 "X45 Sale and repair of motor vehiclesBusinessSituationNextThreeMonths",
 "X46 Wholesale trade  no motor vehicles BusinessSituationNextThreeMonths",
 "X47 Retail trade  not in motor vehicles BusinessSituationNextThreeMonths"
]


# Business Situation Past Three Months
BusinessSituationPastThreeMonths = ["All enterprises  no finance or energy BusinessSituationPastThreeMonths",
 "A Agriculture  forestry and fishingBusinessSituationPastThreeMonths",
 "B Mining and quarryingBusinessSituationPastThreeMonths",
 "C Industry  H S services and 45 47BusinessSituationPastThreeMonths",
 "C ManufacturingBusinessSituationPastThreeMonths",
 "F ConstructionBusinessSituationPastThreeMonths",
 "G Wholesale and retail tradeBusinessSituationPastThreeMonths",
 "X45 Sale and repair of motor vehiclesBusinessSituationPastThreeMonths",
 "X46 Wholesale trade  no motor vehicles BusinessSituationPastThreeMonths",
 "X47 Retail trade  not in motor vehicles BusinessSituationPastThreeMonths"
]

# BeloningSeizoengecorrigeerd_2
BeloningSeizoengecorrigeerd = ["BeloningSeizoengecorrigeerd_2"]

 # International GDP
InternationalGDP = ["Germany_GDP", 
                    "France_GDP", 
                    "Italy_GDP", 
                    "Spain_GDP", 
                    "Belgium_GDP"]

####################
####################

categories       = [InternationalGDP,
                    NonFinancialCorporations,
                    NonFinancialCorporations_ratios,
                    FinancialCorporations,
                    MarcoComponents,
                    SectorProduction,
                    BusinessConfidence,
                    BusinessSituationNextThreeMonths,
                    BusinessSituationPastThreeMonths,
                    BeloningSeizoengecorrigeerd
                    ]

categories_names = [ 'InternationalGDP',
                    'NonFinancialCorporations',
                   'NonFinancialCorporations_ratios',
                   'FinancialCorporations',
                   'MacroComponents',
                   'SectorProduction',
                   'BusinessConfidence',
                   'BusinessSituationNextThreeMonths',
                   'BusinessSituationPastThreeMonths',
                   'BeloningSeizoengecorrigeerd'
                  ]

# combine lists into one large list
categories_combine = itertools.chain(*categories)

# select relevant columns from quarterlyData_categorized
quarterlyData_categorized = quarterlyData_categorized[categories_combine]

# add category name to columns
quarterlyData_categorized_names = list()
for enum, cat1 in enumerate(categories):
    dt1 = quarterlyData_categorized.loc[:,quarterlyData_categorized.columns.isin(cat1)]
    dt1.columns = [categories_names[enum] + '_' + col for col in dt1.columns]
    quarterlyData_categorized_names.append(dt1)

quarterlyData_categorized = pd.concat(quarterlyData_categorized_names, axis=1)
quarterlyData_categorized.to_csv(output_file)