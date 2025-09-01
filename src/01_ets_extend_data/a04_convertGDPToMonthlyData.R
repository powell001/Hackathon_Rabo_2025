library(tempdisagg)
library(zoo)

print('################################')
print('a04_convertGDPToMonthlyData')

output_dir <- "C:/Users/jpark/vscode/Hackathon_Rabo_2025/final_forecasts//"

# load data   
input_data_qt  <- "C:/Users/jpark/vscode/Hackathon_Rabo_2025/data/02_processed_data/a0_combinedQuarterly_use_this.csv"
dt1 <- read.csv(input_data_qt, sep = ",")

# what we want to predict
gdp1 <- dt1[['GrossDomesticProduct_2_seasonCorrected_expenditure']]

# transform to ts object
gdp1 <- ts(gdp1, frequency = 4, start=c(1995,1))

plot(gdp1)

# simple transformation
m1 <- td(gdp1 ~ 1, to = "monthly", method = "denton-cholette")
m1 <- predict(m1)


df_final1 <- data.frame("gdp_convertedTo_Monthly_SeasonallyAdjusted" = as.matrix(m1), date=as.Date(as.yearmon(time(m1))))
rownames(df_final1) <- df_final1$date

# drop date row
df_final1$date <- NULL

write.csv(df_final1, file = paste0(output_dir, "gdp_convertedTo_Monthly_SeasonallyAdjusted.csv"),fileEncoding="UTF-8")

