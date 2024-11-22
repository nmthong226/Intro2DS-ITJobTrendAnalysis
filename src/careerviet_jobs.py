import csv
import time
import random
import pandas as pd
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up headless Chrome
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")

# Create a browser instance
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)


def extract_skills(text):
    """
    Extracts programming skills and IT-related skills from the provided text.
    
    Args:
        text (str): The text content from which to extract skills.
    
    Returns:
        list: A list of detected skills.
    """
    # List of common IT-related keywords
    skill_keywords = [
        'Python', 'C++', 'Java', 'SQL', 'JavaScript', 'HTML', 'HTML5', 'CSS', 'CSS3', 'AJAX', 'Tailwind CSS',
        'React', 'Node.js', 'Tableau', 'Power BI', 'Qlik', 'Excel', 
        'MS Excel', 'Data analysis', 'Data science', 'Odoo', 'PC', 
        'Power Point', 'Statistics', 'Analysis', '.NET', 'PHP', 'C#', 'C/C++', 'NodeJS', 'JQuery',
        'Express', 'Nest', 'NestJS', 'MongoDB', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'gRPC',
        'Angular', 'Vue.js', 'TypeScript', 'Bootstrap', 'Sass', 'jQuery',
        'Flask', 'Django', 'Spring', 'Ruby on Rails', 'Laravel', 
        'PostgreSQL', 'MySQL', 'Redis', 'ElasticSearch', 'Firebase',
        'GraphQL', 'REST API', 'Restful API', 'SOAP', 'Jenkins', 'Git', 'GitHub',
        'Bitbucket', 'CI/CD', 'Terraform', 'Ansible', 'Chef', 'Puppet', 'Puppeteer',
        'Linux', 'Unix', 'Bash', 'Shell scripting', 'Pandas', 'NumPy', 
        'SciPy', 'TensorFlow', 'Keras', 'PyTorch', 'Hadoop', 'Spark', 'Selenium',
        'Big Data', 'Machine Learning', 'Deep Learning', 'AI', 'Data Mining',
        'NoSQL', 'JIRA', 'Confluence', 'Agile', 'Scrum', 'Kanban',
        'VMware', 'Hyper-V', 'Networking', 'TCP/IP', 'Firewall',
        'Load Balancing', 'Microservices', 'Serverless', 'Figma', 'Adobe XD',
        'UI/UX', 'Responsive Design', 'SEO', 'Content Management Systems',
        'WordPress', 'Drupal', 'Joomla', 'Salesforce', 'SAP', 'ERP',
        'Business Intelligence', 'ETL', 'SAS', 'MATLAB', 'R', 'Jupyter',
        'HDFS', 'Tableau Server', 'Pentaho', 'Snowflake', 'BigQuery',
        'Airflow', 'Kafka', 'RabbitMQ', 'Nginx', 'Apache', 'IIS',
        'Android', 'iOS', 'Swift', 'Kotlin', 'Xamarin', 'Flutter', 
        'React Native', 'Cordova', 'Unity', 'Unreal Engine', 'Game Development'
    ]

    # Find skills that match the keywords
    skills = []
    if isinstance(text, str):  # Ensure the input is a string
        for skill in skill_keywords:
            if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
                skills.append(skill)

    return skills

