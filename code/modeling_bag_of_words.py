import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import TextVectorization
from sklearn.preprocessing import OneHotEncoder
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import regularizers

# Load dataset.
df = pd.read_csv('../output/eda_and_cleaning/ok_computer_reviews_cleaned.csv')

X = df['Review'].copy()
y = df['Rating'].copy().astype(str)

y.unique()

X_train, X_valid_test, y_train, y_valid_test = train_test_split(X, y, stratify=y, test_size=0.20, random_state=1)
X_valid, X_test, y_valid, y_test = train_test_split(X_valid_test, y_valid_test, stratify=y_valid_test, test_size=0.50, random_state=1)

# Retrieve vocabulary from training reviews.
text_vectorization = TextVectorization(max_tokens = 13010, output_mode="multi_hot")
text_vectorization.adapt(X_train)

# Vectorize reviews.
X_train = text_vectorization(X_train)
X_train.shape
X_valid = text_vectorization(X_valid)
X_valid.shape
X_test = text_vectorization(X_test)
X_test.shape

# OneHotEncode Ratings.
enc = OneHotEncoder(handle_unknown='ignore')
y_train = enc.fit_transform(y_train.values.reshape(-1,1)).toarray()
y_train.shape
y_valid = enc.transform(y_valid.values.reshape(-1,1)).toarray()
y_valid.shape
y_test = enc.transform(y_test.values.reshape(-1,1)).toarray()
y_test.shape

def get_model(max_tokens=13010, hidden_dim=16):
    inputs = keras.Input(shape=(max_tokens,))
    x = layers.Dense(hidden_dim, activation='relu', kernel_regularizer=regularizers.L1L2(l1=1e-2, l2=1e-2),
                     bias_regularizer=regularizers.L2(1e-2),
                     activity_regularizer=regularizers.L2(1e-2))(inputs)
    x= layers.Dropout(0.7)(x)
    outputs = layers.Dense(10,activation="softmax")(x)
    model = keras.Model(inputs, outputs)
    model.compile(loss="categorical_crossentropy",
                  optimizer= "adam",
                  metrics=['accuracy'])
    return model

model = get_model()
model.summary()
callbacks = [
    keras.callbacks.ModelCheckpoint("../output/modeling/bag-of-words/binary_1gram.keras",
                                    save_best_only=True)]
history = model.fit(
    x = X_train,
    y = y_train,
    epochs=10,
    callbacks=callbacks,
    validation_data = [X_valid,y_valid])

result = pd.DataFrame(history.history)
fig, ax = plt.subplots(nrows=1, ncols=2,figsize=(18,6))
ax = ax.flatten()
ax[0].plot(result[['accuracy','val_accuracy']])
ax[0].set_title("Accuracy")
ax[1].plot(result[['loss','val_loss']])
ax[1].set_title("Loss")
plt.show()