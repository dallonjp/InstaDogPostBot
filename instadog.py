# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 20:34:33 2019

@author: dallon penney
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
assert sys.version_info >= (3, 5, 2), "Python version too low."
from pprint import pprint
from urllib import request as urlrequest, parse as urlparse
import json
import urllib.request

class DogAPI(object):

    def list(self):
        return self._api_request("breeds/list")

    def list_images(self, breed, subbreed=None):
        if subbreed is None:
            return self._api_request("breed/{}/images".format(breed))
        else:
            return self._api_request("breed/{}/{}/images".format(breed, subbreed))

    def random(self, breed=None, subbreed=None):
        if breed is None:
            return self._api_request("breeds/image/random".format(breed))
        if subbreed is None:
            return self._api_request("breed/{}/images/random".format(breed))
        else:
            return self._api_request("breed/{}/{}/images/random".format(breed, subbreed))

    def _api_request(self, endpoint):
        # print(self._build_url(endpoint)) # Useful for debugging, but not enough to implement a logger
        return json.loads(urlrequest.urlopen(
            urlparse.urljoin("https://dog.ceo/api/", endpoint)
        ).read().decode("utf-8"))

def fetch():
    from pprint import pprint
    from random import choice
    import os
    global dogbreed
    global breedlist
    wpath = "C:/Users/dallo/instabotdog" #where the images will be saved
    #*path must match path in .exe script called within instadog func()
    os.chdir(wpath)
    dogapi = DogAPI()
    randomdoggy = dogapi.random()
    #breedlist = dogapi.list()
    #pprint(randomdoggy)
    for d in randomdoggy:
        if randomdoggy[d] == 'success':
            pass
        else:
            dogurl = randomdoggy[d]
            pprint(dogurl)

            dogurlarray = dogurl.split('/')
            for index, part in enumerate(dogurlarray):
                if part == 'breeds':
                    dogbreed = dogurlarray[index+1]
                    #pprint(f"you caught a {dogbreed}!")
    #download random dog image
    urllib.request.urlretrieve(dogurl, "00000001.jpg")
    #specify name of downloaded image file
def check_img():
    import imagesize
    from pprint import pprint

    imgpath = "C:/Users/dallo/instabotdog/00000001.jpg"
    #should be the same as 'path' in fetch and the same image name
    width, height = imagesize.get(imgpath)
    size = height * width

    if size < 100000:
        pprint('size of image pulled is too small, quitting')
        quit()
def get_dogquote():
    from pprint import pprint
    import random
    global dogquote
    global author
    dogquotespath = "C:/Users/dallo/instabotdog/dogquotes.txt"
	#path to dogquotes on user's machine
    with open(dogquotespath) as f:
        lines = f.readlines()
        dogquote = random.choice(lines)
        quotearray = dogquote.split('–')
        for index, part in enumerate(quotearray):
            authorstr = quotearray[1]
            authorstrarray = authorstr.split(' ')
            for index, part in enumerate(authorstrarray):
                author = authorstrarray[1]+authorstrarray[2]
                #pprint(authorstrarray[0]+authorstrarray[1])
        pprint(dogquote)
        pprint(author)
def instabot():
    import time
    from pprint import pprint
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import NoSuchElementException
    from selenium.common.exceptions import TimeoutException
    import subprocess
    import os
    #Set working directory
    wpath = "C:/Users/dallo/instabotdog"
    os.chdir(wpath)

    #set up driver
    chrome_options = Options()
    mobile_emulation = { "deviceName": "Nexus 5" }
    #spoof a mobile instance of chrome
    chrome_options.add_argument("--window-size=200,700")
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(executable_path="C:/Users/dallo/AppData/Local/Programs/Python/Python37-32/chromedriver.exe",options=chrome_options)

    #Load Instagram
    driver.set_page_load_timeout(10)
    wait = WebDriverWait(driver, 10)
    driver.get('https://www.instagram.com/accounts/login/')
    #username and password
    insta_username = ''
    insta_password = ''
    #Login
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Phone number, username, or email']")))
        username = driver.find_element_by_xpath("//*[@aria-label='Phone number, username, or email']")
        username.send_keys(insta_username)
        password = driver.find_element_by_xpath("//*[@aria-label='Password']");
        password.send_keys(insta_password,Keys.ENTER)
        pprint('Login Successful!')
    except NoSuchElementException:
        pprint('login failed!')
        driver.quit()
    #Click through popups
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='GAMXX']")))
        try:
            driver.find_element_by_xpath("//*[@class='GAMXX']").click()
        except NoSuchElementException:
            pprint('no not now button')
    except TimeoutException:
        pprint('--> element timeout!')
    try:
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Not Now')))
        try:
            driver.find_element_by_link_text('Not Now').click()
        except NoSuchElementException:
            pprint('no not now button')
    except TimeoutException:
        pprint('--> element timeout!')

    try:
        driver.find_element_by_xpath("//*[@class='aOOlW   HoLwm ']").click()
    except NoSuchElementException:
        pprint('1st popup did not load')

    driver.execute_script("window.scrollTo(0, 10)")
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='aOOlW   HoLwm ']")))
        try:
            driver.find_element_by_xpath("//*[@class='aOOlW   HoLwm ']").click()
        except NoSuchElementException:
            pprint('2nd popup did not load')
    except TimeoutException:
        pprint('--> element timeout!')
    #upload photo
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='New Post']")))
        try:
            driver.find_element_by_xpath("//*[@aria-label='New Post']").click()
        except NoSuchElementException:
            pprint('could not find the post button')
            driver.quit()
    except TimeoutException:
        pprint('--> element timeout!')
    wait = WebDriverWait(driver, 20)
    subprocess.run(args=r"C:\Users\dallo\AppData\Roaming\Python\Python37\chromefileupload.exe"); #specify full path to autoit3 script
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='UP43G']")))
    driver.find_element_by_xpath("//*[@class='UP43G']").click()

    #write custom hashtags based on breed
    if '-' in dogbreed:
        pprint('dogbreed is hyphenated')
        hybreed = dogbreed.split('-')
        checkedbreed = f'{hybreed[1]}{hybreed[0]}'
        pprint(checkedbreed)
    else:
        checkedbreed = dogbreed

    tags = f'#{checkedbreed} #{author}quotes'
    #write tags for post
    paragraph = dogquote + " " + tags
    pprint(paragraph + " will be written as the description!")

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='_472V_']")))
        try:
            driver.find_element_by_xpath("//*[@class='_472V_']").send_keys(paragraph)
            time.sleep(2)
        except NoSuchElementException:
            pprint('could not write quote and tags')
            time.sleep(2)
            driver.quit()
    except NoSuchElementException:
        pprint('could not load the post page!')
        time.sleep(2)
        driver.quit()
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='UP43G']")))
        try:
            driver.find_element_by_xpath("//*[@class='UP43G']").click()
            pprint('dog posted!')
            time.sleep(2)
        except NoSuchElementException:
            pprint('could not click the post button!')
            time.sleep(2)
            driver.quit()
    except NoSuchElementException:
        pprint('the post button did not load!')
        time.sleep(2)
        driver.quit()
    driver.quit()

if __name__ == "__main__":
    fetch()
    check_img()
    get_dogquote()
    instabot()
