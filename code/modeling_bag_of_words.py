import pandas as pd
from tensorflow.keras.layers import TextVectorization

# Load dataset.
df = pd.read_csv('../output/eda_and_cleaning/ok_computer_reviews_cleaned.csv')

# Retrieve vocabulary from reviews.
text_vectorization = TextVectorization(output_mode="int")
text_vectorization.adapt(df['Review'])
vocabulary = text_vectorization.get_vocabulary()