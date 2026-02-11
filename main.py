from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)
data = []
driver.get("https://books.toscrape.com/")

def find_by_name(name):
    mystery_button = driver.find_element(By.PARTIAL_LINK_TEXT, name)
    mystery_button.click()
    time.sleep(2)
    try:
        page_count = driver.find_element(By.CLASS_NAME, "current").text
        page_count = int(page_count[-1])
    except NoSuchElementException:
        page_count = 1
    count = 0
    for i in range(page_count):
        ol = driver.find_element(By.TAG_NAME, "ol")
        table = ol.find_elements(By.TAG_NAME, "li")
        for item in table:
            count+=1
            name = item.find_element(By.TAG_NAME,"h3" ).text
            price = item.find_element(By.CLASS_NAME,"price_color").text
            row = {'Name':name,'Price':price}
            data.append(row)
        if i!=page_count-1:
            next = driver.find_element(By.PARTIAL_LINK_TEXT, "next")
            next.click()
    print(count)
    df=pd.DataFrame(data)
    df.to_excel('empty_excel_file.xlsx', index=False)
find_by_name("Sequential Art")
print(data)
time.sleep(1000)

