# LAAFEI_Statistic

LAAFEI attempts to quantify and standardize the effectiveness of four-seam fastballs in the uppermost three quadrants of the strike zone along with above the strike zone thrown by pitchers based on characteristics of their fastball [VAA (vertical approach angle), iVB (induced vertical break), and velocity]. This stat is adjusted so that a score of 100 is league average and 115 is 1 standard deviation above league average. Our goal in creating this stat was to measure how effective some pitchers can be with this collection of four seam fastball characteristics up in the zone.

## LAAFEI_stat.py

This file contains the code that was used to calculate LAAFEI for each pitcher, create a leaderboard sorted in descending order of LAAFEI, and create a linear regression of LAAFEI compared to top of the strike zone and above Whiff% on four-seam fastballs. The .csv file "new_stat_11_6_24.csv" was pulled from Baseball Savant's website and contains all of the pitch metrics of four-seam fastballs thrown by pitchers in the 2024 season, up to date as of November 6, 2024, used to obtain league and individual pitchers' averages. The other .csv file "savant_data_11_6_24.csv" (also pulled from Baseball Savant's website) contains all of the outcome data of four-seam fastballs thrown at the top of the zone or above, used to determine individual pitchers' Whiff% on those pitches.

## LAAFEI_calc.py

This file contains the code that functions as a calculator to determine any one pitcher's LAAFEI when provided their name, average velocity, average VAA, and average iVB. The same "new_stat_11_6_24.csv" file was used as previously mentioned.
