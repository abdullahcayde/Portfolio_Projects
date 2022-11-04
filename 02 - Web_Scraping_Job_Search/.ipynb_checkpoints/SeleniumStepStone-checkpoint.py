import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

'''
Title : Web Scrapping by Selenium 
Project Purpose: From StepStone scrap data for some Job Titels
1 - Create Driver
2 - Go to Website
3 - Create ActionChain Object
    3.1 - Click Banned Accept
4 - Take Title and Infos from Page
    4.1 - Create Lists 
    4.2 - Create DataFrame
    4.3 - Repeat Process
    4.4 - Print and Save DataFrame
'''

print('---------------------- StepStone Job Searching Selenium Project ----------------------')
def sleep(x):
    time.sleep(x)
def wait(x):
    driver.implicitly_wait(x)

start=datetime.now()  
# 0 Link Descriptions
link_original = 'https://www.stepstone.de/jobs/data-analyst/in-rietberg?radius=50&page=2'

job_name = 'Data Analyst'
ort_ = 'Rietberg'
radius = 50
page_number = 1

#  1 - Create Driver
Path = '/Users/macbook/Desktop/projects/Github_Repositories/Portfolio Projects/02 - Web_Scraping_Job_Search/chromedriver'
driver = webdriver.Chrome(Path)

#  2 - Go to Website
job_link = job_name.replace(' ', '-').lower()
ort_link = ort_.lower()
link = f'https://www.stepstone.de/jobs/{job_link}/in-{ort_link}?radius={radius}&page={page_number}'

driver.get(link)
wait(10)
sleep(2)

#  3 - ActionChain Object created
# 3.1 - Click Banned Accept
actions = ActionChains(driver)
akzeptieren = driver.find_element(By.ID, 'ccmgt_explicit_accept')
actions.click(akzeptieren).perform()
wait(10)
sleep(0.5)

# 4 -  Take Infos from Page
# Headers, Company, City, Description
header = driver.find_elements(By.CLASS_NAME, 'resultlist-12iu5pk')
publish = driver.find_elements(By.CLASS_NAME, 'resultlist-3asi6i')
company = driver.find_elements(By.CLASS_NAME, 'resultlist-1v262t5')
ort = driver.find_elements(By.CLASS_NAME, 'resultlist-dettfq') #resultlist-53y8on
description = driver.find_elements(By.CLASS_NAME, 'resultlist-1pq4x2u')
result = driver.find_elements(By.CLASS_NAME, 'resultlist-xeyevn')


# 4.1 -
list_header = [title.text for title in header]
list_publish = [pub.text for pub in publish]
list_company = [comp.text for comp in company]
list_ort = [o.text for o in ort]
list_description = [des.text for des in description]

# Total Search Page Number
list_result = [res.text for res in result]
number_of_page = int(list_result[0].split(' ')[-1])
print(f'Number of Jobs Pages = {number_of_page}')

# 4.2 - DataFrame df
d = {'job_title':list_header, 'publish':list_publish, 'company_name' : list_company, 'city':list_ort , 'Description':list_description}
df = pd.DataFrame(d)
dff = df.head(2)
print(dff)

# 4.3 Repeat Process for every Web Page
while  page_number < number_of_page:
    page_number+=1
    
    link = f'https://www.stepstone.de/jobs/{job_link}/in-{ort_link}?radius={radius}&page={page_number}'
    driver.get(link)
    wait(10)
    sleep(1.5)
    # Headers, City , Description
    header = driver.find_elements(By.CLASS_NAME, 'resultlist-12iu5pk')
    publish = driver.find_elements(By.CLASS_NAME, 'resultlist-3asi6i')
    company = driver.find_elements(By.CLASS_NAME, 'resultlist-1v262t5')
    ort = driver.find_elements(By.CLASS_NAME, 'resultlist-dettfq')
    description = driver.find_elements(By.CLASS_NAME, 'resultlist-1pq4x2u')

    # 4 -  Headers List
    # 4.1 -
    list_header = [title.text for title in header]
    list_publish = [pub.text for pub in publish]
    list_company = [comp.text for comp in company]
    list_ort = [o.text for o in ort]
    list_description = [des.text for des in description]
    
    d = {'job_title':list_header, 'publish':list_publish, 'company_name' : list_company, 'city':list_ort , 'Description':list_description}
    df2 = pd.DataFrame(d)
    print(f'Page Number : {page_number} , DataFrame shape : {df2.shape}')
    df = pd.concat([df,df2], axis=0, ignore_index=True)
    

# 4.4 Save Data as csv and xlsx    
print(f'DataFrame End : {df.shape}')
# 4.3 - Save DataFrame
# 4.3.1 - to csv
df.to_csv(f'stepstone-{job_link}.csv')

# 4.3.2 - to excel
# install openpyxl
df.to_excel(f'stepstone-{job_link}.xlsx', sheet_name='Sheet1')

end =datetime.now() 
print('Code Runned No Problem')
print(f'Time = {end - start}')
sleep(10)
driver.quit()