#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python Version: 3.12
"""
File: parcer.py
Author: Vlad421
Date: 2/4/2024
Description: collects data from layoffs.fyi using Selenium with ChromeDriver
Requirements: selenium, BeautifulSoup, html5lib, tqdm

pip install selenium, bs4, html5lib, tqdm

"""


import time
from datetime import datetime, timezone
import csv
import os

from random import random

from tqdm import tqdm

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup


URL_prev = "https://airtable.com/appzLUHyhTU5xpkdZ/shrclnXK0pfoGjtih/tblQ0U46nsYopm2CR"
columns = ["id", "Company", "Location HQ", "# Laid Off", "Date", "%", "Industry", "Source", "List of emploees laid", "Stage", "$ Raised mm", "Country", "Date added","Is US based"]

dir = os.path.dirname(os.path.relpath(__file__)) + '/'


def scrap():

    def fix_date(old_date: str) -> str:

        date_format = "%m/%d/%Y"

        return datetime.strptime(old_date, date_format).strftime('%Y-%m-%d')

    def update_pos(scrH, panH, curP):
        """Linear relationship function for step position update
        """

        # initial proportion
        x1 = 900
        y1 = scrH-panH
        x2 = 5
        y2 = scrH

        # m = (y2-y1)/(x2-x1)
        m = (y2-y1)/(x2-x1)
        # y = mx+b
        # y = y1, x = x1
        b = y1-(x1*m)

        # x = (y-b)/m
        pos = int((curP-b)/m)

        return pos

    # Define the Chrome webdriver options
    opts = ChromeOptions()
    opts.add_argument("--window-size=2000,11440")
    opts.add_argument("--headless")
    opts.add_argument('--blink-settings=imagesEnabled=false')
    opts.add_argument("--log-level=3")

    # Pass the defined options objects to initialize the web driver
    driver = Chrome(opts)
    # Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
    driver.implicitly_wait(8)

    URL = "https://airtable.com/app1PaujS9zxVGUZ4/shrqYt5kSqMzHV9R5/tbl8c8kanuNB6bPYr"

    driver.get(URL)
    time.sleep(random()*3)

    total = "#view > div > div.paneContainer > div.summaryBarContainer > div.leftPaneWrapper > div > div > div > div.absolute.z1.flex-inline.border-top.border-transparent > div"
    number_of_rows_s = driver.find_element(By.CSS_SELECTOR, total).text
    number_of_rows = ""
    for l in number_of_rows_s:
        if l.isnumeric():
            number_of_rows += l

    number_of_rows = int(number_of_rows)

    table = {}

    slider_div = "#view > div > div.paneContainer > div.scrollOverlay.antiscroll-wrap > div.antiscroll-scrollbar.antiscroll-scrollbar-vertical.antiscroll-scrollbar-shown"
    slider = driver.find_element(
        By.CSS_SELECTOR, slider_div)

    table_grid_pane = "#view > div > div.paneContainer"
    data = driver.find_element(By.CSS_SELECTOR, table_grid_pane)
    index = 0

    # Get page height
    page_height = driver.get_window_size()['height']

    # Get table grid heigth
    table_pane = "#view > div > div.paneContainer > div.headerAndDataRowContainer"
    scroll_pane_height = driver.find_element(
        By.CSS_SELECTOR, table_pane).size['height']

    new_pos = 0

    last_index = -1

    prev_count = 0
    pbar = tqdm(total=number_of_rows)
    while len(table) != number_of_rows:

        # If this line causes an error, run 'pip install html5lib' or install html5lib
        soup = BeautifulSoup(data.get_attribute('innerHTML'), 'html5lib')

        for row in soup.findAll('div', attrs={"data-rowindex": True}):

            index = int(row["data-rowindex"])
            if index not in table:
                table[index] = []

            text = row.text

            if (len(table.get(index)) < len(columns)-2):

                if text == '':
                    text = "no-data"

                table.get(index).append(text)

        pbar.set_description("Aquired ["+str(len(table))+"] items")

        if index > last_index:
            last_index = index

            pbar.update(len(table)-prev_count)
            prev_count = len(table)

        new_pos = update_pos(
            page_height, scroll_pane_height, slider.location['y'])

        ActionChains(driver).move_to_element(slider).click_and_hold(
            slider).move_by_offset(0, new_pos).release().perform()
        time.sleep(4+random()*4)

    time.sleep(2+random()*2)

    del pbar

    print("Creating list..")
    out = []

    for i in tqdm(table):
        line = [i]+table[i]

        out.append(line)

    print("Checking data")
    for l in tqdm(out):
        for i in l:
            if hasattr(i, '__iter__') and '\n' in i :
                 i = i.replace('\n','')
            elif hasattr(i, '__iter__') and  "/\n" in i:
                 i = i.replace("/\n",'')

    print("Fixing date format")
    for l in tqdm(out):
        l[4] = fix_date(l[4])
        l[12] = fix_date(l[12])



    # add US, Non US column
   
    for l in out:
        if "Non-U.S." in l[2]:
            l[2]=l[2].replace("Non-U.S.", '')
            l.append("No")
        else:
            l.append("Yes")

    print("Writing output to out.log")
    with open(dir+"out.log", 'w', encoding="utf-8") as file:
        for line in out:
            file.write(f"{line}\n")

            
    prev = -1
    is_done = False
    for i in tqdm(table):
        if prev != i-1:
            print(
                f"Something wrong. Check out.log. Not all lines :(id={i})")
            break
        elif len(out[i]) != len(columns):
            print(
                f"Something wrong. Check out.log. Data inconsistant :(id={i})")
            break
        else:
            prev = i
            if prev+1 == number_of_rows:
                is_done = True

        

    if is_done:
        print("Everithing correct ")
        print("\nConverting to csv")
        file = dir+"layoffs.fyi_" + \
            str(datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"))+".csv"
        print(f"Writing to {file}")
        with open(file, 'w', newline='', encoding="utf-8") as output:
            wr = csv.writer(output, delimiter=';',
                            quoting=csv.QUOTE_ALL)
            wr.writerow(columns)
            wr.writerows(out)

        print("Done")


if __name__ == "__main__":
    scrap()
