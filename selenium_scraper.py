from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.ycombinator.com/companies?batch=S22&isHiring=true")
print(driver.title)


# checking if the page has loaded the company names
company = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR,"div[class='XDx1u99BGLHPJBO_LPs4']"))
)
print(company.text)

# scrolling to the end of the page so that all the companies are loaded (because the website lazy loads the company list)

# Checking if the website needs to scorll to the bottom
loading = ""

try:
    loading = driver.find_element(By.CSS_SELECTOR,"div[class='q1vdpoLtJkwUT8jN22K2 dsStC1AzZueqISZqfHLZ'] + div").text
except NoSuchElementException as e:
    loading = "Not Loading anymore!"
except:
    print("there was some other error with loading...")

while(loading == "Loading more..."):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        loading = driver.find_element(By.CSS_SELECTOR,"div[class='q1vdpoLtJkwUT8jN22K2 dsStC1AzZueqISZqfHLZ'] + div").text
        print(loading)
        time.sleep(2)
    except:
        print("reached the EOP")
        loading = "Not Loading anymore!"
# after while loop the company list is all loaded
    
# getting all the anchor tags from the company list.  
companies = driver.find_elements(By.CSS_SELECTOR,"div[class='q1vdpoLtJkwUT8jN22K2 dsStC1AzZueqISZqfHLZ'] > a")

company_websites = dict()
# linkedin_links = []

for x in companies:
    url = str(x.get_attribute("href"))
    parsed = url.split('/')[-1]
    company_websites[parsed] = []

    try:
        # opening the company website and waiting for it to load then switching to it
        x.click()
        handles = driver.window_handles
        driver.switch_to.window(handles[1])
        driver.get(url)

        anchors = driver.find_element(By.CSS_SELECTOR , "div[class='hidden md:inline-block']")
        company_websites[parsed].append(anchors.text)
        
        linkedin_links = driver.find_elements(By.CSS_SELECTOR, "a[title='LinkedIn profile']")
        for link in linkedin_links:
            print(link.get_attribute("href"))
            company_websites[parsed].append(link.get_attribute("href"))

        driver.close()
        driver.switch_to.window(handles[0])
        
    except:
        print("error with this website ", parsed)
print(company_websites)

driver.close()