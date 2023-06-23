# Packages
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")
import statsmodels.api as sm

# WD
wd = r"C:\Users\alexa\Documents\Studium\MSc (WU)\Topics in Macroeconomic Theory and Policy\Assignment\Topics-in-Macro-Assignment"
os.chdir(wd)

# Read Data
gdp = pd.read_csv("PWT_RGDP.csv", usecols=[1, 2, 3], 
                  names=["Country", "Year", "RGDP"],
                  header=0,
                  parse_dates=["Year"])

gdp["RGDP"] = np.log(gdp["RGDP"])

# Sort
gdp = gdp.sort_values(by=["Country", "Year"])
gdp = gdp.reset_index(drop=True)

# Get Periods for filtering by Period
period1 = pd.date_range(start="1/1/1960", end="1/1/1990", freq="YS")
period2 = pd.date_range(start="1/1/1990", end="1/1/2019", freq="YS")

# Get Countries for loop
countries = gdp.Country.unique()

# Get Growth Rates for Period 1 (1960-1990)    
gdp_p1 = gdp.loc[gdp.Year.isin(period1)]
red_gdp1 = {}
for country in countries:
    #print(country),
    red_gdp1[country] = gdp_p1.loc[(gdp_p1.Country == country)].RGDP.pct_change().mean()

min(red_gdp1.items(), key=lambda x: x[1])
max(red_gdp1.items(), key=lambda x: x[1])

# DF for GDP growth Period 1
df_gr_p1 = pd.DataFrame.from_dict(red_gdp1, orient="index")
df_gr_p1 = df_gr_p1.rename(columns={0:"GDP_GR"})

# Get GDP Level for Period 1
level_gpd_p1 = {}
for country in countries:
    try:
        gdp_level = gdp_p1.loc[gdp_p1.Country == country].RGDP.values
        gdp_level_init = gdp_level[0]
        level_gpd_p1[country] = gdp_level_init
    except:
        pass
    
df_level_p1 = pd.DataFrame.from_dict(level_gpd_p1, orient="index")
df_level_p1 = df_level_p1.rename(columns={0:"GDP_Level"})



# Get Growth Rates for Period 2 (1960-1990)
gdp_p2 = gdp.loc[gdp.Year.isin(period2)]
red_gdp2 = {}
for country in countries:
    #print(country),
    red_gdp2[country] = gdp_p2.loc[(gdp_p2.Country == country)].RGDP.pct_change().mean()

min(red_gdp2.items(), key=lambda x: x[1])
max(red_gdp2.items(), key=lambda x: x[1])

# DF for Period 2
df_gr_p2 = pd.DataFrame.from_dict(red_gdp2, orient="index")
df_gr_p2 = df_gr_p2.rename(columns={0:"GDP_GR"})

# Get GDP Level for Period 2
level_gpd_p2 = {}
for country in countries:
    try:
        gdp_level = gdp_p2.loc[gdp_p2.Country == country].RGDP.values
        gdp_level_init = gdp_level[0]
        level_gpd_p2[country] = gdp_level_init
    except:
        pass
    
df_level_p2 = pd.DataFrame.from_dict(level_gpd_p2, orient="index")
df_level_p2 = df_level_p2.rename(columns={0:"GDP_Level"})


# Get Join 
df_p1 = df_gr_p1.join(df_level_p1).dropna()
df_p2 = df_gr_p2.join(df_level_p2).dropna()

# Models
# Period 1
df_p1["const"] = 1
X = df_p1[["const", "GDP_Level"]]
y = df_p1["GDP_GR"]

model = sm.OLS(y, X)
results = model.fit()
results.summary()

# Period 2
df_p2["const"] = 1
X = df_p2[["const", "GDP_Level"]]
y = df_p2["GDP_GR"]

model = sm.OLS(y, X)
results = model.fit()
print(results.summary())

# Plots

sns.regplot(x=df_p1["GDP_Level"], y=df_p1["GDP_GR"], color="b").set(title="Period 1 (1960-1990)")

sns.regplot(x=df_p2["GDP_Level"], y=df_p2["GDP_GR"], color="orange").set(title="Period 2 (1990-2019)")

#%% Playing around

# gdp.Year = gdp.Year.dt.to_period("Y")

# gdp1 = gdp.groupby(["Country"])

gdp.loc[gdp.Country == "ABW"].RGDP.pct_change().mean()

gdp.loc[gdp.Country == "ABW"].RGDP

gdp_p1.loc[gdp_p1.Country == "AUT"]

gdp.loc[gdp.Year.isin(period1)]

red_gdp = {}
for country in countries:
    print(country),
    red_gdp[country] = gdp.loc[gdp.Country == country].RGDP.pct_change().mean()


level_gdp = list(gdp_p1.loc[gdp_p1.Country == country].RGDP)


