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
            
        
    
    #helper function if we want to change window size for inserting in future
    def setWindow(self, windowSize):
        return 24*60 / windowSize
    

db = Db()
data = '{"created_at":"Sat Nov 14 17:39:50 +0000 2015","id":665584940151607297,"id_str":"665584940151607297","text":"Besleybean #HillaryClinton fired for lies, unethical behavior #Hillary2016 #HillaryForPrison2016 #UniteBlue \u2026 https:\/\/t.co\/vPk6I9e8nu","source":"\u003ca href=\"http:\/\/ifttt.com\" rel=\"nofollow\"\u003eIFTTT\u003c\/a\u003e","truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":3110899521,"id_str":"3110899521","name":"Mike Vee","screen_name":"MikeVee5","location":null,"url":null,"description":null,"protected":false,"verified":false,"followers_count":1636,"friends_count":1882,"listed_count":427,"favourites_count":857,"statuses_count":476602,"created_at":"Tue Mar 24 17:24:04 +0000 2015","utc_offset":null,"time_zone":null,"geo_enabled":false,"lang":"en","contributors_enabled":false,"is_translator":false,"profile_background_color":"C0DEED","profile_background_image_url":"http:\/\/abs.twimg.com\/images\/themes\/theme1\/bg.png","profile_background_image_url_https":"https:\/\/abs.twimg.com\/images\/themes\/theme1\/bg.png","profile_background_tile":false,"profile_link_color":"0084B4","profile_sidebar_border_color":"C0DEED","profile_sidebar_fill_color":"DDEEF6","profile_text_color":"333333","profile_use_background_image":true,"profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/580420358827872257\/eRTjWEVi_normal.jpg","profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/580420358827872257\/eRTjWEVi_normal.jpg","profile_banner_url":"https:\/\/pbs.twimg.com\/profile_banners\/3110899521\/1438904985","default_profile":true,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":null,"contributors":null,"is_quote_status":false,"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[{"text":"HillaryClinton","indices":[11,26]},{"text":"Hillary2016","indices":[62,74]},{"text":"HillaryForPrison2016","indices":[75,96]},{"text":"UniteBlue","indices":[97,107]}],"urls":[{"url":"https:\/\/t.co\/vPk6I9e8nu","expanded_url":"http:\/\/ift.tt\/1MxzreP","display_url":"ift.tt\/1MxzreP","indices":[110,133]}],"user_mentions":[],"symbols":[]},"favorited":false,"retweeted":false,"possibly_sensitive":false,"filter_level":"low","lang":"en","timestamp_ms":"1447522790359"}'
timestamp = 1447722300
print 'file: ',timestamp/86400
db.insert(timestamp, 'sanders',2)

