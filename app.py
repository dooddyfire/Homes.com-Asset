import requests
from bs4 import BeautifulSoup 
import datetime
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
#Fix
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


export_url = []
export_sell_date = []
export_price = []
export_image = []
export_url = []
export_propname = []
export_address = []
export_agentname = []
export_membername = []
export_email = []
export_phone = []
export_zip = []
export_close = []
export_about = []

main_url = 'https://www.homes.com/reading-ma/'

driver = webdriver.Chrome()

driver.get(main_url)

input('Enter if ready : ')

url_lis = [ x.find_element(By.CSS_SELECTOR,'a').get_attribute('href') for x in driver.find_elements(By.CSS_SELECTOR,'li.placard-container')]

for i in url_lis[:10]:

    url = i
    driver.get(url)

    soup = BeautifulSoup(driver.page_source,'html.parser')

    lis_script = [ x.get_attribute('innerHTML') for x in driver.find_elements(By.CSS_SELECTOR,'script[type="application/ld+json"]')]

    prop_src = lis_script[0]
    agent_src = lis_script[1]

    try:
        propname = driver.find_element(By.CSS_SELECTOR,'div.property-info-address').text 
    except:
        propname = '-'
    export_propname.append(propname)
    print(propname)

    try:
        price = driver.find_element(By.CSS_SELECTOR,'span.property-info-price').text 
    except:
        price = '-'
    print(price)
    export_price.append(price)

    try:
        sell_date = driver.find_element(By.CSS_SELECTOR,'div.property-info-status-pill-container').text 
    except:
        sell_date = '-'
    print(sell_date)
    export_sell_date.append(sell_date)

    try:
        prop_json = json.loads(prop_src)
        x = prop_json
        print(prop_json)

        url = x['url']
        image = x['image']
        offer = x[ 'offers']
        ent = x['mainEntity']['address']

        zip_code = ent['postalCode']
        street_address = ent['streetAddress']

    except:
        image = '-'
        zip_code = '-'
        street_address = '-'    

    print('Street Address : ',ent['streetAddress'])
    print('Zip Code : ',ent['postalCode'])
    
    export_image.append(image)
    export_zip.append(zip_code)
    export_address.append(street_address)
    
    try:
        y = json.loads(agent_src)

        agent_url = y['url']

        print(y)
        member = y['memberOf']
        
        try:
            name = member['name']
        except: 
            name = '-'

        try:
            agent_name = y['name']
        except:
            agent_name = '-'

        try:
            phone = y['telephone']
        except:
            phone = '-'

        try:
            email = y['email']
        except:
            email = member['email']




    except:
        name = '-'
        phone = '-'
        email = '-'
        agent_name = '-'

    
    driver.get(agent_url)

    try:
        close = [ g.text for g in driver.find_elements(By.CSS_SELECTOR,'.stat-item')][0]
    except:
        close = '-'

    try:
        about = driver.find_element(By.CSS_SELECTOR,'article.adp-bio-container').text 

    except:
        about = '-'

    print('Name : ',name)
    print('Phone : ',phone)
    print('Email : ',email)
    print('Agent Name : ',agent_name)
    print('Close : ',close)
    print('About : ',about)


    export_membername.append(name)
    export_agentname.append(agent_name)
    export_phone.append(phone)
    export_email.append(email)
    export_close.append(close)
    export_about.append(about)

if __name__ == '__main__': 

    df = pd.DataFrame()
    df['Property Title'] = export_propname 
    df['Url'] = url_lis[:10]
    df['Image'] = export_image
    df['Price'] = export_price
    df['Sell Date'] = export_sell_date
    df['Address'] = export_address
    df['Agent'] = export_agentname
    df['Address'] = export_address 
    df['Seller Name'] =  export_membername
    df['Email'] = export_email 
    df['Phone'] = export_phone 
    df['About'] = export_about 
    df['Close'] = export_close

    df.to_excel('testloadsell.xlsx')

    print('Finish ...')
