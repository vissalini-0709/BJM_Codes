#This code to select ALL

#This code to select Supra and Bond
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # <-- Import Options
import time

# Set up Chrome options to keep the browser open after script ends
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Specify the path to chromedriver.exe
service = Service(r"path to chromedriver")

# Initialize WebDriver with the Service object and options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the target webpage
driver.get("https://mft.eip.openapipnb.com.my/")  # Replace with your actual URL

# Locate the input element using the relative XPath
input_element = driver.find_element(By.XPATH, "//input[@id='mat-input-0']")
input_element2 = driver.find_element(By.XPATH, "//input[@id='mat-input-1']")
submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

# Input a value into the field
input_value = "username"
input_element.send_keys(input_value)

input_value2 = "password"
input_element2.send_keys(input_value2)

submit_button.click()
driver.maximize_window()
time.sleep(10)

# Click Explorer
explorer_element = driver.find_element(By.XPATH, "//span[@class='text m-left-sm'][normalize-space()='Explorer']")
explorer_element.click()

# Click Job Directory Browser
job_directory_browser_element = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Job Directory Browser']"))
)
job_directory_browser_element.click()

# Click Icon
icon_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//tbody/tr[1]/td[6]/mat-icon[1]"))
)
icon_element.click()

# Click File Browser
file_browser_icon = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='File Browser']//span[@class='icon-wrapper']"))
)
file_browser_icon.click()

wait = WebDriverWait(driver, 4)

# Click first 2 checkboxes
# Base absolute path structure
base_path = "/html[1]/body[1]/app-root[1]/app-mft[1]/div[1]/div[1]/div[1]/app-file-browser-job-detail-page[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/form[1]/div[1]/div[3]/section[1]/div[1]/div[1]/div[1]/div[2]/app-file-browser[1]/div[1]/div[1]/div[3]/ul[1]/li[{}]/mat-checkbox[1]/label[1]/div[1]"

# Number of checkboxes to click
num_checkboxes = 2

# Click checkboxes using dynamic absolute paths
for i in range(1, num_checkboxes + 1):
    try:
        xpath = base_path.format(i)
        checkbox = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)  # Scroll into view
        time.sleep(0.2)  # Stabilize before clicking
        
        # Use JavaScript click to bypass obstruction issues
        driver.execute_script("arguments[0].click();", checkbox)
        print(f"Clicked checkbox {i}")
        
    except Exception as e:
        print(f"Failed to click checkbox {i}: {e}")

# Click the "Download Selected" button
try:
    download_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Download Selected']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", download_button)  # Scroll into view
    time.sleep(0.5)  # Stabilize before clicking
    
    # Use JavaScript click if normal click fails
    driver.execute_script("arguments[0].click();", download_button)
    print("Clicked the 'Download Selected' button successfully.")
    
    # Wait for download completion
    time.sleep(2)  # Simple wait; consider using a more sophisticated method
    
except Exception as e:
    print(f"Failed to click the 'Download Selected' button: {e}")

# To select EQ and Domestic
    # Click Job Directory Browser
job_directory_browser_element = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Job Directory Browser']"))
)
job_directory_browser_element.click()

# Click Icon
icon_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//tbody/tr[2]/td[6]/mat-icon[1]"))
)
icon_element.click()

# Click File Browser
file_browser_icon = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='File Browser']//span[@class='icon-wrapper']"))
)
file_browser_icon.click()

wait = WebDriverWait(driver, 4)

# Click first 1 checkboxes
# Absolute XPath for the checkbox
checkbox_xpath = "/html[1]/body[1]/app-root[1]/app-mft[1]/div[1]/div[1]/div[1]/app-file-browser-job-detail-page[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/form[1]/div[1]/div[3]/section[1]/div[1]/div[1]/div[1]/div[2]/app-file-browser[1]/div[1]/div[1]/div[3]/ul[1]/li[1]/mat-checkbox[1]/label[1]/div[1]"

try:
    checkbox = wait.until(EC.presence_of_element_located((By.XPATH, checkbox_xpath)))
    driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)  # Scroll into view
    time.sleep(0.2)  # Stabilize before clicking
    
    # Use JavaScript click to bypass obstruction issues
    driver.execute_script("arguments[0].click();", checkbox)
    print("Clicked checkbox successfully.")
    
except Exception as e:
    print(f"Failed to click checkbox: {e}")

