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
    def getAllTeamsName(self, arg):
        teamsName = {}
        index = 1
        for id in arg.keys():
            teamsName[index] = arg[id]['title']
            index += 1
        return teamsName
            
            
    