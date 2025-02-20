import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import plotly.express as px

# Import databases
# new_stat_11_6_24.csv contains metrics of all pitches thrown in the 2024 MLB Season as of November 6, 2024
pitcher_char = pd.read_csv("new_stat_11_6_24.csv")
# pitcher_char = name, VAA, iVB, velocity and only includes four-seam fastballs
pitcher_char = pitcher_char[pitcher_char["pitch_type"] == 'FF']
pitcher_char = pitcher_char.loc[:, ["pitcher_name", "release_speed", "induced_vb", "vaa"]]
# create a new column called fb_count that contains the number of fastballs thrown by counting the
# number of times the name appears in the fastball sorted dataframe
pitcher_char["fb_count"] = pitcher_char["pitcher_name"].map(pitcher_char["pitcher_name"].value_counts())


# Step 1: Calculate league averages and standard deviations then filter
avg_iVB = float(np.mean(pitcher_char[["induced_vb"]]))
sd_iVB = float(np.std(pitcher_char["induced_vb"], ddof=1))

avg_VAA = float(np.mean(pitcher_char[["vaa"]]))
sd_VAA = float(np.std(pitcher_char["vaa"], ddof=1))

avg_velocity = float(np.mean(pitcher_char[["release_speed"]]))
sd_velocity = float(np.std(pitcher_char["release_speed"], ddof=1))

pitcher_char = pitcher_char.groupby("pitcher_name").mean().reset_index()
pitcher_char = pitcher_char[pitcher_char["fb_count"] >= 250]

# svant_data_11_6_24.csv contains all outcomes of four-seam fastballs thrown in the upper third and above 
# the strike zone
pitcher_stats = pd.read_csv("savant_data_11_6_24.csv")
# pitcher_stats = total pitches, whiffs, swings
pitcher_stats = pitcher_stats.loc[:, ["player_name", "total_pitches", "whiffs", "swings"]]


# Step 2: Calculate LAAFEI for each pitcher by applying the appropriate averages
def LAAFEI_calculation(row):
    Z_iVB = (row["induced_vb"] - avg_iVB) / sd_iVB
    Z_VAA = (row["vaa"] - avg_VAA) / sd_VAA
    Z_velocity = (row["release_speed"] - avg_velocity) / sd_velocity
    weighted_Z = (Z_iVB * 0.4) + (Z_VAA * 0.55) + (Z_velocity * 0.05)
    # Calculate LAAFEI score with a mean of 100 and standard deviation factor of 15
    LAAFEI = 100 + (weighted_Z * 15)
    return LAAFEI

pitcher_char["LAAFEI"] = pitcher_char.apply(LAAFEI_calculation, axis=1)


# Step 3: calculate Whiff% for each pitcher
def whiffperc_calc(row):
    whiff_perc = (row["whiffs"] / row["swings"]) * 100
    return whiff_perc

pitcher_stats["Whiff%"] = pitcher_stats.apply(whiffperc_calc, axis=1)


# Step 4: Create the sorted LAAFEI leaderboard linear regression for the data
# Split `player_name` and reorder to "firstname lastname"
pitcher_stats['player_name'] = pitcher_stats['player_name'].apply(lambda name: ' '.join(reversed(name.split(', '))))
pitcher_data = pitcher_char.merge(pitcher_stats, left_on="pitcher_name", right_on="player_name", how="inner")
pitcher_data = pitcher_data.drop('player_name', axis=1)
pitcher_data = pitcher_data.groupby('pitcher_name').mean().reset_index()
LAAFEI_data = pitcher_data.loc[:, ["LAAFEI"]]
whiff_data = pitcher_data.loc[:, "Whiff%"]
LAAFEI_leaderboard = pitcher_data.sort_values(by='LAAFEI', ascending=False)
LAAFEI_leaderboard = LAAFEI_leaderboard.drop(["release_speed", "induced_vb", "vaa", "fb_count", "total_pitches", 
                                              "whiffs", "swings", "Whiff%"], axis=1)

lr = LinearRegression(fit_intercept=True)
lr.fit(LAAFEI_data, whiff_data)
whiff_pred = lr.predict(LAAFEI_data)
slope = lr.coef_[0]
intercept = lr.intercept_
r_value = lr.score(LAAFEI_data, whiff_data)

regression_info = f"y = {slope:.2f}x + {intercept:.2f}\nR^2 = {r_value:.2f}"


# Step 5: Plot the results
# Convert to 1D arrays for plotting
LAAFEI_data_values = LAAFEI_data.values.ravel()
whiff_data_values = whiff_data.values.ravel()

fig = px.scatter(pitcher_data, x='LAAFEI', y='Whiff%', hover_name='pitcher_name',
                 hover_data=['LAAFEI', 'Whiff%'], title="Relationship Between LAAFEI and Whiff% on Elevated Fastballs")
fig.add_scatter(x=pitcher_data['LAAFEI'], y=whiff_pred, mode='lines', name='Regression Line')
fig.add_annotation(
    x=87.5,
    y=42.5,
    text=regression_info,
    showarrow=False,
    font=dict(size=18, color="black"),
    bgcolor="white",
    borderpad=4
)
fig.show()

