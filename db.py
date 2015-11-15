import json
#[update <timestamp> Hillary 5]

class Db:
    def __init__(self):
        self.countMap = {}
        for i in range(0,288):
            self.countMap[i*5] = {}
        
    def get_data(self,timestamp,data):
        ##assumes timestamp is passed in seconds
        filename = timestamp / 86400
        countMap = []
        
        with open(str(filename)+'.txt', 'a') as outfile:
            json.loads(data)


    def insert(self,timestamp, keyword, count):
        ##assume values is coming in the python form:
        ##[('clinton', 1),('sanders',1)]
        ##do we want to store individual timestamps as well
        filename = timestamp / 86400
        tempTime = timestamp / 300
        bucket = tempTime % 288
        keywords = self.countMap[bucket]
    
        if not keyword in keywords:
            self.countMap[bucket][keyword] = count
        else:
            self.countMap[bucket][keyword]+=count
        with open(str(filename)+'.txt', 'a') as outfile:
            json.loads(self.countMap) ## we don't want to load it every time. 
        return True

    #for right now, we only support one timestamp for select
    def select(self, timestamp, keyword):
        filename = timestamp / 86400
        tempTime = timestamp / 300
        bucket = tempTime % 288
        #first get the associated page with this data & timestamp
        with open(str(filename)+'.txt') as data_file:
            dataMap = json.load(data_file)
        if not dataMap[bucket][keyword]:
            return 0
        else:
            return dataMap[bucket][keyword]
            
            
    def update(self,timestamp, values):

    def checkIfExists(timestamp):
    
    #helper function if we want to change window size for inserting in future
    def setWindow(self, windowSize):
        return 24*60 / windowSize
    
        
