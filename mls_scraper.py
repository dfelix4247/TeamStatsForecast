from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait 
import pandas as pd
import time

# change url and csv year as needed

driver = webdriver.Chrome()
driver.get('https://www.mlssoccer.com/stats/players/#season=2020&competition=mls-regular-season&club=all&statType=general&position=all')
df2 = pd.DataFrame()

while True:
    try:
        time.sleep(5)  
        table_html = driver.find_element(By.CLASS_NAME, "mls-o-table").get_attribute('outerHTML')
        df = pd.read_html(table_html)[0]
        print(df)
        df2 = pd.concat([df,df2], ignore_index=True)
        print(df2)
        element = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main-content']/section/div/div[2]/div[2]/div/button[2]")))
        driver.execute_script("arguments[0].click();", element)
    except:
        break
    df2.to_csv("mls_2020.csv", encoding='utf-8',index=False)



