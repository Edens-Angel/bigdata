from sqlalchemy import create_engine
from sklearn.metrics import accuracy_score
import pandas as pd
import plotly.express
import pickle

engine = create_engine("mysql+pymysql://aldabap:H#gGtA47WH+GsN@oege.ie.hva.nl:3306/zaldabap")
conn = engine.connect()

df = pd.read_sql("""SELECT * FROM hotel_reviews""", conn)

linear = open("./models/Logistic_regression_model.pickle", "rb")
linear_model = pickle.load(linear)

multi = open("./models/Naive_bayes_model.pickle", "rb")
multi_model = pickle.load(multi)

rforest = open(",.models/RandomForest_model.pickle", "rb")
rforest_model = pickle.load(rforest)
