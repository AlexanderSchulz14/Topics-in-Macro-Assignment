getwd()
setwd("F:/Master/Topics in Macroeconomic Theory Crespo")
rm(list=ls())

gdp <- read.csv("PWT_RGDP.csv")
pop <- read.csv("PWT_PopGr.csv")
s <- read.csv("PWT_InvShare.csv")


gdp$RGDP <- log(gdp$AggValue)
gdp$gdp <- gdp$AggValue
pop$L <- pop$AggValue
s$saving <- s$AggValue

data <- merge(gdp, pop, by = c("RegionCode", "YearCode"))
data <- merge(data, s, by = c("RegionCode", "YearCode"))
data$gdppc <- data$gdp/data$L
data$loggdppc <- log(data$gdppc)

data1 <- data[data$YearCode %in% c(1960, 1990), ]
data2 <- data[data$YearCode %in% c(1990, 2019), ]

data1 <- data.frame(data1$RegionCode, data1$YearCode, data1$gdp, data1$RGDP, data1$L, data1$saving, data1$gdppc, data1$loggdppc)
names(data1) <- c("Region", "Year", "GDP", "RGDP", "L", "Saving", "GDPPC", "LOGGDPPC")            
data2 <- data.frame(data2$RegionCode, data2$YearCode, data2$gdp, data2$RGDP, data2$L, data2$saving, data2$gdppc, data2$loggdppc)
names(data2) <- c("Region", "Year", "GDP", "RGDP", "L", "Saving", "GDPPC", "LOGGDPPC") 

#cleanup data1
region_counts <- table(data1$Region)
single_entry_regions <- names(region_counts[region_counts == 1])
data1 <- data1[!(data1$Region %in% single_entry_regions), ]
names(data1) <- c("Region", "Year", "GDP", "RGDP", "L", "Saving", "GDPPC", "LOGGDPPC")   

#cleanup data2
region_counts <- table(data2$Region)
single_entry_regions <- names(region_counts[region_counts == 1])
data2 <- data2[!(data2$Region %in% single_entry_regions), ]
names(data2) <- c("Region", "Year", "GDP", "RGDP", "L", "Saving", "GDPPC", "LOGGDPPC")  


#g data1
regions <- unique(data1$Region)

for (region in regions) {
  
  filtered_data <- subset(data1, Region == region)

  
  subset_data <- subset(filtered_data, Year %in% c(1960, 1990))
  
  growth_rate <- c(NA)
  
  if (nrow(subset_data) > 1) {
    growth_rate <- c(NA, diff(subset_data$GDP) / lag(subset_data$GDP))
  }
  
  merge_row <- subset_data$Year == 1990
  
  data1$GrowthRate[merge_row] <- growth_rate[length(growth_rate)]
}

#g data2
regions <- unique(data2$Region)

for (region in regions) {
  
  filtered_data <- subset(data2, Region == region)
  
  
  subset_data <- subset(filtered_data, Year %in% c(1990, 2019))
  
  growth_rate <- c(NA)
  
  if (nrow(subset_data) > 1) {
    growth_rate <- c(NA, diff(subset_data$GDP) / lag(subset_data$GDP))
  }
  
  merge_row <- subset_data$Year == 2019
  
  data2$GrowthRate[merge_row] <- growth_rate[length(growth_rate)]
}

data1 <- data1[!is.na(data1$GrowthRate), ]
data2 <- data2[!is.na(data2$GrowthRate), ]


#1960-1990
R1 <- lm(RGDP ~ GrowthRate, data = data1)
summary(R1)

R2 <- lm(RGDP ~ GrowthRate + L + Saving, data = data1)
summary(R2)

#1990-2019
R1 <- lm(RGDP ~ GrowthRate, data = data2)
summary(R1)

R2 <- lm(RGDP ~ GrowthRate + L + Saving, data = data2)
summary(R2)





