import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

import data_parsing

db_location = "../Data/soccer/database.sqlite"

# ***********  get pandas DataFrames from sqlite file ***********
data_parsing.set_db_location(db_location)
countries = data_parsing.get_table_as_pd_dataframe('Country')
leagues = data_parsing.get_table_as_pd_dataframe('League')
matches = data_parsing.get_table_as_pd_dataframe('Match')
players_data = data_parsing.get_table_as_pd_dataframe('Player')
player_attributes = data_parsing.get_table_as_pd_dataframe('Player_Attributes')
teams_data = data_parsing.get_table_as_pd_dataframe('Team')
team_attributes = data_parsing.get_table_as_pd_dataframe('Team_Attributes')

# ***********  merge some tables  ***********
players = (players_data.merge(player_attributes, how='inner', on=[
           'player_fifa_api_id', 'player_api_id'], suffixes=('', '_pa'), validate='one_to_many')).drop(columns=['id_pa', 'id'])
teams = (teams_data.merge(team_attributes, how='inner', on=['team_fifa_api_id', 'team_api_id'], suffixes=(
    '', '_pa'), validate='one_to_many')).drop(columns=['id_pa', 'id'])

# ***********  clean the data  ***********
teams['team_fifa_api_id'] = pd.to_numeric(
    teams['team_fifa_api_id'], downcast='integer', errors='coerce')

# *********** TODO ***********
print(teams.head())
