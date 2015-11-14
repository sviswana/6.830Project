#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
#from pandas import DataFrame
import json
#import openpyxl
#Variables that contains the user credentials to access Twitter API 
access_token = "3709172475-yw5YC6gyBWI1vRrd8BOjtUx7mRFFTlBSxaZYD6B"
access_token_secret = "L0cMB61JzlDYS5Ruetq9snDJdHUul7gSTJxpxygbnxdWI"
consumer_key = "yvTfWDweHifXsUH4eWsrnwCRq"
consumer_secret = "h011BGqMG5eyJb6bZdWFIyMqgbyqlSdbIEJi9yYTTh5lUzT5YJ"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
 #       df1= json.loads(data)
 #       print "df1", df1
 #       df = DataFrame(df1)
        #print "df", df
 #       df.to_excel('twitter-excel.xlsx', sheet_name='sheet1', index=False)
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['Clinton', 'clinton','Sanders','sanders','FeelTheBern','Trump', 'hillaryclinton','rubio', 'jeb','Jeb','Carson','carson','Fiorina','fiorina','Cruz','cruz','Jindall','jindall','Rand','rand'])
#    {'locations':'-180,-90,180,90'}
#    stream.filter(locations=[-180,-90,180,90])
