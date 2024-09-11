from dataclasses import dataclass
from datetime import datetime
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
import tkinter as tk
import os

@dataclass(frozen=True)
class PaymentInfo:
    name: str
    ein: str
    pin: str
    internet_password: str
    year: str
    quarter: str
    payment_amount: str
    social_security_amount: str
    medicare_amount: str
    federal_tax_amount: str


def on_click(payment_info, settle_date):
    login_link = 'http://127.0.0.1:5500/'
    driver = webdriver.Chrome()
    driver.get(login_link)

    try:
        ein1_input = driver.find_element(by=By.NAME, value="EIN1")
        ein2_input = driver.find_element(by=By.NAME, value="EIN2")

        ein1_input.send_keys(payment_info.ein[:2])
        ein2_input.send_keys(payment_info.ein[2:])

        pin_input = driver.find_element(by=By.NAME, value="PIN")
        pin_input.send_keys(payment_info.pin)

        internet_password_input = driver.find_element(by=By.NAME, value="password")
        internet_password_input.send_keys(payment_info.internet_password)

        login_button = driver.find_element(by=By.NAME, value="Login")
        login_button.click()
        # Delay to make sure the elements are loaded before we try to interact with them
        driver.implicitly_wait(5)
        payments_link = driver.find_element(by=By.LINK_TEXT, value="PAYMENTS")
        payments_link.click()
        driver.implicitly_wait(5)


        taxform_input = driver.find_element(by=By.ID, value="TaxForm_EditField")
        taxform_input.send_keys("941")

        next_button = driver.find_element(by=By.NAME, value="_eventId_next")
        next_button.click()
        driver.implicitly_wait(5)

        tax_radio_button = driver.find_element(By.ID, "5")
        tax_radio_button.click()

        next_button = driver.find_element(by=By.NAME, value="_eventId_next")
        next_button.click()
        driver.implicitly_wait(5)

        amount_input = driver.find_element(by=By.ID, value="singlePayment.amount.value")
        amount_input.send_keys(payment_info.payment_amount)

        year_input = driver.find_element(by=By.NAME, value="singlePayment.taxPeriodYear")
        year_input.send_keys(payment_info.year)

        settle_date_input = driver.find_element(by=By.NAME, value="singlePayment.settlementDate.dateString")
        settle_date_input.send_keys(settle_date)

        quarter_dropdown = Select(driver.find_element(by=By.NAME, value="singlePayment.taxPeriodMonth"))
        quarter_dropdown.select_by_visible_text(payment_info.quarter)

        next_button = driver.find_element(by=By.NAME, value="_eventId_next")
        next_button.click()
        driver.implicitly_wait(5)

        social_security_amount_input = driver.find_element(by=By.NAME, value="singlePayment.subCategories[0].amount.value")
        medicare_amount_input = driver.find_element(by=By.NAME, value="singlePayment.subCategories[1].amount.value")
        federal_tax_amount_input = driver.find_element(by=By.NAME, value="singlePayment.subCategories[2].amount.value")

        social_security_amount_input.send_keys(payment_info.social_security_amount)
        medicare_amount_input.send_keys(payment_info.medicare_amount)
        federal_tax_amount_input.send_keys(payment_info.federal_tax_amount)

        next_button = driver.find_element(by=By.NAME, value="_eventId_next")
        next_button.click()
        driver.implicitly_wait(5)
    except:
        print("error")
        driver.quit()
        exit()
        raise

    while True:
        pass

def main():  
    # Seperate file with sensitive data
    sensitive_data = None
    with open('company_data.json', 'r') as file:
        sensitive_data = json.load(file)

    # Get the list of csv files in the tax_liability folder
    folder_path = 'tax_liability'
    file_list = os.listdir(folder_path)

    # Iterate through each file and create PaymentInfo objects for each company
    payment_info_list = []
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        
        df = pd.read_csv(file_path, header=None)
        company_name = df.iloc[0][0].split('\n')[0].strip()


        company_details = sensitive_data[company_name]
        ein = company_details['ein']
        pin = company_details['pin']
        internet_password = company_details['internet_password']

        date_range = df.iloc[1][0]
        start_date = datetime.strptime(date_range.split(' to ')[0], '%m/%d/%Y')
        year = start_date.year
        quarter = (start_date.month - 1) // 3 + 1


        payment_amount = ((df[df[2] == '941 Total'].values[0][-1]).replace(',', ''))
        social_security_amount = ((df[df[2] == 'Social Security Wages'].values[0][-1]).replace(',', ''))
        medicare_amount = (df[df[2] == 'Medicare Wages & Tips'].values[0][-1]).replace(',', '')
        federal_tax_amount = (df[df[2] == 'Federal Income Tax'].values[0][-1]).replace(',', '')

        if (float(social_security_amount) + float(medicare_amount) + float(federal_tax_amount)) != float(payment_amount):
            print("Amounts don't match for company: ", company_name)
            exit()
        
        payment_info = PaymentInfo(
            name=company_name,
            ein=ein,
            pin=pin,
            internet_password=internet_password,
            year=year,
            quarter=quarter,
            payment_amount=payment_amount,
            social_security_amount=social_security_amount,
            medicare_amount=medicare_amount,
            federal_tax_amount=federal_tax_amount,
        )
        payment_info_list.append(payment_info)


    window = tk.Tk()
    label = tk.Label(text="Payment Settle Date\n(MM/DD/YYYY)")
    settle_entry = tk.Entry()
    settle_entry.insert(0, datetime.today().strftime('%m/%d/%Y'))
    label.pack()
    settle_entry.pack()

    for payment_info in payment_info_list:
        button = tk.Button(
            text= payment_info.name,
            width=25,
            height=5,
            bg="gray",
            fg="black",
            command=lambda pi=payment_info: on_click(pi, settle_entry.get())
        )
        button.pack()

    window.mainloop()

if __name__ == '__main__':
    main()