
import json
import os
import ast
import random
import time
#[update <timestamp> Hillary 5]
from LRU import LRU
import collections
class Database:
    

    def __init__(self):

        self.counts = {"Hillary Clinton":0,"Carly Fiorina":0,"Bernie Sanders":0,"Marco Rubio":0, "Donald Trump":0, "Ted Cruz":0, "Ben Carson":0, "Rand Paul":0}
        self.runningMean = {"Hillary Clinton":0,"Carly Fiorina":0,"Bernie Sanders":0,"Marco Rubio":0, "Donald Trump":0, "Ted Cruz":0, "Ben Carson":0, "Rand Paul":0}
        self.runningVar = {"Hillary Clinton":0,"Carly Fiorina":0,"Bernie Sanders":0,"Marco Rubio":0, "Donald Trump":0, "Ted Cruz":0, "Ben Carson":0, "Rand Paul":0}
        self.totalCounts = {"Hillary Clinton":0,"Carly Fiorina":0,"Bernie Sanders":0,"Marco Rubio":0, "Donald Trump":0, "Ted Cruz":0, "Ben Carson":0, "Rand Paul":0}
        self.squaredCounts = {"Hillary Clinton":0,"Carly Fiorina":0,"Bernie Sanders":0,"Marco Rubio":0, "Donald Trump":0, "Ted Cruz":0, "Ben Carson":0, "Rand Paul":0}
        self.previousBucket = (int(time.time()) / 300) % 288
        self.candidateList = ["Hillary Clinton","Carly Fiorina","Bernie Sanders","Marco Rubio", "Donald Trump", "Ted Cruz", "Ben Carson", "Rand Paul"]
        self.incrementalCount = {}  
        self.incrementalCount["startTime"] =  int(time.time()) / 300    
        self.incrementalCount["lastTime"] =  int(time.time()) / 300
        #LRU.cache = collections.OrderedDict()
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
        print "current bucket", bucket
        print "previous bucket", self.previousBucket
        if bucket != self.previousBucket:
            self.incrementalCount[timestamp / 300] = {}
            for candidate in self.candidateList:
                if candidate in dataMap[str(self.previousBucket)]:
                    count = dataMap[str(self.previousBucket)][candidate]
                    squaredCount = dataMap[str(self.previousBucket)][candidate] ** 2
                else:
                    count = 0
                    squaredCount = 0
                self.totalCounts[str(candidate)] += count
                self.squaredCounts[str(candidate)] += squaredCount
                newMean = self.updateMean(self.counts[str(candidate)]+1, self.runningMean[str(candidate)], count)
                newVar = self.updateVar(self.counts[str(candidate)]+1, self.totalCounts[str(candidate)], self.squaredCounts[str(candidate)])
                self.runningVar[str(candidate)] = newVar
                self.runningMean[str(candidate)] = newMean
                self.counts[str(candidate)]+=1
                if (timestamp/300 -1) not in self.incrementalCount:
                    self.incrementalCount[timestamp/300][candidate] = 0
                else:
                    self.incrementalCount[timestamp/300][candidate] = self.incrementalCount[timestamp/300 - 1][candidate] +count
                self.incrementalCount["lastTime"] = timestamp/300
            print("COUNTS: ", self.counts)
            print("RUNNING AVERAGE:", self.runningMean)
            print("RUNNING VAR:", self.runningVar)
            print("INCREMENTAL COUNT", self.incrementalCount)
            self.previousBucket = bucket
        #print 'dataMap', dataMap#str(dataMap).replace("u\'","\'")
        #print "bucket", bucket
        keywords = dataMap[str(bucket)]
        bucket = str(bucket)
        #print 'keywords', keywords
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
    
    def updateMean(self, currentCount, runningMean, newTerm):
        return runningMean + (float((newTerm - runningMean))/currentCount)

    def updateVar(self, n, currentCount, currentSqCount):
        if n == 1:
            return 0
        else:
            return float(n*currentSqCount - currentCount*currentCount)/float(n * (n - 1))

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
    
    def getAggregateCountInRange(self, startTimestamp, endTimestamp, keyword):
        if endTimestamp > self.incrementalCount["lastTime"]:
            endTimestamp = self.incrementalCount["lastTime"]
        if startTimestamp < self.incrementalCount["startTime"]:
            startTimestamp = self.incrementalCount["startTime"]
        if not endTimestamp/300 in self.incrementalCount:
            return str(0)
        if not startTimestamp/300 in self.incrementalCount:
            return str(0)
        endCounts = self.incrementalCount[endTimestamp/300][str(keyword)]
        startCounts = self.incrementalCount[startTimestamp/300 - 1][str(keyword)]
        return str(endCounts - startCounts)


    def getAverage(self, startTimestamp, endTimestamp, keyword):
        totalCounts = selectFastRange(startTimestamp, endTimestamp, keyword)
        buckets = (endTimestamp - startTimestamp) / (60*5)
        return str(float(totalCounts) / buckets)

    def getRunningAverage(self, candidate):
        print "start time running average", time.clock()
        ans = self.runningMean[candidate]
        print "end time running average", time.clock()
        return str(ans)
        #return str(self.runningMean[candidate])

    def getRunningVariance(self, candidate):
        return str(self.runningVar[candidate])

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
        print "start Time: ", startTimestamp
        if (endTimestamp < startTimestamp):
            return []
        tick = 5 * 60 #seconds to add - assuming window size is 5 here!
        bucketMod = self.setWindow(5)
        print "bucketMod", bucketMod
        [startFileNumber, startBucket] = self.getNames(startTimestamp) #convert bucket to string
        [endFileNumber, endBucket] = self.getNames(endTimestamp)

        print "fileNum", startFileNumber, endFileNumber
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
                        try:
                            dataMap = json.load(data_file)
                        except:
                            for i in range(t, endTimestamp+300, 300):
                                finalList.append((str(i), str(0)))
                            return finalList
                        LRU.set(str(fileNumber), dataMap)
                else:
                    dataMap = LRU.get(str(fileNumber))
                if bucketNumber in dataMap and str(keyword) in dataMap[bucketNumber]:
                    count=dataMap[bucketNumber][str(keyword)]
                    finalList.append((str(t), str(count), keyword))
                else:
                    finalList.append((str(t),str(0), keyword))
                t = t+ tick
        if finalList == []:
            for i in range(t, endTimestamp+300, 300):
                finalList.append((str(i), str(0), keyword))
            return finalList
        return finalList

    def selectRangeAndInterval(self, startTime, endTime, interval, keyword):
        stime = time.time()
        print "start time in select range and interval", stime
        print "start time in select range and interval process", time.clock()
        interval = interval / 300000
        tick = interval * 60
        numBuckets = interval / 5
        bucketMod = self.setWindow(interval)
        [startFileNumber, startBucket] = self.getNames(startTime) #convert bucket to string
        [endFileNumber, endBucket] = self.getNames(endTime)
        print startFileNumber, endFileNumber

