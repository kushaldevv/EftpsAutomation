import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

login_link = 'http://127.0.0.1:5500/'
driver = webdriver.Chrome()
driver.get(login_link)

# get this from the csv file for each company monthly report
year = '2024'
quarter = 'Q3'
settle_date = '09/11/2024'
payment_amount = '100.50'
social_security_amount = '101.50'
medicare_amount = '102.50'
federal_tax_amount = '103.50'
company_name = "AMS"

with open('company_data.json', 'r') as file:
    data = json.load(file)

company_details = data[company_name]
ein = company_details['ein']
pin = company_details['pin']
internet_password = company_details['internet_password']

print(ein, pin, internet_password)
# try:
#     ein1_input = driver.find_element(by=By.NAME, value="EIN1")
#     ein2_input = driver.find_element(by=By.NAME, value="EIN2")

#     ein1_input.send_keys(ein[:2])
#     ein2_input.send_keys(ein[2:])

#     pin_input = driver.find_element(by=By.NAME, value="PIN")
#     pin_input.send_keys(pin)

#     internet_password_input = driver.find_element(by=By.NAME, value="password")
#     internet_password_input.send_keys(internet_password)

#     login_button = driver.find_element(by=By.NAME, value="Login")
#     login_button.click()
#     # Delay to make sure the elements are loaded before we try to interact with them
#     driver.implicitly_wait(5)
#     payments_link = driver.find_element(by=By.LINK_TEXT, value="PAYMENTS")
#     payments_link.click()
#     driver.implicitly_wait(5)


#     taxform_input = driver.find_element(by=By.ID, value="TaxForm_EditField")
#     taxform_input.send_keys("941")

#     next_button = driver.find_element(by=By.NAME, value="_eventId_next")
#     next_button.click()
#     driver.implicitly_wait(5)

#     tax_radio_button = driver.find_element(By.ID, "5")
#     tax_radio_button.click()

#     next_button = driver.find_element(by=By.NAME, value="_eventId_next")
#     next_button.click()
#     driver.implicitly_wait(5)

#     amount_input = driver.find_element(by=By.ID, value="singlePayment.amount.value")
#     amount_input.send_keys(payment_amount)

#     year_input = driver.find_element(by=By.NAME, value="singlePayment.taxPeriodYear")
#     year_input.send_keys(year)

#     settle_date_input = driver.find_element(by=By.NAME, value="singlePayment.settlementDate.dateString")
#     settle_date_input.send_keys(settle_date)

#     quarter_dropdown = Select(driver.find_element(by=By.NAME, value="singlePayment.taxPeriodMonth"))
#     quarter_dropdown.select_by_visible_text(quarter)

#     next_button = driver.find_element(by=By.NAME, value="_eventId_next")
#     next_button.click()
#     driver.implicitly_wait(5)

#     social_security_amount_input = driver.find_element(by=By.NAME, value="singlePayment.subCategories[0].amount.value")
#     medicare_amount_input = driver.find_element(by=By.NAME, value="singlePayment.subCategories[1].amount.value")
#     federal_tax_amount_input = driver.find_element(by=By.NAME, value="singlePayment.subCategories[2].amount.value")

#     social_security_amount_input.send_keys(social_security_amount)
#     medicare_amount_input.send_keys(medicare_amount)
#     federal_tax_amount_input.send_keys(federal_tax_amount)

#     next_button = driver.find_element(by=By.NAME, value="_eventId_next")
#     next_button.click()
#     driver.implicitly_wait(5)
# except:
#     print("error")
#     driver.quit()
#     exit()
#     raise

# while True:
#     pass