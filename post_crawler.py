import os
import io
import time
import uuid
import pickle
import requests
import datetime
import selenium
from PIL import Image
from pprint import pprint
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException




def login_func(driver,search_url,mailid,password,sleep_time=4):
    driver.get(search_url)
    inputElement = driver.find_element_by_id("username")
    inputElement.send_keys(mailid)

    inputElement = driver.find_element_by_id("password")
    inputElement.send_keys(password)

    driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()
    time.sleep(sleep_time)

def get_credentials(filepath):
    f = open(filepath, "r")
    lines = f.read()
    return lines.split("\n")[0],lines.split("\n")[1]


def load_posts(duration=10):
    SCROLL_PAUSE_TIME = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")
    start_time=time.time()
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        # if new_height == last_height:
        #     break
        last_height = new_height
        end_time=time.time()
        if end_time-start_time>=duration:
            break

def crawl_posts(driver):
    posts_data=driver.find_elements_by_class_name('feed-shared-update-v2')
    res = []
    for post in posts_data:
        try:
            temp = {}
            temp["unique_id"] = uuid.uuid4()
            temp['name'] = post.find_element_by_class_name("feed-shared-actor").find_element_by_class_name("app-aware-link").find_element_by_class_name("feed-shared-actor__meta").find_element_by_class_name("feed-shared-actor__name").text
            temp['profile_link'] = post.find_element_by_class_name("feed-shared-actor").find_element_by_class_name("app-aware-link").get_attribute("href").split("?")[0]
            try:
                temp['content'] = post.find_element_by_class_name("feed-shared-update-v2__description-wrapper").find_element_by_class_name("feed-shared-inline-show-more-text").find_element_by_class_name("feed-shared-text").text
            except:
                temp["content"] = ""
            try:
                engagement = post.find_element_by_class_name("social-details-social-activity").find_element_by_class_name("social-details-social-counts").find_elements_by_class_name("social-details-social-counts__item")
            except:
                engagement = None
            try:
              
                try:
                    temp["likes"]=engagement[0].find_element_by_class_name("t-black--light").find_element_by_class_name("social-details-social-counts__social-proof-fallback-number").text
                except:
                    temp["likes"]=engagement[0].find_element_by_class_name("t-black--light").find_element_by_class_name("social-details-social-counts__reactions-count").text
            except:
                temp['likes'] = '0'
            try:
                temp['comments'] = engagement[1].find_element_by_class_name("t-black--light").text
            except:
                temp['comments'] = '0 comments'
            try:
                temp['shares'] = engagement[2].find_element_by_class_name("t-black--light").text
            except:
                temp['shares'] = '0 shares'
            try:
                temp["time_posted"] =post.find_element_by_class_name("feed-shared-actor").find_element_by_class_name('app-aware-link')\
                                            .find_element_by_class_name('feed-shared-actor__meta')\
                                            .find_element_by_class_name('feed-shared-actor__sub-description')\
                                            .text
            except:
                temp['time_posted'] = 'null'
            try:
                temp["url_link"] = post.find_element_by_class_name("feed-shared-image").find_element_by_class_name('relative')\
                                        .find_element_by_class_name('feed-shared-image__container')\
                                        .find_element_by_class_name('feed-shared-image__image-link')\
                                        .find_element_by_class_name('ivm-image-view-model')\
                                        .find_element_by_class_name('ivm-view-attr__img-wrapper')\
                                        .find_element_by_class_name('ivm-view-attr__img--centered').get_attribute('src')
            except:
                temp["url_link"] = "null"

            res.append(temp)
        except:
            print("--------------------exception occured---------------------")
    return res


def write_to_pickle(directory_path,data):
    file_name=datetime.datetime.now().strftime('%d_%b_%G_%I_%M_%p')+'.pickle'
    path = os.path.join(directory_path,file_name)
    # Open a file and use dump()
    with open(path, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    




if __name__ == '__main__':
    #Install Driver
    driver = webdriver.Chrome(executable_path=r"/Users/h0s060n/Downloads/chromedriver")
    #Specify Search URL 
    search_url="""https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"""
    username,password = get_credentials("./credentials.txt")
    login_func(driver,search_url,username,password)
    _=load_posts(duration=1200)
    crawl_post_data=crawl_posts(driver)
    write_to_pickle("../data/post_data",crawl_post_data)
    pprint(crawl_post_data)
    print(len(crawl_post_data))
    driver.close()

# if __name__ == '__main__':
#     #Install Driver
#     driver = webdriver.Chrome(executable_path=r"/Users/h0s060n/Downloads/chromedriver")
#     #Specify Search URL 
#     search_url="""https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"""
#     username,password = get_credentials("./credentials.txt")
#     login_func(driver,search_url,username,password)
#     crawl_post_data=[]
#     for i in range(100):
#         _=load_posts(duration=5)
#         temp_post_data=crawl_posts(driver)
#         crawl_post_data.extend(temp_post_data)
#     write_to_pickle("../data/post_data",crawl_post_data)
#     pprint(crawl_post_data)
#     print(len(crawl_post_data))
#     driver.close()

