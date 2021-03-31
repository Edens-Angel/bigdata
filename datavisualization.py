from sqlalchemy import create_engine
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
import pandas as pd
import plotly.express as plt
import pickle

pd.options.plotting.backend = "plotly"

engine = create_engine("mysql+pymysql://aldabap:H#gGtA47WH+GsN@oege.ie.hva.nl:3306/zaldabap")
conn = engine.connect()

df = pd.read_sql("SELECT * FROM hotel_reviews", conn)



df["Full_Review"] = df["Negative_Review"] + " " + df["Positive_Review"] 


english_stop_words = stopwords.words('english')
stopwords_set = set(STOPWORDS)
stopwords_set.update(english_stop_words)
stopwords_set.update(["hotel", "room", "rooms"])

wc = WordCloud(max_words=1000, stopwords=stopwords_set).generate(" ".join(df["Full_Review"]))
plt.imshow(wc)
wc.to_file("./wordcloud/reviews.png")

pos_wc = WordCloud(max_words=1000, stopwords=stopwords_set).generate(" ".join(df["Positive_Review"]))
plt.imshow(pos_wc)
pos_wc.to_file("./wordcloud/positive_reviews.png")

neg_wc = WordCloud(max_words=1000, stopwords=stopwords_set).generate(" ".join(df["Negative_Review"]))
plt.imshow(neg_wc)
neg_wc.to_file("./wordcloud/negative_reviews.png")


reviews_plot = df["Reviewer_Nationality"].value_counts().plot(kind="bar").show()

word_count_plot = df[["Review_Total_Positive_Word_Counts", "Review_Total_Negative_Word_Counts"]].plot(kind="histogram").show()

avg_rev_score = df["Reviewer_Score"].value_counts().plot(kind="barh").show()

plt.histogram(avg_rev_score)
print(avg_rev_score)