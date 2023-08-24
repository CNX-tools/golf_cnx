import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
import zipfile
import os


class UserActivity():
    def __init__(self, **kwargs):
        """
        Constructor ~
        - If you don't mention the user profile, this will open a browser with an new user profile
        - Remember that, if you want to open a browser with an existing profile, then you must to CLOSE all Chrome windows first
        Kwargs:
            profile_dir (string): The link to the profile folder  
            profile_name (string): The name of the profile (If not mentioned, the default value is "Default")
            proxy (string): Proxy you want to connect (IP:port)
        """

        # Add options to the Chrome driver
        options = uc.ChromeOptions()

        options.add_argument("--log-level=3")

        # Headless mode
        # options.add_argument("--headless")
        # options.add_argument("--disable-gpu")

        if "profile_dir" in kwargs:
            profile_dir = kwargs.get("profile_dir")
            profile_name = kwargs.get("profile_name", "Default")

            # Add profile arguments
            options.add_argument(f"--user-data-dir={profile_dir}")
            options.add_argument(f"--profile-directory={profile_name}")

        if "proxy" in kwargs:
            proxy = kwargs.get("proxy")
            options.add_argument(f"--proxy-server={proxy}")

        if "download_location" in kwargs:
            location = kwargs.get("download_location")
            prefs = {'download.default_directory': f'{location}'}
            options.add_experimental_option('prefs', prefs)

        if "proxy_auth" in kwargs:
            proxy_data = kwargs.get('proxy_auth')
            print(proxy_data)
            host = proxy_data['host']
            port = proxy_data['port']
            user = proxy_data['user']
            password = proxy_data['password']

            pluginfile = 'proxy_auth_plugin.zip'

            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", get_background_js(
                    host, port, user, password))
            options.add_extension(pluginfile)

        if "unpacked_extension_path" in kwargs:
            unpacked_extension_path = kwargs.get("unpacked_extension_path")
            options.add_argument("--load-extension=" + unpacked_extension_path)

        if "extension_path" in kwargs:
            extension_path = kwargs.get("extension_path")
            options.add_extension(extension=extension_path)

        # Get the Chrome driver
        self.driver = uc.Chrome(
            driver_executable_path=os.path.join(os.getcwd(), 'chromedriver.exe'),
            browser_executable_path=r'C:\Users\Thinkbook 14 G3 ACL\AppData\Local\Chromium\Application\chrome.exe',
            options=options)
