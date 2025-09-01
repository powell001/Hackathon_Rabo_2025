library(tidyverse)
library(xts)
library(zoo)
library(svglite)
library(TSstudio)
library(zoo)
library(dlm)
library(forecast)
library(expsmooth)
library(ggplot2)
#library(ggfortify)
library(changepoint)
library(KFAS)
library(httpgd)
library(funtimes)
library(seastests)
library(car)
library(lmtest)
library(data.table)
library(lubridate)
library(stringr)
library(zoo)
library(dplyr)

##############################
# Possible analyses
##############################

##############################
finalforecastHorizon <- 20 #from previous script, must be same
##############################

print('################################')
print('a01_2_analyses_month_ETS')

combined_data_input_file <- "C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/02_processed_data/a0_combinedMonthly_use_this.csv"


forecasts_dir    <- "C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/03_final_data/mo_data_extended/forecasts//"
intermediate_dir <- "C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/03_final_data/mo_data_extended/intermediate_data//"
combinedFinalForecasts                  <- "C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/03_final_data/mo_data_extended/intermediate_data/combined_final_forecasts.csv"
combinedFinal_Historical_plus_Forecasts <- "C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/03_final_data/mo_data_extended/intermediate_data/combined_final_Historical_plus_Forecasts_ets_mo.csv"

combinedFinal_Historical_plus_Forecasts_final <- "C:/Users/jpark/vscode/Hackathon_Rabo_2025/final_forecasts/combined_final_Historical_plus_Forecasts_ets_mo.csv"


# remove files
#do.call(file.remove, list(list.files(analyse_dir, full.names = TRUE)))

###
# Combine all forecasts
###

# select final forecasts from forecasts directory
files <- list.files(forecasts_dir, pattern = "final_forecasts.*\\.csv$", full.names = TRUE)
combinedForecasts <- read.csv(files[1])

# Merge data frames using a loop
for (fl in files[2:length(files)]) {
  file_df <- read.csv(fl)
  combinedForecasts <- rbind(combinedForecasts, file_df)
}

# Combines all forecast into one file
write.table(combinedForecasts, file = paste0(intermediate_dir, "combined_final_forecasts.csv"), sep =",",row.names = FALSE)

######################
# Type of model for each analysis
######################

fun_ETS_Used <- function(){

    # get the model used in the historical data
    files_Raw  <- list.files(forecasts_dir, pattern = "Historical_Data\\.csv$", full.names = TRUE)
    
    #get first value, this is needed to combine all the other values
    chosenModel_seriesName <- read.csv(files_Raw[1])[1,c(3,1)]

    # Merge data frames using a loop
    for (fl in files_Raw[2:length(files_Raw)]) {
    file_df <- read.csv(fl)
    chosenModel_seriesName <- rbind(chosenModel_seriesName, file_df[1,c(3,1)])
    } 

    write.table(chosenModel_seriesName, file = paste0(intermediate_dir, "combined_model_used.csv"), sep =",",row.names = FALSE)
}

fun_ETS_Used()

######################
# Percentage Changes
######################

fun_percentage_change <- function(){

    # select historical forecasts from forescasts directory
    files_Raw  <- list.files(forecasts_dir, pattern = "Historical_Data\\.csv$", full.names = TRUE)
    initial_df <- read.csv(files_Raw[1])[,c(1,4,5)]
    
    if (is.numeric(initial_df$ObservationDate)){
        initial_df['ObservationDate'] <- format(date_decimal(initial_df$ObservationDate), "%Y-%m-01")}

    initial_df <- initial_df |> mutate(growth_monthbefore = (RawData - dplyr::lag(RawData, 1))/dplyr::lag(RawData, 1) * 100)
    initial_df <- initial_df |> mutate(growth_twomonthbefore = (RawData - dplyr::lag(RawData, 1))/dplyr::lag(RawData, 2) * 100)
    initial_df <- initial_df |> mutate(growth_threemonthbefore = (RawData - dplyr::lag(RawData, 1))/dplyr::lag(RawData, 3) * 100)
    initial_df <- initial_df |> mutate(growth_yearbefore = (RawData - dplyr::lag(RawData, 12))/dplyr::lag(RawData, 12) * 100)
    initial_df <- initial_df |> mutate(growth_fouryearbefore = (RawData - dplyr::lag(RawData, 48))/dplyr::lag(RawData, 48) * 100)
    
    # Merge data frames using a loop

    for (fl in files_Raw[2:length(files_Raw)]) {
       
        nextFile <- fl
        file_df <- read.csv(nextFile)[,c(1,4,5)]

         if (is.numeric(initial_df$ObservationDate)){
            file_df['ObservationDate'] <- format(date_decimal(file_df$ObservationDate), "%Y-%m-01")}

        file_df <- file_df |> mutate(growth_monthbefore = (RawData - dplyr::lag(RawData, 1))/dplyr::lag(RawData, 1) * 100)
        file_df <- file_df |> mutate(growth_twomonthbefore = (RawData - dplyr::lag(RawData, 1))/dplyr::lag(RawData, 2) * 100)
        file_df <- file_df |> mutate(growth_threemonthbefore = (RawData - dplyr::lag(RawData, 1))/dplyr::lag(RawData, 2) * 100)
        file_df <- file_df |> mutate(growth_yearbefore = (RawData - dplyr::lag(RawData, 12))/dplyr::lag(RawData, 12) * 100)
        file_df <- file_df |> mutate(growth_fouryearbefore = (RawData - dplyr::lag(RawData, 48))/dplyr::lag(RawData, 48) * 100)

        initial_df <- rbind(initial_df, file_df)
    } 

    write.table(initial_df, file = paste0(intermediate_dir, "combined_percentageChanges.csv"), sep =",",row.names = FALSE)
}

