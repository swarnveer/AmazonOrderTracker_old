from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd

orders_df = pd.DataFrame(columns=["OrderDate","Amount"])

def get_order_details(driver):
    global orders_df
    driver.implicitly_wait(5)
    ordersContainer = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.ID, 'ordersContainer')))
    individual_orders = ordersContainer.find_elements(By.CLASS_NAME, 'order')
    for order in individual_orders:
        order_date = order.find_element(By.XPATH, 'div[1]/div/div/div/div[1]/div/div[1]/div[2]/span').text
        order_value = order.find_element(By.XPATH, 'div[1]/div/div/div/div[1]/div/div[2]/div[2]/span/span').text
        orders_df = orders_df.append({"OrderDate": order_date, "Amount": float(order_value.strip().replace(',',''))},ignore_index=True)
def get_order_list(driver):
    try:
        element = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.ID, 'yourOrders')))
    except Exception:
        driver.quit()
    order_years_list_id = driver.find_element(By.ID,'orderFilter')
    order_years = order_years_list_id.find_elements(By.TAG_NAME, 'option')
    years=[year.text for year in order_years if(len(year.text)==4)]

    for year in years:
        order_years_list_id = driver.find_element(By.ID,'orderFilter')
        select = Select(order_years_list_id)
        select.select_by_visible_text(year)
        get_order_details(driver)
        while True:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, 'html/body/div[1]/div[2]/div[1]/div[5]/div[12]/div/ul/li[12]/a'))).click()
                get_order_details(driver)
            except Exception:
                break
    print(orders_df)
    orders_df.to_excel("Amazon.xlsx", index=False)
