from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from matplotlib import pyplot as plt
from nltk.corpus import stopwords
import nltk
import pandas as pd
import numpy as np
import pickle

english_stop_words = stopwords.words('english')
english_stop_words.append("hotel")
english_stop_words.append("room")

def remove_stop_words(corpus):
    removed_stop_words = []
    for review in corpus:
        removed_stop_words.append(
            ' '.join([word for word in review.split() 
                      if word not in english_stop_words])
        )
    return removed_stop_words

engine = create_engine("mysql+pymysql://aldabap:H#gGtA47WH+GsN@oege.ie.hva.nl:3306/zaldabap")
conn = engine.connect()

db_df = pd.read_sql("CALL get_all_reviews()", conn)

# form a new array with the reviews
db_df["Negative_Review_Label"] = 0
db_df["Positive_Review_Label"] = 1

temp_neg = db_df[["Negative_Review", "Negative_Review_Label"]].rename(
  columns={"Negative_Review": "Review", "Negative_Review_Label": "Label"})

temp_pos = db_df[["Positive_Review", "Positive_Review_Label"]].rename(
  columns={"Positive_Review": "Review", "Positive_Review_Label": "Label"})

review_df = pd.DataFrame([])
review_df = pd.concat([review_df, temp_neg, temp_pos])
review_df = review_df.dropna()
review_df = review_df.sample(frac=1)

# labeling data
X = review_df["Review"]
y = review_df["Label"]

vect = TfidfVectorizer(ngram_range=(1, 3), max_features=1000)

# split data
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

Xbase = vect.fit_transform(x_train)
Xtest_base = vect.transform(x_test)

remove_stop_words(Xbase)
remove_stop_words(Xtest_base)

## models

# Naive base
model = MultinomialNB()
model.fit(Xbase, y_train)
predict = model.predict(Xtest_base)
roc_score = roc_auc_score(y_test, predict)



    # Logistic regression
linear = LogisticRegression(C=0.8)
linear.fit(Xbase, y_train)
predict = linear.predict(Xtest_base)
linear_score = roc_auc_score(y_test, predict)


rforest = RandomForestClassifier()
rforest.fit(Xbase, y_train)
rforest_pred = rforest.predict(Xtest_base)
rforest_auc = roc_auc_score(y_test, rforest_pred)

