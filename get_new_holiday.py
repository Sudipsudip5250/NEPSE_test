"""
This code will update new holiday list including weekend holidays (Friday & Saturday)
Runs on the 1st of every month via GitHub Actions
"""

import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
import subprocess

load_dotenv()

# GitHub Credentials
GITHUB_USERNAME = os.getenv("USERNAME_GITHUB")
GITHUB_TOKEN = os.getenv("TOKEN_GITHUB")
GITHUB_REPO = os.getenv("REPO_GITHUB")
GITHUB_USER_EMAIL = os.getenv("USER_EMAIL_GITHUB")

# Verify GITHUB_TOKEN is set
if not GITHUB_TOKEN:
    print("❌ Error: GITHUB_TOKEN environment variable is not set.")
    exit(1)

IN_COLAB = 'google.colab' in sys.modules

# Determine root path depending on environment
if IN_COLAB:
    root_path = "/content"
else:
    try:
        root_path = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        root_path = os.getcwd()

print(f"📂 Root path set to: {root_path}")
os.chdir(root_path)

# Step 1: Set Git user credentials
os.system(f"git config --global user.email {GITHUB_USER_EMAIL}")
os.system(f"git config --global user.name {GITHUB_USERNAME}")

print("="*70)
print("🔄 Starting Holiday Calendar Update Process")
print("="*70)

# --- Part 0: Load existing calendar (local or GitHub) ---

CALANDER_CSV_PATH = "other_nepse_detail/trading_calendar.csv"
CALANDER_GITHUB_RAW = "https://raw.githubusercontent.com/Sudipsudip5250/Nepal_Stock_Data/main/other_nepse_detail/trading_calendar.csv"

if os.path.exists(CALANDER_CSV_PATH):
    calendar_df = pd.read_csv(CALANDER_CSV_PATH, parse_dates=['Date'])
    print(f"✅ Loaded local {CALANDER_CSV_PATH}")
else:
    calendar_df = pd.read_csv(CALANDER_GITHUB_RAW, parse_dates=['Date'])
    print(f"✅ Fetched calendar from GitHub")

calendar_df['date_str'] = calendar_df['Date'].dt.strftime("%Y-%m-%d")

# --- Part 1: Add Weekend Holidays (Friday & Saturday) ---

print(f"\n{'='*70}")
print(f"📅 Processing Weekend Holidays")
print(f"{'='*70}")

# Get the current date and determine which months to process
current_date = datetime.now()
start_date = calendar_df['Date'].min()
end_date = calendar_df['Date'].max()

print(f"📊 Calendar date range: {start_date.date()} to {end_date.date()}")

# Function to add weekend holidays for a given month
def add_weekend_holidays_for_month(year, month, calendar_df):
    """
    Add weekend holidays (Friday and Saturday) for a given month
    """
    month_name = datetime(year, month, 1).strftime("%B %Y")
    print(f"\n🔍 Processing {month_name}...")
    
    # Get first and last day of the month
    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    # Get all dates in the month
    current = first_day
    weekends_added = 0
    weekends_existing = 0
    weekends_corrected = 0
    
    while current <= last_day:
        date_str = current.strftime("%Y-%m-%d")
        weekday = current.weekday()
        
        # Friday = 4, Saturday = 5
        if weekday in [4, 5]:
            # Check if date exists in calendar
            mask = calendar_df['date_str'] == date_str
            
            if mask.any():
                # Date exists - check if it's correctly marked as weekend
                existing_row = calendar_df[mask].iloc[0]
                is_trading_day = existing_row['IsTradingDay']
                holiday_name = existing_row['HolidayName']
                
                if is_trading_day == False:
                    # Already marked as non-trading day (weekend or holiday)
                    # Only update HolidayName to "Weekend" if it's empty/None (don't overwrite public holidays)
                    if pd.isna(holiday_name) or holiday_name == '' or holiday_name == 'Weekend':
                        if holiday_name != 'Weekend':
                            calendar_df.loc[mask, 'HolidayName'] = 'Weekend'
                            weekends_corrected += 1
                            print(f"  ✏️ Corrected {date_str} to Weekend")
                        else:
                            weekends_existing += 1
                    else:
                        # Already has a public holiday name - don't overwrite it
                        weekends_existing += 1
                else:
                    # IsTradingDay is True but it's a weekend - correct it
                    calendar_df.loc[mask, 'IsTradingDay'] = False
                    calendar_df.loc[mask, 'HolidayName'] = 'Weekend'
                    weekends_corrected += 1
                    print(f"  ✏️ Corrected {date_str} to Weekend")
            else:
                # Date doesn't exist - add it
                new_row = pd.DataFrame([{
                    'Date': current,
                    'IsTradingDay': False,
                    'HolidayName': 'Weekend'
                }])
                calendar_df = pd.concat([calendar_df, new_row], ignore_index=True)
                weekends_added += 1
                print(f"  ➕ Added {date_str} as Weekend")
        
        current += timedelta(days=1)
    
    print(f"  📊 Summary for {month_name}:")
    print(f"    - Existing weekends: {weekends_existing}")
    print(f"    - Added weekends: {weekends_added}")
    print(f"    - Corrected weekends: {weekends_corrected}")
    
    return calendar_df, weekends_added, weekends_corrected

