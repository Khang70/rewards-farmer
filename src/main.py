import rewards_tasks
import mouse_trajectory
import mimic_typing
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
# (Hoặc nếu trên GitHub Actions dùng Chromium thay vì Edge, bạn có thể chuyển sang dùng Chrome/Chromium options)

options = webdriver.EdgeOptions()

# Bật chế độ Headless (ẩn giao diện) để chạy trên GitHub Actions
options.add_argument("--headless=new") 
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

# Lưu ý: Trên GitHub Actions, các thư mục profile cục bộ sẽ trống ở mỗi lần chạy mới.
# Do đó, đoạn code đăng nhập tự động bằng cookie/session sẽ cần được tối ưu thêm nếu cần.
# options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
# options.add_argument(f"--profile-directory={PROFILE_NAME}")

driver = webdriver.Edge(options=options)

mouse = mouse_trajectory.MouseUtils(driver)
keyboard = mimic_typing.KeyboardUtils(driver)

rewards = rewards_tasks.RewardsTaskUtils(driver)

rewards.complete_all_tasks()

# Bỏ dòng input() đi vì GitHub Actions chạy tự động không có ai bấm Enter được
# input("Press Enter to exit...")

driver.quit()
