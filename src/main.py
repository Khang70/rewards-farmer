import os
import json
import time
import rewards_tasks
import mouse_trajectory
import mimic_typing
from selenium import webdriver

options = webdriver.EdgeOptions()

# Bật chế độ Headless (ẩn giao diện) để chạy trên GitHub Actions
options.add_argument("--headless=new") 
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Vẫn giữ user-data-dir để tận dụng cache nếu muốn
options.add_argument("--user-data-dir=/home/runner/.cache/ms-rewards-profile")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Edge(options=options)

mouse = mouse_trajectory.MouseUtils(driver)
keyboard = mimic_typing.KeyboardUtils(driver)

# --- NẠP COOKIE TỪ GITHUB SECRETS ---
print("[INFO] Đang tiến hành nạp session cookies...")
driver.get("https://www.bing.com/") # Phải truy cập domain trước thì mới add cookie vào được

ms_cookies_raw = os.getenv("MS_COOKIES")

if ms_cookies_raw:
    try:
        cookies = json.loads(ms_cookies_raw)
        for cookie in cookies:
            # Selenium yêu cầu loại bỏ một số trường không hợp lệ nếu có
            if 'sameSite' in cookie:
                if cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                    cookie['sameSite'] = "Lax"
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                pass
        print("[INFO] Nạp cookies thành công! Đang làm mới trang...")
        driver.refresh()
        time.sleep(3)
    except Exception as e:
        print(f"[WARNING] Lỗi khi xử lý chuỗi cookies: {e}")
else:
    print("[WARNING] Không tìm thấy biến môi trường MS_COOKIES!")
# ------------------------------------

rewards = rewards_tasks.RewardsTaskUtils(driver)

rewards.complete_all_tasks()

driver.quit()
