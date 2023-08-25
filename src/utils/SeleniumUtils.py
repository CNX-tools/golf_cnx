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
            options.add_argument("--disable-gpu")

        # Get the Chrome driver
        self.driver = uc.Chrome(
            driver_executable_path=os.path.join(os.getcwd(), 'chromedriver.exe'),
            browser_executable_path=os.path.join(os.getcwd(), 'Chromium', 'Application', 'chromium.exe'),
            options=options)
