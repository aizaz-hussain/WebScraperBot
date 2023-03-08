# Importing Libraries
import os
import csv
import time
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import urllib.request
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.request import Request, urlopen

# Search Criteria
src = ''
carModel=''
carCity=''
priceMin=''
priceMax=''


# Launching Webpage
service = Service('/usr/local/bin/chromedriver/chromedriver')
opener = urllib.request.URLopener()
opener.addheader('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
driver = webdriver.Chrome(service=service)
driver.get(f'https://www.pakwheels.com/used-cars/search/-/ct_{carCity}/pr_{priceMin}_{priceMax}/?q={carModel}')
# driver.get('https://www.pakwheels.com/used-cars/search/-/?page=500')



# Reading ADS
adContainer = driver.find_elements(By.XPATH, "//*[contains(@class, 'ad-container')]")

# Defining Variables
img_dir = f'./Images'
header = ['Ad Posted', 'Ad Id', 'Car Name', 'Car Price', 'Price Unit', 'City', 'Year', 'Distance', 'Distance Unit', 'Fuel Type', 'HP', 'Transmission', 'AD Type']
csv_filename = './data.csv'


def adDate(dt):
    _date = ''
    if 'minute' in dt or 'hour' in dt:
        _date = date.today()
    elif 'day' in dt:
        dys = int(dt.split(' ')[1])
        _date = date.today() - timedelta(days=2)
    elif 'month' in dt:
        dys = int(dt.split(' ')[1])
        _date = date.today() - relativedelta(months=2)
    elif 'year' in dt:
        dys = int(dt.split(' ')[1])
        _date = date.today() - relativedelta(years=2)
    return _date


flag_header = 0

# Check if rows are present in the csv files
if os.path.exists(csv_filename):
    with open(csv_filename, mode='r', newline='') as file:
        row_count = list(csv.reader(file))
        if len(row_count) > 0:
            flag_header = 1

# Open csv for writing the data
with open(csv_filename, 'a', newline='') as file:
    writer = csv.writer(file)
    if flag_header == 0:
        writer.writerow(header)  # Writing header if there are no rows

    # Traversing through each AD to scrape data
    for idx in range(1, len(adContainer)):
        count = 0
        adId = adContainer[idx].find_element(By.CLASS_NAME, "car-name")
        adId = adId.get_attribute('href').split('-')[-1]

        # Storing Vehicle Information
        carName = adContainer[idx].find_element(By.CLASS_NAME, "car-name").text

        # Price Details
        carPrice = adContainer[idx].find_element(By.CLASS_NAME, "price-details").text
        _price = ''
        _unit = ''

        if carPrice != 'Call':
            _price = carPrice.split(' ')[1]
            _unit = carPrice.split(' ')[2]

        carCity = adContainer[idx].find_element(By.CLASS_NAME, "search-vehicle-info").text
        carInfo = adContainer[idx].find_element(By.CLASS_NAME, "search-vehicle-info-2")
        li = carInfo.find_elements(By.TAG_NAME, "li")
        year = li[0].text

        dist = li[1].text.replace(',', '')
        _dist = dist.split(' ')[0]
        _distunit = dist.split(' ')[1]

        fuel = li[2].text
        hp = li[3].text
        transmission = li[4].text
        adPosted = adDate(adContainer[idx].find_element(By.CLASS_NAME, "dated").text)

        adType = ''
        if adContainer[idx].text.find("FEATURED") > -1:
            adType = "FEATURED"
        else:
            adType = "NORMAL"

        # Storing Image Information
        img_gallery = adContainer[idx].find_element(By.CLASS_NAME, "image-gallery");
        img_src = img_gallery.get_attribute('data-galleryinfo')
        img_src = img_src.replace('[', '')
        img_src = img_src.replace(']', '')
        img_list = img_src.split(',')

        for idx in range(len(img_list)):
            if '"src":"' in img_list[idx]:
                src = img_list[idx].split('":"')[1].replace('"', '')
                img_dir = f'./Images/{src.split("/")[-2]}/'
                img_name = f'{src.split("/")[-2]}_{count}.webp'

                if not os.path.exists(img_dir):
                    os.mkdir(img_dir)

                count += 1
                filename, headers = opener.retrieve(src, img_dir + img_name)

        writer.writerow(
            [adPosted, adId, carName, _price, _unit, carCity, year, _dist, _distunit, fuel, hp, transmission, adType])