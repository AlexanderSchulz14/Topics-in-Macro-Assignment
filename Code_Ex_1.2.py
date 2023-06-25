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
# GDP
gdp = pd.read_csv("PWT_RGDP.csv", 
                  usecols=[1, 2, 3], 
                  names=["Country", "Year", "RGDP"],
                  header=0,
                  parse_dates=["Year"])

# Sort
gdp = gdp.sort_values(by=["Country", "Year"])
gdp = gdp.reset_index(drop=True)

# Pop. Growth
pop = pd.read_csv("PWT_PopGr.csv",
                  usecols=[1, 2, 3],
                  names=["Country", "Year", "Population"],
                  header=0,
                  parse_dates=["Year"])

# Sort
pop.sort_values(by=["Country", "Year"],
                      inplace=True,
                      ignore_index=True)


# Investment Share
s = pd.read_csv("PWT_InvShare.csv",
                usecols=[1, 2, 3],
                names=["Country", "Year", "Inv_Share"],
                header=0,
                parse_dates=["Year"])

# s["Inv_Share"] = np.log(s["Inv_Share"])

# Sort
s.sort_values(by=["Country", "Year"],
              inplace=True,
              ignore_index=True)

# Merge Data
data_full = gdp.merge(pop, on=["Country", "Year"])
data_full = data_full.merge(s, on=["Country", "Year"])

# Transformation and Addition of Variables
data_full["RGDPpc"] = data_full["RGDP"] / data_full["Population"]
data_full["RGDPpc"] = np.log(data_full["RGDPpc"])


# Get Periods for filtering by Period
period1 = pd.date_range(start="1/1/1960", end="1/1/1990", freq="YS")
period2 = pd.date_range(start="1/1/1990", end="1/1/2019", freq="YS")

# Get Countries for loop 
# (use only countries that have data available from 1960 onwards)
countries = data_full.Country.unique()
# countries = data_full.loc[data_full.Year == "1960"].Country.unique()
# countries_p2 = gdp.loc[gdp.Year == "1990"].Country.unique()

# Get GDP Growth Rates for Period 1 (1960-1990)    
data_full_p1 = data_full.loc[data_full.Year.isin(period1)]
red_gdp1 = {}
for country in countries:
    #print(country),
    red_gdp1[country] = data_full_p1.loc[(data_full_p1.Country == country)].RGDPpc.diff().mean()

min(red_gdp1.items(), key=lambda x: x[1])
max(red_gdp1.items(), key=lambda x: x[1])

# DF for GDP growth Period 1
df_gr_p1 = pd.DataFrame.from_dict(red_gdp1, orient="index").dropna()
df_gr_p1 = df_gr_p1.rename(columns={0:"GDP_GR"})

# Get GDP Level for Period 1
level_gpd_p1 = {}
for country in countries:
    try:
        gdp_level = data_full_p1.loc[data_full_p1.Country == country].RGDPpc.values
        gdp_level_init = gdp_level[0]
        level_gpd_p1[country] = gdp_level_init
    except:
        pass
    
df_level_p1 = pd.DataFrame.from_dict(level_gpd_p1, orient="index").dropna()
df_level_p1 = df_level_p1.rename(columns={0:"GDP_Level"})



# Get GDP Growth Rates for Period 2 (1960-1990)
data_full_p2 = data_full.loc[data_full.Year.isin(period2)]
red_gdp2 = {}
for country in countries:
    #print(country),
    red_gdp2[country] = data_full_p2.loc[(data_full_p2.Country == country)].RGDPpc.diff().mean()

min(red_gdp2.items(), key=lambda x: x[1])
max(red_gdp2.items(), key=lambda x: x[1])

# DF for Period 2
df_gr_p2 = pd.DataFrame.from_dict(red_gdp2, orient="index").dropna()
df_gr_p2 = df_gr_p2.rename(columns={0:"GDP_GR"})

# Get GDP Level for Period 2
level_gpd_p2 = {}
for country in countries:
    try:
        gdp_level = data_full_p2.loc[data_full_p2.Country == country].RGDPpc.values
        gdp_level_init = gdp_level[0]
        level_gpd_p2[country] = gdp_level_init
    except:
        pass
    
df_level_p2 = pd.DataFrame.from_dict(level_gpd_p2, orient="index").dropna()
df_level_p2 = df_level_p2.rename(columns={0:"GDP_Level"})


# Get Population Growth for Period 1
# pop_p1 = pop.loc[pop.Year.isin(period1)]
pop_growth_p1 = {}

for country in countries:
    pop_growth_p1[country] = data_full_p1.loc[data_full_p1.Country == country].Population.pct_change().mean()

