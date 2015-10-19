#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from random import choice
import time

import sys

sys.getdefaultencoding()

getquaninty = 0

browser = webdriver.Firefox()

browser.get("http://s.weibo.com")

keywordseq = [
    "wokamon",
    "走星人",
    "小米手环",
    "fitbit",
    "运动",
    "happy"
]

username = "smallcorpse@hotmail.com"
password = "l4g3s2b3lb"

def search(searchWord):

    time.sleep(5)
    inputBtn = browser.find_element_by_class_name("searchInp_form")
    inputBtn.clear()
    inputBtn.send_keys(searchWord.strip().decode("utf-8"))
    browser.find_element_by_class_name('searchBtn').click()

    print "searching :" + searchWord

def login(username, password):

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
            print msg.get_attribute("mid")
            try:
                browser.find_element_by_class_name("W_close").click()
                time.sleep(7200)
                print "sleeping"
            except:
                getquaninty += 1
                time.sleep(choice([1,2,3,4]))

def nextpage():

    try:
        nextpagebtn = browser.find_element_by_xpath("//div[@class='W_pages']/a[2]")
    except:
        nextpagebtn = browser.find_element_by_xpath("//div[@class='W_pages']/a")

    if nextpagebtn != None:
        nextpagebtn.click()
    else:
        #browser.quit()
        print "end"

    time.sleep(5)

#begin

search(choice(keywordseq))
login(username,password)

for i in range(0,50):
    getid()
    nextpage()

print str(getquaninty)  + " messages got"

time.sleep(5)
browser.quit()

