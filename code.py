from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from IPython.display import FileLink

# Step 1: Set up the WebDriver
driver_path = 'C:\\Users\\T Vishnu vardhan\\OneDrive\\Desktop\\chromedriver\\chromedriver-win64\\chromedriver.exe'  # Replace with your WebDriver path
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Step 2: Navigate to LinkedIn and log in
driver.get('https://www.linkedin.com/login')
time.sleep(3)

# Replace 'your_username' and 'your_password' with your LinkedIn credentials
username = driver.find_element(By.ID, 'username')
password = driver.find_element(By.ID, 'password')
username.send_keys('your_username')
password.send_keys('your_password')
driver.find_element(By.XPATH, '//*[@type="submit"]').click()
time.sleep(5)

# Step 3: Search for Adobe Experience Manager job listings in the past month
driver.get('https://www.linkedin.com/jobs/search/?currentJobId=3976160847&f_TPR=r2592000&geoId=103644278&keywords=adobe%20experience%20manager&location=Bangalore&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true')
time.sleep(5)

# Step 4: Extract job listings
job_titles = []
companies = []
locations = []
applicants = []
times = []

# Scroll to load more jobs
SCROLL_PAUSE_TIME = 10

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

job_cards = driver.find_elements(By.CSS_SELECTOR, 'div.job-card-container')

for job in job_cards:
    try:
        title = job.find_element(By.CSS_SELECTOR, 'a.job-card-list__title').text
        company = job.find_element(By.CSS_SELECTOR, 'span.job-card-container__primary-description').text
        location = job.find_element(By.CSS_SELECTOR, 'li.job-card-container__metadata-item').text
        try:
            applicant_count = job.find_element(By.CSS_SELECTOR, 'li.job-card-container__footer-item.inline-flex.align-items-center > strong > span').text
        except:
            applicant_count = 'N/A'
        try:
            posted_time = job.find_element(By.CSS_SELECTOR, 'li > time').text
        except:
            posted_time = 'N/A'
        
        job_titles.append(title)
        companies.append(company)
        locations.append(location)
        applicants.append(applicant_count)
        times.append(posted_time)
    except Exception as e:
        print(f'Error: {e}')
        continue

# Step 5: Export to Excel
job_data = {
    'Job Title': job_titles,
    'Company': companies,
    'Location': locations,
    'Applicants': applicants,
    'Posted Time': times,
}

df = pd.DataFrame(job_data)
print(df)
file = 'Adobe_Job_Listings.xlsx'
df.to_excel(file, index=False)
display(FileLink(file))

# Close the driver
driver.quit()

print("Job listings have been exported to Adobe_Job_Listings.xlsx")
