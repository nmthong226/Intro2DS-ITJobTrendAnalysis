from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException


# ------------------------------
# 1. Setup WebDriver
# ------------------------------
def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = uc.Chrome(options=options)
    return driver

def get_text_or_empty(element):
    """Trả về văn bản từ phần tử nếu nó tồn tại, nếu không trả về chuỗi rỗng."""
    return element.text.strip() if element else ''

def get_attr_or_empty(element, attr):
    """Lấy giá trị thuộc tính từ phần tử nếu nó tồn tại, nếu không trả về chuỗi rỗng."""
    return element.get(attr, '').strip() if element else ''
# ------------------------------
# 2. Hàm Crawl Dữ Liệu
# ------------------------------
def crawl_topcv(keyword):
    driver = setup_driver()
    jobs_data = []
    
    try:
        driver.get("https://www.topcv.vn")
        print("✅ Đã truy cập trang TopCV thành công.")
        time.sleep(random.uniform(3, 5))  # Chờ ngẫu nhiên
        
        # Tìm ô tìm kiếm
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'keyword'))
        )
        print("✅ Đã tìm thấy ô tìm kiếm.")
        
        # Nhập từ khóa và tìm kiếm
        search_box.send_keys(keyword)
        time.sleep(random.uniform(1, 3))
        search_box.send_keys(Keys.RETURN)
        print(f"🔍 Đã nhập từ khóa '{keyword}' và bắt đầu tìm kiếm.")
        time.sleep(random.uniform(3, 5))
        
        # Lấy số lượng trang
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        pagination_text = soup.find('span', id='job-listing-paginate-text').text.strip()
        
        # Loại bỏ ký tự không hợp lệ (non-breaking space)
        pagination_text = pagination_text.replace('\xa0', ' ')  # Thay thế ký tự '\xa0' bằng khoảng trắng thông thường
        
        # Trích xuất số trang
        num_pages = int(pagination_text.split(' ')[-2])
        print(f"Số lượng trang: {num_pages}")

        # Lặp qua các trang
        for page in range(num_pages):
            print(f"📄 Đang thu thập dữ liệu từ trang {page + 1}...")

            # Đảm bảo trang đã tải
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'job-list-search-result'))
            )

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_listings = soup.find_all('div', class_='job-list-search-result')  # Cập nhật class name tại đây

            if not job_listings:
                print("❌ Không tìm thấy tin tuyển dụng trên trang này.")
                continue
            
            for job in job_listings:
                job_items = job.find_all('div', class_='job-item-search-result')
                for job in job_items:
                    try:
                        job_data = {
                            'Job Title': get_text_or_empty(job.find('h3', class_='title')),
                            'Role': get_text_or_empty(job.find('a', class_='company job-pro')),  # Role từ công ty
                            'Level': get_text_or_empty(job.find('label', class_='title-salary')),  # Mức lương
                            'Years of Experience': get_text_or_empty(job.find('label', class_='exp')),  # Kinh nghiệm
                            'Company': get_text_or_empty(job.find('span', class_='company-name')),  # Tên công ty
                            'Location': get_text_or_empty(job.find('span', class_='city-text')),  # Vị trí
                            'Salary Range': get_text_or_empty(job.find('label', class_='title-salary')),  # Mức lương
                            'Required Skills': get_text_or_empty(job.find('div', class_='tag')),  # Kỹ năng yêu cầu
                            'Job URL': get_attr_or_empty(job.find('a'), 'href'),  # URL của công việc
                            'Source Platform': 'TopCV'
                        }
                        jobs_data.append(update_jobs_data_with_details(job_data))
                    except AttributeError as e:
                        print(f"error ", e)
                        continue
            
            print(f"✅ Đã thu thập dữ liệu từ trang {page + 1}.")
            time.sleep(random.uniform(2, 4))
            
            # Chuyển trang
            try:
                # Sử dụng cách tìm nút "Next" bằng thuộc tính 'rel' hoặc 'aria-label'
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[rel="next"]'))
                )
                next_button.click()
                print("➡️ Đang chuyển sang trang tiếp theo.")
                time.sleep(random.uniform(3, 5))
            except Exception as e:
                print(f"🚫 Không tìm thấy nút chuyển trang. Lỗi: {e}")
                break
                
    except Exception as e:
        print(f"🚨 Lỗi trong quá trình thu thập dữ liệu: {e}")
        
    finally:
        try:
            # Đảm bảo việc đóng driver không gây lỗi
            if driver:
                driver.quit()
                print("🚪 Đã đóng trình duyệt.")
        except Exception as e:
            print(f"❌ Lỗi khi đóng trình duyệt: {e}")
    print(f"✅ Dữ liệu thu thập được: {len(jobs_data)} công việc.")
    return jobs_data

