import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.offsetbox import AnchoredText
from matplotlib.animation import FuncAnimation
import time

import tweepy

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)

#query = ['#IndvsAus -filter:retweets']
query = ['Federer']

fig = plt.figure(figsize=(10, 10))  #basically in inches  19.2, 10.8
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_extent([65, 100, 6, 40])
ax.stock_img()
ax.add_feature(cfeature.OCEAN, facecolor='white')
states_provinces = cfeature.NaturalEarthFeature(
category='cultural',
name='admin_0_countries',
scale='10m',
facecolor='none')
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(states_provinces, edgecolor='grey')
ax.add_feature(cfeature.BORDERS, linestyle=':')

x = list()
y = list()
    
class CustomStreamListener(tweepy.StreamListener):
    @staticmethod
    def gettw(tweet):
        if tweet.coordinates is not None:
            global x,y 
            #x,y = map(tweet.coordinates['coordinates'][0], tweet.coordinates['coordinates'][1])
            x.append(tweet.coordinates['coordinates'][0])
            y.append(tweet.coordinates['coordinates'][1])
            print(x,y)
            
    def on_status(self, status):
        #print (status.text)
        self.gettw(status)

#    def on_data(self, data):
#        json_data = json.loads(data)
#        file.write(str(json_data))

    def on_error(self, status_code):
        print ('Encountered error with status code:', status_code)
        return True # Don't kill the stream

    def on_timeout(self):
        print('Timeout...')
        return True # Don't kill the stream

    

def update(data): #must accept a input
    #lat = int(input("Enter a latitude: "))
    #lon = int(input("Enter a longitude: "))
    global x,y
    ax.scatter(x,y, transform=ccrs.PlateCarree(), marker='o', color='Red')#lon, lat -- lists or numpy arrays
    x = list()
    y = list()
    
myStream = tweepy.streaming.Stream(auth, listener=CustomStreamListener())
#myStream.filter(track=query, async=True, languages=["en"]) #,locations=[65, 2, 96, 36]

myStream.filter(track=query,locations=[65, 2, 96, 36], async=True, languages=["en"])
#myStream.filter(track=[query],locations=[-180, -90, 180, 90], async=True)
#SouthWest Corner(Long, Lat), NorthEast Corner(Long, Lat)

animation = FuncAnimation(fig, update, interval=5000, blit=False)
plt.show()
