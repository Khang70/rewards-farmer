import os
import json
import time
import rewards_tasks
import mouse_trajectory
import mimic_typing
from selenium import webdriver

options = webdriver.EdgeOptions()

# Bật chế độ Headless mới và các cờ bắt buộc để chạy ổn định trên Linux/GitHub Actions
options.add_argument("--headless=new") 
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222") # Khắc phục lỗi chrome not reachable

# Tạm thời tắt user-data-dir nếu dùng cookies để tránh xung đột quyền khóa tệp trên Linux
# options.add_argument("--user-data-dir=/home/runner/.cache/ms-rewards-profile")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Edge(options=options)

mouse = mouse_trajectory.MouseUtils(driver)
keyboard = mimic_typing.KeyboardUtils(driver)

# --- NẠP COOKIE TỪ GITHUB SECRETS ---
print("[INFO] Đang tiến hành nạp session cookies...")
driver.get("https://www.bing.com/")

ms_cookies_raw = os.getenv("MS_COOKIES")

if ms_cookies_raw:
    try:
        cookies = json.loads(ms_cookies_raw)
        for cookie in cookies:
            if 'sameSite' in cookie:
                if cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                    cookie['sameSite'] = "Lax"
            try:
                driver.add_cookie(cookie)
            except Exception:
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