fun_percentage_change()

######################
# BIG Percentage Changes
######################

fun_big_percentage_change <- function(){
    ###
    # Biggest percentage movers, current month as starting point 
    percentFile <- paste0(intermediate_dir, "combined_percentageChanges.csv")
    percent_df <- read.csv(percentFile)

    # System date should give the most current date
    latest_date <- percent_df$ObservationDate[length(percent_df$ObservationDate)]

    percent_movers_latest <- percent_df[percent_df$ObservationDate == latest_date, ]
    percent_movers_latest %>% 
        group_by(SeriesName) %>%
        filter(row_number() == 1) -> lastest_percentage_movers

    write.table(lastest_percentage_movers, file = paste0(intermediate_dir, "combined_percentMovers_newMonth.csv"), sep =",",row.names = FALSE)
}

fun_big_percentage_change()

######################
# Combined Historical data plus level forecasts
######################

### Horizons
horizon <- finalforecastHorizon

fun_combine_hist_forecast <- function(){ 

    ############
    # Original, historical data
    ############
    historical_data <- read.csv(combined_data_input_file)
    historical_data$X <- as.Date(historical_data$X)
    rownames(historical_data) <- historical_data$X

    # dimensions
    print(dim(historical_data))

    ############
    # Forecast data
    ############
    finalForecasts <- read.csv2(combinedFinalForecasts, header = TRUE, sep = ",")
    finalForecasts$featureNames <- str_sub(finalForecasts$Key1, 12) #this drops the date from the name
    finalForecasts$X <- as.Date(as.yearmon(finalForecasts$Forecast_Period, format = "%b %Y"))
  
    # select relevant columns
    f1 <- finalForecasts[c('Point.Forecast','featureNames','X')]
    forecast2 <- f1 |> pivot_wider(names_from = featureNames, values_from = Point.Forecast)

    # data (forecasts)
    forecast2 <- as.data.frame(forecast2)
    forecast2 <- forecast2[names(historical_data)]
   
    forecast3 <- forecast2[order(forecast2$X),]
    rownames(forecast3) <- forecast3$X

    # get rows from data for column and forecasts, these should be contiguous dates

    list_dfs <- list()

    for(col in names(historical_data)[2:length(names(historical_data))]){

       #col <- "ASML.AS"
        print(col)
        historical_data1 <- historical_data[col]
        historical_data1 %>% slice(1:nrow(na.trim(historical_data1, "right", is.na = "any"))) -> historical_data2

        # remove NAs from forecast columns
        forecast_noNA   <- na.omit(forecast3[col])

        new_data_col <- rbind(historical_data2, forecast_noNA)
        new_data_col['Date'] <- rownames(new_data_col)

        list_dfs[[col]] <- new_data_col        

    }

    purrr::reduce(.x = list_dfs, merge, by = c('Date'), all = T) -> df3
    row.names(df3) <- seq(ymd("1995-01-01"), length = nrow(df3), by = "months")

    df3 %>% filter(Date <= '2025-12-31') -> df3

    write.table(df3, file = combinedFinal_Historical_plus_Forecasts, sep =",",row.names = FALSE)

    # final forecast file
    write.table(df3, file = combinedFinal_Historical_plus_Forecasts_final, sep =",",row.names = FALSE)

}

fun_combine_hist_forecast()
