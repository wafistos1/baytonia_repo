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
import re
from selenium.webdriver.support.ui import Select
from dataclasses import dataclass, field

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)
driver.get('https://canvasy.net/product-category/%d9%84%d9%88%d8%ad%d8%a7%d8%aa-%d8%a7%d8%b2%d9%87%d8%a7%d8%b1/page/9/')
urls = []
r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
soup = BeautifulSoup(r, "html.parser")
time.sleep(1)
products = soup.find_all('a', {'class': 'product-image-link'})
print(len(products))
liens = [toto['href']  for toto in products]
urls += liens


def scrap_product(driver, prozes=None, size=None):
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    name = soup.find('h1',{'class': 'product_title entry-title wd-entities-title'}).text.strip()
    try:
        prices = soup.find('div', {'class': 'single_variation_wrap'}).find_all('span', {'class': 'woocommerce-Price-amount amount'})
        try:
            price = prices[0].text.replace('ر.س', '').strip()
            special_price = prices[1].text.replace('ر.س', '').strip()
        except:
            price = prices[0].text.replace('ر.س', '').strip()
            special_price = ''
    except: 
        price =''
        special_price = ''
    description = soup.find('div', {'class': 'woocommerce-product-details__short-description'}).text.strip()
    cat1 = soup.find('a', {'class': 'breadcrumb-link breadcrumb-link-last'}).text.strip()
    sku = soup.find('span', {'class', 'sku'}).text.strip()
    try:
        qty = soup.find('p', {'class': 'stock in-stock'}).text.replace('متوفر في المخزون', '').strip()
    except:
        qty = ''
    time.sleep(1)
    images = soup.find_all('div', {'class': 'product-image-thumbnail'})
    len(images)
    list_images = [img.find('img')['src'].replace('-300x300', '') for img in images]
    base_image = list_images[0]
    add_images = ','.join(list_images[1:])

    configurable_variations = ''
    if size and prozes:
        additional_attributes = f'painting_available_sizes={size},frame_colors = {prozes}'
        product_type = 'simple'
        toto = f'sku={sku}, painting_available_sizes={size},frame_colors = {prozes}'
        visibility = 'Not visible individually'  
    else:
        additional_attributes = ''
        product_type = 'configurable'
        toto = ''
        visibility = 'Catalog, Search'
        
    attribute_set_code = 'sizescolors'
    meta_description = description
    
    data = {
        'sku': sku,
        'name': name,
        'price': price,
        'special_price': special_price,
        'weight': 5,
        'link_url': driver.current_url,
        'qty': qty,
        'prozes': prozes,
        'size': size,
        'toto': toto,
        'product_type': product_type,
        'additional_attributes': additional_attributes,
        'attribute_set_code': attribute_set_code,
        'visibility': visibility,
        'description': description,
        'meta_description': meta_description,
        'base_image': base_image,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': '',
        
    }
    return data

df = pd.read_excel('cancasy_product_model.xlsx')
def try_except(name):
        try:
            return name.first_selected_option.text
        except:
            return None

        
for i, url in enumerate(urls):
    print('Count: ', i)
    print('URL: ', url)
    driver.get(url)
    time.sleep(1)
    prozes = driver.find_elements_by_xpath('//table[@class="variations"]//ul[@class="variable-items-wrapper image-variable-wrapper"]//li')
    
    
    #select = Select(driver.find_element_by_id('pa_retsting'))
    count = len(prozes)
    list_configurable = []
    for t in prozes:
        time.sleep(1)
        t.click()
        print('Dans le prozes')
        proz = t.find_element_by_tag_name('img').get_attribute('alt')
        print('prozes', t.find_element_by_tag_name('img').get_attribute('alt'))
        sizes1 = driver.find_elements_by_xpath('//table[@class="variations"]//select')
        sizes_id = sizes1[1].get_attribute('id')
        sizes = driver.find_elements_by_xpath(f'//select[@id="{sizes_id}"]//option')
        select = Select(driver.find_element_by_id(sizes_id))
        for i in range(1, len(sizes)):
            time.sleep(1)
            select.select_by_index(i)
            size =try_except(select)
            print('Size: ', size)
            data = scrap_product(driver, prozes=proz, size=size)
            list_configurable.append(data['toto'])
            df1 = pd.DataFrame([data])
            df = pd.concat([df, df1], ignore_index=True)
            df.to_excel('cancasy_product_update.xlsx')
    driver.get(url)
    time.sleep(2)
    data = scrap_product(driver)
    data['configurable_variations'] = ','.join(list_configurable)
    list_configurable = []
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('cancasy_product_update.xlsx')
