
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from QueryEngine import QueryEngine
from QueryEngine import QueryType
import socket
from db import db
from Constants import Constants
#from pandas import DataFrame
import json
#import openpyxl
#Variables that contains the user credentials to access Twitter API
access_token = "3709172475-yw5YC6gyBWI1vRrd8BOjtUx7mRFFTlBSxaZYD6B"
access_token_secret = "L0cMB61JzlDYS5Ruetq9snDJdHUul7gSTJxpxygbnxdWI"
consumer_key = "yvTfWDweHifXsUH4eWsrnwCRq"
consumer_secret = "h011BGqMG5eyJb6bZdWFIyMqgbyqlSdbIEJi9yYTTh5lUzT5YJ"


#This is a basic listener that just prints received tweets to stdout.
class TweetListener(StreamListener):
    def __init__(self, host, port):
        self.sock = socket.socket()
        self.sock.connect((host, port))
        self.queryEngine = QueryEngine()

    def checkWords(self, wordList, text):
        for word in wordList:
            if word in text:
                return True
        return False
    def on_data(self, data):
        #print data
        print 'START'
        newdata = json.loads(data)
        keywords = Constants.KEYWORDS
        if "text" in newdata:
            text = newdata["text"]
            
            #print 'DATA', data
            timestamp = newdata["timestamp_ms"]
            keywordMap = {}
            text = text.replace("'", "")
            # print 'TEXT', text
            for word in keywords:
                #print "word", word
                #print 'text', text
                wordList = keywords[word]

                if self.checkWords(wordList,text):
                    if not word in keywordMap:
                        keywordMap[word]=1
                    else:
                        keywordMap[word]+=1
                # print "keyword map", keywordMap
            currMax = 0
            maxKeyWord = ''
            for word in keywordMap.keys():
                if keywordMap[word] > currMax:
                    currMax = keywordMap[word]
                    maxKeyWord = word
            print keywordMap
            
            queryString = self.queryEngine.serialize([QueryType.INSERT, timestamp, maxKeyWord, 1])
            print queryString
            self.sock.send(queryString)


     #       df1= json.loads(data)
     #       print "df1", df1
     #       df = DataFrame(df1)
            #print "df", df
     #       df.to_excel('twitter-excel.xlsx', sheet_name='sheet1', index=False)
            return True

    def on_error(self, status):
        print status

    def close(self):
        self.sock.close()


if __name__ == '__main__':

    #Define the stream and port number
    host = Constants.HOST
    port = Constants.PORT
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = TweetListener(host, port)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    print 'constant', Constants.KEYWORDS
    stream.filter(track=Constants.KEYWORDS)
#    {'locations':'-180,-90,180,90'}
#    stream.filter(locations=[-180,-90,180,90])