def update_jobs_data_with_details(jobs_data):
    driver = setup_driver()  # Khởi tạo Selenium WebDriver

    try:
        job_url = jobs_data.get('Job URL')
        if not job_url:
            print("🚫 Không có URL công việc. Bỏ qua.")
        # Truy cập URL công việc
        driver.get(job_url)
        print(f"✅ Đã truy cập thành công: {job_url}")
        time.sleep(random.uniform(3, 5))  # Chờ ngẫu nhiên để tránh bị chặn

        # Đảm bảo trang đã tải xong phần tử cần thiết
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'box-general-group-info-value'))
            )
        except TimeoutException:
            print("🚨 Không tìm thấy phần tử cần thiết trên trang. Bỏ qua công việc này.")

        # Dùng BeautifulSoup để phân tích nội dung trang
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Lấy thông tin cấp bậc
        cap_bac = soup.find('div', class_='box-general-group-info-value')
        jobs_data['Level'] = cap_bac.text.strip() if cap_bac else 'N/A'

        # Lấy kỹ năng cần có
        skills_section = soup.find('div', class_='box-category collapsed')
        if skills_section:
            # Tìm phần tử có nội dung "Kỹ năng cần có"
            skills_tags = skills_section.find('div', class_='box-category-tags').find_all('a')
            skills_list = [skill.text.strip() for skill in skills_tags]
            jobs_data['Required Skills'] = ', '.join(skills_list)
        else:
            jobs_data['Required Skills'] = 'N/A'


        print(f"🔄 Đã cập nhật thông tin chi tiết cho công việc: {jobs_data['Job Title']}")

    except Exception as e:
        print(f"🚨 Lỗi khi xử lý công việc '{job.get('Job Title', 'N/A')}': {e}")
    finally:
        try:
            if driver:
                driver.quit()
                print("🚪 Đã đóng trình duyệt.")
        except Exception as e:
            print(f"❌ Lỗi khi đóng trình duyệt: {e}")


    print("✅ Hoàn tất cập nhật dữ liệu chi tiết.")
    print("❌ job_data", jobs_data)

    return jobs_data



# ------------------------------
# 3. Lưu Dữ Liệu Thành CSV
# ------------------------------
def save_to_csv(jobs_data, filename='D://merged_data.csv'):
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Kiểm tra dữ liệu thu thập trước khi lưu
    if not jobs_data:
        print("❌ Không có dữ liệu để lưu.")
        return
    
    df = pd.DataFrame(jobs_data)
    
    # Lưu dữ liệu vào CSV với mã hóa utf-8-sig để giữ dấu tiếng Việt
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"💾 Dữ liệu đã được lưu vào '{filename}'.")

# ------------------------------
# 4. Chạy Chương Trình Chính
# ------------------------------
def main():
    keyword = 'IT'
    print(f"🔑 Từ khóa tìm kiếm: {keyword}")
    jobs_data = crawl_topcv(keyword)
    save_to_csv(jobs_data)

# ------------------------------
# 5. Điểm Bắt Đầu
# ------------------------------
if __name__ == "__main__":
    main()
