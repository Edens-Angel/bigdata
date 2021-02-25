# TODO drop columns
# TODO remove duplicates
# TODO merge dataframes
# TODO set to database
import pandas as pd

drop_col = ["Additional_Number_of_Scoring", "Tags", "Total_Number_of_Reviews_Reviewer_Has_Given"]

df = pd.read_csv("./csv/webscraped.csv")


print(df)