import pandas as pd
import scraper_reviews as rym

df_album_info = pd.read_csv("rym_top_5000_all_time.csv") 
df_album_info = df_album_info[['Album', 'Artist Name', 'Number of Reviews']]

transformed_albums = []
for album in df_album_info['Album']:
    temp = album.replace(" ", "-").replace("&","and").replace(",","").replace(".","_").replace("!","").replace("(","").replace(")","").replace("'","").replace("[","").replace("]","").lower()
    transformed_albums.append(temp)
    
transformed_artists = []
for artist in df_album_info['Artist Name']:
    temp = artist.replace(" ", "-").replace("&","and").replace(",","").replace(".","_").replace("!","").replace("(","").replace(")","").replace("'","").replace("[","").replace("]","").lower()
    transformed_artists.append(temp)

urls = []
for i in range(len(transformed_artists)):
    url = "https://rateyourmusic.com/release/album/{}/{}/reviews/1/".format(transformed_artists[i],transformed_albums[i])
    urls.append(url)
    
df_urls = pd.concat([pd.Series(urls), df_album_info['Number of Reviews']], axis=1)

reviews = pd.DataFrame()

for idx in range(500):
    
    try:
        df = rym.get_album_reviews(df_urls[0][idx])
        reviews=pd.concat([reviews,df],axis=0)
    except:
        pass
    

reviews.to_csv('../scraped_reviews/album_reviews.csv', index=False)