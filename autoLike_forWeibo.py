#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.keys import Keys
from random import choice
import pickle
import time
import sys

sys.getdefaultencoding()

likequaninty = 0

browser = webdriver.Firefox()

keywordseq = [
    "小米手环",
    "fitbit",
    "运动"
]

username = "noodum.wokamon@gmail.com"
password = "123qweasd"

def cookielogin():

    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
        log("cookie loaded")
    except:
        log("there is no cookie")
        return


def log(str):
    print "[" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "] " + str

def search(searchWord):

    time.sleep(5)
    inputBtn = browser.find_element_by_class_name("searchInp_form")
    inputBtn.clear()
    inputBtn.send_keys(searchWord.strip().decode("utf-8"))
    log("input key entered")
    browser.find_element_by_class_name('searchBtn').click()
    log("search button clicked")

    #ActionChains(browser).send_keys(Keys.ENTER).perform()

def login(username, password):

    time.sleep(5)
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

    pickle.dump( browser.get_cookies(), open("cookies.pkl","wb"))
    log("cookie saved")

def like():
    global likequaninty

    likelist = browser.find_elements_by_xpath("//div[@action-type='feed_list_item']/div[2]/ul/li[4]/a")
    for like in likelist :
        if like.get_attribute("title") == u"赞":
            like.click()
            try:
                browser.find_element_by_class_name("W_close").click()
                print "sleeping"
                time.sleep(1800)
            except:
                likequaninty += 1
                log(str(likequaninty)  + " liked")
                time.sleep(choice([6,7,8,9]))


def nextpage():

    try:
        nextpagebtn = browser.find_element_by_xpath("//div[@class='W_pages']/a[2]")
    except:
        nextpagebtn = browser.find_element_by_xpath("//div[@class='W_pages']/a")

    if nextpagebtn != None:
        nextpagebtn.click()
    else:
        browser.quit()

    log("next page")

    time.sleep(5)

#begin

def main():


    browser.get("http://s.weibo.com")
    log("weibo loaded")
    cookielogin()
    search(choice(keywordseq))
    log("search finished")
    try:
        login(username,password)
        log("logged in")
    except:
        log("can`t login by username&password")


    for i in range(0,50):
        like()
        nextpage()

    time.sleep(5)
    log("server finished")
    browser.quit()

main()