#If timestamps span more than a day, we need to ensure that we get all the buckets in the range
        t = startTime
        finalList = []
        
        for fileNumber in range(startFileNumber, endFileNumber+1):
            if LRU.get(str(fileNumber)) == -1:
                with open(str(fileNumber)+'.txt') as data_file:
                    try:
                        dataMap = json.load(data_file)
                        LRU.set(str(fileNumber), dataMap)
                    except:
                        for i in range(t, endTime+tick, tick):
                            finalList.append((str(i), str(0), keyword))
                        print "end time", time.time()
                        print "end time", time.clock()
                
            dataMap = LRU.get(str(fileNumber))
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
               
                total_count = 0
                for bucket in range(int(bucketNumber), int(bucketNumber) + numBuckets):
                    if str(bucket) in dataMap and str(keyword) in dataMap[str(bucket)]:
                        count=dataMap[str(bucket)][str(keyword)]
                        total_count += count
                finalList.append((str(t), str(total_count), keyword))
                t = t+ tick
        if finalList == []:
            for i in range(t, endTime+tick, tick):
                finalList.append((str(i), str(0), keyword))
            print "end time", time.time()
            print "end time", time.clock()
            return finalList       
        print "end time", time.time()     
        print "end time", time.clock()
        return finalList
    
    #helper function if we want to change window size for inserting in future
    def setWindow(self, windowSize):
        return 24*60 / windowSize
db = Database()

#print db.selectFastRange(1448081400, 1448083000, 'Carly Fiorina')
#print db.selectRange( 1448081559999/1000, 1448082159999/1000,'Carly Fiorina')
#names = ['Hillary Clinton','Carly Fiorina','Bernie Sanders','BernieSanders','Marco Rubio','Donald Trump','Ted Cruz','Ben Carson','Rand Paul']

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

