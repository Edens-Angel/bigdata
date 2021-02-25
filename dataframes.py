import pandas as pd
import plotly.express as pl

pd.options.plotting.backend = "plotly"


df = pd.read_csv("csv/Hotel_Reviews.csv")

# print(df["lng"])
print(df.dtypes)
print(df.tail())

