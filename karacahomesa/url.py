
import time
import os
import requests
import re, logging
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
from random import randint
import pandas as pd
import numpy as np

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

options = Options()
ua = UserAgent()
userAgent = ua.random
logging.info(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)



list_urls = [
    {'cat1': 'مفارش', 'cat2': 'مفارش مواليد', 'cat3': 'بطانيات مواليد', 'url': 'https://karacahomesa.com/category/yyPXP'},
    {'cat1': 'مفارش', 'cat2': 'مفارش مواليد', 'cat3': 'مفارش مواليد', 'url': 'https://karacahomesa.com/category/lzmEa'},
    {'cat1': 'مفارش', 'cat2': 'مفارش أطفال', 'cat3': '', 'url': 'https://karacahomesa.com/category/DYmNj'},
    {'cat1': 'مفارش', 'cat2': 'مفارش مفرد', 'cat3': '', 'url': 'https://karacahomesa.com/category/xWgqa'},
    {'cat1': 'مفارش', 'cat2': 'مفارش مزدوج', 'cat3': 'مفارش مزدوج كوين', 'url': 'https://karacahomesa.com/category/rXPZy'},
    {'cat1': 'مفارش', 'cat2': 'مفارش مزدوج', 'cat3': 'مفارش مزدوج كينج', 'url': 'https://karacahomesa.com/category/KvQzq'},
    {'cat1': 'مفارش', 'cat2': 'مفارش مزدوج', 'cat3': 'مفارش مزدوج سوبر كينج', 'url': 'https://karacahomesa.com/category/aRYZn'},
    {'cat1': 'مفارش', 'cat2': 'مفارش عرائس', 'cat3': '', 'url': 'https://karacahomesa.com/category/AxOwe'},
    {'cat1': 'مفارش', 'cat2': 'بطانيات ولحافات', 'cat3': 'لحافات خفيفة', 'url': 'https://karacahomesa.com/category/eorKO'},
    {'cat1': 'مفارش', 'cat2': 'بطانيات ولحافات', 'cat3': 'لحافات قطنية', 'url': 'https://karacahomesa.com/category/Xobrw'},
    {'cat1': 'مفارش', 'cat2': 'بطانيات ولحافات', 'cat3': 'بطانيات شتوية', 'url': 'https://karacahomesa.com/category/qNgWN'},
    {'cat1': 'مفارش', 'cat2': 'بطانيات ولحافات', 'cat3': 'أطقم لحافات', 'url': 'https://karacahomesa.com/category/zXzaG'},
    {'cat1': 'مفارش', 'cat2': 'إكسسوارات السرير', 'cat3': 'مخدات', 'url': 'https://karacahomesa.com/category/xNqzY'},
    {'cat1': 'مفارش', 'cat2': 'إكسسوارات السرير', 'cat3': 'شراشف', 'url': 'https://karacahomesa.com/category/aoXgZ'},
    {'cat1': 'مفارش', 'cat2': 'إكسسوارات السرير', 'cat3': 'حشوات لحافات', 'url': 'https://karacahomesa.com/category/bGzXX'},
    {'cat1': 'مفارش', 'cat2': 'إكسسوارات السرير', 'cat3': 'لبادات و واقيات مراتب', 'url': 'https://karacahomesa.com/category/OeABw'},
    #
    # {'cat1': '', 'cat2': '', 'cat3': '', 'url': ''},
    # {'cat1': '', 'cat2': '', 'cat3': '', 'url': ''},
    # {'cat1': '', 'cat2': '', 'cat3': '', 'url': ''},
    # {'cat1': '', 'cat2': '', 'cat3': '', 'url': ''},
]





def get_data(url, driver, count):
    logging.info('URL: %s', url)
    url = url + f'?page={count}'
    driver.get(url)
    body=WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
    r = body.get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class': 'product'})
    liens = [toto.find('a')['href']  for toto in products]
    logging.info('Len products', len(liens))
    return liens

def scrap_url_product(url1):
    
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    count = 1
    while True:
        urls_list = get_data(url, driver, count)
        if len(urls_list) == 0:
            break
        for toto in urls_list:
            data.append({
            'url':toto,
            'cat1': cat1,
            'cat2': cat2,
            'cat3': cat3,
            })

        count += 1
        url = url.split('?')[0]
    logging.info( 'Scrape Categorie Done --> Next .')
    return data
df = pd.read_excel('karacahomesa_url_model.xlsx')   
for i, url in enumerate(list_urls):
    logging.info('Count: %s', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('karacahomesa_url_update.xlsx')
logging.info('Scraping URL Done.')

