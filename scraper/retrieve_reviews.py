import scraper_reviews as rym
import pandas as pd

df = rym.get_album_reviews("https://rateyourmusic.com/release/album/pink-floyd/wish-you-were-here/reviews/1/", 1015,0)

df.to_csv('../scraped_reviews/wish_you_were_here_reviews.csv', index=False)


