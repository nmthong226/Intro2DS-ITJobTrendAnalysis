import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set up headless Chrome
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")

# Create a browser instance
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Loop through each page
num_pages = 5  # Number of pages to scrape
job_list = []

for page in range(1, num_pages + 1):
    # Construct the page URL (Change the URL format as per the target website)
    url = f"https://vn.indeed.com/jobs?q=it&l=Hanoi&start={page * 10}"  # Example Indeed URL for IT jobs in Hanoi
    print(f"Scraping page: {url}")
    
    # Open the URL
    driver.get(url)
    
    # Get the page content
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Find the job elements and extract data
    jobs = soup.find_all('div', class_='job_seen_beacon')
    for job in jobs:
        title = job.find('h2', class_='jobTitle').text.strip() if job.find('h2', class_='jobTitle') else "N/A"
        company = job.find('span', class_='companyName').text.strip() if job.find('span', class_='companyName') else "N/A"
        location = job.find('div', class_='companyLocation').text.strip() if job.find('div', class_='companyLocation') else "N/A"
        salary = job.find('div', class_='salarySnippet').text.strip() if job.find('div', class_='salarySnippet') else "N/A"
        posted_date = job.find('span', class_='date').text.strip() if job.find('span', class_='date') else "N/A"
        link = job.find('a', href=True)['href'] if job.find('a', href=True) else "N/A"
        
        job_list.append({
            'Title': title,
            'Company': company,
            'Location': location,
            'Salary': salary,
            'Posted Date': posted_date,
            'Link': f"https://vn.indeed.com{link}" if link != "N/A" else "N/A"
        })

# Close the browser
driver.quit()

# Save the data to a CSV file
df = pd.DataFrame(job_list)
df.to_csv('indeed_jobs.csv', index=False, encoding='utf-8-sig')
