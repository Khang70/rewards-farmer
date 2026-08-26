import os
import time
import rewards_tasks
import mouse_trajectory
import mimic_typing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

options = webdriver.EdgeOptions()

# Bật chế độ Headless (ẩn giao diện) để chạy trên GitHub Actions
options.add_argument("--headless=new") 
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Thêm user-data-dir để lưu profile và giữ session qua các lần chạy GitHub Actions
options.add_argument("--user-data-dir=/home/runner/.cache/ms-rewards-profile")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Edge(options=options)

mouse = mouse_trajectory.MouseUtils(driver)
keyboard = mimic_typing.KeyboardUtils(driver)

# --- ĐOẠN CODE ĐĂNG NHẬP TỰ ĐỘNG ---
print("[INFO] Đang tiến hành kiểm tra / đăng nhập tài khoản Microsoft...")
driver.get("https://login.live.com/")

ms_user = os.getenv("MS_USER")
ms_pass = os.getenv("MS_PASS")

if ms_user and ms_pass:
    try:
        # Nếu đã có session lưu trong profile cache, trang có thể tự vào thẳng bên trong 
        # mà không hiện ô điền email, đoạn này sẽ tự bắt ngoại lệ hoặc xử lý tiếp.
        email_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "loginfmt"))
        )
        keyboard.send_keys(ms_user)
        email_field.send_keys(Keys.ENTER)
        time.sleep(3)

        pass_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "passwd"))
        )
        keyboard.send_keys(ms_pass)
        pass_field.send_keys(Keys.ENTER)
        time.sleep(4)

        try:
            yes_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "idSIButton9"))
            )
            yes_btn.click()
            time.sleep(3)
        except:
            pass
            
        print("[INFO] Đăng nhập thành công!")
    except Exception as e:
        print(f"[INFO] Có thể session cũ vẫn còn hiệu lực hoặc không cần đăng nhập lại: {e}")
else:
    print("[WARNING] Không tìm thấy biến môi trường MS_USER hoặc MS_PASS!")
# ---------------------------------------------

rewards = rewards_tasks.RewardsTaskUtils(driver)

rewards.complete_all_tasks()

driver.quit()
