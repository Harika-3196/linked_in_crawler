import os
import re
import io
import time
import uuid
import pickle
import requests
import datetime
import selenium
import pandas as pd
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

# profile-content
# body
# scaffold-layout
# scaffold-layout__inner 
# scaffold-layout__row 
# scaffold-layout__main
# artdeco-card ember-view 
# ph5
# pv-top-card--list 
# text-body-small
# ember-view 

def crawl_profiles(driver,profile_links):
    res=[]
    for link in profile_links:
        try:
            driver.get(link)
            temp={}
            temp["link"] =link
            temp["followers"],temp["connections"] = driver.find_element_by_class_name('authentication-outlet')\
                                                    .find_element_by_id('profile-content')\
                                                    .find_element_by_class_name('body')\
                                                    .find_element_by_class_name('scaffold-layout')\
                                                    .find_element_by_class_name('scaffold-layout__inner')\
                                                    .find_element_by_class_name('scaffold-layout__row')\
                                                    .find_element_by_class_name('scaffold-layout__main')\
                                                    .find_element_by_class_name('artdeco-card')\
                                                    .find_element_by_class_name('ph5')\
                                                    .find_element_by_class_name('pv-top-card--list').text.split("\n")


            temp["profile_description"] = driver.find_element_by_class_name('authentication-outlet')\
                                                .find_element_by_id('profile-content')\
                                                .find_element_by_class_name('body')\
                                                .find_element_by_class_name('scaffold-layout')\
                                                .find_element_by_class_name('scaffold-layout__inner')\
                                                .find_element_by_class_name('scaffold-layout__row')\
                                                .find_element_by_class_name('scaffold-layout__main')\
                                                .find_element_by_class_name('artdeco-card')\
                                                .find_element_by_class_name('ph5')\
                                                .find_element_by_class_name('mt2')\
                                                .find_element_by_class_name('pv-text-details__left-panel')\
                                                .find_element_by_class_name('text-body-medium').text

    

            res.append(temp)
            time.sleep(5)
        except:
            m=0
    return res

    
def write_to_pickle(directory_path,data):
    file_name=datetime.datetime.now().strftime('%d_%b_%G_%I_%M_%p')+'.pickle'
    path = os.path.join(directory_path,file_name)
    # Open a file and use dump()
    with open(path, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_pickle(file_path):
    with open(file_path, 'rb') as handle:
        data = pickle.load(handle)
    return data




# if __name__ == '__main__':
#     #Install Driver
#     driver = webdriver.Chrome(executable_path=r"/Users/h0s060n/Downloads/chromedriver")
#     #Specify Search URL 
#     search_url="""https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"""
#     username,password = get_credentials("./credentials.txt")
#     login_func(driver,search_url,username,password)
#     profile_data=crawl_profiles(driver,['https://www.linkedin.com/in/kg2000'])
#     write_to_pickle("../data/profile_data",profile_data)
#     print(profile_data)
#     driver.close()

if __name__ == '__main__':
    #Install Driver
    driver = webdriver.Chrome(executable_path=r"/Users/h0s060n/Downloads/chromedriver")
    #Specify Search URL 
    search_url="""https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"""
    username,password = get_credentials("./credentials.txt")
    login_func(driver,search_url,username,password)
    data_directory = "../data/post_data"
    post_files = os.listdir(data_directory)
    post_files = [os.path.join(data_directory,path) for path in post_files]
    data=[]
    for path in post_files:
        print(path)
        data.extend(load_pickle(path))
    df =pd.DataFrame(data)
    df.drop_duplicates(subset=["content"],inplace=True)
    profile_links=list(set(df["profile_link"]))[0:100]
    profile_data=crawl_profiles(driver,profile_links)
    write_to_pickle("../data/profile_data",profile_data)
    print(profile_data)
    print(len(profile_data))
    driver.close()

   