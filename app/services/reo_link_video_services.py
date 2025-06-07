import os
import time
import glob
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

class Reo_Link_Services():
    def retrieve_footage(self) -> str:
        """
        This is deisgned to retrieve the latest footage from Reolink 
        and store it in the footage folder (found in the root dir)
        """

        print("------------- Setting up download env")

        email = "abdllaa165@gmail.com"
        password = "3pa-4ccess!"

        # Set up download directory
        download_dir = os.path.join(os.getcwd(), "footage")
        os.makedirs(download_dir, exist_ok=True)
        print(f"Download directory set to: {download_dir}")

        # Set Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)

        print("------------- Launching browser")
        # Launch browser
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        try:
            print("------------- Opening login page")
            # Open Reolink Cloud
            driver.get("https://cloud.reolink.com/user/cloud-library/")
            time.sleep(5)

            print("------------- Locating login fields and submitting credentials")
            # Log in
            email_input = driver.find_element(By.ID, "email")
            password_input = driver.find_element(By.ID, "password")
            email_input.send_keys(email)
            password_input.send_keys(password)
            driver.find_element(By.CSS_SELECTOR, 'button.login-button').click()

            print("------------- Logging in")
            time.sleep(5)

            print("------------- Searching for the first available video")
            # Navigate to first video
            video_list = driver.find_element(By.CLASS_NAME, "video-list")
            first_video_wrap = video_list.find_element(By.CLASS_NAME, "wrap")
            video_link_tag = first_video_wrap.find_element(By.CSS_SELECTOR, "a.cover")
            video_href = video_link_tag.get_attribute("href")
            driver.get(video_href)

            print(f"Navigated to video playback page: {video_href}")
            time.sleep(3)

            print("------------- Extracting direct video URL")
            # Extract direct video URL
            download_element = driver.find_element(By.XPATH, "//video[@src]")
            video_url = download_element.get_attribute("src")
            print(f"Direct video URL: {video_url}")
            driver.get(video_url)

            print("------------- Waiting for download to begin")
            time.sleep(5)

            print("------------- Checking for downloaded files")
            # Rename downloaded file to footage_X.mp4
            downloaded_files = sorted(
                glob.glob(os.path.join(download_dir, "*.mp4")),
                key=os.path.getmtime,
                reverse=True
            )

            if downloaded_files:
                latest_file = downloaded_files[0]
                existing = glob.glob(os.path.join(download_dir, "footage_*.mp4"))
                next_number = len(existing) + 1
                new_name = f"footage_{next_number}.mp4"
                new_path = os.path.join(download_dir, new_name)

                os.rename(latest_file, new_path)
                print(f"Video downloaded: {new_name}")
                
                time.sleep(5)
                print("------------- DONE")
                return new_name
            else:
                raise FileNotFoundError("No .mp4 files found")

        except Exception as e:
            print("------------- An error occurred during execution")
            raise RuntimeError(f"Error: {e}")
        finally:
            print("------------- Cleaning up and closing browser")
            driver.quit()



