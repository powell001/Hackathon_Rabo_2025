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
library(tools)


input_file   <- "C:\\Users\\jpark\\vscode\\Hackathon_Rabo_2025\\src\\02_create_categories\\data\\quarterly_toMonthlydata_categorized.csv"
output_file  <- "C:\\Users\\jpark\\vscode\\Hackathon_Rabo_2025\\src\\02_create_categories\\data\\quarterly_toMonthlydata_categorized_extended_useThis.csv"

# Model consists of three letters following Hyndman (2008) and here: https://search.r-project.org/CRAN/refmans/forecast/html/ets.html

# First letter is the error type:     A, M or Z
# Second letter is the trend type:    N, A, M, Z
# Third letter is the season type:    N, A, M, Z

# Some of the models have names:
#     ANN is simple exponential smoothing with additive errors.
#     MAM is multiplicative Holt-Winters with multiplicative errors.


ENDDATE <- "2025-08-01" ######################################################################## Should be the last month of available data
PLOT_PRINT <- "FALSE"

####################################
go_back_in_time <- 10
finalforecastHorizon <- 10
####################################

appropriateModels <- c("ANNX", "ANAX", "ANMX",
                       "AANX", "AAAX", "AAMX",
                       "AAND", "AAAD", "ANMD",
                       "AMNX", "AMAX", "AMMX",
                       "AMND", "AMAD", "AMMD",
                       "MNNX", "MNAX", "MNMX",
                       "MANX", "MAAX", "MAMX",
                       "MAND", "MAAD", "MNMD",
                       "MMNX", "MMAX", "MMMX",
                       "MMND", "MMAD", "MMMD")


# load data
dt1 <- read.csv(input_file, sep = ",")

rownames(dt1) <- dt1$X
colnames(dt1)
dim(dt1)
allColumns <- colnames(dt1)

# remove perioden column
data_columns <- allColumns[c(-1)]

##########################
# start date
##########################
start_date <- "1995-01-01"
mystart = c(1995,1,1)

### Last date of real data:
end_date <- ENDDATE  # choose series with the most recent data (missing data will be forecasted)

dt1 %>% filter(rownames(dt1) >= start_date &  rownames(dt1) <= end_date) -> dt1

##########################
# FOR LOOP
##########################

list_of_forecasts <- list()
count = 0
for(colName in data_columns){ 

  count = count + 1
  print(count)

  # Test column
  #colName = "InternationalGDP_Germany_GDP"

  # connects all the data
  Key1 <- paste(Sys.Date(), "_", colName, sep="")

  series1 <- ts(dt1[colName], frequency = 12, start=mystart)
  series1 <- na.omit(series1)

  #########################
  # Which model to use
  #########################

  bestMod <- function(appropriateModels, data, lowest_aic = Inf){

      for (mod in appropriateModels){

      tryCatch({

          ##############################
          #print(mod)  

          error1 <- str_sub(mod, 1, 1)
          trend2 <- str_sub(mod, 2, 2)
          season3 <- str_sub(mod, 3, 3)
          damp4 <- str_sub(mod, 4, 4)
          ##############################

      if(damp4 == "X"){ #damped is FALSE
              model <- ets(data, model = mod, damped = FALSE)
              out1 <- list(mod, model$aic, damped = FALSE)

              } else { #damped is TRUE
                  model <- ets(data, model = mod, damped = TRUE)

                  out1 <- list(mod, model$aic, damped = TRUE)
              }
        }, error=function(e){})
      # }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})    

      new_aic <- out1[[2]]

      if (new_aic < lowest_aic){
          lowest_aic <- out1[[2]]
          best_model <- out1
      }
      }

      bm_df <- t(as.data.frame(matrix(unlist(best_model)),nrow=1,ncol=3))  

      colnames(bm_df) <- c("Model", "AIC", "Damped")
      rownames(bm_df) <- c("model")

      return(bm_df)
  }

  #########################
  # Which model to use
  #########################

  choosenModel <- bestMod(appropriateModels, series1)
  modelform <- choosenModel[1,1]
  dampform  <- choosenModel[1,3]

  if(dampform == "FALSE"){
    fit <- ets(series1, model=modelform, damped=FALSE)
  } else {
    fit <- ets(series1, model=modelform, damped=TRUE)
  }

  # Train Test Split (go_back_in_time is the period you want to go back in time)  
  train <- head(series1, round(length(series1) - go_back_in_time))
  test <- tail(series1, go_back_in_time)

   if(dampform == "FALSE"){
    fit <- ets(train, model=modelform, damped=FALSE)
  } else {
    fit <- ets(train, model=modelform, damped=TRUE)
  }
  
  forecasted_train <- forecast(fit, h=go_back_in_time)

  if (PLOT_PRINT == "TRUE"){
    png(filename=paste(figures_dir, Key1, "TrainTestForecast.png", sep = "_"))
    print(autoplot(forecasted_train, include=go_back_in_time+2) + autolayer(test) + ggtitle(colName))
    dev.off()
  }

  ####################
  # final forecast
  ####################

  if(dampform == "FALSE"){
    fit <- ets(series1, model=modelform, damped=FALSE)
  } else {
    fit <- ets(series1, model=modelform, damped=TRUE)
  }

  forecast_oneMonth <- forecast(fit, h=finalforecastHorizon)

  if (PLOT_PRINT == "TRUE"){
    png(filename=paste(figures_dir, Key1, "final_forecasts.png", sep = "_"))
    print(autoplot(tail(series1, 2)) + autolayer(forecast_oneMonth) + ggtitle(colName))
    dev.off()
  }

  ################################
  # Saving
  ################################

  ###
  # Raw Data
  ###

  data <- data.frame(
    SeriesName   = colName, 
    DateAnalysis = Sys.Date(), 
    ETSmodel = modelform,
    ObservationDate = as.yearmon(time(series1)),
    RawData = series1
  )
  data$Key1 <- Key1

  colnames(data) <- c("SeriesName", "DateAnalysis", "ETSmodel", "ObservationDate", "RawData", "Key1")

  ###
  # TrainTestForecast
  ###
  forecast_tibble <- as.data.frame(forecast_oneMonth)
  forecast_tibble$Key1 <- Key1 

  

  ###
  # finalForecast
  ###
  forecast_Months <- forecast(fit, h=finalforecastHorizon)
  finalForecast <- as.data.frame(forecast_Months, row.names = NULL)
  finalForecast$Key1 <- Key1
  finalForecast <- tibble::rownames_to_column(finalForecast, "Forecast_Period")  

  
###
# Add final forecast to Historical Data
###
# Create new dataframe based on 'data' dataframe and then rbind

# pick any chunk of data dataframe with same size as horizon
forecastDF <- tail(data, finalforecastHorizon)
forecastDF[c(5)] <- unclass(c(forecast_Months$mean))
forecastDF$ObservationDate <- as.yearmon(time(forecast_oneMonth$mean))

data1 <- rbind(unclass(data), forecastDF)

colnames(data1) <- c("SeriesName", "DateAnalysis", "ETSmodel", "date", colName, "Key1")

list_of_forecasts[[count]] <- data1[,c("date", colName)]

} 

############# END LOOP ##############
############# END LOOP ##############
############# END LOOP ##############

quarterly_combined_extended <- list_of_forecasts %>% reduce(full_join, by = "date")


write.csv(quarterly_combined_extended, output_file, row.names = FALSE)