#import packages
from selenium import webdriver
import time
import pandas as pd
import numpy as np
from selenium.common.exceptions import NoSuchElementException 

#function for requesting number of reviews
def get_album_reviews(review_page_url, num_reviews=np.inf, verbose=0):
    
    '''Gathers albums as a dataframe, scraped from rateyourmusic.com'''   
    
    #initialize chrome driver
    driver = webdriver.Chrome(executable_path="C:/Users/malex/Desktop/rate_your_music_nlp/scraper/chromedriver.exe")
    driver.set_window_size(1120, 1000)

    #url to begin scraping from
    url = review_page_url
    try:
        driver.get(url)
    except:
        try:
            driver.close()
            return None
        except:
            return None
    
    #wait for browser to open
    time.sleep(3)
    
    #initialize reviews array
    reviews = []
    
    # Count number of review fails, if three fail then exit scraping
    consecutive_failed = 0
    
    #while number of collected reviews does not equal number of requested reviews 
    while len(reviews) < num_reviews:
        
        try:
            #get review ids
            review_ids = driver.find_elements_by_xpath('.//div[@id="column_container_right"]//div[contains(@id,"reviews")]//div[contains(@id, "std")]')
        except:
            try:
                time.sleep(3)
                review_ids = driver.find_elements_by_xpath('.//div[@id="column_container_right"]//div[contains(@id,"reviews")]//div[contains(@id, "std")]')
            except:
                try:
                    driver.close()
                    return pd.DataFrame(reviews)
                except:
                    return pd.DataFrame(reviews)
    
        
        #for each review
        for ids in review_ids:
            
            #determine the location of the review
            location = ids.get_attribute('id')
            
            #xpath to specify review location
            xpath = './/div[@id="'
            xpath += str(location)
            xpath += '"]'
            
            #initialize variable to break while loop
            collected_successfully = False
            grab_review_attempts = 3
            
            #runs until collected_successfully = True
            while (grab_review_attempts != 0) and (collected_successfully == False):
                
                #try to find items for scraping
                try:
                    
                    review = []
                    user = driver.find_element_by_xpath('{}//div[contains(@class, "review_header")]//a[contains(@class, "user")]'.format(xpath)).text
                    review_loc = driver.find_elements_by_xpath('{}//div[contains(@class, "body")]//span[contains(@class, "rendered")]'.format(xpath))
                    
                    #reviews are in list form so append
                    for value in review_loc:
                        review.append(value.text)
                    
                    #if rating exists record otherwise set to nan
                    try:
                        rating_loc = driver.find_element_by_xpath('{}//div[contains(@class, "header")]//span[contains(@class, "rating")]/img[@width="90"]'.format(xpath))
                        rating = rating_loc.get_attribute("title")
                    except NoSuchElementException:
                        rating = np.nan
                        
                    #set true to break while loop
                    collected_successfully = True
                    consecutive_failed = 0
                
                #if page hasn't loaded yet wait 5 seconds
                except:
                    time.sleep(1)
                    grab_review_attempts -= 1
    
            if collected_successfully == True:
                #append scraped information to reviews array
                reviews.append({"User": user,
                                "Review": review,
                                "Rating": rating})
            else:
                consecutive_failed += 1
                
            if (len(reviews) == num_reviews) or (consecutive_failed >= 3):
                break
        
        if (len(reviews) == num_reviews) or (consecutive_failed == 4):
            break
        
        #click next page
        try:
            driver.find_element_by_xpath('.//a[@class="navlinknext"]').click()
            time.sleep(2)
        
        #if on last page then break from while condition
        except NoSuchElementException:
            try: 
                driver.close()
                return pd.DataFrame(reviews)
            except:
                return pd.DataFrame(reviews)
        
    # Close browser after scraping has finished.    
    driver.close()
        
    #return requested reviews as a dataframe
    return pd.DataFrame(reviews)