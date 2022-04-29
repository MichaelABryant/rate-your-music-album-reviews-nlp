import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ast import literal_eval
import contractions
from googletrans import Translator
import re

# Load dataset.
df = pd.read_csv('../ok_computer_reviews.csv')

# Display dtypes and null value counts.
df.info()

# Display head.
df.head()

# Display first review.
df['Review'][0]

# Remove usernames from dataset.
df = df.drop('User',axis=1)

# Remove "stars" from ratings.
df['Rating'] = df['Rating'].str.replace(' stars','')

# Display head.
df.head()

# Initialize Google Translator.
translator = Translator()

# Standardize data: remove \n, translate to English, convert contractions,
# remove everything but letters, numbers, and spaces, and convert to lowercase.
reviews = []
for idx,val in enumerate(df['Review']):
    temp = literal_eval(val) #converts list stored as string to actual list
    temp = max(temp,key=len)
    temp = str(temp).replace('\n',' ')
    translation = translator.translate(temp)
    if translation.src != 'en':
        temp = str(translation.text)
    expanded_words = []   
    for word in temp.split():
        word = contractions.fix(word)
        word = re.sub(r'[^a-zA-Z0-9\s]+', '', word)
        expanded_words.append(word)
    temp = ' '.join(expanded_words)
    reviews.append(temp.lower())

# Check to make sure all reviews were retrieved.
len(df) == len(reviews)

# Replace uncleaned reviews with cleaned reviews.
df.loc[:,'Review'] = reviews

# Display unique ratings.
df['Rating'].unique()

# Print reviews with missing ratings.
for idx, val in enumerate(df.loc[df['Rating'].isna(),'Review']):
    print(val)
    
sns.barplot(x=df['Rating'].value_counts().index, y=df['Rating'].value_counts().values)
plt.xlabel('Rating')
plt.ylabel('Count')
plt.savefig('../output/eda_and_cleaning/barplot_rating.jpg', bbox_inches='tight')
plt.show()

review_lengths = []
for idx, val in enumerate(df['Review']):
    review_lengths.append(len(val))
    
df['Review Length'] = review_lengths

sns.histplot(df, x='Review Length')
plt.savefig('../output/eda_and_cleaning/histplot_review_length.jpg', bbox_inches='tight')
plt.show()

mean_review_length = []
for i in df.groupby(['Rating']).mean().values:
    mean_review_length.append(i[0])

sns.barplot(x=df.groupby(['Rating']).mean().index, y=mean_review_length)
plt.xlabel('Rating')
plt.ylabel('Mean Review Length')
plt.savefig('../output/eda_and_cleaning/barplot_rating_mean.jpg', bbox_inches='tight')
plt.show()

median_review_length = []
for i in df.groupby(['Rating']).median().values:
    median_review_length.append(i[0])

sns.barplot(x=df.groupby(['Rating']).median().index, y=median_review_length)
plt.xlabel('Rating')
plt.ylabel('Median Review Length')
plt.savefig('../output/eda_and_cleaning/barplot_rating_median.jpg', bbox_inches='tight')
plt.show()

total_review_length = []
for i in df.groupby(['Rating']).sum().values:
    total_review_length.append(i[0])

sns.barplot(x=df.groupby(['Rating']).sum().index, y=total_review_length)
plt.xlabel('Rating')
plt.ylabel('Total Review Length')
plt.savefig('../output/eda_and_cleaning/barplot_rating_sum.jpg', bbox_inches='tight')
plt.show()

df['Rating'] = df['Rating'].fillna('0.50').astype(str)

df.info()

df['Rating'].unique()

# Export to csv.
df.to_csv('../output/eda_and_cleaning/ok_computer_reviews_cleaned.csv', index=False)
