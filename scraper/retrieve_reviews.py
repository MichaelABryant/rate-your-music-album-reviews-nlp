import scraper_reviews as rym
import pandas as pd

df = rym.get_album_reviews(1548,0)

compression_opts = dict(method='zip', archive_name='dsotm_reviews.csv')  
df.to_csv('dsotm_reviews.zip', index=False, compression=compression_opts)