# Process current month and future months up to the calendar end date
total_added = 0
total_corrected = 0

# Process from current month to the last month in calendar
current_month = current_date.replace(day=1)
end_month = end_date.replace(day=1)

while current_month <= end_month:
    calendar_df, added, corrected = add_weekend_holidays_for_month(
        current_month.year, 
        current_month.month, 
        calendar_df
    )
    total_added += added
    total_corrected += corrected
    current_month += relativedelta(months=1)

print(f"\n✅ Weekend Processing Complete:")
print(f"  - Total weekends added: {total_added}")
print(f"  - Total weekends corrected: {total_corrected}")

# Update date_str after modifications
calendar_df['date_str'] = calendar_df['Date'].dt.strftime("%Y-%m-%d")

# --- Part 2: Scrape Public Holidays from Website ---

print(f"\n{'='*70}")
print(f"🌐 Scraping Public Holidays from Website")
print(f"{'='*70}")

# Store existing holidays for comparison
existing_holidays = set(zip(
    calendar_df['date_str'],
    calendar_df['HolidayName']
))

# Determine which years to scrape
start_year = calendar_df['Date'].dt.year.max()
years_to_scrape = list(range(start_year, 2006, -1))

print(f"📅 Will scrape years: {', '.join(map(str, years_to_scrape))}")

# Static page counts per year (adjust if the site changes)
page_counts = {
    2007: 7, 2008: 31, 2009: 32, 2010: 32, 2011: 32, 2012: 32, 2013: 30,
    2014: 6, 2015: 6, 2016: 4, 2017: 4, 2018: 3, 2019: 3, 2020: 11,
    2021: 3, 2022: 4, 2023: 4, 2024: 4, 2025: 5, 2026: 2
}

# Configure Selenium WebDriver
# NOTE: Headless mode is disabled because ng-select dropdown doesn't initialize properly in headless mode
# Instead, we use direct URL navigation to bypass the dropdown interaction issue
print(f"\n🔧 Configuring browser...")
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-application-cache")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_page_load_timeout(30)

print(f"✅ Browser configured successfully")

try:
    driver.get("https://nepalstock.com.np/holiday-listing")
    print(f"✅ Loaded holiday listing page")
    # Wait for Angular to render completely
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    time.sleep(5)  # Additional wait for ng-select to initialize

    def select_year(year):
        """Select year by navigating directly to URL with year parameter"""
        try:
            # Instead of interacting with ng-select (which doesn't work well in headless mode),
            # navigate directly to the URL with year parameter
            url_with_year = f"https://www.nepalstock.com.np/holiday-listing?fiscalYear={year}"
            driver.get(url_with_year)
            
            # Wait for page to load and table to be present
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "table"))
            )
            time.sleep(2)
            return True
        except Exception as e:
            print(f"  ⚠️ Error navigating to year {year}: {e}")
            return False

    def go_to_page(page_num):
        """Navigate to specific page"""
        try:
            # Try to find pagination link with scroll and click
            page_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    f"//li/a/span[contains(text(),'{page_num}')] | //a[contains(@ng-click, 'pageNumber')]/span[text()='{page_num}']"
                ))
            )
            driver.execute_script("arguments[0].scrollIntoView();", page_link)
            time.sleep(1)
            page_link.click()
            time.sleep(2)
            return True
        except Exception as e:
            print(f"  ⚠️ Error navigating to page {page_num}: {e}")
            return False

    def scrape_table():
        """Scrape holiday data from current page"""
        try:
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
        except Exception as e:
            print(f"  ⚠️ Error scraping table: {e}")
            return []

    all_new = []

    for idx, year in enumerate(years_to_scrape):
        print(f"\n📅 Scraping {year}...")
        
        if not select_year(year):
            print(f"  ❌ Failed to select year {year}, skipping...")
            continue

        year_new = []
        max_pages = page_counts.get(year, 1)

        for page in range(1, max_pages + 1):
            if page > 1:
                if not go_to_page(page):
                    print(f"  ⏹️ No page {page}, stopping year {year}")
                    break

            print(f"  📄 Scraping page {page}/{max_pages}")
            page_data = scrape_table()

            if not page_data:
                print(f"  ⏹️ No data on page {page}, stopping year {year}")
                break

            new_entries = []
            for e in page_data:
                key = (e['Holiday Date'], e['Holiday Description'])
                if key not in existing_holidays:
                    new_entries.append(e)
                    existing_holidays.add(key)

            if not new_entries:
                print(f"  ✅ No new entries on page {page}")
                if page == 1:  # If first page has no new entries, stop processing this year
                    break
            else:
                print(f"  ➕ Found {len(new_entries)} new holiday(s)")
                year_new.extend(new_entries)

        all_new.extend(year_new)

        # Decide whether to continue scraping earlier years
        if idx == 0:
            # Always check the second year
            continue

        if len(year_new) == 0:
            print(f"  ⏹️ No new entries in {year}, stopping further scraping")
            break

