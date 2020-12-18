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
                teams_data = helper.generateData(script.text)
                infos['teams'] = helper.getAllTeamsName(ast.literal_eval(helper.generateData(script.text)), filter)
                infos['allteams'] = teams_data
            if 'playersData' in script.text:
                infos['players'] = helper.generateData(script.text)
            if 'datesData' in script.text:
                infos['dates'] = helper.generateData(script.text)

        return infos
       

    def helloworld(self, arg):
        print('Hello World UnderStat')
    
