import requests
import json
import ast
from bs4 import BeautifulSoup
from lib import Helper
from constants import understat_constants
from datetime import datetime
from os import path
class UnderStatService:
    
    # Get data for Betting
    def getBettingData(self):
        globalInfos = []
        filter = {'type': ''}
        present = datetime.now()
        for league in understat_constants.leagues:
            # Chargement des données de la league depuis football-data.co.uk
            fdata = []
            if path.exists(league +'.json'):
                with open(league +'.json') as json_file:
                    fdata = json.load(json_file)
            leagueInfos = {'name': league, 'fixtures': []}
            data = self.getInfosByLeague(league, filter)
            datesData = json.loads(data['dates'])
            # Chargement des équipes de la league en cours
            teams = data['teams']
            teamsName = self.getTeamsName(teams)
            statsLeague = [];
            for team in teamsName:
                infosTeam = self.getInfosByTeam(team['Team'])
                # Liste des joueurs de l'équipe
                playersData = json.loads(infosTeam['playersData'])
                # for player in playersData:
                    # idPlayer = player['id']
                    # statsPlayer = self.getPlayerStats(idPlayer)
                    # player['stats'] = statsPlayer 
                # Historique de l'équipe
                histoData = json.loads(infosTeam['datesData'])
                histoData = [x for x in histoData if (datetime.strptime(x['datetime'], "%Y-%m-%d %H:%M:%S") <= present) & (x['isResult'] == True)]
                
                # Statistiques de l'équipe + liste des équipes w, d et l
                histoTeams = {'w': [], 'd':[], 'l': []}
                for histMatch in histoData:
                        tm = {'id':'', 'title':''}
                        if histMatch['side'] == 'h':
                            tm['id'] = histMatch['a']['id']
                            tm['title'] = histMatch['a']['title']
                        if histMatch['side'] == 'a':
                            tm['id'] = histMatch['h']['id']
                            tm['title'] = histMatch['h']['title']
                        if histMatch['result'] == 'w':
                            histoTeams['w'].append(tm)
                        if histMatch['result'] == 'd':
                            histoTeams['d'].append(tm)
                        if histMatch['result'] == 'l':
                            histoTeams['l'].append(tm)
                team['stats'] = json.loads(infosTeam['statisticsData'])
                team['histo'] = histoTeams
                team['players'] = playersData
                if len(fdata) > 0:
                    team['results'] = self.getResultsFromFootballDataCoUk(fdata,team['Team'])
                statsLeague.append(team);
                
            leagueInfos['stats'] = statsLeague
            # Fixtures : Recherche des prochains matchs
            datesData = [x for x in datesData if (datetime.strptime(x['datetime'], "%Y-%m-%d %H:%M:%S") >= present) & (x['isResult'] == False)]
            for evt in datesData:
                homeTeamId = evt['h']['id']
                awayTeamId = evt['a']['id']
                homeTeam = [x for x in data['teams'] if x['id'] == homeTeamId][0]
                awayTeam = [x for x in data['teams'] if x['id'] == awayTeamId][0]
                match = {'date': evt['datetime'],
                         'home' : {'id': homeTeam['id'], 'Team': homeTeam['Team']},
                         'away' : {'id': awayTeam['id'], 'Team': awayTeam['Team']}
                        }
                # print(match)
                leagueInfos['fixtures'].append(match)
            globalInfos.append(leagueInfos)
            with open('data.json', 'w') as outfile:
                json.dump(globalInfos, outfile)
    
    # Team : Récupération des données des matchs passées d'une équipe depuis football-data.co.uk
    def getResultsFromFootballDataCoUk(self, datacouk, team):
        results = []
        for data in datacouk:
            result = {'time': data['Date'], 'h': data['HomeTeam'].replace(' ','_'), 'a': data['AwayTeam'].replace(' ','_'), 'HTR': 
                     data['HTR'], 'FTR': data['FTR'],'HTHG': data['HTHG'], 'HTAG': data['HTAG'], 'FTHG': data['FTHG'], 'FTAG': 
                     data['FTAG'], 'B365H': data['B365H'],'B365D': data['B365D'],'B365A': data['B365A'], 'B365>2.5': data['B365>2.5'], 
                     'B365<2.5': data['B365<2.5'] }
            if data['HomeTeam'].replace(' ','_') == team:
                result['side'] = 'h'
                results.append(result)
            if data['AwayTeam'].replace(' ','_') == team:
                result['side'] = 'a'
                results.append(result)
        return results 
                
        
    # League : Classement des équipes, statistiques des joueurs de la ligue, calendrier et résultats des équipes
    def getInfosByLeague(self, league, filter):
        helper = Helper.Utils()
        infos = {'teams': {}, 'allteams': {}, 'players': {}, 'dates': {}}
        url = understat_constants.base_url_league+'/'+league
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "lxml")
        scripts = soup.find_all('script')
        for script in scripts:
            if 'teamsData' in script.text:
                teams_data = helper.extractDataFromScript(script.text)
                infos['teams'] = helper.getStatsDataForLeague(ast.literal_eval(teams_data), filter)
                infos['allteams'] = teams_data
            if 'playersData' in script.text:
                infos['players'] = helper.extractDataFromScript(script.text)
            if 'datesData' in script.text:
                infos['dates'] = helper.extractDataFromScript(script.text)

        return infos
       
    # Team : Calendrier et résultats de l'équipe, statistiques de l'équipe, statistiques des joueurs de l'équipe 
    def getInfosByTeam(self, team):
        helper = Helper.Utils()
        infos = {'datesData': {}, 'statisticsData': {}, 'playersData': {}}
        url = understat_constants.base_url_team+'/'+team
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "lxml")
        scripts = soup.find_all('script')
        for script in scripts:
            if 'datesData' in script.text:
                datesData = helper.extractDataFromScript(script.text)
                infos['datesData'] = datesData
            if 'statisticsData' in script.text:
                statisticsData = helper.extractDataFromScript(script.text)
                infos['statisticsData'] = statisticsData
            if 'playersData' in script.text:
                playersData = helper.extractDataFromScript(script.text)
                infos['playersData'] = playersData
        return infos
    
    # API : Récupération des statistiques des joueurs d'une équipe
    def getPlayersStats(self, filter):
        url = understat_constants.base_url_players_stats
        res = requests.post(url, data = filter)
        print(res.text)
    
    # API : Récupération des statistiques d'un joueur
    def getPlayerStats(self, id):
        helper = Helper.Utils()
        infos = {'groupsData': {}, 'minMaxPlayerStats': {}, 'shotsData': {}, 'matchesData': {}}
        url = understat_constants.base_url_player_stats + id
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "lxml")
        scripts = soup.find_all('script')
        for script in scripts:
            if 'groupsData' in script.text:
                groupsData = helper.extractDataFromScript(script.text)
                infos['groupsData'] = json.loads(groupsData)
            if 'minMaxPlayerStats' in script.text:
                minMaxPlayerStats = helper.extractDataFromScript(script.text)
                infos['minMaxPlayerStats'] = json.loads(minMaxPlayerStats)
            if 'shotsData' in script.text:
                shotsData = helper.extractDataFromScript(script.text)
                infos['shotsData'] = json.loads(shotsData)
            if 'matchesData' in script.text:
                matchesData = helper.extractDataFromScript(script.text)
                infos['matchesData'] = json.loads(matchesData)
        return infos
    
    # Utilitaire : retourne la liste des noms des équipes de la league
    def getTeamsName(self, arg):
        teamsName = []
        for team in arg:
            team['Team'] = team['Team'].replace(' ','_')
            teamsName.append(team)
        return teamsName
            
    
