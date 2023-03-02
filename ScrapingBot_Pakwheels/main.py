import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


service = Service('/usr/local/bin/chromedriver/chromedriver')
driver = webdriver.Chrome(service=service)


# Edit the software using JSON
carModel='Civic Rebirth'
carCity=''
priceMin=''
priceMax=''


driver.get(f'https://www.pakwheels.com/used-cars/search/-/ct_{carCity}/pr_{priceMin}_{priceMax}/?q={carModel}')


adContainer = driver.find_elements(By.XPATH, "//*[contains(@class, 'ad-container')]")

# carTitle = driver.find_elements(by=By.CLASS_NAME, value='car-name')
# carCity = driver.find_elements(by=By.CLASS_NAME, value='search-vehicle-info')
# carInfo = driver.find_elements(By.XPATH, "//*[contains(@class, 'search-vehicle-info-2')]")



for idx in range(len(adContainer)):

    # saving image to local dir
    adcontainer = adContainer[idx].find_element(By.XPATH, "//*[contains(@class, 'image-gallery')]")
    tag_class = adcontainer.get_attribute('data-galleryinfo')
    tag_class = tag_class.replace('[','')
    tag_class = tag_class.replace(']','')
    galleryinfo_list=tag_class.split(',')
    print(galleryinfo_list)

    break




# for idx in range(len(adContainer)):
#
#     print('AD Posted Date')
#     print(f'Car: {carTitle[idx].text},\t City: {carCity[idx].text}')
#     child_elements = carInfo[idx].find_elements(By.XPATH, ".//li")
#     print('Year:\t', child_elements[0].text)
#     print('KM:\t', child_elements[1].text)
#     print('Fuel Type:\t', child_elements[2].text)
#     print('Horsepower:\t', child_elements[3].text)
#     print('Car Type:\t', child_elements[4].text)
#
#     print('\n\n')
#     break



# time.sleep(10000)