# Get DF Pop. Growth Period 1
df_pop_gr_p1 = pd.DataFrame.from_dict(pop_growth_p1, orient="index").dropna()
df_pop_gr_p1.rename(columns={0:"Pop_Growth"}, inplace=True)

# Get Population Growth for Period 2
# pop_p2 = pop.loc[pop.Year.isin(period2)]
pop_growth_p2 = {}

for country in countries:
    pop_growth_p2[country] = data_full_p2.loc[data_full_p2.Country == country].Population.pct_change().mean()

# Get DF Pop. Growth Period 2
df_pop_gr_p2 = pd.DataFrame.from_dict(pop_growth_p2, orient="index").dropna()
df_pop_gr_p2.rename(columns={0:"Pop_Growth"}, inplace=True)


# Get avg. Inv. Share Period 1
# s_p1 = s.loc[s.Year.isin(period1)]
s_avg_p1 = {}

for country in countries:
    s_avg_p1[country] = data_full_p1.loc[data_full_p1.Country == country].Inv_Share.mean()

# Get DF avg. Inv. Share Period 1
df_s_avg_p1 = pd.DataFrame.from_dict(s_avg_p1,orient="index").dropna()
df_s_avg_p1.rename(columns={0:"Inv_Share"}, inplace=True)

# Get avg. Inv. Share Period 2
# s_p2 = s.loc[s.Year.isin(period2)]
s_avg_p2 = {}

for country in countries:
    s_avg_p2[country] = data_full_p2.loc[data_full_p2.Country == country].Inv_Share.mean()

# Get DF avg. Inv. Share Period 2
df_s_avg_p2 = pd.DataFrame.from_dict(s_avg_p2,orient="index").dropna()
df_s_avg_p2.rename(columns={0:"Inv_Share"}, inplace=True)

# Get Join unconditional beta convergence
df_p1 = df_gr_p1.join(df_level_p1)
df_p2 = df_gr_p2.join(df_level_p2)

# Models
# Unconditional beta convergence
# Period 1
df_p1["const"] = 1
X = df_p1[["const", "GDP_Level"]]
y = df_p1["GDP_GR"]

model = sm.OLS(y, X)
results = model.fit()
print(results.summary())

# Period 2
df_p2["const"] = 1
X = df_p2[["const", "GDP_Level"]]
y = df_p2["GDP_GR"]

model = sm.OLS(y, X)
results = model.fit()
print(results.summary())

# Plots
# Period 1
sns.regplot(x=df_p1["GDP_Level"], 
            y=df_p1["GDP_GR"], 
            color="b").set(title="Period 1 (1960-1990)")
plt.savefig("Uncoditional_Period1.pdf", dpi=500)
plt.show()


# Period 2
sns.regplot(x=df_p2["GDP_Level"], 
            y=df_p2["GDP_GR"], 
            color="orange").set(title="Period 2 (1990-2019)")
plt.savefig("Uncoditional_Period2.pdf", dpi=500)
plt.show()

# Conditional beta convergence
# Join DFs

#Period 1
df_p1_cond = df_gr_p1.join(df_level_p1).join(df_pop_gr_p1).join(df_s_avg_p1)

# Model Period 1
df_p1_cond["const"] = 1
X = df_p1_cond[["const", "GDP_Level", "Pop_Growth", "Inv_Share"]]
y = df_p1_cond["GDP_GR"]

model = sm.OLS(y, X)
results = model.fit()
print(results.summary())

# Plot Period 1
sns.regplot(x=df_p1_cond["GDP_Level"], 
            y=df_p1_cond["GDP_GR"], 
            color="b").set(title="Period 1 (1960-1990)")
plt.savefig("Conditional_Period1.pdf", dpi=500)
plt.show()


#Period 2
df_p2_cond = df_gr_p2.join(df_level_p2).join(df_pop_gr_p2).join(df_s_avg_p2)

# Model Period 2
df_p2_cond["const"] = 1
X = df_p2_cond[["const", "GDP_Level", "Pop_Growth", "Inv_Share"]]
y = df_p2_cond["GDP_GR"]

model = sm.OLS(y, X)
results = model.fit()
print(results.summary())

# Plot Period 2
sns.regplot(x=df_p2_cond["GDP_Level"], 
            y=df_p2_cond["GDP_GR"], 
            color="orange").set(title="Period 2 (1990-2019)")
plt.savefig("Conditional_Period2.pdf", dpi=500)
plt.show()

#%% Playing around

# gdp.Year = gdp.Year.dt.to_period("Y")

# gdp1 = gdp.groupby(["Country"])

gdp.loc[gdp.Country == "ABW"].RGDP.diff().mean()
gdp.loc[gdp.Country == "ABW"].RGDP.pct_change().mean()




# gdp.groupby("Country").RGDP.diff()






