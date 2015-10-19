#!/usr/bin/env python
# -*- coding: utf-8 -*-

import weibo
import time
import pickle
from selenium import webdriver
from random import choice

APP_KEY = "3186675918"
APP_SECRET = "5d8529ae73fdd0f78368d0e04344b95b"

REDIRECT_URL = "https://api.weibo.com/oauth2/default.html"

username = "smallcorpse@hotmail.com"
password = "l4g3s2b3lb"

keywordseq = [
    "wokamon",
    "走星人",
    "小米手环",
    "fitbit",
    "运动",
    "happy"
]

Commentusername = "smallcorpse@hotmail.com"
Commentpassword = "l4g3s2b3lb"

Commentseq = [
    u"随机从一个评论中选取一个进行评论",
    u"随机从一个评论中选取一个进行评论",
    u"随机从一个评论中选取一个进行评论",
    u"随机从一个评论中选取一个进行评论"
]

getquaninty = 0

api = weibo.APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=REDIRECT_URL)

authorize_url = api.get_authorize_url()

browser = webdriver.Firefox()
browser.get(authorize_url)

def log(str):
    print "[" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "] " + str

def login(username, password):

    time.sleep(5)
    user = browser.find_element_by_xpath("//input[@id='userId']")
    user.clear()
    user.send_keys(username)
    psw = browser.find_element_by_xpath("//input[@name='passwd']")
    psw.clear()
    psw.send_keys(password)
    try:
        browser.find_element_by_xpath("//div[@class='oauth_login_submit']/p/a").click()
    except:
        time.sleep(1)
    time.sleep(5)
    try:
        browser.find_element_by_xpath("//div[@class='oauth_login_submit']/p/a").click()
    except:
        time.sleep(1)

    log("appuser logined")

login(username,password)

code = browser.current_url.strip("https://api.weibo.com/oauth2/default.html?code=")

browser.quit()

try:
    request = api.request_access_token(code,REDIRECT_URL)
    log("request acces token")
    access_token = request.access_token
    expires_in = request.expires_in
    pickle.dump( access_token, open("access_token.pkl","wb"))
    pickle.dump( expires_in, open("expires_in.pkl","wb"))
    log("token has been saved")

except:
    access_token = pickle.load(open("access_token.pkl", "rb"))
    expires_in = pickle.load(open("expires_in.pkl", "rb"))
    log("token has been loaded")

api.set_access_token(access_token, expires_in)

log("accessed weibo api")

#https://api.weibo.com/2/comments/create.json

browser = webdriver.Firefox()

browser.get("http://s.weibo.com")

def search(searchWord):

    time.sleep(5)
    inputBtn = browser.find_element_by_class_name("searchInp_form")
    inputBtn.clear()
    inputBtn.send_keys(searchWord.strip().decode("utf-8"))
    browser.find_element_by_class_name('searchBtn').click()

    log("searching :" + searchWord)

def userlogin(username, password):

    browser.find_element_by_xpath("//a[@node-type='loginBtn']").click()

    time.sleep(5)

    user = browser.find_element_by_xpath("//input[@name='username']")
    user.clear()
    user.send_keys(username)
    psw = browser.find_element_by_xpath("//input[@name='password']")
    psw.clear()
    psw.send_keys(password)
    browser.find_element_by_xpath("//div[6]/a").click()

    time.sleep(5)

def getid():
    global getquaninty

    msglist = browser.find_elements_by_xpath("//div[@action-type='feed_list_item']")
    for msg in msglist :
        if msg.get_attribute("mid"):
            api.comments.create.post(comment=choice(Commentseq),id=int(msg.get_attribute("mid")))
            log (msg.get_attribute("mid") + " has been commend")
            try:
                browser.find_element_by_class_name("W_close").click()
                time.sleep(7200)
                log("sleeping")
            except:
                getquaninty += 1
                time.sleep(choice([10,12,13,14]))

def nextpage():

    try:
        nextpagebtn = browser.find_element_by_xpath("//div[@class='W_pages']/a[2]")
    except:
        nextpagebtn = browser.find_element_by_xpath("//div[@class='W_pages']/a")

    if nextpagebtn != None:
        nextpagebtn.click()
    else:
        #browser.quit()
        log("end")

    time.sleep(5)

#begin

search(choice(keywordseq))
userlogin(username,password)

for i in range(0,50):
    getid()
    nextpage()

log(str(getquaninty)  + " messages got")

time.sleep(5)
browser.quit()

