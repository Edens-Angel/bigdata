# scrape 

## before reviews

 - Hotel_name
 - Hotel_Adress
 - Average_Score
 - Tags
 - Total_Number_of_Reviews
 - lat
 - lng


## during reviews
 - review date#
 - reviewer nationality#
 - reviewer score#
 - days_since_review#
 - negative review
 - positive review

## technical after reviews
 - wordcount positive
 - wordcount negative


## dont know
 - additional number of scoring
 - total_Number_of_Reviews_Reviewer_Has_Given


-----------------------------
# Scraping proces 

1. loop through the url 

2. function `scrape hotel` (parameter `url`)
    scrapes all the data from url
    puts all data in a dataframe
    calls function `scrape reviews` (parameter `driver`, `review`)
        - scrapes all reviews on page 1
        - loops through all paginations
        - filters out the bad comments
        - returns the data in a Dataframe
        - creates for each review a copy of the preData from hotel and adds the     reviewData
        ``returns`` the total dataframe
    ``returns`` the total dataframe

3. Concats all dataframes



# TODO 
merge dataframes
figure out [additional number of scoring, total_Number_of_Reviews_Reviewer_Has_Given]
