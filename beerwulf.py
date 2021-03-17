from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import json

with open('details.json') as f:
  data = json.load(f)

browser = webdriver.Chrome()
browser.set_window_size(1920, 1080)
browser.get(data["product"])

inStock = False
browser.find_element_by_id("eighteenTrigger").click()
browser.find_element_by_id("ensBtnYes").click()

# If the item is not in stock then the page will refresh every second until it is
while not inStock:
    try:
        atcButton = browser.find_element_by_css_selector(".row .disabled") 
        time.sleep(1)
        browser.refresh()
    
    except:
        try:
            browser.find_element_by_css_selector(".row .plus").click()
        except:
            browser.find_element_by_css_selector(".product-meta:nth-child(2) .plus").click()
        
        # Address section
        browser.find_element_by_id("shoppincarttotal").click()
        browser.find_element_by_css_selector(".totals-row > .button").click()
        browser.find_element_by_css_selector(".full-width").click()
        browser.find_element_by_id("AddressFormWrapper_EmailAddress").click()
        email = browser.find_element_by_id("AddressFormWrapper_EmailAddress")
        email.send_keys(data["email"])
        browser.find_element_by_id("AddressFormWrapper_PhoneNumber").click()
        phone = browser.find_element_by_id("AddressFormWrapper_PhoneNumber")
        phone.send_keys(data["phone"])
        fname = browser.find_element_by_id("CheckoutForm_AddressFormWrapper_ShippingAddress_Firstname")
        fname.click()
        fname.send_keys(data["fname"])
        lname = browser.find_element_by_id("CheckoutForm_AddressFormWrapper_ShippingAddress_Lastname")
        lname.click()
        lname.send_keys(data["lname"])
        addy = browser.find_element_by_id("CheckoutForm_AddressFormWrapper_ShippingAddress_AddressLine1")
        addy.click()
        addy.send_keys(data["road"])
        city = browser.find_element_by_id("CheckoutForm_AddressFormWrapper_ShippingAddress_CityName")
        city.click()
        city.send_keys(data["city"])
        postcode = browser.find_element_by_id("CheckoutForm_AddressFormWrapper_ShippingAddress_PostalCode")
        postcode.click()
        postcode.send_keys(data["postcode"])
        browser.find_element_by_id("CheckoutForm_AddressFormWrapper_ShippingAddress_RegionName").click()
        browser.find_element_by_id("submitStep1").click()

        # The line below determines checkout method, currently it only works for visa but
        # if you changed ".row:nth-child(3) .label-free" to ".row:nth-child(2) .label-free"
        # then it would work for mastercard and ".row:nth-child(4) .label-free" for paypal.
        # If you pick paypal then you would need to delete all the code in the payment section
        browser.find_element_by_css_selector(".row:nth-child(3) .label-free").click()
        browser.find_element_by_id("submitStep2").click()

        # Depending on whether the email has be used before the 18+ element changes so both are checked
        try:
            browser.find_element_by_css_selector("body > div.checkout.js-checkout.checkout-step-three.shipping-business-transaction.billing-business-transaction > div.checkout-column.js-checkout-column > form > div.step-3-checkbox-container > div:nth-child(2) > div > label").click()
        except:
            browser.find_element_by_css_selector("body > div.checkout.js-checkout.checkout-step-three.shipping-business-transaction.billing-business-transaction > div.checkout-column.js-checkout-column > form > div.step-3-checkbox-container > div:nth-child(3) > div > label").click()
        
        browser.find_element_by_id("submitStep3").click()

        # Card payment section
        card = browser.find_element_by_id("card.cardNumber")
        card.click()
        card.send_keys(data["cardNumber"])
        cardName = browser.find_element_by_id("card.cardHolderName")
        cardName.click()
        cardName.send_keys(data["cardName"])
        expiryMonth = Select(browser.find_element_by_id("card.expiryMonth"))
        expiryMonth.select_by_value(data["expiryMonth"])
        expiryYear = Select(browser.find_element_by_id("card.expiryYear"))
        expiryYear.select_by_value(data["expiryYear"])
        cvc = browser.find_element_by_id("card.cvcCode")
        cvc.click()
        cvc.send_keys(data["cvc"])
        browser.find_element_by_id("mainSubmit").click()
        
        inStock = True

        time.sleep(10000)
        browser.close()