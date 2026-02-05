# `listed_company_update.py`

## Purpose
Keeps `other_nepse_detail/listed_company.csv` up-to-date. The CSV drives which companies and sectors the main scraper iterates.

## Dependencies
`requests`, `pandas`, `python-dotenv`

## Run
```bash
python listed_company_update.py
```

## Notes
- Ensure the downloaded `listed_company.csv` is validated; invalid structure can break the main scraper.
