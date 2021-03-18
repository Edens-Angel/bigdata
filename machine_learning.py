from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import linear_model
import pandas as pd
import numpy as np

engine = create_engine("mysql+pymysql://aldabap:H#gGtA47WH+GsN@oege.ie.hva.nl:3306/zaldabap")
conn = engine.connect()

df = pd.read_sql("""SELECT Negative_Review, Review_Total_Negative_Word_Counts,
  Positive_Review, Review_Total_Positive_Word_Counts FROM hotel_reviews""", conn)

# df changes
df["Full_Review"] = df["Negative_Review"] + " " + df["Positive_Review"] 

X = df["Full_Review"]
y = df

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

vect = CountVectorizer()
Xbase = vect.fit_transform(x_train)
Xtest_base = vect.transform(x_test)

model = linear_model.LogisticRegression()
model.fit(x_train, y_train)
print(model.score())