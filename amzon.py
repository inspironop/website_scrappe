from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from amazoncaptcha import AmazonCaptcha

search_term=input("Enter your search term:- ")

Service=Service(executable_path="chromedriver.exe")
driver=webdriver.Chrome(service=Service)
driver.get("https://www.amazon.in")
driver.maximize_window()
time.sleep(4)


# # amzon captha
# link=driver.find_element(By.XPATH,"//div[@class='a-row a-text-center']//img").get_attribute('src')
# capthca=AmazonCaptcha.fromlink(link)
# captcha_value=AmazonCaptcha.solve(capthca)
# input_field=driver.find_element(By.ID,"captchacharacters").send_keys(captcha_value)
# button=driver.find_element(By.CLASS_NAME,"a-button-text")
# button.click()



input_element =driver.find_element(By.ID,"twotabsearchtextbox")
input_element.clear()
input_element.send_keys(search_term + Keys.ENTER)
driver.find_element(By.XPATH,"//span[text()='Dell']").click()
time.sleep(4)



laptop_name=[]
laptop_price=[]
laptop_review=[]
laptop_asin=[]
# laptop_seller=[]

for i in range(1,18):

# we have to url of that page
    driver.get("https://www.amazon.in/s?k=dell+laptop&i=computers&rh=n%3A1375424031%2Cp_89%3ADell&dc&page=6&qid=1708366028&rnid=3837712031&ref=sr_pg_{}".format(i))


    # all items
    all_products=driver.find_elements(By.XPATH,"//div[@data-component-type='s-search-result']")
    # print(len(all_products))

    for all_product in all_products:

#       ASIN number
        asin_element = all_product.get_attribute("data-asin")
        laptop_asin.append(asin_element)  


        # names
        names=all_product.find_elements(By.XPATH,".//span[@class='a-size-medium a-color-base a-text-normal']")
        for name in names:
            laptop_name.append(name.text)


        #  price
        try:
            if len(all_product.find_elements(By.XPATH,".//span[@class='a-price-whole']"))>0:
                prices=all_product.find_elements(By.XPATH,".//span[@class='a-price-whole']")
                for price in prices:
                    laptop_price.append(price.text)
            else:
                laptop_price.append("0")
        except:
            pass

        # reviews
        try:
            if len(all_product.find_elements(By.XPATH,".//span[@class='a-size-base s-underline-text']"))>0:
                reviwes=all_product.find_elements(By.XPATH,".//span[@class='a-size-base s-underline-text']")
                for review in reviwes:
                    laptop_review.append(review.text)
            else:
                laptop_review.append("0")
        except:
            pass
        

        
    next_button= driver.find_element(By.XPATH,"//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")
    next_button.click()


print(len(laptop_name))
print(len(laptop_price))
print(len(laptop_review))
print(len(laptop_asin))
# print(len(laptop_seller))

import pandas as pd

df = pd.DataFrame(zip(laptop_name, laptop_price, laptop_review,laptop_asin),
                  columns=['laptop_name', 'laptop_price', 'laptop_review','laptop_asin'])
df.to_excel(r"C:\python\amzondata2_laptop.xlsx", index=False)

driver.quit()