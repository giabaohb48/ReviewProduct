from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,WebDriverException,NoSuchElementException
import time
import pandas as pd
import sys



# element
CMT_LIST = 'div > div.product-ratings__list > div.shopee-product-comment-list > .shopee-product-rating'
# CMT_CONTENT = '.shopee-product-rating__content'
CMT_CONTENT = '._3NrdYc'
CMT_RATING = '.shopee-product-rating__rating'
CMT_STAR_ACTIVE = '.icon-rating-solid--active'


def load_url_selenium_shopee(url):
    s=Service(ChromeDriverManager().install())

    # s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    # driver.maximize_window()
    
    print("Loading url=", url)
    driver.get(url)
    time.sleep(1)

    list_review = []
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    for j in range(1, total_height, 200):
        driver.execute_script("window.scrollTo(0, {});".format(j))
        time.sleep(0.5)

    # just craw 10 page
    x=0
    while x<5:

        list_cmt = driver.find_elements_by_css_selector(CMT_LIST)
        for it in list_cmt:
            try:
                content = it.find_element_by_css_selector(CMT_CONTENT).text.replace('\n',' ')   
                list_review.append(content)
                
            except (NoSuchElementException):
                print('no comment')

        #Check for button next-pagination-item have disable attribute then jump from loop else click on the next button
        try:
            elm = driver.find_element_by_class_name('shopee-icon-button--right')
            elm.click()
            print("next page")
            time.sleep(2)
            x +=1
        except (TimeoutException, WebDriverException) as e:
            print("Load several page!")
            break
    
    driver.close()
    return list_review


# url = str(sys.argv)
# data = load_url_selenium_shopee(url)
# dict = {'content':data}
# df = pd.DataFrame(dict)
# df.to_csv('E:\\1OneDrive\\OneDrive - Trường ĐH CNTT - University of Information Technology\\2021_1\\Big Data\\project\\test.csv')