# Click the "Download Selected" button
try:
    download_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Download Selected']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", download_button)  # Scroll into view
    time.sleep(0.5)  # Stabilize before clicking
    
    # Use JavaScript click if normal click fails
    driver.execute_script("arguments[0].click();", download_button)
    print("Clicked the 'Download Selected' button successfully.")
    
    # Wait for download completion
    time.sleep(2)  # Simple wait; consider using a more sophisticated method
    
except Exception as e:
    print(f"Failed to click the 'Download Selected' button: {e}")

#To select efront
    # Click Job Directory Browser
job_directory_browser_element = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Job Directory Browser']"))
)
job_directory_browser_element.click()

# Click Icon
icon_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//tbody/tr[4]/td[6]/mat-icon[1]"))
)
icon_element.click()

# Click File Browser
file_browser_icon = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='File Browser']//span[@class='icon-wrapper']"))
)
file_browser_icon.click()

wait = WebDriverWait(driver, 4)

# Base absolute path structure
base_path = "/html[1]/body[1]/app-root[1]/app-mft[1]/div[1]/div[1]/div[1]/app-file-browser-job-detail-page[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/form[1]/div[1]/div[3]/section[1]/div[1]/div[1]/div[1]/div[2]/app-file-browser[1]/div[1]/div[1]/div[3]/ul[1]/li[{}]/mat-checkbox[1]/label[1]/div[1]"

# Number of checkboxes to click
num_checkboxes = 3

# Click checkboxes using dynamic absolute paths
for i in range(1, num_checkboxes + 1):
    try:
        xpath = base_path.format(i)
        checkbox = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)  # Scroll into view
        time.sleep(0.2)  # Stabilize before clicking
        
        # Use JavaScript click to bypass obstruction issues
        driver.execute_script("arguments[0].click();", checkbox)
        print(f"Clicked checkbox {i} successfully.")
        
    except Exception as e:
        print(f"Failed to click checkbox {i}: {e}")

# Click the "Download Selected" button
try:
    download_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Download Selected']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", download_button)  # Scroll into view
    time.sleep(0.5)  # Stabilize before clicking
    
    # Use JavaScript click if normal click fails
    driver.execute_script("arguments[0].click();", download_button)
    print("Clicked the 'Download Selected' button successfully.")
    
    # Wait for download completion
    time.sleep(2)  # Simple wait; consider using a more sophisticated method
    
except Exception as e:
    print(f"Failed to click the 'Download Selected' button: {e}")

#To select SCD
# Click Job Directory Browser
job_directory_browser_element = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Job Directory Browser']"))
)
job_directory_browser_element.click()

# Click Icon
icon_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//tbody/tr[5]/td[6]/mat-icon[1]"))
)
icon_element.click()

# Click File Browser
file_browser_icon = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='File Browser']//span[@class='icon-wrapper']"))
)
file_browser_icon.click()

# Click HAC5001
hac5001_element = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='HAC5001']"))
)
hac5001_element.click()

# Click Menu Item Button
menu_item_button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@role='menuitem']"))
)
menu_item_button.click()

wait = WebDriverWait(driver, 10)

# Click first 39 checkboxes

   # Base absolute path structure
base_path = "/html[1]/body[1]/app-root[1]/app-mft[1]/div[1]/div[1]/div[1]/app-file-browser-job-detail-page[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/form[1]/div[1]/div[3]/section[1]/div[1]/div[1]/div[1]/div[2]/app-file-browser[1]/div[1]/div[1]/div[3]/ul[1]/li[{}]/mat-checkbox[1]/label[1]/div[1]"

# Number of checkboxes to click
num_checkboxes = 39

# Click checkboxes using dynamic absolute paths
for i in range(1, num_checkboxes + 1):
    try:
        xpath = base_path.format(i)
        checkbox = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)  # Scroll into view
        time.sleep(0.2)  # Stabilize before clicking
        
        # Use JavaScript click to bypass obstruction issues
        driver.execute_script("arguments[0].click();", checkbox)
        print(f"Clicked checkbox {i} successfully.")
        
    except Exception as e:
        print(f"Failed to click checkbox {i}: {e}")

# Click the "Download Selected" button
try:
    download_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Download Selected']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", download_button)  # Scroll into view
    time.sleep(0.5)  # Stabilize before clicking
    
    # Use JavaScript click if normal click fails
    driver.execute_script("arguments[0].click();", download_button)
    print("Clicked the 'Download Selected' button successfully.")
    
    # Wait for download completion
    time.sleep(15)  # Simple wait; consider using a more sophisticated method
    
except Exception as e:
    print(f"Failed to click the 'Download Selected' button: {e}")
