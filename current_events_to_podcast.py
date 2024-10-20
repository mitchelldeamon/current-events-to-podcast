import os
import requests
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import threading
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
DISCORD_TAG = os.getenv("DISCORD_TAG")


def scrape_events():
    print("Starting event scraping...")
    yesterday = datetime.now() - timedelta(days=1)
    formatted_date = yesterday.strftime(
        '%Y_%B_') + str(int(yesterday.strftime('%d')))
    url = f"https://en.wikipedia.org/wiki/Portal%3ACurrent_events/{formatted_date}"

    response = requests.get(url)
    if response.status_code == 200:
        print("Successfully accessed Wikipedia page.")
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find(
            'div', class_="current-events-content description")
        if content_div:
            print("Found the content div. Extracting information...")
            scraped_content = ""
            for element in content_div.descendants:
                if element.name == 'b':
                    scraped_content += f"Header: {element.get_text(strip=True)}\n"
                elif element.name == 'li':
                    info_text = []
                    for item in element.contents:
                        if item.name == 'a' and item.get('href'):
                            info_text.append(item.get_text(strip=True))
                        elif item.name is None:
                            info_text.append(item.strip())
                    information = " ".join(info_text).strip()
                    if information:
                        scraped_content += f"Information: {information}\n"
            print("Finished extracting information.")
            return scraped_content
        else:
            print("Content div not found.")
    else:
        print(
            f"Failed to retrieve the webpage. Status code: {response.status_code}")
    return None


def simulate_typing(textarea, text):
    print("Simulating typing...")
    for char in text:
        textarea.send_keys(char)
    print("Finished typing the content.")


def open_chrome_and_login(url, scraped_content):
    print("Setting up Chrome options...")
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")

    print("Initializing ChromeDriver...")
    driver = uc.Chrome(version_main=129, options=options)

    driver.get(url)
    print(f"Opened URL: {url}")
    time.sleep(5)  # Allow initial page to load

    try:
        # Login sequence
        print("Waiting for the email input field...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input = driver.find_element(By.ID, "identifierId")
        email_input.send_keys(EMAIL)
        print("Entered email.")
        time.sleep(2)

        print("Clicking 'Next' button after email entry...")
        next_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//button[contains(@class, 'VfPpkd-LgbsSe') and .//span[text()='Next']]")
            )
        )
        next_button.click()
        time.sleep(5)

        # Wait for the password field
        print("Waiting for the password input field...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "Passwd"))
        )
        password_input = driver.find_element(By.NAME, "Passwd")
        password_input.send_keys(PASSWORD)
        print("Entered password.")
        time.sleep(2)

        print("Clicking 'Next' button after password entry...")
        next_password_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//button[contains(@class, 'VfPpkd-LgbsSe') and .//span[text()='Next']]")
            )
        )
        next_password_button.click()
        time.sleep(5)

        # Wait for and click the '+' button
        print("Waiting for the '+' button to be clickable...")
        plus_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[contains(@class, 'project-button-box-icon') and text()='+']")
            )
        )
        driver.execute_script("arguments[0].click();", plus_button)
        print("Clicked the '+' button.")
        time.sleep(2)

        # Wait for and click the "Copied text" button
        print("Waiting for the 'Copied text' button...")
        copied_text_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Copied text']")
            )
        )
        driver.execute_script("arguments[0].click();", copied_text_button)
        print("Clicked the 'Copied text' button.")
        time.sleep(2)

        # Wait for the textarea to be present and type the content
        print("Waiting for the textarea to be present...")
        textarea = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "mat-input-0"))
        )
        simulate_typing(textarea, scraped_content)
        time.sleep(2)

        # Submit the content
        print("Submitting the content...")
        textarea.send_keys(Keys.TAB)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        time.sleep(5)

        # NEW CODE: Wait for the "Generate" button and click it
        print("Waiting for the 'Generate' button...")
        generate_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//span[@class='mdc-button__label' and text()='Generate']")
            )
        )
        driver.execute_script("arguments[0].click();", generate_button)
        print("Clicked the 'Generate' button.")
        time.sleep(2)

        # Wait for the 'ios_share' icon to appear and click it
        while True:
            try:
                print("Waiting for the 'ios_share' icon...")
                ios_share_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//mat-icon[text()='ios_share']")
                    )
                )
                driver.execute_script(
                    "arguments[0].click();", ios_share_button)
                print("Clicked the 'ios_share' icon.")
                time.sleep(2)
                break
            except Exception:
                print("Waiting for 'ios_share' icon...")
                time.sleep(10)

        # Wait for and click the switch button
        print("Waiting for the switch button...")
        switch_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//button[@role='switch' and contains(@class, 'mdc-switch')]")
            )
        )
        driver.execute_script("arguments[0].click();", switch_button)
        print("Clicked the switch button.")
        time.sleep(2)

        # Extract the generated link and send it to Discord
        print("Extracting the generated link...")
        copied_link = driver.execute_script(
            "return document.querySelector('.share-actions a').getAttribute('href');"
        )

        base_url = "https://notebooklm.google.com"
        full_link = base_url + \
            copied_link if copied_link.startswith('/') else copied_link
        print(f"Extracted link: {full_link}")

        print("Sending the link to Discord...")
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json={"content": f"{DISCORD_TAG} Here is today's podcast link: {full_link}"}
        )

        if response.status_code == 204:
            print("Link successfully sent to Discord.")
        else:
            print(
                f"Failed to send link to Discord. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred during login or scraping: {e}")
    finally:
        print("Closing the browser...")
        driver.quit()


def start_scrape_process():
    try:
        print("Starting the scraping process...")
        content = scrape_events()
        if content:
            print("Opening Chrome and logging in...")
            open_chrome_and_login("https://notebooklm.google.com", content)
            print("Scraping and file upload completed!")
        else:
            print("No content found.")
    except Exception as e:
        print(f"Error during scraping process: {e}")


# Start the scraping process directly
if __name__ == "__main__":
    start_scrape_process()
