# 📈 Nepal_Stock_Data Repository

This repository contains structured datasets of companies listed in the **Nepal Stock Exchange (NEPSE)**. The data is categorized by industry sectors and scraped from public websites. It is ideal for:

- 🧠 Machine Learning & AI model training  
- 📊 Financial & statistical analysis  
- 🎓 Academic research and education  
# Nepal_Stock_Data — full project overview

This repository centralizes automated scrapers and supporting tools that collect, normalize, and store historical price and calendar data for companies listed on the Nepal Stock Exchange (NEPSE).

The project aims to provide clean, machine-readable CSV datasets for research, analytics, teaching, and lightweight production use.

Key uses — who benefits
- Data scientists: build and evaluate time-series models (LSTM, Transformer, ARIMA/GARCH, etc.).
- Quant researchers & traders: backtesting strategies, feature engineering, and signal analysis.
- Analysts & dashboard authors: dashboards, sector analysis, KPIs, and visualizations.
- Educators and students: real-world financial time-series for exercises and projects.

Disclaimer
- The data is scraped from public sources (e.g., `sharesansar.com`, `nepalstock.com.np`). If you are a data owner who objects to the collection or publication, contact the maintainer and the data will be removed.

Repository layout (top-level)

- `Nepse_Data/` — per-sector folders containing company CSVs (one CSV per company)
- `other_nepse_detail/` — helper files: `listed_company.csv`, `trading_calendar.csv`, `only_public_holidays.csv`, `public_and_weekly_holidays.csv`
- `nepse_data_update.py` — main scraper that updates company CSVs
- `nepse_holiday_update.py` — builds & updates trading calendar and holiday lists
- `get_new_holiday.py`, `listed_company_update.py`, `company_full_data_get.py` — utilities and helpers
- `Nepse_Data_Update.ipynb` — notebook for interactive runs and debugging
- `requirements.txt` — Python dependencies
- `docs/` — per-script documentation and usage notes

Core data format
- Company CSVs include columns: `S.N.`, `Date`, `Open`, `High`, `Low`, `Ltp`, `% Change`, `Qty`, `Turnover`.
- Date format: ISO `YYYY-MM-DD` (converted to `datetime` when processed).

How the system works (high level)

1. Source list: `other_nepse_detail/listed_company.csv` contains sectors and symbols to process.
2. `nepse_data_update.py` iterates sectors and symbols, navigates to each company's price history page, scrapes paginated tables, and appends only new rows based on the most recent date in the CSV.
3. Each company's CSV is saved with newest dates first and `S.N.` re-indexed.
4. Sector-level commits are created and pushed only when there are actual updates (avoids empty commits).
5. `nepse_holiday_update.py` loads or fetches the trading calendar, ensures weekends are present, scrapes public holidays, merges them, and writes the holiday CSVs. It also commits only when changes occur.

Step-by-step: running locally

1. Create a `.env` file (see `.env.example`) and set required variables:

- `USERNAME_GITHUB` — GitHub username
- `TOKEN_GITHUB` — Personal access token with repo permissions
- `REPO_GITHUB` — repo name (optional)
- `USER_EMAIL_GITHUB` — e-mail to use for Git commits

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the scraper interactively or from the command line:

```bash
python nepse_data_update.py
python nepse_holiday_update.py
```

Or open `Nepse_Data_Update.ipynb` in Jupyter/Colab and run cells step-by-step.

Automation (GitHub Actions)

This project is designed to be automated. A typical setup:

- `nepse_data_update.py` runs daily to capture newly available price rows.
- `nepse_holiday_update.py` runs monthly to refresh the trading calendar and holiday files.

Example workflow snippet (place as `.github/workflows/daily-update.yml`):

```yaml
name: Daily NEPSE Update

on:
	schedule:
		- cron: '0 1 * * *'   # runs daily at 01:00 UTC
	workflow_dispatch: {}

jobs:
	update:
		runs-on: ubuntu-latest
		steps:
			- uses: actions/checkout@v4
			- name: Set up Python
				uses: actions/setup-python@v4
				with:
					python-version: '3.10'
			- name: Install requirements
				run: pip install -r requirements.txt
			- name: Run scraper
				env:
					USERNAME_GITHUB: ${{ secrets.USERNAME_GITHUB }}
					TOKEN_GITHUB: ${{ secrets.TOKEN_GITHUB }}
					REPO_GITHUB: ${{ secrets.REPO_GITHUB }}
					USER_EMAIL_GITHUB: ${{ secrets.USER_EMAIL_GITHUB }}
				run: python nepse_data_update.py
```

CI/Secrets best-practices

- Store credentials as repository secrets and avoid putting tokens in source.
- Use a token with only the permissions needed to push changes.
- Ensure the runner environment has Chrome (or another supported browser) installed for Selenium; `webdriver-manager` will download a matching chromedriver.

How you can use the data (practical examples)

- Train forecasting models: LSTM, GRU, Transformer, or classical ARIMA/GARCH models.
- Backtest trading rules using daily candles and volume data.
- Build dashboards & reports (Plotly, Dash, Streamlit) for sector performance, volume spikes, and top movers.
- Create indices or aggregate metrics by sector or market-cap buckets.
- Research: event studies, volatility analysis, correlation and co-integration tests.
- Education: practical datasets for workshops and assignments.

Development notes & extensions

- The notebook `Nepse_Data_Update.ipynb` mirrors the scripts and is useful for debugging or exploring intermediate data.
- The `docs/` folder contains per-script markdown files describing usage and environment variables.
- Consider adding pinned dependency versions in `requirements.txt` for reproducible CI runs.

Ethics & responsible scraping

- Respect site terms of service and robots.txt when scraping.
- Rate-limit requests and use polite waits; the scripts include wait times for reliability.
- If you are a data owner and object to the scraped publication, contact the maintainer to request removal.

Contributing

- Fork the repo, make changes, and open a pull request.
- Add tests or small validation scripts if you modify scraping logic.
- Report issues and suggest improvements via GitHub Issues.

License & contact

- This project is open-source. Check the repository for an explicit license file (add one if you plan to publish).
- Contact: sudipsudip5250@gmail.com

---

If you'd like, I can:
- pin dependency versions in `requirements.txt`,
- add the example workflow file `.github/workflows/daily-update.yml`, or
- run a quick dependency install check in this environment.

Thanks — tell me which of the above you'd like next.
					TOKEN_GITHUB: ${{ secrets.TOKEN_GITHUB }}
					REPO_GITHUB: ${{ secrets.REPO_GITHUB }}
					USER_EMAIL_GITHUB: ${{ secrets.USER_EMAIL_GITHUB }}
				run: python nepse_data_update.py
```

Secrets and notes:

- Store credentials as repository secrets (`Settings → Secrets`) and never commit them in source control.
- Provide a token with minimal `repo` scope required to push changes.
- Ensure the runner has Chrome available (or use a headless driver compatible with the environment). `webdriver-manager` helps download a matching chromedriver.

If you want, I can add a ready-to-use workflow file to the repository and a short contributing doc that explains how to set secrets.

## Documentation

Per-script docs live in the `docs/` directory. Each markdown file explains purpose, env vars, usage examples, and implementation notes.

## Contributing

- Respect site terms and scraping etiquette
- Do not commit secrets
- Open an issue or PR for improvements

---

If you'd like, I can pin dependency versions in `requirements.txt` or add a GitHub Actions workflow to run scrapers on a schedule.

Thank you — contributions welcome!


**📌 Final Note**
