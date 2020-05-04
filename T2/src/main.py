import sqlite3
import pandas as pd

db_location = "../Data/soccer/database.sqlite"

# ***********  get tables from sqlite file ************
con = sqlite3.connect(db_location)
cur = con.cursor()

cur.execute('SELECT * FROM Country;')
countries = cur.fetchall()

cur.execute('SELECT * FROM League;')
leagues = cur.fetchall()

cur.execute('SELECT * FROM Match;')
matches = cur.fetchall()

cur.execute('SELECT * FROM Player WHERE player_name="Moussa Marega";')
players = cur.fetchall()

cur.execute('SELECT * FROM Player_Attributes;')
player_attributes = cur.fetchall()

cur.execute('SELECT * FROM Team;')
teams = cur.fetchall()

cur.execute('SELECT * FROM Team_Attributes;')
team_attributes = cur.fetchall()

con.close()

# *********** TODO ************

print(players)
