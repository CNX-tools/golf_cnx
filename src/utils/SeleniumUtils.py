import undetected_chromedriver as uc
import os


class UserActivity():
    def __init__(self, headless=False):
        # Add options to the Chrome driver
        options = uc.ChromeOptions()

        options.add_argument("--log-level=3")

        # Disable keyword suggestions
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)

        if headless:
            # Headless mode
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-renderer-backgrounding")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-client-side-phishing-detection")
            options.add_argument("--disable-crash-reporter")
            options.add_argument("--disable-oopr-debug-crash-dump")
            options.add_argument("--no-crash-upload")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-low-res-tiling")
            options.add_argument("--silent")

        # Get the Chrome driver
        self.driver = uc.Chrome(
            driver_executable_path=os.path.join(os.getcwd(), 'chromedriver.exe'),
            browser_executable_path=os.path.join(os.getcwd(), 'Chromium', 'Application', 'chromium.exe'),
            options=options,
        )
