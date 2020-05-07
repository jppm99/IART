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

# *********** drop useless columns ***********
matches.drop(list(matches.filter(regex='^[A-Z]+$')), axis=1, inplace=True)
matches.drop(columns=['country_id', 'possession', 'corner', 'cross',
                      'card', 'foulcommit', 'shotoff', 'shoton', 'goal'], inplace=True)
players_data.drop(columns=['birthday', 'height', 'weight'], inplace=True)
player_attributes = player_attributes[[
    'id', 'player_fifa_api_id', 'player_api_id', 'date', 'overall_rating']]

# ***********  merge some tables  ***********
players = (players_data.merge(player_attributes, how='inner', on=['player_fifa_api_id', 'player_api_id'], suffixes=(
    '', '_pa'), validate='one_to_many')).drop(columns=['id_pa', 'id'])
teams = (teams_data.merge(team_attributes, how='inner', on=['team_fifa_api_id', 'team_api_id'], suffixes=(
    '', '_pa'), validate='one_to_many')).drop(columns=['id_pa', 'id'])

# ***********  clean the data  ***********
teams['team_fifa_api_id'] = pd.to_numeric(
    teams['team_fifa_api_id'], downcast='integer', errors='coerce')

players = players.dropna()
players['overall_rating'] = players['overall_rating'].astype('int8')

countries = countries.dropna()
leagues = leagues.dropna()

# teams with buildUpPlayDribblingClass as 'little' will have buildUpPlayDribbling as NaN
teams.buildUpPlayDribbling = teams.buildUpPlayDribbling.fillna(20)
teams = teams.dropna()

matches = matches.dropna(subset=['B365A', 'B365D', 'B365H', 'id', 'league_id', 'season',
                                 'match_api_id', 'home_team_api_id', 'away_team_api_id', 'home_team_goal', 'away_team_goal'])

# *********** TODO ***********
