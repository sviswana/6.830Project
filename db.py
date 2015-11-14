import json


class Db:
    def get_data(self,timestamp,data):
        ##assumes timestamp is passed in seconds
        filename = timestamp / 86400
        with open(str(filename)+'.txt', 'a') as outfile:
            json.dump(data, outfile)



        
