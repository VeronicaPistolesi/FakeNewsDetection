# -*- coding: utf-8 -*-
"""data_preprocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10DMGpttRpDQhVKr4Bd-FxS7PSujgOkQb
"""

from google.colab import drive
drive.mount('/content/drive')

"""## Libraries"""

import pandas as pd
import numpy as np
import nltk
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

"""## Data Loading"""

train = pd.read_csv('/content/drive/Shareddrives/ProgettoHLT/FakeNewsDetection/Data/train.csv')
test = pd.read_csv('/content/drive/Shareddrives/ProgettoHLT/FakeNewsDetection/Data/test.csv')

"""## Data Analysis"""

display(train)

words = [] # Number of total words
for article in train.text:
    for word in article.split():
        words.append(word)
       
unique_words = len(list(set(words))) # Number of unique words 
print('Number of unique words: ', unique_words)

nltk.download('punkt')

articles = [text for text in train.text]
max_len = 0
min_len = 10000
articles_len = []

for article in articles:
    articles_len.append(len(nltk.word_tokenize(article)))
    max_len = max(len(nltk.word_tokenize(article)), max_len)
    min_len = min(len(nltk.word_tokenize(article)), min_len)
    
print('Number of news:', len(articles)) # Number of news
print('Max length of the news:', max_len, 'tokens') # Max len
print('Min length of the news:', min_len, 'tokens') # Min len

mean_len = round(np.mean(articles_len)) # Mean len
print('Mean length of the news:', mean_len, 'tokens')
print('Standard Deviation of the news:',round(np.std(articles_len),2), 'tokens') # Standard deviation

median = round(np.median(articles_len)) # Median 
print('Median length of the news:', median)

# Adding length column
train['length']= articles_len

# New look of the Training Set
train.head()

# Check the number of outliers
Q1, Q3 = np.quantile(articles_len, np.array([0.25, 0.75])) # first and third quartiles
IQR = Q3-Q1 # interquartile range
min = round(Q1- 1.5* IQR) # Boxplot minimum value
max = round(1.5* IQR + Q3) # Boxplot maximum value
outliers = 0
for length in articles_len:
  if length > max or length < min: 
    outliers = outliers+1

percentage = round((outliers*100)/train.shape[0],2)
print('Number of outliers:', outliers)
print('Percentage outliers', percentage,'%')

# Boxplot distribution with outliers
plt.figure(figsize=(20,4))
age_boxplot = sns.boxplot(x='length', data=train)
plt.title("Boxplot distribution with outliers", size = 18)
quantiles = np.quantile(articles_len, [0.00, 0.25, 0.50, 0.75, 1.00])
quantiles = np.append(quantiles, max)
age_boxplot.vlines(quantiles, [0] * quantiles.size, [1] * quantiles.size, color='b', ls=':', lw=0.8, zorder=0)
age_boxplot.set_xticks(quantiles)
age_boxplot.tick_params(axis="x", labelsize=9)
age_boxplot.set_ylim(bottom=0.7, auto=True)
age_boxplot.set_xlabel("News lengths", rotation = "horizontal", size = 12)
plt.show()

# Countplot distribution (the most significant ones)
plt.figure(figsize=(18,4))
g = sns.countplot(x="length", data=train)                                                   
ax = plt.gca()
ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))
ax.xaxis.set_major_locator(ticker.MultipleLocator(base=50))
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))
ax.yaxis.set_major_locator(ticker.MultipleLocator(base=5))
plt.tight_layout()
plt.axvline(median, color='k', linestyle='dashed', linewidth=3)  # highlighted value (median)
plt.show()

"""### Splitting train.csv into Training Set (80%) and Validation Set (20%)"""

# Splitting train.csv into Training Set (80%) and Validation Set (20%)
train_v, val_v = train_test_split(train, test_size=0.20, train_size=0.80, stratify=train['label'])
# Reset Index
train = train_v.reset_index(drop=True)
val = val_v.reset_index(drop=True)

# Shapes
print('Training Set shape:', train.shape)
print('Validation Set shape:', val.shape)
print('Test Set shape:', test.shape)

"""### Training Set Distribution"""

# Training Set Distribution
sns.countplot(y="label", palette="coolwarm", data=train).set_title('True and Fake News Distribution (training set)')
plt.show()

# Number of True News in the Training Set  
print('Number of True News in the Training Set:', len(train.loc[train['label']==0]))

# Number of Fake News in the Training Set
print('Number of Fake News in the Training Set:', len(train.loc[train['label']==1]))

"""### Validation Set Distribution"""

# Validation Set Distribution
sns.countplot(y="label", palette="coolwarm", data=val).set_title('True and Fake News Distribution (validation set)')
plt.show()

# Number of True News in the Validation Set
print('Number of True News in the Validation Set:', len(val.loc[val['label']==0]))

# Number of Fake News in the Validation Set
print('Number of Fake News in the Validation Set:', len(val.loc[val['label']==1]))

"""## Tokenization and Padding"""

# Final Configurations

# Training Set
X_train = train.text
Y_train = train.label
# Validation Set
X_val = val.text
Y_val = val.label
# Test Set
X_test = test.text
Y_test = test.label

# Sequences of tokenized words
tokenizer = Tokenizer(num_words= unique_words)
tokenizer.fit_on_texts(X_train)
train_sequences = tokenizer.texts_to_sequences(X_train)
val_sequences = tokenizer.texts_to_sequences(X_val)
test_sequences = tokenizer.texts_to_sequences(X_test)
word_index = tokenizer.word_index

# Padding
padded_train = pad_sequences(train_sequences, maxlen = median, padding = 'post', truncating = 'post')
padded_val = pad_sequences(val_sequences, maxlen = median, padding= 'post', truncating = 'post') 
padded_test = pad_sequences(test_sequences, maxlen = median, padding= 'post', truncating = 'post')