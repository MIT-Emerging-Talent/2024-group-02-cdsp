#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python Version: 3.12
"""
File: parcer.py
Author: Vlad421
Date: 2/4/2024
Description: collects data from layoffs.fyi using Selenium with ChromeDriver
Requirements: selenium, BeautifulSoup, html5lib

pip install selenium, bs4, html5lib

"""


import time
from datetime import datetime, timezone
import csv
import re

from tqdm import tqdm

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup


URL_prev = "https://airtable.com/appzLUHyhTU5xpkdZ/shrclnXK0pfoGjtih/tblQ0U46nsYopm2CR"
columns = ["id", "Company", "Location HQ", "# Laid Off", "Date", "%", "Industry",
           "Source", "List of emploees laid", "Stage", "$ Raised mm", "Country", "Date added"]


def scrap():

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
    time.sleep(2)

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

    regex = r"(\d{1,2}\/\d{1,2}\/\d{4})"
    refex_g_docs = r"^(https:\/\/docs.google.com)"
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

            if (len(table.get(index)) < len(columns)-1) and (text not in table[index] or re.search(regex, text) or re.search(refex_g_docs, text)):

                if text == '':
                    text = "no-data"

            # info = table.get(index)
            # if text not in info or text == "" or re.search(regex, text) or re.search(refex_g_docs, text):
                table.get(index).append(text)

        pbar.set_description("Aquired ["+str(len(table))+"] items")
        # pbar.set_description_str("Aquired - "+str(len(table))+" - lines")
        if index > last_index:
            last_index = index

            pbar.update(len(table)-prev_count)
            prev_count = len(table)

        new_pos = update_pos(
            page_height, scroll_pane_height, slider.location['y'])

        ActionChains(driver).move_to_element(slider).click_and_hold(
            slider).move_by_offset(0, new_pos).release().perform()
        time.sleep(5)

    time.sleep(2)

    del pbar

    print("Creating list..")
    out = []
    for i in table:
        line = [i]+table[i]

        out.append(line)

    with open("out.log", 'w', encoding="utf-8") as file:
        for line in out:
            file.write(f"{line}\n")
    print("Writing output to out.log")

    prev = -1
    is_done = False
    for i in table:
        if prev != i-1:
            print("Something missed")
            break
        else:
            prev = i
            if prev+1 == number_of_rows:
                is_done = True
    if is_done:
        print("Everithing correct ")
        print("\nConverting to csv")
        print("Writing to {name}", file)
        file = "layoffs.fyi_" + \
            str(datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"))+".csv"
        with open(file, 'w', newline='', encoding="utf-8") as output:
            wr = csv.writer(output, delimiter=';',
                            quoting=csv.QUOTE_NONNUMERIC)
            wr.writerow(columns)
            wr.writerows(out)

        print("Done")


if __name__ == "__main__":
    scrap()
