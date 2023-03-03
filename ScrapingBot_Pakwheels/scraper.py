import time
import os
import urllib.request
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.request import Request, urlopen


src = ''
carModel='Civic Rebirth'
carCity=''
priceMin=''
priceMax=''



service = Service('/usr/local/bin/chromedriver/chromedriver')
opener = urllib.request.URLopener()
opener.addheader('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
driver = webdriver.Chrome(service=service)
driver.get(f'https://www.pakwheels.com/used-cars/search/-/ct_{carCity}/pr_{priceMin}_{priceMax}/?q={carModel}')

adContainer = driver.find_elements(By.XPATH, "//*[contains(@class, 'ad-container')]")
img_dir = f'/home/aizazhussain/PycharmProjects/WebScraperBot/ScrapingBot_Pakwheels/Images/'

for idx in range(1, len(adContainer)):

    count = 0

    img_gallery = adContainer[idx].find_element(By.CLASS_NAME, "image-gallery");
    img_src = img_gallery.get_attribute('data-galleryinfo')
    img_src = img_src.replace('[', '')
    img_src = img_src.replace(']', '')
    img_list = img_src.split(',')

    for idx in range(len(img_list)):
        if 'src' in img_list[idx]:
            src = img_list[idx].split('":"')[1].replace('"', '')
            img_dir = f'/home/aizazhussain/PycharmProjects/WebScraperBot/ScrapingBot_Pakwheels/Images/{src.split("/")[-2]}/'
            img_name = f'{src.split("/")[-2]}_{count}.webp'

            if not os.path.exists(img_dir):
                os.mkdir(img_dir)

            count += 1
            filename, headers = opener.retrieve(src, img_dir + img_name)







