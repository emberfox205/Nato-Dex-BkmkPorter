from csv_IO import retrieve_data, write_data
import re
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def web_setup(browser, full_path, profile):
    option_type = {
        "firefox": FirefoxOptions,
        "edge": EdgeOptions,
        "chrome": ChromeOptions,
    }
    options = option_type[browser]()
    options.add_argument("-headless")
    if browser == "firefox":
        options.profile = full_path
    elif browser in ("edge", "chrome"):
        options.add_argument("--user-data-dir={}".format(full_path))
        options.add_argument("--profile-directory={}".format(profile))
    return options


def init_web(browser, options):
    driver_type = {
        "firefox": webdriver.Firefox,
        "edge": webdriver.Edge,
        "chrome": webdriver.Chrome,
    }
    driver = driver_type[browser](options=options)
    # Get site and prepare
    driver.get("https://manganato.com/bookmark")
    driver.maximize_window()
    print(f"Webdriver session initialized")
    return driver
    
def quit_web(driver):
    driver.quit()

def scrape(driver):
    limit_page_text = driver.find_element(By.CSS_SELECTOR, ".go-p-end").text.strip()
    limit_page_obj = re.search(r"\((\d+)\)", limit_page_text)
    limit_page = int(limit_page_obj.group(1))
    total_titles_text = driver.find_element(By.CSS_SELECTOR, ".quantitychapter").text.strip()
    total_titles_obj = re.search(r" (\d+) ", total_titles_text)
    limit_page = int(limit_page_obj.group(1))
    total_titles = int(total_titles_obj.group(1))
    print(f"Total number of titles: {total_titles}")
    print(f"Total number of bookmark page(s): {limit_page}")
    data = {"title": [], "manganato": [], "mangadex": []}
    # Scrape and store
    for page_num in range(1, limit_page):
        driver.get(f"https://manganato.com/bookmark?page={page_num}")
        time.sleep(2)
        all_items = driver.find_elements(By.CLASS_NAME, "bm-title")
        for item in all_items:
            title = item.find_element(By.TAG_NAME, "a").text
            time.sleep(0.5)
            data["title"].append(title)
            data["manganato"] = True
            data["mangadex"] = False
            print(f"Saving: {title}")
        time.sleep(0.5)
    write_data(data)


def upload(driver):
    data = retrieve_data()
    upload_fail = []
    for id in range(0, len(data["title"])):
        title = data["title"][id]
        res = requests.get(f"{"https://api.mangadex.org"}/manga", params={"title": title})
        ids = [manga["id"] for manga in res.json()["data"]]
        try:
            driver.get(f"https://mangadex.org/title/{ids[0]}")
        except IndexError:
            print(f"WARNING :: No result found: {title}")
            upload_fail.append(title)
            continue
        driver.maximize_window()
        print(f"Bookmarking: {title}")
        try:
            driver.find_element(By.CSS_SELECTOR, ".flex-grow-0").click()
        except Exception:
            print(f"Title already uploaded: {title}")
            pass
        time.sleep(0.1)
        try:
            driver.find_element(
                By.CSS_SELECTOR, "button.flex-grow:nth-child(2)"
            ).click()
        except Exception:
            pass
        data["mangadex"][id] = True
    write_data(data)
    if len(upload_fail) > 0:
        print("WARNING :: Titles failed to upload:")
        for fail in upload_fail:
            print(f"WARNING :: No result found: {fail}")
    