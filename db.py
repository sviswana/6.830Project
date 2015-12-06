import json
import os
import ast
import random
#[update <timestamp> Hillary 5]
from LRU import LRU
class Database:
    candidateList = ["Hillary Clinton","Carly Fiorina","Bernie Sanders","Marco Rubio", "Donald Trump", "Ted Cruz", "Ben Carson", "Rand Paul"]
    def get_data(self,timestamp,data):
        ##assumes timestamp is passed in seconds
        filename = timestamp / 86400
        countMap = []
        
        with open(str(filename)+'.txt', 'a') as outfile:
            json.loads(data)

    '''
    def accumulateFile(self, fileName):
        #Load the file we want to accumulate values for
        with open(fileName) as current_file:
            dataMap = json.load(current_file)

        startTimestamp = int(filename[:-4]) * 86400
        #load the accumulated counts file
        with open('accumulatedCounts.txt') as currentCounts_file:
            currentMap = json.load(currentCounts_file)
            for i in range(0,288):
                for candidate in candidateList:
                    if candidate in dataMap[str(i)]:
                        currentMap[] += currentMap[startTimestamp - ]
                for candidate in dataMap[str(i)]:
                    dataMap[i]
                startTimestamp +=300

    '''


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
        
        if LRU.get(str(filename)) == -1:
            with open(str(filename)+'.txt') as data_file:
                dataMap = json.load(data_file)
                LRU.set(str(filename), dataMap)
        else:
            dataMap = LRU.get(str(filename))       
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
            #counts per bucket
            dataMap[bucket][keyword]+=count
        #to get the aggregate counts for each keyword for a day
        if not keyword in dataMap:
            dataMap[keyword] = count
        else:
            dataMap[keyword]+=count
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
    ##NOTE THAT THIS RETURNS A STRING VALUE (NEED TO CHANGE IN FUTURE)
    def select(self, timestamp, keyword):
        [filename, bucket] = self.getNames(timestamp)
        bucket = str(bucket)
        keyword = str(keyword)
        #first get the associated page with this data & timestamp
        if LRU.get(str(filename)) == -1:
            with open(str(filename)+'.txt') as data_file:
                dataMap = json.load(data_file)
                LRU.set(str(filename), dataMap)
        else:
            dataMap = LRU.get(str(filename))
        if bucket in dataMap and keyword in dataMap[bucket]:
            return str(dataMap[bucket][keyword])
        else:
            return str(0)
            

    #for right now, support start and end timestamp, and one keyword
    def selectRange(self, startTimestamp, endTimestamp, keyword):
        [startFileNumber, startBucket] = getNames(startTimestamp) 
        [endFileNumber, endBucket] = getNames(endTimestamp)
        aggregateCount = 0
        #If timestamps span more than a day, we need to ensure that we get all the buckets in the range
        for fileNumber in range(startFileNumber, endFileNumber+1):
            if fileNumber == startFileNumber:
                startB = startBucket
                endB = 287 #hardcoding right now, but can call windowsize if we want this to work for different time ranges
            elif fileNumber == endFileNumber:
                startB = 0
                endB = endBucket
            else:
                startB = 0
                endB = 287
            for bucketNumber in range(startB, endB+1):
                bucketNumber = str(bucketNumber)
                if LRU.get(str(fileNumber)) == -1:
                    with open(str(fileNumber)+'.txt') as data_file:
                        dataMap = json.load(data_file)
                        LRU.set(str(fileNumber), dataMap)
                else:
                    dataMap = LRU.get(str(fileNumber))
                if bucketNumber in dataMap and str(keyword) in dataMap[bucketNumber]:
                    aggregateCount+=dataMap[bucketNumber][str(keyword)]
        return str(aggregateCount)
        
        #windowSize can be 
    def selectRangeForDisplay(self, startTimestamp, endTimestamp, keyword):
        #sample timestamp is 1449186990 (assuming was divided by 1000 already)
        tick = 5 * 60 #seconds to add - assuming window size is 5 here!
        bucketMod = setWindow(5)
        [startFileNumber, startBucket] = getNames(startTimestamp) #convert bucket to string
        [endFileNumber, endBucket] = getNames(endTimestamp)
        
        #If timestamps span more than a day, we need to ensure that we get all the buckets in the range
        t = timestamps[0]
        finalList = []
        for fileNumber in range(startFileNumber, endFileNumber+1):
            if fileNumber == startFileNumber:
                startB = startBucket
                if startFileNumber==endFileNumber:
                    endB = endBucket
                else:
                    endB = bucketMod-1 
            elif fileNumber == endFileNumber+1:
                startB = 0
                endB = endBucket
            else:
                startB = 0
                endB = bucketMod -1
            for bucketNumber in range(startB, endB+1):

                bucketNumber = str(bucketNumber)
                if LRU.get(str(fileNumber)) == -1:
                    with open(str(fileNumber)+'.txt') as data_file:
                        dataMap = json.load(data_file)
                        LRU.set(str(fileNumber), dataMap)
                else:
                    dataMap = LRU.get(str(fileNumber))
                if bucketNumber in dataMap and str(keyword) in dataMap[bucketNumber]:
                    count=dataMap[bucketNumber][str(keyword)]
                    finalList.append((t, count))
                t = t+ tick
                    
        return finalList

    
    #helper function if we want to change window size for inserting in future
    def setWindow(self, windowSize):
        return 24*60 / windowSize
db = Database()

'''
names = ['Hillary Clinton','Carly Fiorina','Bernie Sanders','BernieSanders','Marco Rubio','Donald Trump','Ted Cruz','Ben Carson','Rand Paul']


count = 2500
for name in names:   
    db.insert(1448082159999/1000, name, count)
    count +=random.randint(1000,5000)
    db.insert(1448081559999/1000, name, count)
    count+=random.randint(1000,5000)
    db.insert(1448080959999/1000, name,count)
    count+=random.randint(1000,5000)
    db.insert(1448081859999/1000, name, count)
    count+=random.randint(1000,5000)
    db.insert(1448081259999/1000, name, count)
    count+=random.randint(1000,5000)

'''

