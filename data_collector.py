from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import date, datetime
from time import sleep
import pandas as pd
import re
import locale

locale.setlocale(locale.LC_TIME, "nl_NL.utf8")
column_names = ["Hotel_Address","Additional_Number_of_Scoring",
        "Review_Date","Average_Score","Hotel_Name","Reviewer_Nationality",
        "Negative_Review","Review_Total_Negative_Word_Counts",
        "Total_Number_of_Reviews","Positive_Review",
        "Review_Total_Positive_Word_Counts",
        "Total_Number_of_Reviews_Reviewer_Has_Given","Reviewer_Score",
        "Tags","days_since_review","lat","lng"]

# driver options
def driver_setup():
    DRIVER_PATH = r"C:\Users\Paulus\Desktop\School\Big data\assignments\assignment 1\chromedriver/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    return driver


def scrapeHotel(driver, url):
    combined_frames = []
    driver.get(url)

    # remove cookie screen
    try:
        cookie_accept_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, r"//*[@id='onetrust-accept-btn-handler']")))
        cookie_accept_button.click()
    except NoSuchElementException:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "hp_hotel_name")))
    
    # clean hotelname
    hotel_name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "hp_hotel_name"))).text
    hotel_name = " ".join(hotel_name.split()[1:])

    # clean adress
    hotel_adress = driver.find_element_by_css_selector(
        "#showMap2 > span.hp_address_subtitle.js-hp_address_subtitle.jq_tooltip").text
    hotel_adress = "".join(hotel_adress.split(sep=","))
    
    # clean average score
    avg_score = driver.find_element_by_class_name("bui-review-score__badge").text
    avg_score = ".".join(avg_score.split(sep=","))
    
    # clean total reviews
    total_reviews = driver.find_element_by_class_name("bui-review-score__content").text
    total_reviews = "".join(total_reviews.split(sep="."))
    total_reviews = total_reviews.split()[1]

    # Lat Long values
    hotel_location = driver.find_element_by_css_selector("#hotel_address").get_attribute("data-atlas-latlng")
    latitude = hotel_location.split(sep=",")[0]
    longitude = hotel_location.split(sep=",")[1]


    # setup for scraping reviews
    review_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CLASS_NAME, "hp-topic-filter-score-suffix")))
    review_btn.click()

    # access filters for reviews
    language_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//*[@id='review_lang_filter']/button")))
    language_btn.click()

    eng_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, r"//*[@id='review_lang_filter']/div/div/ul/li[3]/button")))
    eng_btn.click()

    sleep(1)

    ## Actual review scraping
    # loop through paginations
    pagination_div = driver.find_element_by_class_name("c-pagination")
    last_pagination = pagination_div.find_elements_by_class_name("bui-pagination__item")
    last_pagination.pop()
    number_of_pages = int(last_pagination[-1].text.split()[0])
    for _ in range(number_of_pages):
        sleep(1)
        reviews_container = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='review_list']/li")))
        
        try:
            next_btn = driver.find_element_by_class_name("pagenext")
        except NoSuchElementException:
            break
         
        # loop through reviews
        for _ in reviews_container:
            left_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "c-review-block__left")))
            right_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "c-review-block__right")))

            # check if review is valid
            review_box = right_container.find_element_by_class_name("c-review")
            list_of_reviews = review_box.find_elements_by_class_name("c-review__row")
            
            if len(list_of_reviews) <= 1 :
                break

            if len(list_of_reviews) <= 2:
                continue

            list_of_reviews.pop()

            # standard review data
            review_date = right_container.find_element_by_class_name("c-review-block__date").text
            nationality = left_container.find_element_by_class_name("bui-avatar-block__subtitle").text
            review_score = right_container.find_element_by_class_name("bui-review-score__badge").text

            # clean date
            date_reggex = re.compile(r"[0-9]{2} [A-z]* [0-9]{4}")
            match = re.match(date_reggex, review_date)
            cleaned_date = review_date
            
            if match:
                cleaned_date = re.findall(date_reggex, review_date)[0]
                cleaned_date = datetime.strptime(cleaned_date, "%d %B %Y")
            else:
                cleaned_date = " ".join(cleaned_date.split()[1:])
                cleaned_date = datetime.strptime(cleaned_date, "%d %B %Y")

            days_since_review = date.today() - cleaned_date.date()
            days_since_review = str(days_since_review).split(sep=",")[0]
            
            cleaned_date = cleaned_date.strftime("%m/%d/%Y")

            # clean reviewer score
            review_score = ".".join(review_score.split(sep=","))

            # postive and negative reviews
            postive = ""
            negative = ""
            postive_word_count = 0
            negative_word_count = 0
            for k, item in enumerate(list_of_reviews):
                review_text = item.text.split(sep=" ")
                review_text = review_text[2:]
                review_text = " ".join(review_text)
                
                if k == 0:
                    postive += review_text
                    postive_word_count += len(review_text)
                else:
                    negative += review_text
                    negative_word_count += len(review_text)

            total_data = [hotel_adress, None, cleaned_date, avg_score, hotel_name, nationality,
                        negative, negative_word_count, total_reviews, postive, postive_word_count,
                        None, review_score, None, days_since_review, latitude, longitude]

            curr_df = pd.DataFrame([total_data], columns=column_names)
            combined_frames.append(curr_df)
        
        next_btn.click()
    driver.quit()
    return pd.concat(combined_frames, ignore_index=True)


total_df_array = []
with open("./resources/url.txt") as file:
    for row in file:
        driver = driver_setup()
        total_df_array.append(scrapeHotel(driver, row))
    file.close()

final_df = pd.concat(total_df_array, ignore_index=True)
final_df.drop_duplicates()
final_df.to_csv("./csv/webscraped.csv", index=False)