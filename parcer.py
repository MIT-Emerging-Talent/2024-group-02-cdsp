#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python Version: 3.12
"""
File: parcer.py
Author: Vlad421
Date: 1/23/2024
Description: collects data from layoffs.fyi
Requirements: selenium, BeautifulSoup, html5lib

pip install selenium, bs4, html5lib

"""


import time


from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup

def update_pos(scrH, panH, curP):
    """linear relationship
    """

    print(scrH)
    print(panH)
    print(curP)
    x1 = 1000
    y1= scrH-panH
    x2= 10
    y2 = scrH
    # m = (y2-y1)/(x2-x1)
    m =(y2-y1)/(x2-x1)
    
    # y = mx+b
    # y = y1, x = x1
    b = y1-(x1*m)
    
    #x = (y-b)/m
    pos = int((curP-b)/m)
    print(pos)


    return pos
    


# Define the Chrome webdriver options
opts = ChromeOptions()
opts.add_argument("--window-size=1000,10440")
opts.add_argument("--headless")
opts.add_argument('--blink-settings=imagesEnabled=false')
opts.add_argument("--log-level=3")

# Pass the defined options objects to initialize the web driver
driver = Chrome(opts)
# Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
driver.implicitly_wait(5)

URL = "https://airtable.com/appzLUHyhTU5xpkdZ/shrclnXK0pfoGjtih/tblQ0U46nsYopm2CR"


driver.get(URL)
time.sleep(5)



number_of_rows_s = driver.find_element(
    By.CSS_SELECTOR, "#view > div > div.paneContainer > div.summaryBarContainer > div.leftPaneWrapper > div > div > div > div.absolute.z1.flex-inline.border-top.border-transparent > div").text
number_of_rows = ""
for l in number_of_rows_s:
    if l.isnumeric():
        number_of_rows += l

number_of_rows = int(number_of_rows)

html = ""
table = {}
sourceFile = open('txtoutput.html', 'w', encoding="utf-8")
slider = driver.find_element(
    By.CSS_SELECTOR, "#view > div > div.paneContainer > div.scrollOverlay.antiscroll-wrap > div.antiscroll-scrollbar.antiscroll-scrollbar-vertical.antiscroll-scrollbar-shown")


dist = 3
data = driver.find_element(By.CSS_SELECTOR, "#view > div > div.paneContainer ")
index = 0
jsSyyle = "'3px solid red'"


page_height = driver.get_window_size()['height']  # Get page height

'''scroll_bar = driver.find_element(
    By.XPATH, "//*[@id=\"view\"]/div/div[1]/div[1]/div[3]")
print(scroll_bar.location[y])
# Substracted 160 fro page height to compensate differnec between window and screen height
ActionChains(driver).drag_and_drop_by_offset(
    scroll_bar, 0, scroll_bar.location.values).perform()

'''
scroll_pane_height = driver.find_element(By.CSS_SELECTOR, "#view > div > div.paneContainer > div.scrollOverlay.antiscroll-wrap").size['height']


prev_size = 0
new_pos = 0
#while False:

prev_loc = 0
#for i in  range (1):
while len(table) != number_of_rows:
    driver.execute_script("arguments[0].style.border=" + jsSyyle, slider)

    # If this line causes an error, run 'pip install html5lib' or install html5lib
    soup = BeautifulSoup(data.get_attribute('innerHTML'), 'html5lib')
    info = []

    for row in soup.findAll('div',
                            attrs={"data-rowindex": True}):
        # print(row["data-rowindex"])
        index = int(row["data-rowindex"])
        if index not in table:
            table[index] = []
        text = row.text
        info = table.get(index)
        if text not in info:
            table.get(index).append(row.text)
        # info.append(row.text)
    print(len(table))
    """
    if prev_size == len(table) and  slider.location['y'] ==  prev_loc:
        ActionChains(driver).move_to_element(slider).click_and_hold(slider).move_by_offset(0, -400).release().perform()
        print("performed")
        time.sleep(0.5)
    """

    # ActionChains(driver).move_to_element(slider).click_and_hold(slider).move_by_offset(0, dist).release().perform()
    
    
    new_pos = update_pos(page_height, scroll_pane_height, slider.location['y'])
    
    #ActionChains(driver).drag_and_drop( slider, 0, new_pos).click().perform()
    ActionChains(driver).move_to_element(slider).click_and_hold(slider).move_by_offset(0, new_pos).release().perform()
    time.sleep(2.5)
    
    prev_loc = slider.location['y']
    prev_size = len(table)
    
    

print("done")

time.sleep(2)

for i in table:

    print(i, end=" - ")
    print("\t"+str(table[i]))

prev = -1
is_done = False
for i in table:
    if prev != i-1:
        print("something missed")
        break
    else:
        prev = i
        if prev+1 == number_of_rows:
            is_done = True
if is_done:
    print("everithing correct ")

# soup = BeautifulSoup(table.get_attribute('innerHTML'), 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib

# print(soup,file=sourceFile)
