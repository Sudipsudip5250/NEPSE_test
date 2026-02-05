# `nepse_holiday_update.py`

## Purpose
Builds and maintains a trading calendar that includes weekends and public holidays. Generates:
- `other_nepse_detail/trading_calendar.csv`
- `other_nepse_detail/only_public_holidays.csv`
- `other_nepse_detail/public_and_weekly_holidays.csv`

## Key behavior
- Loads existing calendar (local or from GitHub raw), fills missing months, and ensures weekends are marked.
- Scrapes public holidays from `https://nepalstock.com.np/holiday-listing` using Selenium with dynamic pagination.
- Merges new public holidays into the calendar and saves updated CSVs.
- Commits and pushes only when changes are detected.

## Dependencies
Python packages: `pandas`, `selenium`, `webdriver-manager`, `python-dotenv`, `requests`, `python-dateutil`

## Environment variables
- `USERNAME_GITHUB`, `TOKEN_GITHUB`, `REPO_GITHUB`, `USER_EMAIL_GITHUB`

## Run
```bash
python nepse_holiday_update.py
```

## Notes
- The scraper uses longer waits to allow Angular-driven pages to finish rendering.
- When running in CI, provide Git credentials via secrets and ensure `GITHUB_TOKEN` is set.
