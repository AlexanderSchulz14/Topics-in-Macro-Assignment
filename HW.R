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


#g gdp data1
regions <- unique(data1$Region)
for (region in regions) {
  # Filter the data set for the current region
  filtered_data <- subset(data1, Region == region)
  
  # Subset the filtered data for the years 1960 and 1990
  subset_data <- subset(filtered_data, Year %in% c(1960, 1990))
  
  # Calculate the growth rate of GDP
  if (nrow(subset_data) == 2) {
    growth_rate <- (subset_data$GDP[2] - subset_data$GDP[1]) / subset_data$GDP[2]
  } else {
    growth_rate <- NA
  }
  
  # Identify the row with the corresponding Region and Year 1990
  merge_row <- subset_data$Year == 1990
  
  # Merge the growth rate into the data1 data frame
  data1$GrowthRate[merge_row] <- growth_rate
}
  
#g L data1
regions <- unique(data1$Region)

# Loop over each region and calculate the growth rate for L
for (region in regions) {
  # Filter the data set for the current region
  filtered_data <- subset(data1, Region == region)
  
  # Subset the filtered data for the years 1960 and 1990
  subset_data <- subset(filtered_data, Year %in% c(1960, 1990))
  
  # Calculate the growth rate of L
  if (nrow(subset_data) == 2) {
    growth_rate <- (subset_data$L[2] - subset_data$L[1]) / subset_data$L[2]
  } else {
    growth_rate <- NA
  }
  
  # Identify the row with the corresponding Region and Year 1990
  merge_row <- subset_data$Year == 1990
  
  # Merge the growth rate into the data1 data frame
  data1$N[merge_row] <- growth_rate
}

#g s data1
regions <- unique(data1$Region)

# Loop over each region and calculate the growth rate for Saving
for (region in regions) {
  # Filter the data set for the current region
  filtered_data <- subset(data1, Region == region)
  
  # Subset the filtered data for the years 1960 and 1990
  subset_data <- subset(filtered_data, Year %in% c(1960, 1990))
  
  # Calculate the growth rate of Saving
  if (nrow(subset_data) == 2) {
    growth_rate <- (subset_data$Saving[2] - subset_data$Saving[1]) / subset_data$Saving[2]
  } else {
    growth_rate <- NA
  }
  
  # Identify the row with the corresponding Region and Year 1990
  merge_row <- subset_data$Year == 1990
  
  # Merge the growth rate into the data1 data frame
  data1$S[merge_row] <- growth_rate
}


###########

#g gdp data2
regions <- unique(data2$Region)

# Loop over each region and calculate the growth rate for GDP
for (region in regions) {
  # Filter the data set for the current region
  filtered_data <- subset(data2, Region == region)
  
  # Subset the filtered data for the years 1990 and 2019
  subset_data <- subset(filtered_data, Year %in% c(1990, 2019))
  
  # Calculate the growth rate of GDP
  if (nrow(subset_data) == 2) {
    growth_rate <- (subset_data$GDP[2] - subset_data$GDP[1]) / subset_data$GDP[2]
  } else {
    growth_rate <- NA
  }
  
  # Identify the row with the corresponding Region and Year 2019
  merge_row <- subset_data$Year == 2019
  
  # Merge the growth rate into the data2 data frame
  data2$GrowthRate[merge_row] <- growth_rate
}


#g L data2
regions <- unique(data2$Region)

# Loop over each region and calculate the growth rate for L
for (region in regions) {
  # Filter the data set for the current region
  filtered_data <- subset(data2, Region == region)
  
  # Subset the filtered data for the years 1990 and 2019
  subset_data <- subset(filtered_data, Year %in% c(1990, 2019))
  
  # Calculate the growth rate of L
  if (nrow(subset_data) == 2) {
    growth_rate <- (subset_data$L[2] - subset_data$L[1]) / subset_data$L[2]
  } else {
    growth_rate <- NA
  }
  
  # Identify the row with the corresponding Region and Year 2019
  merge_row <- subset_data$Year == 2019
  
  # Merge the growth rate into the data2 data frame
  data2$N[merge_row] <- growth_rate
}

#g s data2
regions <- unique(data2$Region)

# Loop over each region and calculate the growth rate for Saving
for (region in regions) {
  # Filter the data set for the current region
  filtered_data <- subset(data2, Region == region)
  
  # Subset the filtered data for the years 1990 and 2019
  subset_data <- subset(filtered_data, Year %in% c(1990, 2019))
  
  # Calculate the growth rate of Saving
  if (nrow(subset_data) == 2) {
    growth_rate <- (subset_data$Saving[2] - subset_data$Saving[1]) / subset_data$Saving[2]
  } else {
    growth_rate <- NA
  }
  
  # Identify the row with the corresponding Region and Year 2019
  merge_row <- subset_data$Year == 2019
  
  # Merge the growth rate into the data2 data frame
  data2$S[merge_row] <- growth_rate
}






data1 <- data1[!is.na(data1$GrowthRate), ]
data1 <- data1[!is.na(data1$N), ]
data1 <- data1[!is.na(data1$S), ]
data2 <- data2[!is.na(data2$GrowthRate), ]
data2 <- data2[!is.na(data2$N), ]
data2 <- data2[!is.na(data2$S), ]


#1960-1990
R1 <- lm(GrowthRate ~ LOGGDPPC, data = data1)
summary(R1)

R2 <- lm(GrowthRate ~ LOGGDPPC + N + Saving, data = data1)
summary(R2)

#1990-2019
R1 <- lm(GrowthRate ~ LOGGDPPC, data = data2)
summary(R1)

R2 <- lm(GrowthRate ~ LOGGDPPC + N + S, data = data2)
summary(R2)





