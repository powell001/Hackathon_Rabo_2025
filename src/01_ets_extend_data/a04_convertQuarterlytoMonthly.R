library(tempdisagg)
library(zoo)
library(tidyverse)

print('################################')
print('a04_convertGDPToMonthlyData')

output_dir <- "C:/Users/jpark/vscode/Hackathon_Rabo_2025/final_forecasts//"

# load data
input_file <- "C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/02_processed_data/a0_combinedQuarterly_use_this.csv"
dt1 <- read.csv(input_file, sep = ",")

####################################
# Seasonal adjustment
####################################

# transform to ts object 
qt_data <- ts(dt1, frequency = 4, start=c(1995,1)) 
qt_to_monthly <- qt_data

alldfs <- list()
# simple transformation
for (i in colnames(qt_to_monthly)) {
    print(i)
    coldata <- qt_to_monthly[,i]
    m1 <- td(coldata ~ 1, to = "monthly", method = "denton-cholette")
    m1 <- predict(m1)    

    df_final1 <- data.frame(xxx = as.matrix(m1), date=as.Date(as.yearmon(time(m1))))
    rownames(df_final1) <- df_final1$date
    
    # drop date row
    #df_final1$date <- NULL
    alldfs[[i]] <- df_final1
}

alldfs %>% reduce(full_join, by = "date") -> combinedMonthlydata
combinedMonthlydata[1] <- NULL
colnames(combinedMonthlydata) <- colnames(qt_to_monthly)


write.csv(combinedMonthlydata, file = paste0(output_dir, "gdp_QuarterlyData_to_MonthlyData.csv"),fileEncoding="UTF-8")

