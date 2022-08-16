
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
import os
from fake_useragent import UserAgent
from random import randint
import pandas as pd
import numpy as np
import requests
import pandas as pd
import re, logging


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


urls = pd.read_excel('path excel url file')
list_urls = []
for index, row in urls.iterrows():
    list_urls.append(
        {
            'url': row['url'],
            'categories1': row['categories1'],
            'categories2': row['categories2'],
            'categories3': row['categories3'],
        }
    )


def scrape_data(url):
    data = {
        
    }
    return data

for i, url in enumerate(urls):
    logging.info('--Count: %s', i)
    data = scrape_data(url)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel()
