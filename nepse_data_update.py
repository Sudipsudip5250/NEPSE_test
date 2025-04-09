import csv
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import requests
import sys
from dotenv import load_dotenv

load_dotenv()
# GitHub Credentials
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

IN_COLAB = 'google.colab' in sys.modules # Detect if we're in Colab
# Determine root path depending on environment
if IN_COLAB:
    root_path = "/content"
else:
    try:
        root_path = os.path.dirname(os.path.abspath(__file__)) # For local: use script location or current working directory
    except NameError:
        # For interactive sessions like Jupyter
        root_path = os.getcwd()

print(f"📂 Root path set to: {root_path}")
os.chdir(root_path)

# Define path to repo folder
folder_path = os.path.join(root_path, GITHUB_REPO)

# Step 1: Check if the repo folder exists and remove the remote link
if os.path.exists(folder_path):
    print("✅ Old repository folder found!")
else:
    print("📁 Repository folder does not exist. Proceeding to clone.")
    clone_cmd = f"git clone https://github.com/Sudipsudip5250/Nepal_Stock_Data.git"
    os.system(clone_cmd)
    print("Cloned successfully!")

# Step 3: Set Git user credentials
os.chdir(folder_path)  # Move into the cloned repo
os.system("git config user.email 'you@example.com'")
os.system("git config user.name 'Your Name'")

# Step 4: Reset the remote URL
remote_cmd = f'git remote set-url origin https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git'
os.system(remote_cmd)

print("Repository reset and cloned successfully!")

# Define base directory
BASE_FOLDER = "Nepse_Data"
listed_company = "other_nepse_detail/listed_company.csv"

# GitHub raw file URL
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Sudipsudip5250/Nepal_Stock_Data/main/other_nepse_detail/listed_company.csv"

# Check if the file exists
if not os.path.exists(listed_company):
    print(f"⚠ File '{listed_company}' not found! Downloading from GitHub...")

    try:
        response = requests.get(GITHUB_RAW_URL, timeout=10)
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)

        with open(listed_company, "wb") as file:
            file.write(response.content)

        print(f"✅ Successfully downloaded '{listed_company}' from GitHub.")

    except requests.RequestException as e:
        print(f"❌ Failed to download file: {e}")
        exit(1)  # Exit script if download fails

# Read the CSV file
with open(listed_company, 'r', encoding='utf-8') as file:
    reader = list(csv.reader(file))
    categories = reader[0]
    symbols_by_category = list(zip(*reader[1:]))
print("✅ Successfully loaded symbol data.")

# Configure Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # New headless mode (recommended)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 3)

# Process each category and its symbols
for category, symbols in zip(categories, symbols_by_category):
    if not category.strip():
        continue

    category_folder = os.path.join(BASE_FOLDER, category.strip())
    os.makedirs(category_folder, exist_ok=True)

    for symbol in symbols:
        symbol = symbol.strip()
        if not symbol:
            continue

        csv_filename = os.path.join(category_folder, f"{symbol}.csv")
        url = f"https://www.sharesansar.com/company/{symbol}"
        driver.get(url)
        time.sleep(1)

        try:
            price_history_button = wait.until(EC.element_to_be_clickable((By.ID, "btn_cpricehistory")))
            price_history_button.click()
            time.sleep(1)
        except Exception as e:
            print(f"Error accessing price history for {symbol}: {e}")
            continue

        try:
            select_element = wait.until(EC.presence_of_element_located((By.NAME, "myTableCPriceHistory_length")))
            Select(select_element).select_by_value("50")
            time.sleep(1)
        except Exception as e:
            print(f"Failed to change display option for {symbol}: {e}")
            continue

        # Determine the latest date already present (if any)
        latest_date = None
        if os.path.exists(csv_filename):
            try:
                existing_df = pd.read_csv(csv_filename, encoding="utf-8")
                latest_date = existing_df["Date"].astype(str).max()
                print(f"📌 {symbol}: Latest data in CSV is from {latest_date}")
            except Exception as e:
                print(f"Error reading {csv_filename}: {e}")

        new_data = []
        page_count = 0
        stop_scraping = False

        # Loop until the "Next" button is disabled or no longer available
        while True:
            page_count += 1
            print(f"Scraping {symbol} - processing page {page_count}")
            try:
                # Re-locate the table on each page to avoid stale element reference
                table = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='cpricehistory']//table")))
                rows = table.find_elements(By.XPATH, ".//tbody/tr")

                # Iterate through rows and extract data
                for row in rows:
                    # Re-locate cells within each row
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) < 9:
                        continue

                    data = [cell.text.strip() for cell in cells]
                    row_date = data[1]

                    # If we already have data and this row is not new, flag to stop scraping further pages
                    if latest_date and row_date <= latest_date:
                        stop_scraping = True
                        break
                    new_data.append(data)

            except Exception as e:
                print(f"No table found for {symbol}: {e}")
                break

            if stop_scraping:
                print(f"Stopping further scraping for {symbol} as older data encountered.")
                break

            # Try to find and click the "Next" button; if not available or disabled, break the loop
            try:
                next_button = driver.find_element(By.XPATH, "//a[contains(text(),'Next')]")
                if "disabled" in next_button.get_attribute("class").lower():
                    print("Next button is disabled. Reached last page.")
                    break
                next_button.click()
                time.sleep(1)  # You might need to adjust the wait time
            except Exception:
                print("No 'Next' button found or an error occurred. Ending pagination.")
                break

        if new_data:
            new_df = pd.DataFrame(new_data, columns=["S.N.", "Date", "Open", "High", "Low", "Ltp", "% Change", "Qty", "Turnover"])
            latest_scraped_date = new_df["Date"].max()  # Get the latest date from new data

            if os.path.exists(csv_filename):
                updated_df = pd.concat([new_df, existing_df], ignore_index=True)
            else:
                updated_df = new_df

            # Optional: convert Date column to datetime and sort (adjust ascending/descending as needed)
            updated_df["Date"] = pd.to_datetime(updated_df["Date"], format="%Y-%m-%d", errors="coerce")
            # Sort so that the newest dates appear first; change ascending=True for oldest-first
            updated_df = updated_df.sort_values(by="Date", ascending=False).reset_index(drop=True)
            # Reassign S.N. sequentially starting from 1
            updated_df["S.N."] = updated_df.index + 1
            # Rearrange columns to place S.N. first
            cols = ["S.N.", "Date", "Open", "High", "Low", "Ltp", "% Change", "Qty", "Turnover"]
            updated_df = updated_df[cols]

            # Save updated CSV file
            updated_df.to_csv(csv_filename, index=False, encoding='utf-8')
            print(f"✅ New data added for {symbol} in {csv_filename}")

            # Git Add, Commit, and Push with latest scraped date
            print(os.system("git add --all"))
            commit_message = f'Updated {symbol} data up to {latest_scraped_date}' if latest_scraped_date else f'Updated {symbol} data'
            print(os.system(f'git commit -m "{commit_message}" --allow-empty'))
            # print(os.system("git push origin main"))
            print("\n")
        else:
            print(f"⚠ No new data found for {symbol}. Skipping update.")
    print(os.system("git push origin main"))

driver.quit()
print("✅ Scraping completed for all symbols.")
