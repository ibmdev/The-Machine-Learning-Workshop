import requests
import json
import ast
from bs4 import BeautifulSoup
from lib import Helper
from constants import understat_constants
class UnderStatService:
    
    def getInfosByLeague(self, league, filter):
        helper = Helper.Utils()
        infos = {'teams': {}, 'allteams': {}, 'players': {}, 'dates': {}}
        url = understat_constants.base_url+'/'+league
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "lxml")
        scripts = soup.find_all('script')
        # Affichage de la liste des scripts
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
       

    def helloworld(self, arg):
        print('Hello World UnderStat')
    
