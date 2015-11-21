import json
import os
import ast
#[update <timestamp> Hillary 5]

class Db:
        
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
        if not os.path.isfile(str(filename)+'.txt'):
            print 'file doesnt exist'
            dataMap = {}
            for i in range(0,288):
                dataMap[i] = {}
            with open(str(filename)+'.txt','w') as data_file:
                #json.dump(ast.literal_eval(str(dataMap)), data_file)
                json.dump(dataMap, data_file)
                
        with open(str(filename)+'.txt') as data_file:
            dataMap = json.load(data_file)
        #print 'dataMap', dataMap#str(dataMap).replace("u\'","\'")
        print "bucket", bucket
        keywords = dataMap[str(bucket)]
        bucket = str(bucket)
        print 'keywords', keywords
        if not keyword in keywords:
            print 'not in keyword so adding'
            dataMap[bucket][keyword] = count
            #print 'dataMap', dataMap
        else:
            dataMap[bucket][keyword]+=count
            
        with open(str(filename)+'.txt', 'w') as outfile:
            print 'writing to json output'
            #print dataMap
            json.dump(dataMap, outfile) ## we don't want to load it every time. 
        return True


    def getNames(self, timestamp):
        filename = timestamp / 86400
        tempTime = timestamp / 300
        bucket = tempTime % 288
        return [filename, bucket]

    #for right now, we only support one timestamp for select
    def select(self, timestamp, keyword):
        [filename, bucket] = getNames(timestamp)
        
        #first get the associated page with this data & timestamp
        with open(str(filename)+'.txt') as data_file:
            dataMap = json.load(data_file)
        if not keyword in dataMap[bucket]:
            return 0
        else:
            return dataMap[bucket][keyword]
            
    #for right now, support start and end timestamp, and one keyword
    def selectRange(self, timestamps, keyword):
        [startFileNumber, startBucket] = getNames(timestamps[0])
        [endFileNumber, endBucket] = getNames(timestamps[1])
        aggregateCount = 0
        for fileNumber in range(startFileNumber, endFileNumber+1):
            with open(str(fileNumber)+'.txt') as data_file:
                dataMap = json.load(data_file)
            if keyword in dataMap[bucket]:
                aggregateCount+=dataMap[bucket][keyword]
        return aggregateCount
        
        

    
    #helper function if we want to change window size for inserting in future
    def setWindow(self, windowSize):
        return 24*60 / windowSize
    