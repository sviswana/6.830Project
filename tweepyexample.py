import tweepy
 
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Consumer keys and access tokens, used for OAuth
consumer_key = 'yvTfWDweHifXsUH4eWsrnwCRq'
consumer_secret = 'h011BGqMG5eyJb6bZdWFIyMqgbyqlSdbIEJi9yYTTh5lUzT5YJ'
access_token = '3709172475-yw5YC6gyBWI1vRrd8BOjtUx7mRFFTlBSxaZYD6B'
access_token_secret = 'L0cMB61JzlDYS5Ruetq9snDJdHUul7gSTJxpxygbnxdWI'
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)
 
# Creates the user object. The me() method returns the user whose authentication keys were used.
user = api.me()
 
print('Name: ' + user.name)
print('Location: ' + user.location)
print('Friends: ' + str(user.friends_count))

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    
    def on_data(self, data):
        print data
        return True
    
    def on_error(self, status):
        print status
    
#This handles Twitter authetification and the connection to Twitter Streaming API
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)

#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
stream.filter(locations=[-180, -90, 180, 90])