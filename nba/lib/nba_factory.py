import numpy as np
import pandas as pd
import requests
import json
import ast
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from os import path
class NbaService:
    
    def getStats(self, url):
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        soup.findAll('tr', limit=2)
        headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        headers = headers[1:]
        rows = soup.findAll('tr')[1:]
        player_stats = [[td.getText() for td in rows[i].findAll('td')]
                        for i in range(len(rows))]
        stats = pd.DataFrame(player_stats, columns = headers)
        print(len(player_stats))
        return player_stats
    
    def getTeamsName(self, player_stats):
        teamsName = []
        for i in range(len(player_stats)):
            if len(player_stats[i]) > 0:
                playerjson = {'name': player_stats[i][0]}
                teamsName.append(player_stats[i][3])
                teamsName = list(dict.fromkeys(teamsName))
        return teamsName
    
    def getAllStats(self, teamsName, player_stats):
        allStats = []
        for team in teamsName:
            teamJson = {'team': team, 'players': []}
            for i in range(len(player_stats)):
                if len(player_stats[i]) > 0 and player_stats[i][3] == team:
                    playerjson = {'name': player_stats[i][0],
                                  'position': player_stats[i][1],
                                  'age': player_stats[i][2],
                                  'games': player_stats[i][4],
                                  'games_started': player_stats[i][5],
                                  'minutes_played_per_game': player_stats[i][6],
                                  'field_goal_per_game': player_stats[i][7],
                                  'field_goal_attempt_per_game': player_stats[i][8],
                                  'field_goal_percent_per_game': player_stats[i][9],
                                  'three_points_field_goal_per_game': player_stats[i][10],
                                  'three_points_field_goal_attempt_per_game': player_stats[i][11],
                                  'three_points_field_goal_percent_per_game': player_stats[i][12],
                                  'two_points_field_goal_per_game': player_stats[i][13],
                                  'two_points_field_goal_attempt_per_game': player_stats[i][14],
                                  'two_points_field_goal_percent_per_game': player_stats[i][15],
                                  'effective_field_goal_percent_per_game': player_stats[i][16],
                                  'free_throws_per_game': player_stats[i][17],
                                  'free_throws_attempt_per_game': player_stats[i][18],
                                  'free_throws_percent_per_game': player_stats[i][19],
                                  'offensive_rebound_per_game': player_stats[i][20],
                                  'defensive_rebound_per_game': player_stats[i][21],
                                  'total_rebound_per_game': player_stats[i][22],
                                  'assists_per_game': player_stats[i][23],
                                  'steal_per_game': player_stats[i][24],
                                  'block_per_game': player_stats[i][25],
                                  'turnover_per_game': player_stats[i][26],
                                  'personal_fouls_per_game': player_stats[i][27],
                                  'points_per_game': player_stats[i][28]
                                 }
                    teamJson['players'].append(playerjson)
            allStats.append(teamJson)        
        return allStats