def get_job_details(job_link):
    driver.get(job_link)
    time.sleep(random.uniform(2, 5))  # Wait for the page to load

    # Parse the job detail page HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Initialize variables for experience and skills
    experience = "N/A"
    skills = []

    # Try to get the experience from the first selector
    experience_element = soup.select_one('#tab-1 > section > div.bg-blue > div > div:nth-child(3) > div > ul > li:nth-child(2)')
    
    if experience_element and "Kinh nghiệm" in experience_element.get_text(strip=True):
        raw_experience = experience_element.get_text(strip=True)
        experience = raw_experience.replace("Kinh nghiệm", "")
        experience = re.sub(r'\s+', ' ', experience).strip()
    else:
        # Fallback: Search the broader section for keywords like "years", "năm kinh nghiệm", or "năm"
        fallback_section = soup.select_one('#tab-1 > section > div:nth-child(3)')
        if fallback_section:
            text_content = fallback_section.get_text(separator=' ', strip=True)
            experience_regex = r'(\d{1,2}\s*(năm|year|years))'
            
            experience_match = re.search(experience_regex, text_content, re.IGNORECASE)
    
            if experience_match:
                # Clean and return the matched experience
                experience = experience_match.group(0).strip()
    
    # Add the third selector case to extract experience
    if experience == "N/A":
        additional_experience_element = soup.select_one('body > main > section.template.template04 > div.bottom-template > div > div > div.col-lg-9-custom > div.box-info > div.content > div > div:nth-child(2) > div > table > tbody > tr:nth-child(3) > td.content')
        
        if additional_experience_element:
            raw_experience = additional_experience_element.get_text(strip=True)
            experience = raw_experience.strip()  # You can process this further if needed

    # If still no experience found, set it to "N/A"
    if experience == "N/A":
        experience = "N/A"  # Or set it to another default value

    # Extract the required skills (adjust selector based on actual HTML structure)
    skills_section = soup.select_one('#tab-1 > section > div:nth-child(4)')  # Adjust class for skills section if necessary
    
    if skills_section:
        # Convert the `Tag` object to string to extract skills
        skills_text = skills_section.get_text(separator=' ', strip=True) if isinstance(skills_section, Tag) else str(skills_section)
        skills = extract_skills(skills_text)

    # Convert the skills list to a comma-separated string
    skills_list = ', '.join(skills) if skills else "N/A"

    # Extract additional job information
    role_level = soup.find('span', class_='role-level')  # Adjust class based on actual HTML
    role_level = role_level.get_text(strip=True) if role_level else "N/A"

    # Return the detailed data as a dictionary
    return {
        'Role Level': role_level,
        'Years of Experience': experience,
        'Required Skills': skills_list
    }


def scrape_jobs_careerviet(num_pages):
    job_list = []

    # Loop through each page from 1 to num_pages
    for page in range(1, num_pages + 1):
        # Construct the page URL
        url = f"https://careerviet.vn/viec-lam/cntt-phan-mem-c1-trang-{page}-vi.html"
        print(f"Scraping page: {url}")
        
        # Open the URL
        driver.get(url)
        time.sleep(random.uniform(2, 5))
        # Wait until the job items are fully loaded
        try:
            # Wait for job elements to be present
            WebDriverWait(driver, 50).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'job-item'))
            )
        except Exception as e:
            print(f"Error loading page {page}: {e}")
            continue

        # Get the page content after it's fully loaded
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Use a regular expression to match job items with 'job-item' and 'has-background'
        job_elements = soup.find_all('div', class_=re.compile(r'\bjob-item\b'))
        print(f"Number of job elements found on page {page}: {len(job_elements)}")

        for job_element in job_elements:
            # Extract job title and link from the <a> tag with class "job_link"
            job_link_tag = job_element.find('a', class_='job_link')
            title = job_link_tag.get_text(strip=True) if job_link_tag else "N/A"
            link = job_link_tag.get('href', 'N/A') if job_link_tag else "N/A"
            full_link = link if link.startswith('https://careerviet.vn') else f"https://careerviet.vn{link}"

            # Extract company name from the <a> tag with class "company-name"
            company_name_tag = job_element.find('a', class_='company-name')
            company_name = company_name_tag.get_text(strip=True) if company_name_tag else "N/A"

            # Extract salary from the <div> tag with class "salary"
            salary_tag = job_element.find('div', class_='salary')
            if salary_tag:
                salary = salary_tag.get_text(strip=True)
                # Remove the 'Lương: ' part of the string
                salary = salary.replace('Lương: ', '').strip()
            else:
                salary = "N/A"

            # Extract location from the <div> tag with class "location"
            location_tag = job_element.find('div', class_='location')
            location = location_tag.get_text(strip=True) if location_tag else "N/A"
            
            # Scrape additional details from the job detail page
            job_details = get_job_details(full_link)

            # Left two fields as N/A due to not enough data
            role = "N/A"
            level = "N/A"

            # Add the job details to the list
            job_list.append({
                'Job Title': title,
                'Role': role,
                'Level': level,
                'Years of Experience': job_details['Years of Experience'],
                'Company': company_name,
                'Location': location,
                'Salary Range': salary,
                'Required Skills': job_details['Required Skills'],
                'Source Platform': 'Careerviet',
                'Job Link': full_link
            })
        # Random sleep to avoid getting blocked
        time.sleep(random.uniform(2, 5))
    time.sleep(random.uniform(2, 5))   
    return job_list

# Example usage
num_pages = 25  # Specify the number of pages you want to scrape

# Call the scrape_jobs_careerviet function
job_list = scrape_jobs_careerviet(num_pages)

# Save the data to a CSV file
df = pd.DataFrame(job_list)
df.to_csv('careerviet_jobs_2024.csv', index=False, encoding='utf-8-sig')

# Close the browser
driver.quit()
