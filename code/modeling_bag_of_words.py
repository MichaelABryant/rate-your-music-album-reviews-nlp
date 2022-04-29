import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import TextVectorization
from sklearn.preprocessing import OneHotEncoder
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import regularizers
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn import metrics

# Load dataset.
df = pd.read_csv('../output/eda_and_cleaning/ok_computer_reviews_cleaned.csv')

X = df['Review'].copy()
y = df['Rating'].copy().astype(str)

y.unique()

X_train, X_valid_test, y_train, y_valid_test = train_test_split(X, y, stratify=y, test_size=0.20, random_state=1)
X_valid, X_test, y_valid, y_test = train_test_split(X_valid_test, y_valid_test, stratify=y_valid_test, test_size=0.50, random_state=1)

# Retrieve vocabulary from training reviews.
max_tokens = 10000
text_vectorization = TextVectorization(ngrams=2, max_tokens = max_tokens, output_mode="tf_idf")
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


def get_model(max_tokens=max_tokens, hidden_dim=256/4):
    inputs = keras.Input(shape=(max_tokens,))
    x = layers.Dense(hidden_dim, activation='relu', kernel_regularizer=regularizers.L1L2(l1=1e-2, l2=1e-2),
                     bias_regularizer=regularizers.L2(1e-2),
                     activity_regularizer=regularizers.L2(1e-2))(inputs)
    x= layers.Dropout(0.7)(x)
    x = layers.Dense(hidden_dim, activation='relu', kernel_regularizer=regularizers.L1L2(l1=1e-2, l2=1e-2),
                     bias_regularizer=regularizers.L2(1e-2),
                     activity_regularizer=regularizers.L2(1e-2))(x)
    x= layers.Dropout(0.7)(x)
    outputs = layers.Dense(10,activation="softmax")(x)
    model = keras.Model(inputs, outputs)
    model.compile(loss="categorical_crossentropy",
                  optimizer= "adam",
                  metrics=['accuracy'])
    return model

model = get_model()
model.summary()

early_stopping = EarlyStopping(monitor='val_loss',
                               min_delta=0.001,
                               restore_best_weights=True,
                               patience=1)

reduce_lr = ReduceLROnPlateau(monitor='val_loss',
                                factor=0.5,
                                patience=0,
                                verbose=1)

model_checkpoint = ModelCheckpoint("../output/modeling/bag-of-words/model.keras",
                                   save_best_only=True)


callbacks = [early_stopping, reduce_lr, model_checkpoint]

history = model.fit(
    x = X_train,
    y = y_train,
    epochs=100,
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

y_pred = model.predict(X_test)
array = metrics.confusion_matrix(y_test.argmax(axis=1), y_pred.argmax(axis=1))
df_cm = pd.DataFrame(array, np.linspace(0.5,5,10), np.linspace(0.5,5,10))
sns.set(font_scale=1.4) # for label size
sns.heatmap(df_cm, annot=True, annot_kws={"size": 16})

plt.show()