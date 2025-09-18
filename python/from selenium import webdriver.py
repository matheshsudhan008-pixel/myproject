from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.saucedemo.com")

# Login
driver.find_element(By.ID, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()

# Wait for products title
try:
    products_title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )
    if "PRODUCTS" in products_title.text.upper():
        print("Login Test Passed ✅")
    else:
        print("Login Test Failed ❌")
except:
    print("Login Test Failed ❌")

# Add first product to cart
driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
print("Added first product to cart ✅")

driver.quit()
