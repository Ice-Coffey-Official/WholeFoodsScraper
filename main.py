from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from typing import List
from config import config
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


edge_options = Options()
edge_options.add_argument("ms:inPrivate")
edge_options.add_argument("headless")
edge_options.add_argument("disable-gpu")
driver = webdriver.Edge(options=edge_options)
BaseUrl = "https://www.wholefoodsmarket.com/stores"

configuration = config()

states: List[str] = configuration.getStates()

locations = []
output = [['Store Name', 'Store Number', 'Phone Number', 'Address', 'Url', 'Longitude', 'Latitude', 'City', 'State']]

page = driver.get(BaseUrl)
timeout = 3

for i in tqdm(range(len(states))):
    state = states[i]
    time.sleep(configuration.getBackoff() + configuration.getVariableBackoff())
    search_bar = driver.find_element(by=By.XPATH, value='//*[@id="store-finder-search-bar"]')
    search_bar.send_keys(state)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(1)
    element_present = EC.presence_of_element_located((By.CLASS_NAME, "w-store-finder-store-name"))
    try:
        WebDriverWait(driver, timeout).until(element_present)
    except:
        pass
    stores = driver.find_elements(by=By.CLASS_NAME, value="w-store-finder-store-name")
    for s in stores:
        link = s.find_element(by=By.TAG_NAME, value="a").get_attribute('href')
        locations.append(link)
    search_bar.clear()

driver.close()

for j in tqdm(range(len(locations))):
    location = locations[j]
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
        'referer':'https://www.google.com/'
    }
    try:
        page = requests.get(location, headers=header)
    except:
        try:
            time.sleep(configuration.getBackoff() + configuration.getVariableBackoff())
            page = requests.get(location, headers=header)
        except:
            continue

    soup = BeautifulSoup(page.text, 'lxml')

    storeNum = ''
    cityName = location.split('/')[-1].strip()

    try:
        state = soup.find("span", { "class" : "w-mailing-address-section--description-last" }).text.split(' ')[-2]
    except:
        state = ''

    try:
        name = soup.find("h1", { "class" : "w-core-info__name w-fs-hero2" }).text.strip()
    except Exception as e:
        name = ''

    try:
        phoneNumber = soup.find("a", { "class" : "w-phone-number--link"}).text
    except Exception as e:
        phoneNumber = ''

    try:
        address1 = soup.find("span", { "class" : "w-mailing-address-section--description-first"}).text
        address2 = soup.find("span", { "class" : "w-mailing-address-section--description-last"}).text
        address = "{} {}".format(address1, address2)
    except Exception as e:
        address = ''

    try:
        coords = soup.find("script", { "type" : "application/ld+json"}).text
        latitude = coords.split('"latitude": "')[-1][:11].strip().strip(',').strip('"')
        longitude = coords.split('"longitude": "')[-1][:11].strip().strip(',').strip('"')
    except Exception as e:
        latitude = ''
        longitude = ''

    output.append([name, storeNum, phoneNumber, address, location, longitude, latitude, cityName, state])


print('Saving...')
df = pd.DataFrame(output[1:],columns=output[0])

if('csv' in configuration.getSaveAs()):
    df.to_csv('{data}.csv'.format(data = configuration.getSavePath()), index=False)
if('excel' in configuration.getSaveAs()):
    df.to_excel("{data}.xlsx".format(data = configuration.getSavePath()), index=False)
