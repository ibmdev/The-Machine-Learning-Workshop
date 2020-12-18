import operator

class Utils:
    def find_ind_start(self, arg):
        return arg.index("('")+2
    
    def find_ind_end(self, arg):
        return arg.index("')")
    
    def generateData(self, arg):
        data_json = arg.strip()
        ind_start = self.find_ind_start(data_json)
        ind_end =   self.find_ind_end(data_json)
        data = data_json[ind_start:ind_end]
        data = data.encode('utf8').decode('unicode_escape')
        return data
    def get_PTS(self, obj):
        return obj['PTS']
    
    def getAllTeamsName(self, data, filter):
        temp = []
        index = 1
        for id in data.keys():
            W = 0
            D = 0
            L = 0
            GF = 0
            GA = 0
            PTS = 0
            xG = 0
            xGA = 0
            xPTS = 0
            npxG = 0
            npxGA = 0
            xG_diff = 0
            xGA_diff = 0
            xPTS_diff = 0
            histories = data[id]['history'] 
            if 'h' == filter['type'] or 'a' == filter['type']:
                histories = [x for x in data[id]['history'] if x['h_a'] == filter['type']]
            for histo in histories:
                W += histo['wins']
                D += histo['draws']
                L += histo['loses']
                GF += histo['scored']
                GA += histo['missed']
                PTS += histo['pts']
                xG += histo['xG']
                xGA += histo['xGA']
                xPTS += histo['xpts']
                npxG += histo['npxG']
                npxGA += histo['npxGA']
                xG_diff += histo['xG'] - histo['scored']
                xGA_diff += histo['xGA'] - histo['missed']
                xPTS_diff += histo['xpts'] - histo['pts']
            team = {
                   'Team' : data[id]['title'],
                   'M': len(histories),
                   'W': W,
                   'D' : D,
                   'L': L,
                   'GF': GF,
                   'GA': GA,
                   'PTS': PTS,
                   'xG' : xG,
                   'xG_diff' : xG_diff,
                   'npxG' : npxG, 
                   'xGA' : xGA,
                   'xGA_diff' : xGA_diff,
                   'npxGA' : npxGA,
                   'xPTS' : xPTS,
                   'xPTS_diff' : xPTS_diff 
                   }
            temp.append(team)
            index += 1
        temp.sort(key=self.get_PTS, reverse=True)
        return temp
            
            
    