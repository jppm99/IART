import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

import data_parsing

db_location = "../Data/soccer/database.sqlite"

# ***********  get pandas DataFrames from sqlite file ************
data_parsing.set_db_location(db_location)
countries = data_parsing.get_table_as_pd_dataframe('Country')
leagues = data_parsing.get_table_as_pd_dataframe('League')
matches = data_parsing.get_table_as_pd_dataframe('Match')
players = data_parsing.get_table_as_pd_dataframe('Player')
player_attributes = data_parsing.get_table_as_pd_dataframe('Player_Attributes')
teams = data_parsing.get_table_as_pd_dataframe('Team')
team_attributes = data_parsing.get_table_as_pd_dataframe('Team_Attributes')

# *********** TODO ************
print(matches.head())
