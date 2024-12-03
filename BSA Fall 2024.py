# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 13:18:24 2024

@author: brian
"""

import pandas as pd
from io import StringIO
from datetime import datetime


"### Importing and Manipulating the datasets"

physical_stats_df = pd.read_csv("BSA fall 2024 Data - Players Speed, Distance and Hustle")

injury_df = pd.read_csv(r"C:\Users\brian\Downloads\BSA\BSA Fall 2024\NBA Player Injury Stats(1951 - 2023).csv")
injury_df = injury_df.drop("Unnamed: 0", axis = 1)
injury_df['Date'] = pd.to_datetime(injury_df['Date']).dt.strftime('%Y-%m-%d')

injury_df_last_5 = injury_df[pd.to_datetime(injury_df['Date']) > pd.to_datetime("2019-10-01")]

# stats_df = pd.read_csv(r"C:\Users\brian\Downloads\BSA\BSA Fall 2024\BSA fall 2024 Data - Players Speed, Distance and Hustle.csv") 
with open(r"C:\Users\brian\Downloads\BSA\BSA Fall 2024\BSA fall 2024 Data - Players Speed, Distance and Hustle.csv", "r", encoding="utf-8", errors="ignore") as f:
    data = f.read()
    
# Use StringIO to simulate a file-like object
data_io = StringIO(data)

# Read the string as if it were a CSV
stats_df = pd.read_csv(data_io)

## No NULLS within data, hopefully its quite clean
'rows_with_nulls = stats_df[stats_df.isnull().any(axis=1)]'

del injury_df
del f
del data_io
del data


"### Manipulating datasets"

# Group injury datasets by players
injury_df_last_5 = injury_df_last_5.reset_index(drop = True)
injury_df_last_5["Player"] = injury_df_last_5["Relinquished"].combine_first(injury_df_last_5["Acquired"])
injury_df_last_5 = injury_df_last_5[["Date", "Team", "Player", "Acquired", "Relinquished", "Notes"]]
injury_df_last_5 = injury_df_last_5.sort_values(["Player", "Date"])

# Identify the first row per player
injury_df_last_5["IsFirst"] = injury_df_last_5.groupby("Player")["Date"].transform("min") == injury_df_last_5["Date"]

# Identify the last row per player
injury_df_last_5["IsLast"] = injury_df_last_5.groupby("Player")["Date"].transform("max") == injury_df_last_5["Date"]

# Filter out rows where it is the first row for a player AND 'Value' is missing
filtered_injury_df = injury_df_last_5[~((injury_df_last_5["IsFirst"]) & (injury_df_last_5["Acquired"].notnull()))].drop(columns="IsFirst")
filtered_injury_df = filtered_injury_df[~((filtered_injury_df["IsLast"]) & (filtered_injury_df["Relinquished"].notnull()))].drop(columns="IsLast")
filtered_injury_df = filtered_injury_df.reset_index(drop = True)


# Check for rows where "Status" contains "Out for season"
# Idea here is to add in an extra row where the season start is located right after the "out for season" row
condition = filtered_injury_df["Notes"].str.contains("out for season", na=False)

# Create duplicate rows for matching rows
duplicated_rows = filtered_injury_df[condition].copy()
duplicated_rows = duplicated_rows.reset_index(drop = True)

# # Iterate through rows and check the year
# for index, row in duplicated_rows.iterrows():
#     year = row["Date"][:4]  # Extract the year from the 'Date' column
    
#     if year == '2020':
#         duplicated_rows.loc[index, "Date"] = "2020-12-22"
#         duplicated_rows.loc[index, "Acquired"] = "2020-12-22"
#         duplicated_rows.loc[index, "Date"] = "2020-12-22"
#         duplicated_rows.loc[index, "Date"] = "2020-12-22"
#     elif year == '2021':
#         duplicated_rows.loc[index, "Date"] = "2021-10-19"
#     elif year == '2022':
#         duplicated_rows.loc[index, "Date"] = "2022-10-18"
#     elif year == '2023':
#         duplicated_rows.loc[index, "Date"] = "2023-10-24"
        

# injury_df_last_5 = pd.concat([injury_df_last_5, duplicated_rows]).sort_values(["Player", "Date"]).reset_index(drop = True)


for index, row in duplicated_rows.iterrows():
    if (pd.to_datetime(row["Date"]) >= pd.to_datetime("2019-10-01")) & (pd.to_datetime(row["Date"]) <= pd.to_datetime("2020-10-11")):
        duplicated_rows.loc[index, "Date"] = "2020-12-22"
        duplicated_rows.loc[index, "Acquired"] = duplicated_rows.loc[index, "Relinquished"]
        duplicated_rows.loc[index, "Relinquished"] = None
        duplicated_rows.loc[index, "Notes"] = "Start of Next Season"
        
    elif (pd.to_datetime(row["Date"]) >= pd.to_datetime("2020-12-22")) & (pd.to_datetime(row["Date"]) <= pd.to_datetime("2021-06-20")):
        duplicated_rows.loc[index, "Date"] = "2021-10-19"
        duplicated_rows.loc[index, "Acquired"] = duplicated_rows.loc[index, "Relinquished"]
        duplicated_rows.loc[index, "Relinquished"] = None
        duplicated_rows.loc[index, "Notes"] = "Start of Next Season"
    
    elif (pd.to_datetime(row["Date"]) >= pd.to_datetime("2021-10-18")) & (pd.to_datetime(row["Date"]) <= pd.to_datetime("2022-06-12")):
        duplicated_rows.loc[index, "Date"] = "2022-10-18"
        duplicated_rows.loc[index, "Acquired"] = duplicated_rows.loc[index, "Relinquished"]
        duplicated_rows.loc[index, "Relinquished"] = None
        duplicated_rows.loc[index, "Notes"] = "Start of Next Season"
    
    elif (pd.to_datetime(row["Date"]) >= pd.to_datetime("2022-10-18")) & (pd.to_datetime(row["Date"]) <= pd.to_datetime("2023-06-17")):
        duplicated_rows.loc[index, "Date"] = "2023-10-24"
        duplicated_rows.loc[index, "Acquired"] = duplicated_rows.loc[index, "Relinquished"]
        duplicated_rows.loc[index, "Relinquished"] = None
        duplicated_rows.loc[index, "Notes"] = "Start of Next Season"
        
# Take note of Klay Thompson, Ivica Zubac 2021-06, Thanasis Antetokounmpo 2021-07

filtered_injury_df = pd.concat([filtered_injury_df, duplicated_rows]).sort_values(["Player", "Date"]).reset_index(drop = True)

# Swap rows
filtered_injury_df.iloc[[863, 864]] = filtered_injury_df.iloc[[864, 863]].values
filtered_injury_df.iloc[[7260, 7261]] = filtered_injury_df.iloc[[7261, 7260]].values

# Dropping certain rows due to various issues
final_injury_df = filtered_injury_df.drop(index=filtered_injury_df.index[[511, 1429, 1501, 1608, 1665, 2002, 2138, 3011, 3099, 3327,
                                                                          3407, 3420, 4689, 4729, 4745, 4779, 5143, 5264, 5422, 5482,
                                                                          5551, 5703, 6282, 6363, 6617, 7135, 7193, 7318, 7362, 7363,
                                                                          7377, 7678, 7725, 7735, 7785, 7786, 7933, 8047]])

final_injury_df[["Injury Length"]] = None

# Convert the "Date" values to datetime if they aren't already
final_injury_df["Date"] = pd.to_datetime(final_injury_df["Date"])
final_injury_df = final_injury_df.reset_index(drop = True)

# Now I have to find the dates between each injury

for index, row in final_injury_df.iterrows():
    
    i = 1
    if (index != 0):
        
        # If statement to see if current relinquished is not none
        if (pd.notnull(final_injury_df.loc[index, "Relinquished"]) and pd.isnull(final_injury_df.loc[index - 1, "Relinquished"])):
            
            
            # While statement to see if index + i relinquished is not none
            while(pd.notnull(final_injury_df.loc[index + i, "Relinquished"])):
                i = i + 1
            
            
            final_injury_df.loc[index + i, "Injury Length"] = (final_injury_df.loc[index + i, "Date"] - final_injury_df.loc[index, "Date"]).days

final_injury_df.loc[1, "Injury Length"] = (final_injury_df.loc[1, "Date"] - final_injury_df.loc[0, "Date"]).days



# I still need to find the exploratory variables for this regression model
# I want to use Lasso Regression

# Does this make sense? Players will get injured multiple times within a season
# We can actually take the sum of how many days a player is injured over a season
# Then we can make a chart of most common injuries?? and run a regression model of how many days 



