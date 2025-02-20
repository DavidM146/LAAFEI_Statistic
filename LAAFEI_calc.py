import pandas as pd
import numpy as np

# Define LAAFEI calculator function
def LAAFEI_calulator(velocity, iVB, VAA):
    Z_velocity = (velocity - avg_velocity) / sd_velocity
    Z_iVB = (iVB - avg_iVB) / sd_iVB
    Z_VAA = (VAA - avg_VAA) / sd_VAA
    weighted_Z = (Z_iVB * 0.4) + (Z_VAA * 0.55) + (Z_velocity * 0.05)
    # LAAFEI centered at 100 with standard error of 15
    LAAFEI = 100 + (weighted_Z * 15)
    print(f"{name}'s LAAFEI is {LAAFEI:.2f}, putting them {weighted_Z:.2f} standard deviations from Major League average")


# Import databases
pitcher_char = pd.read_csv("new_stat_11_6_24.csv")
pitcher_char = pitcher_char[pitcher_char["pitch_type"] == 'FF']
pitcher_char = pitcher_char.loc[:, ["release_speed", "induced_vb", "vaa"]]


# Define league averages and standard deviations
avg_velocity = float(np.mean(pitcher_char[["release_speed"]]))
sd_velocity = float(np.std(pitcher_char[["release_speed"]]))

avg_iVB = float(np.mean(pitcher_char[["induced_vb"]]))
sd_iVB = float(np.std(pitcher_char[["induced_vb"]]))

avg_VAA = float(np.mean(pitcher_char[["vaa"]]))
sd_VAA = float(np.std(pitcher_char[["vaa"]]))

while True:
    # Request information from user
    name = input("Name of Pitcher: ")
    velocity = float(input("Average Velocity: "))
    iVB = float(input("Average Induced Vertical Break (iVB): "))
    VAA = float(input("Average Vertical Approach Angle (VAA): "))

    LAAFEI_calulator(velocity, iVB, VAA)
    restart = input("Would you like to calculate another LAAFEI? (yes/no): ").strip().lower()

    if restart != "yes":
        print("\nExiting the LAAFEI Calculator")
        break


