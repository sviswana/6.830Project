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

    def accumulateFile(self, fileName):
        #Load the file we want to accumulate values for
        with open(fileName,'r') as current_file:
            dataMap = json.load(current_file)

        startTimestamp = int(fileName[:-4]) * 86400

        #load the accumulated counts file
        with open('accumulatedCounts.txt','r') as currentCounts_file:
            try:
                currentMap = json.load(currentCounts_file)
            except:
                currentMap = {}
                currentMap["firstTime"] = startTimestamp
            #go through each bucket
            for bucket in range(0,288):
                currentMap[startTimestamp] = {}
                for candidate in candidateList:
                    if candidate in dataMap[str(bucket)]:
                        if not (startTimestamp-300) in currentMap:
                            currentMap[startTimestamp][candidate] = dataMap[str(bucket)][candidate]
                        else:
                            currentMap[startTimestamp][candidate] = currentMap[startTimestamp - 300][candidate] + dataMap[str(bucket)][candidate]
                    else:
                        if not (startTimestamp-300) in currentMap:
                            currentMap[startTimestamp][candidate] = 0
                        else:
                            currentMap[startTimestamp][candidate] = currentMap[startTimestamp - 300][candidate]                 
                startTimestamp += 300
            currentMap["lastTime"] = startTimestamp
        with open('accumulatedCounts.txt','w') as updated_file:
            json.dump(currentMap, updated_file)
    def insert(self,timestamp, keyword, count):
        ##assume values is coming in the python form:
        ##[('clinton', 1),('sanders',1)]
        ##do we want to store individual timestamps as well
        filename = timestamp / 86400
        tempTime = timestamp / 300
        bucket = tempTime % 288
        print filename
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
            return [timestamp, dataMap[bucket][keyword]]
        else:
            return [timestamp, 0]
            
    def selectFastRange(self,startTimestamp, endTimestamp, keyword):
        with open('accumulatedCounts.txt','r') as cumul_file:
            cumulMap = json.load(cumul_file)
            startTimestamp = (startTimestamp / 300) * 300
            endTimestamp = (endTimestamp / 300) * 300
            if endTimestamp > cumulMap["lastTime"]:
                endTimestamp = cumulMap["lastTime"]
            if startTimestamp < cumulMap["firstTime"]:
                startTimestamp = cumulMap["firstTime"]
            last = cumulMap[str(endTimestamp)][str(keyword)]
            start = cumulMap[str(startTimestamp - 300)][str(keyword)]
            return last - start



    #for right now, support start and end timestamp, and one keyword
    def selectRange(self, startTimestamp, endTimestamp, keyword):
        [startFileNumber, startBucket] = self.getNames(startTimestamp) 
        [endFileNumber, endBucket] = self.getNames(endTimestamp)
        aggregateCount = 0
        #If timestamps span more than a day, we need to ensure that we get all the buckets in the range
        for fileNumber in range(startFileNumber, endFileNumber+1):
            if fileNumber == startFileNumber:
                startB = startBucket
                if startFileNumber==endFileNumber:
                    endB = endBucket
                else:
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
        if (endTimestamp < startTimestamp):
            return []
        tick = 5 * 60 #seconds to add - assuming window size is 5 here!
        bucketMod = self.setWindow(5)
        [startFileNumber, startBucket] = self.getNames(startTimestamp) #convert bucket to string
        [endFileNumber, endBucket] = self.getNames(endTimestamp)
        
        #If timestamps span more than a day, we need to ensure that we get all the buckets in the range
        t = startTimestamp
        finalList = []
        for fileNumber in range(startFileNumber, endFileNumber+1):
            if fileNumber == startFileNumber:
                startB = startBucket
                if startFileNumber==endFileNumber:
                    endB = endBucket
                else:
                    endB = bucketMod-1 
            elif fileNumber == endFileNumber:
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

    def selectRangeAndInterval(self, startTime, endTime, interval, keyword):
        tick = interval * 60
        numBuckets = interval / 5

        [startFileNumber, startBucket] = self.getNames(startTime) #convert bucket to string
        [endFileNumber, endBucket] = self.getNames(endTime)
        print startFileNumber, endFileNumber

#If timestamps span more than a day, we need to ensure that we get all the buckets in the range
        t = startTime
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
            for bucketNumber in range(startB, endB+1, numBuckets):

                bucketNumber = str(bucketNumber)
                if LRU.get(str(fileNumber)) == -1:
                    with open(str(fileNumber)+'.txt') as data_file:
                        dataMap = json.load(data_file)
                        LRU.set(str(fileNumber), dataMap)
                else:
                    dataMap = LRU.get(str(fileNumber))
                total_count = 0
                for bucket in range(int(bucketNumber), int(bucketNumber) + numBuckets):
                    if str(bucket) in dataMap and str(keyword) in dataMap[str(bucket)]:
                        count=dataMap[str(bucket)][str(keyword)]
                        total_count += count
                finalList.append((t, total_count))
                t = t+ tick
                    
        return finalList
    
    #helper function if we want to change window size for inserting in future
    def setWindow(self, windowSize):
        return 24*60 / windowSize
db = Database()

print db.selectFastRange(1448081400, 1448083000, 'Carly Fiorina')
print db.selectRange( 1448081559999/1000, 1448082159999/1000,'Carly Fiorina')
names = ['Hillary Clinton','Carly Fiorina','Bernie Sanders','BernieSanders','Marco Rubio','Donald Trump','Ted Cruz','Ben Carson','Rand Paul']
'''
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

