
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
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

def extract_data(name, soup):
    try:
        return soup.find('li', text=re.compile(name)).text.replace(name, '').replace(':', '').replace('(واط)', '').strip()
    except:
        return ''

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)
urls = pd.read_excel('shareek_update_urls.xlsx')
list_urls = urls['url'].to_list()

df = pd.read_excel('shareek_product_model.xlsx')

for i, url in enumerate(list_urls):
    print('Count: ', i)
    print('URL: ', url)
    driver.get(url)
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    time.sleep(2)
    soup = BeautifulSoup(r, 'html.parser')
    
    cats = soup.find('ol', {'class': 'breadcrumb__list'}).find_all('li')
    cat1 = cats[1].text.strip()
    cat2 = cats[2].text.strip()
    
    name_1 = 'variant-mainBreakerType'
    name_2 = 'variant-noOfWays1'
    name_3 = 'variant-mainBreakerRating'
    name_4 = 'variant-ip'
    
    #select = Select(driver.find_element_by_id('variant-mainBreakerType'))
    select = Select(driver.find_element_by_id(name_1))
    select1 = Select(driver.find_element_by_id(name_2))
    select2 = Select(driver.find_element_by_id(name_3))
    select3 = Select(driver.find_element_by_id(name_4))
    list_select_value = [ option.get_attribute('value') for option in select.options[1: ]]
    list_select_value1 = [ option.get_attribute('value') for option in select1.options[1: ]]
    list_select_value2 = [ option.get_attribute('value') for option in select2.options[1: ]]
    list_select_value3 = [ option.get_attribute('value') for option in select3.options[1: ]]
    
    for value in list_select_value:
        print('Type: ', value)
        toto = driver.find_element_by_xpath(f'//select[@id="{name_1}"]//option[@value="{value}"]')
        toto.click()
        time.sleep(3)
        for value1 in list_select_value1:
            print('Number: ', value1)
            toto1 = driver.find_element_by_xpath(f'//select[@id="{name_2}"]//option[@value="{value1}"]')
            toto1.click()
            time.sleep(3)
            for value2 in list_select_value2:
                print('Power: ', value2)
                toto1 = driver.find_element_by_xpath(f'//select[@id="{name_3}"]//option[@value="{value2}"]')
                toto1.click()
                time.sleep(3)
                for value3 in list_select_value3:
                    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
                    soup = BeautifulSoup(r, 'html.parser')
                    name = soup.find('div', {'class': 'name'})
                    try:
                        sku = soup.find('h4', {'class': 'desc'}).text.strip()
                    except:
                        continue
                    name = soup.find('h4', {'class': 'desc'}).previous_element.strip().replace('', '')
                    description = soup.find('div', {'class': 'product-detail-sec'}).text.strip()
                    print('Securite: ', value3)
                    toto1 = driver.find_element_by_xpath(f'//select[@id="{name_4}"]//option[@value="{value3}"]')
                    number = soup.find('select', {'id': f'{name_4}'}).find_all('option', {'selected': 'selected'})[1].text.strip()

                    toto1.click()
                    time.sleep(3)
                    price = soup.find('p', {'class': 'price js-product-detail-price'}).text.replace("SR", '').strip()
                    try:
                        is_in_stock = soup.find('div', text=re.compile('غير متوفره')).text.strip()
                    except:
                        is_in_stock = 1
                    try:
                        base_image = 'https://shareek.alfanar.com' + soup.find('div', {'class': 'zoomImg'}).find('img')['src']
                    except:
                        base_image = ''
                        
                    brand = extract_data('العلامة التجارية', soup)
                    tech_info = soup.find_all('ul', {'class': 'product-specification__list'})[1].text.strip()
                    #
                    general_info = soup.find_all('ul', {'class': 'product-specification__list'})[0].text.strip()
                    data = {
                        'sku': sku,
                        'name': name,
                        'price': price,
                        'link_url':url,
                        'is_in_stock': is_in_stock,
                        'description': description,
                        'type_': value,
                        'number_lignes': number,
                        'brand': brand,
                        'tech_info': tech_info,
                        'general_info': general_info,
                        'amper': value2,
                        'security': value3,
                        'base_image': base_image,
                        'add_images': '',
                        'cat1': cat1,
                        'cat2': cat2,
                        'cat3': ''
                    }
                    
                    df1 = pd.DataFrame([data])
                    df = pd.concat([df, df1], ignore_index=True)
                    df.to_excel('Shareek_لوحة توزيع الفنار-test1.xlsx')
                    


# for i, url in enumerate(list_urls):
#     print('Count: ', i)
    
#     data = exctrac_data(driver, url)
#     df1 = pd.DataFrame([data])
#     df = pd.concat([df, df1], ignore_index=True)
#     df.to_excel('Shareek_لوحة توزيع الفنار-test.xlsx')
    