# Run auto.arima with a set d
library(tidyverse)
require(tseries)
require(fpp2)
library(zoo)

print('################################')
print('a03_month_quarter_auto_arima')

input_data_mo  <- "C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/02_processed_data/a0_combinedMonthly_use_this.csv"
output_data_mo <- "C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/03_final_data/mo_data_extended/intermediate_data/combined_final_Historical_plus_Forecasts_arima_mo.csv"

combinedFinal_Historical_plus_Forecasts_final <- "C:/Users/jpark/vscode/Hackathon_Rabo_2025/final_forecasts/combined_final_Historical_plus_Forecasts_arima_mo.csv"

arima_month <- function(){

    # load data
    dt1 <- read.csv(input_data_mo, sep = ",", encoding = "Latin-1")

    #dt1 <- dt1[,c(1,2,3,4)]

    rownames(dt1) <- dt1$X
    colnames(dt1)
    dim(dt1)
    allColumns <- colnames(dt1)
    # remove perioden column
    data_columns <- allColumns[c(-1)]


    dfList <- list()
    counter <- 0

    for(colName in data_columns){ 

        counter <- counter + 1
        print(counter)

        #print(colName)

        mystart <- rownames(na.omit(dt1[colName]))[1]
        yr1 <- format(as.Date(mystart,format="%Y-%m-%d"), "%Y")
        mo1 <- format(as.Date(mystart,format="%Y-%m-%d"), "%m")
        do1 <- format(as.Date(mystart,format="%Y-%m-%d"), "%d")
        mystart <- c(as.numeric(yr1), as.numeric(mo1), as.numeric(do1))

        series1 <- ts(na.omit(dt1[colName]), frequency = 12, start = mystart)
        

        arima_m = auto.arima(series1, d = 1, max.p = 2, max.q = 2, seasonal = T) # should distinguish between seasonal and non-seasonal
        summary(arima_m)

        # Forecasting
        my_forecast <- forecast(arima_m, h = 12)

        combData <- c(my_forecast$x, my_forecast$mean)

        combData <- ts(combData, frequency = 12, start = mystart)

        df_data <- data.frame(colName =as.matrix(combData), date=as.Date(as.yearmon(time(combData))))

        colnames(df_data) <- c(colName, "date")

        dfList[[colName]] <- df_data

    }

    df_final <- dfList %>% reduce(full_join, by='date') 

    rownames(df_final) <- df_final$date
    df_final %>% filter(date <= '2025-12-31') -> df_final

    df_final$date <- NULL
    write.csv(df_final, file = output_data_mo, fileEncoding="UTF-8")

    #final forecasts
    write.csv(df_final, file = combinedFinal_Historical_plus_Forecasts_final, fileEncoding="UTF-8")
}

arima_month()

#######################
#######################
#######################

print('################################')
print('a05_auto_arima Quarter')

input_data_qt  <- "C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/02_processed_data/a0_combinedQuarterly_use_this.csv"
output_data_qt <- "C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/03_final_data/qt_data_extended/intermediate_data/combined_final_Historical_plus_Forecasts_arima_qt.csv"

combinedFinal_Historical_plus_Forecasts_final <- "C:/Users/jpark/vscode/Hackathon_Rabo_2025/final_forecasts/combined_final_Historical_plus_Forecasts_arima_qt.csv"

arima_quarter <- function(){

    # load data
    dt1 <- read.csv(input_data_qt, sep = ",", encoding = "Latin-1")

    #dt1 <- dt1[,c(1,2,3,4)]

    rownames(dt1) <- dt1$X
    colnames(dt1)
    dim(dt1)
    allColumns <- colnames(dt1)
    # remove perioden column
    data_columns <- allColumns[c(-1)]

    dfList <- list()

    counter <- 0
    for(colName in data_columns){ 

        counter <- counter + 1
        print(counter)

        # colName <- "GrossDomesticProduct_2_seasonCorrected_expenditure"
        # print(colName)

        mystart <- rownames(na.omit(dt1[colName]))[1]

        yr1 <- format(as.Date(mystart,format="%Y-%m-%d"), "%Y")
        mo1 <- format(as.Date(mystart,format="%Y-%m-%d"), "%m")
        do1 <- format(as.Date(mystart,format="%Y-%m-%d"), "%d")
        mystart = c(as.numeric(yr1), as.numeric(mo1), as.numeric(do1))

        series1 <- ts(na.omit(dt1[colName]), frequency = 4, start = mystart) #not na.omit
       
        arima_qt = auto.arima(series1, d = 1, max.p = 2, max.q = 2, seasonal = T) # should distinguish between seasonal and non-seasonal

        # Forecasting
        my_forecast <- forecast(arima_qt, h = 4)

        combData <- c(my_forecast$x, my_forecast$mean)

        combData <- ts(combData, frequency = 4, start = mystart)

        df_data <- data.frame(colName =as.matrix(combData), date=as.Date(as.yearmon(time(combData))))

        colnames(df_data) <- c(colName, "date")

        dfList[[colName]] <- df_data

    }

    df_final <- dfList %>% reduce(full_join, by='date') 

    rownames(df_final) <- df_final$date

    df_final %>% filter(date <= '2025-12-31') -> df_final

    # order by date
    df_final <- df_final[order(df_final$date),]

    df_final$date <- NULL

    write.csv(df_final, file = output_data_qt, fileEncoding="UTF-8")

    #final forecasts
    write.csv(df_final, file = combinedFinal_Historical_plus_Forecasts_final, fileEncoding="UTF-8")
}

arima_quarter()



