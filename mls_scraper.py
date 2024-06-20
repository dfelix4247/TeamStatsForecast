from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time

def scrape_data(category_xpath, output_csv):
    category_dropdown = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, category_xpath)))
    category_dropdown.click()

    df = pd.DataFrame()

    while True:
        try:
            time.sleep(5)
            table_html = driver.find_element(By.CLASS_NAME, "mls-o-table").get_attribute('outerHTML')
            df_temp = pd.read_html(table_html)[0]
            print(df_temp)
            df = pd.concat([df_temp, df], ignore_index=True)
            print(df)
            next_button = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/main/section[2]/div/div[1]/section/div/div[5]/div/button[2]")))
            driver.execute_script("arguments[0].click();", next_button)
        except:
            break

    df.to_csv(output_csv, encoding='utf-8', index=False)

driver = webdriver.Chrome()
driver.get('https://www.mlssoccer.com/players/darlington-nagbe/match-log/')

scrape_data("//*[@id='main-content']/section[2]/div/div[1]/section/div/div[3]/select[2]/option[4]", "player_stats_def.csv")
scrape_data("//*[@id='main-content']/section[2]/div/div[1]/section/div/div[3]/select[2]/option[3]", "player_stats_att.csv")
scrape_data("//*[@id='main-content']/section[2]/div/div[1]/section/div/div[3]/select[2]/option[1]", "player_stats_gen.csv")

driver.quit()
