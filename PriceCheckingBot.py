import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

sleepTimer = 3
searchQuery = input("Enter Search: ")

driver = webdriver.Chrome()

def ALDI():
    # Search for the product
    print("Searching ALDI")
    driver.get("https://shop.aldi.us/store/aldi/storefront/?current_zip_code=55330&utm_source=yext&utm_medium=local&utm_campaign=brand&utm_content=shopnow_storepage")
    searchBar = driver.find_element(By.ID, "search-bar-input")
    time.sleep(sleepTimer)

    # Enter the search query and submit
    print("Enter searchQuery")
    searchBar.send_keys(searchQuery)
    searchBar.send_keys(Keys.ENTER)
    time.sleep(sleepTimer)

    # Wait for the search results to load
    print("Wait for Results")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.e-8zabzc")))

    # Get all product cards in the search results
    print("Get all Products on Page")
    product_listings = driver.find_elements(By.CSS_SELECTOR, "span.e-8zabzc")

    #Search through all products to find what is closest to searchQuery
    print("Searching Results")
    exactMatch = None
    partialMatches = []

    for listing in product_listings:
        print(listing.text)

        patternExact = re.compile(rf'\b{re.escape(searchQuery)}\b', re.IGNORECASE)
        if re.search(patternExact, listing.text):
            exactMatch = listing
            break
        patternPartial = re.compile(re.escape(searchQuery), re.IGNORECASE)
        if re.search(patternPartial, listing.text):
            partialMatches.append(listing)
    
    if exactMatch:
        exactMatch.click()
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.e-0")))
        price = driver.find_element(By.CSS_SELECTOR, "span.e-0").text
        print("ALDI: ", price)
        return price
    
    if partialMatches:
        partialMatches[0].click()
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.e-0")))
        price = driver.find_element(By.CSS_SELECTOR, "span.e-0").text
        print("ALDI: ", price)
        return price

    print("No Matches Found")
    return None

def Target():
    # Search for the product
    print("Searching Target")
    driver.get("https://www.target.com/")
    searchBar = driver.find_element(By.CSS_SELECTOR, "#search")
    time.sleep(sleepTimer)

    # Enter the search query and submit
    print("Enter searchQuery")
    searchBar.send_keys(searchQuery)
    searchBar.send_keys(Keys.ENTER)
    time.sleep(sleepTimer)

    driver.execute_script("window.scrollBy(0, 500);")

    wait = WebDriverWait(driver, 10)
    titlesSelector = "a.styles__StyledLink-sc-vpsldm-0.styles__StyledTitleLink-sc-14ktig2-1.cbOry.csOImU.h-display-block.h-text-bold.h-text-bs"
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, titlesSelector)))

    # Get all product cards in the search results
    print("Get all Products on Page")
    product_listings = driver.find_elements(By.CSS_SELECTOR, titlesSelector)

    #Search through all products to find what is closest to searchQuery
    print("Searching Results")
    exactMatch = None
    partialMatches = []

    for listing in product_listings:
        print(listing.text)

        patternExact = re.compile(rf'\b{re.escape(searchQuery)}\b', re.IGNORECASE)
        if re.search(patternExact, listing.text):
            exactMatch = listing
            break
        patternPartial = re.compile(re.escape(searchQuery), re.IGNORECASE)
        if re.search(patternPartial, listing.text):
            partialMatches.append(listing)
    
    if exactMatch:
        exactMatch.click()
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-test='product-price']")))
        price = driver.find_element(By.CSS_SELECTOR, "[data-test='product-price']").text
        print("Target: ", price)
        return price
    
    if partialMatches:
        partialMatches[0].click()
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-test='product-price']")))
        price = driver.find_element(By.CSS_SELECTOR, "[data-test='product-price']").text
        print("Target: ", price)
        return price

    print("No Matches Found")
    return None

try:
    # Search Options
    ALDI_price = ALDI()
    Target_price = Target()

    driver.quit()

    ALDI_price = ''.join(filter(str.isdigit, ALDI_price))
    ALDI_price = ALDI_price[:-2] + "." + ALDI_price[-2:]

    Target_price = ''.join(filter(str.isdigit, Target_price))
    Target_price = Target_price[:-2] + "." + Target_price[-2:]

    print("\nAldi:")
    print("$" + ALDI_price)
    print("Target:")
    print("$" + Target_price)

    ALDI_price = ALDI_price.replace("$", "").replace(".", "")
    ALDI_price = int(ALDI_price)
    Target_price = Target_price.replace("$", "").replace(".", "")
    Target_price = float(Target_price)

    if ALDI_price < Target_price:
        print("Shop at ALDI")
    elif ALDI_price > Target_price:
        print("Shop at Target")
    else:
        print("Shop at Either")

    time.sleep(20000)

except Exception as e:
    print(f"An exception has occurred: {str(e)}")
finally:
    driver.quit()
