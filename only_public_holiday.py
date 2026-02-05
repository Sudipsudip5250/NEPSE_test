"""
This code generates only_public_holidays.csv from existing trading_calendar.csv
It extracts only public holidays (excluding weekends) and saves Date,HolidayName
Runs as needed, perhaps via GitHub Actions
"""

import os
import sys
import pandas as pd
from datetime import datetime
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
print("🔄 Starting Holiday Listing Generation Process")
print("="*70)

# --- Load existing calendar ---

CALENDAR_CSV_PATH = "other_nepse_detail/trading_calendar.csv"
ONLY_PUBLIC_HOLIDAYS_CSV_PATH = "other_nepse_detail/only_public_holidays.csv"

if os.path.exists(CALENDAR_CSV_PATH):
    calendar_df = pd.read_csv(CALENDAR_CSV_PATH, parse_dates=['Date'])
    print(f"✅ Loaded {CALENDAR_CSV_PATH}")
else:
    print(f"❌ Error: {CALENDAR_CSV_PATH} not found.")
    exit(1)

# --- Extract public holidays (exclude 'Weekend') ---

print(f"\n📅 Extracting public holidays...")
holiday_df = calendar_df[(calendar_df['IsTradingDay'] == False) & (calendar_df['HolidayName'] != 'Weekend')]
holiday_df = holiday_df[['Date', 'HolidayName']].copy()
holiday_df = holiday_df.sort_values('Date', ascending=False).reset_index(drop=True)

print(f"📊 Found {len(holiday_df)} public holidays")

# --- Save only_public_holidays.csv ---

holiday_df.to_csv(ONLY_PUBLIC_HOLIDAYS_CSV_PATH, index=False)
print(f"✅ Saved to {ONLY_PUBLIC_HOLIDAYS_CSV_PATH}")

# --- Git Operations ---

print(f"\n{'='*70}")
print(f"📤 Committing Changes to Git")
print(f"{'='*70}")

commit_message = "Updated only_public_holidays.csv"

print(f"📝 Commit message: {commit_message}")

# Git add
result = subprocess.run(f"git add {ONLY_PUBLIC_HOLIDAYS_CSV_PATH}", shell=True, capture_output=True, text=True)
print(f"Git add: {result.stdout if result.stdout else 'Done'}")
if result.returncode != 0:
    print(f"❌ Git add failed: {result.stderr}")
    exit(1)

# Git commit
result = subprocess.run(f'git commit -m "{commit_message}"', shell=True, capture_output=True, text=True)
print(f"Git commit: {result.stdout if result.stdout else 'Done'}")
if result.returncode != 0:
    print(f"❌ Git commit failed: {result.stderr}")
    exit(1)

# Git push
result = subprocess.run("git push origin main", shell=True, capture_output=True, text=True)
print(f"Git push: {result.stdout if result.stdout else 'Done'}")
if result.returncode != 0:
    print(f"❌ Git push failed: {result.stderr}")
    exit(1)

print(f"\n{'='*70}")
print(f"🎉 Holiday Listing Generation Completed Successfully!")
print(f"{'='*70}")
print(f"\n📊 Final Summary:")
print(f"  - Public holidays extracted: {len(holiday_df)}")