"""
this code will update new holiday list

"""

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# --- Part 0: Load existing calendar (local or GitHub) ---

CALANDER_CSV_PATH = "other_nepse_detail/trading_calendar.csv"
CALANDER_GITHUB_RAW = "https://raw.githubusercontent.com/Sudipsudip5250/Nepal_Stock_Data/main/other_nepse_detail/trading_calendar.csv"

if os.path.exists(CALANDER_CSV_PATH):
    calendar_df = pd.read_csv(CALANDER_CSV_PATH, parse_dates=['Date'])
    print(f"Loaded local {CALANDER_CSV_PATH}")
else:
    calendar_df = pd.read_csv(CALANDER_GITHUB_RAW, parse_dates=['Date'])
    print(f"Fetched calendar from GitHub")

calendar_df['date_str'] = calendar_df['Date'].dt.strftime("%Y-%m-%d")
existing_holidays = set(zip(
    calendar_df['date_str'],
    calendar_df['HolidayName']
))

start_year = calendar_df['Date'].dt.year.max()
years_to_scrape = list(range(start_year, 2006, -1))

# Static page counts per year (adjust if the site changes)
page_counts = {
    2007: 7, 2008: 31, 2009: 32, 2010: 32, 2011: 32, 2012: 32, 2013: 30,
    2014: 6, 2015: 6, 2016: 4, 2017: 4, 2018: 3, 2019: 3, 2020: 11,
    2021: 3, 2022: 4, 2023: 4, 2024: 4, 2025: 2
}

# --- Part 1: Scrape only new holiday data ---

opts = webdriver.ChromeOptions()
opts.add_argument("--disable-application-cache")
driver = webdriver.Chrome(options=opts)
driver.get("https://nepalstock.com.np/holiday-listing")

def select_year(year):
    dropdown = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "ng-select"))
    )[0]
    driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "ng-select")))
    dropdown.click()

    year_option = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class,'ng-dropdown-panel')]//span[text()='%d']" % year
        ))
    )
    year_option.click()
    time.sleep(2)

def go_to_page(page_num):
    page_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.XPATH,
            f"//li/a/span[text()='{page_num}']"
        ))
    )
    driver.execute_script("arguments[0].scrollIntoView();", page_link)
    page_link.click()
    time.sleep(2)

def scrape_table():
    tbl = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.table"))
    )
    rows = tbl.find_elements(By.TAG_NAME, "tr")[1:]
    out = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) == 3:
            out.append({
                "Holiday Date": cols[1].text.strip(),
                "Holiday Description": cols[2].text.strip()
            })
    return out

all_new = []

for idx, year in enumerate(years_to_scrape):
    print(f"\n→ Scraping {year} …")
    select_year(year)

    year_new = []
    max_pages = page_counts.get(year, 1)

    for page in range(1, max_pages + 1):
        if page > 1:
            try:
                go_to_page(page)
            except Exception:
                print(f"    • No page {page}, stopping year {year}")
                break

        print(f"  • Page {page}")
        page_data = scrape_table()

        new_entries = []
        for e in page_data:
            key = (e['Holiday Date'], e['Holiday Description'])
            if key not in existing_holidays:
                new_entries.append(e)
                existing_holidays.add(key)

        if not new_entries:
            print("    – no new entries on this page, stopping year")
            break

        print(f"    + found {len(new_entries)} new")
        year_new.extend(new_entries)

    all_new.extend(year_new)

    # --- decide whether to continue scraping earlier years ---
    if idx == 0:
        # always go on to the second year
        continue

    if len(year_new) == 0:
        print(f"    – no new entries in {year}, stopping further scraping")
        break
    # else: found new entries, so proceed to next year

driver.quit()

# --- Part 2: Merge new holidays into calendar_df ---

if all_new:
    new_df = pd.DataFrame(all_new)
    new_df['Date'] = pd.to_datetime(new_df['Holiday Date'])

    for _, row in new_df.iterrows():
        d = row['Date']
        desc = row['Holiday Description']
        mask = calendar_df['Date'] == d
        if mask.any():
            calendar_df.loc[mask, 'IsTradingDay'] = False
            calendar_df.loc[mask, 'HolidayName'] = desc
        else:
            calendar_df = pd.concat([
                calendar_df,
                pd.DataFrame([{
                    'Date': d,
                    'IsTradingDay': False,
                    'HolidayName': desc
                }])
            ], ignore_index=True)

    calendar_df = calendar_df.drop(columns=['date_str'], errors='ignore')
    calendar_df = calendar_df.sort_values('Date', ascending=False).reset_index(drop=True)
    calendar_df.to_csv(CALANDER_CSV_PATH, index=False)
    print(f"\n✔️  Added {len(all_new)} new holidays and saved to {CALANDER_CSV_PATH}")
else:
    print("\nℹ️  No new holidays found — calendar is up to date.")

print(os.system("git add --all"))
print(os.system(f'git commit -m "Updated holiday in trading calender." --allow-empty'))
print(os.system("git push origin main"))