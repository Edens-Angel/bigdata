# TODO set to database
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd

keggle_df = pd.read_csv("./csv/Hotel_Reviews.csv")
webscraped_df = pd.read_csv("./csv/webscraped.csv")
handwritten_df = pd.read_csv("./csv/handwritten_reviews.csv")
drop_col = [
    "Additional_Number_of_Scoring", "Tags", "Total_Number_of_Reviews_Reviewer_Has_Given"]

# merge all dataframes
MERGE_ARR = [keggle_df, webscraped_df, handwritten_df]
merged_df = pd.concat(MERGE_ARR, ignore_index=True)

# Filter data
word_count_min = 5
merged_df = merged_df[merged_df["Review_Total_Negative_Word_Counts"] > 5]
merged_df = merged_df[merged_df["Review_Total_Positive_Word_Counts"] > 5]

# clean the dataframe
merged_df = merged_df.drop(columns=drop_col)
merged_df = merged_df.drop_duplicates()
merged_df = merged_df.dropna()

# connect to database
engine = create_engine("mysql+pymysql://aldabap:H#gGtA47WH+GsN@oege.ie.hva.nl:3306/zaldabap")

merged_df.to_sql("hotel_reviews", engine, if_exists="replace", chunksize=1000)
print("Finished inserting data!")