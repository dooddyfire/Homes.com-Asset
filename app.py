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

export_trans = []
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
export_active = []
export_lname = []
export_fname = []
total_view_lis = []
city_lis = []
zipcode_lis = []
agency_name_lis = []

url_lis = []

main_url = 'https://www.homes.com/reading-ma/'

driver = webdriver.Chrome()

driver.get(main_url)

input('Enter if ready : ')
start_page = int(input('Enter Start Page : '))
end_page = int(input('Enter End Page : '))

# start_page = 1
# end_page = 1

for page in range(abs(end_page - start_page+1)):

    url_page = main_url+f"/p{page}"
    all_lis =  [ x.find_element(By.CSS_SELECTOR,'a').get_attribute('href') for x in driver.find_elements(By.CSS_SELECTOR,'li.placard-container')]
    print('Page : {} : {}'.format(page,len(all_lis)))

    for link in all_lis:
        url_lis.append(link)
    
    try:
        next_btn = driver.find_element(By.CSS_SELECTOR,'button.next')
        next_btn.click()
        # หน่วง 2 วิ
        time.sleep(2)
    except:
        print('ไม่มีหน้าต่อไป')

#url_lis = [ x.find_element(By.CSS_SELECTOR,'a').get_attribute('href') for x in driver.find_elements(By.CSS_SELECTOR,'li.placard-container')]

print('URL LIS : ',len(url_lis))

for i in url_lis:

    url = i
    driver.get(url)

    soup = BeautifulSoup(driver.page_source,'html.parser')

    lis_script = [ x.get_attribute('innerHTML') for x in driver.find_elements(By.CSS_SELECTOR,'script[type="application/ld+json"]')]

    prop_src = lis_script[0]
    agent_src = lis_script[1]

    try: 
        total_view = driver.find_element(By.CSS_SELECTOR,'div.property-info-total-views').text.replace('Total Views','')
    except:
        total_view = 0 
    
    print('Total View : ',total_view)
    total_view_lis.append(total_view)

    try: 
        mainshort_address = [ x.text for x in driver.find_element(By.CSS_SELECTOR,'span.property-info-address-citystatezip').find_elements(By.CSS_SELECTOR,'a')]
    except:
        mainshort_address = '-'

    try:
        city = mainshort_address[0]
    except:
        city = '-'

    try:
        zipcode =  mainshort_address[1]
    except:
        zipcode = '-'

    city_lis.append(city)
    zipcode_lis.append(zipcode)

    try:
        agency_name = driver.find_element(By.CSS_SELECTOR,'div.agent-agency-name').text
        
    except:
        agency_name = '-'
    agency_name_lis.append(agency_name)

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

    try: 
        agent_name2 = driver.find_element(By.CSS_SELECTOR,'div.name-container').text 
    except:
        agent_name2 = '-'

    try:
        history = driver.find_element(By.CSS_SELECTOR,'div#transaction-history-panels').text

    except:
        history = '-'

    #agent_name no use -> agent_name2
    try:
        active_listing_lis = len(driver.find_elements(By.CSS_SELECTOR,'a.active-listing-placard-link'))
    except:
        active_listing_lis = 0
    

    print('Name : ',agent_name)
    print('Agent Name Page 2 : ',agent_name2)
    print('Histoy Transact : ',history)
    print('Phone : ',phone)
    print('Email : ',email)
    print('Agent Name : ',agent_name2)
    print('Close : ',close)
    print('About : ',about)
    print('Total Active Listing : ',active_listing_lis)

    try:
        fname = agent_name2.split()[0]
    except:
        fname = '-'
    

    try:    
        lname = agent_name2.split()[-1]
    except:
        lname = '-'

    export_fname.append(fname)
    export_lname.append(lname)

    export_membername.append(agent_name2)
    export_agentname.append(name)
    export_phone.append(phone)
    export_email.append(email)
    export_close.append(close)
    export_about.append(about)
    export_trans.append(history)
    export_active.append(active_listing_lis)

if __name__ == '__main__': 

    df = pd.DataFrame()
    df['Property Title'] = export_propname 
    df['Url'] = url_lis
    df['Image'] = export_image
    df['Price'] = export_price
    df['Sell Date'] = export_sell_date
    df['Address'] = export_address
    df['Zip Code'] = zipcode_lis 
    df['City'] = city_lis 
    df['Agent'] = agency_name_lis
    df['Address'] = export_address 
    df['Seller Name'] =  export_membername
    df['Firstname'] = export_fname 
    df['Lastname'] = export_lname
    df['Email'] = export_email 
    df['Phone'] = export_phone 
    df['About'] = export_about 
    df['Transaction History'] = export_trans
    df['Active Listing'] = export_active
    df['Total View'] = total_view_lis
    df['Close'] = export_close

    df.to_excel('testloadsell.xlsx')

    print('Finish ...')
