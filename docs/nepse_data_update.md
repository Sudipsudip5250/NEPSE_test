# `nepse_data_update.py`

## Purpose
Scrapes historical price data per listed company from public sources and saves per-company CSVs under `Nepse_Data/<Sector>/`.

## Key behavior
- Iterates sectors and symbols from `other_nepse_detail/listed_company.csv`.
- Uses Selenium to navigate company pages and scrape paginated price history tables.
- Skips already-downloaded rows by checking latest date present in each CSV.
- Saves updated CSVs sorted newest-first and reindexes `S.N.`.
- Commits & pushes sector-level updates to Git when changes exist.

## Dependencies
Python packages: `pandas`, `selenium`, `webdriver-manager`, `python-dotenv`, `requests`, `python-dateutil`

## Environment variables
- `USERNAME_GITHUB` — Git username (used for global git config)
- `TOKEN_GITHUB` — GitHub access token (used for push operations)
- `REPO_GITHUB` — Repository name (optional; used for cloning/remotes)
- `USER_EMAIL_GITHUB` — Git user email for commits

## Run
```bash
python nepse_data_update.py
```

## Notes
- Ensure a compatible Chrome installation is available; `webdriver-manager` downloads matching chromedriver.
- In CI, set secrets for the environment variables and don't commit them.
- For debugging or step-by-step runs, open `Nepse_Data_Update.ipynb`.