finally:
    driver.quit()
    print(f"\n✅ Browser closed")

# --- Part 3: Merge new public holidays into calendar_df ---

print(f"\n{'='*70}")
print(f"💾 Merging New Public Holidays")
print(f"{'='*70}")

if all_new:
    print(f"➕ Found {len(all_new)} new public holiday(s)")
    
    new_df = pd.DataFrame(all_new)
    new_df['Date'] = pd.to_datetime(new_df['Holiday Date'])

    for _, row in new_df.iterrows():
        d = row['Date']
        desc = row['Holiday Description']
        date_str = d.strftime("%Y-%m-%d")
        
        mask = calendar_df['Date'] == d
        if mask.any():
            # Update existing entry
            calendar_df.loc[mask, 'IsTradingDay'] = False
            calendar_df.loc[mask, 'HolidayName'] = desc
            print(f"  ✏️ Updated {date_str}: {desc}")
        else:
            # Add new entry
            new_row = pd.DataFrame([{
                'Date': d,
                'IsTradingDay': False,
                'HolidayName': desc
            }])
            calendar_df = pd.concat([calendar_df, new_row], ignore_index=True)
            print(f"  ➕ Added {date_str}: {desc}")
else:
    print("ℹ️ No new public holidays found")

# --- Part 4: Save Updated Calendar ---

print(f"\n{'='*70}")
print(f"💾 Saving Updated Calendar")
print(f"{'='*70}")

# Remove temporary column and sort
calendar_df = calendar_df.drop(columns=['date_str'], errors='ignore')
calendar_df = calendar_df.sort_values('Date', ascending=False).reset_index(drop=True)
calendar_df.to_csv(CALANDER_CSV_PATH, index=False)

print(f"✅ Saved to {CALANDER_CSV_PATH}")
print(f"📊 Total records: {len(calendar_df)}")

# --- Part 5: Git Operations ---

print(f"\n{'='*70}")
print(f"📤 Committing Changes to Git")
print(f"{'='*70}")

# Prepare commit message
changes_made = []
if total_added > 0:
    changes_made.append(f"{total_added} weekend(s) added")
if total_corrected > 0:
    changes_made.append(f"{total_corrected} weekend(s) corrected")
if len(all_new) > 0:
    changes_made.append(f"{len(all_new)} public holiday(s) added")

if changes_made:
    commit_message = f"Updated holiday calendar: {', '.join(changes_made)}"
else:
    commit_message = "Holiday calendar checked - no changes needed"

print(f"📝 Commit message: {commit_message}")

# Git add
result = subprocess.run("git add other_nepse_detail/trading_calendar.csv", shell=True, capture_output=True, text=True)
print(f"Git add: {result.stdout if result.stdout else 'Done'}")
if result.returncode != 0:
    print(f"❌ Git add failed: {result.stderr}")
    exit(1)

# Git commit
# result = subprocess.run(f'git commit -m "{commit_message}" --allow-empty', shell=True, capture_output=True, text=True)
# print(f"Git commit: {result.stdout if result.stdout else 'Done'}")
# if result.returncode != 0:
#     print(f"❌ Git commit failed: {result.stderr}")
#     exit(1)

# Git push
# result = subprocess.run("git push origin main", shell=True, capture_output=True, text=True)
# print(f"Git push: {result.stdout if result.stdout else 'Done'}")
if result.returncode != 0:
    print(f"❌ Git push failed: {result.stderr}")
    exit(1)

print(f"\n{'='*70}")
print(f"🎉 Holiday Calendar Update Completed Successfully!")
print(f"{'='*70}")
print(f"\n📊 Final Summary:")
print(f"  - Weekend holidays added: {total_added}")
print(f"  - Weekend holidays corrected: {total_corrected}")
print(f"  - Public holidays added: {len(all_new)}")
print(f"  - Total calendar entries: {len(calendar_df)}")