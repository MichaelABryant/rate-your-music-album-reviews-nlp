#import packages
from selenium import webdriver
import time
import pandas as pd
import numpy as np
from selenium.common.exceptions import NoSuchElementException 

#function for requesting number of reviews
def get_album_reviews(review_page_url, num_reviews, verbose=0):
    
    '''Gathers albums as a dataframe, scraped from rateyourmusic.com'''   
    
    #initialize chrome driver
    driver = webdriver.Chrome(executable_path="C:/Users/malex/Desktop/rate_your_music_nlp/scraper/chromedriver.exe")
    driver.set_window_size(1120, 1000)

    #url to begin scraping from
    url = review_page_url
    try:
        driver.get(url)
    except:
        driver.quit()
        return None
    
    #wait for browser to open
    time.sleep(5)
    
    #initialize reviews array
    reviews = []
    
    try:
        #while number of collected reviews does not equal number of requested reviews 
        while len(reviews) != num_reviews:
            
            #get review ids
            review_ids = driver.find_elements_by_xpath('.//div[@id="column_container_right"]//div[contains(@id,"reviews")]//div[contains(@id, "std")]')
            
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
            
                #runs until collected_successfully = True
                while not collected_successfully:
                    
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
                    
                    #if page hasn't loaded yet wait 5 seconds
                    except:
                        time.sleep(5)
        
                #append scraped information to reviews array
                reviews.append({"User": user,
                                "Review": review,
                                "Rating": rating})
            
            #click next page
            try:
                driver.find_element_by_xpath('.//a[@class="navlinknext"]').click()
            
                time.sleep(1)
            
            #if on last page then break from if condition
            except NoSuchElementException:
                
                break
    except:
        driver.quit()
        return pd.DataFrame(reviews)
        
    # Close browser after scraping has finished.    
    driver.quit()
        
    #return requested reviews as a dataframe
    return pd.DataFrame(reviews)