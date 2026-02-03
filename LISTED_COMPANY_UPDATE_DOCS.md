# Listed Company Update Script Documentation

## Overview
The `listed_company_update.py` script scrapes the latest company listings from ShareSansar and updates the `other_nepse_detail/listed_company.csv` file.

---

## Features

### ✅ Comprehensive Sector Coverage
- Automatically detects all available sectors from the website dropdown
- Processes each sector individually
- Handles new sectors that may be added in the future

### ✅ Multi-Page Scraping
- Automatically sets display to maximum (50 entries per page)
- Navigates through all pages until the "Next" button is disabled
- Waits for page loading between operations

### ✅ Smart Data Organization
- Sorts all symbols alphabetically within each sector
- Maps website sector names to CSV format (using underscores)
- Maintains consistent column order

### ✅ Git Integration
- Automatically commits and pushes changes
- Uses environment variables for credentials
- Single commit after all sectors are processed

---

## How It Works

### 1. **Sector Discovery**
```
- Loads https://www.sharesansar.com/company-list
- Extracts all sector options from dropdown
- Processes each sector one by one
```

### 2. **Data Scraping Per Sector**
```
For each sector:
  - Select sector from dropdown
  - Click "Search" button
  - Wait for data to load (3 seconds)
  - Change display to 50 entries
  - Wait for table reload (2 seconds)
  
  For each page:
    - Extract all symbols from the table
    - Check if "Next" button is available/enabled
    - If available: Click and wait (2 seconds), continue
    - If disabled/unavailable: Stop pagination
  
  - Sort all collected symbols alphabetically
  - Store in memory
```

### 3. **CSV Generation**
```
- Determine maximum rows needed across all sectors
- Create header row with sector names
- Write data rows:
  - Each column represents a sector
  - Symbols are sorted alphabetically
  - Empty cells where sectors have fewer companies
```

### 4. **Git Operations**
```
- git add other_nepse_detail/listed_company.csv
- git commit -m "Updated listed company data"
- git push origin main
```

---

## Sector Name Mapping

The script automatically converts website sector names to CSV-compatible format:

| Website Sector Name | CSV Column Name |
|---------------------|-----------------|
| Commercial Bank | Commercial_Banks |
| Corporate Debentures | Corporate_Debentures |
| Development Bank | Development_Bank_Limited |
| Finance | Finance |
| Government Bonds | Government_Bonds |
| Hotel & Tourism | Hotels_And_Tourism |
| Hydropower | Hydro_Power |
| Investment | Investment |
| Life Insurance | Life_Insurance |
| Manufacturing and Processing | Manufacturing_And_Processing |
| Microfinance | Microfinance |
| Mutual Fund | Mutual_Fund |
| Non-Life Insurance | Non-Life_Insurance |
| Others | Others |
| Preference Share | Preference_Share |
| Promotor Share | Promotor_Share |
| Trading | Tradings |

**Note:** Any new sectors not in this mapping will be automatically converted by:
- Replacing spaces with underscores
- Replacing "&" with "And"

---

## Timing & Wait Periods

The script includes strategic wait times to ensure proper page loading:

| Action | Wait Time | Reason |
|--------|-----------|--------|
| Initial page load | 3 seconds | Allow website to fully load |
| After selecting sector | 1 second | Dropdown selection |
| After clicking Search | 3 seconds | Table data loading |
| After changing display to 50 | 2 seconds | Table reload |
| After clicking Next | 2 seconds | Next page loading |

---

## Output Format

The CSV file structure:

```csv
Commercial_Banks,Corporate_Debentures,Development_Bank_Limited,Finance,...
ADBL,SYMBOL1,CORBL,BFC,...
CZBIL,SYMBOL2,EDBL,CFCL,...
EBL,SYMBOL3,GBBL,CMB,...
...
```

- **Row 1**: Sector names (with underscores)
- **Rows 2+**: Company symbols (sorted alphabetically within each column)
- **Empty cells**: Where a sector has fewer companies than the maximum

---

## Error Handling

### Graceful Degradation
- If a sector fails to load: Continue to next sector
- If a page fails to scrape: Move to next sector
- If table reading fails: Log warning and continue
- If git operations fail: Exit with error code

### Logging
The script provides detailed console output:
- ✅ Success messages (green)
- ⚠️ Warning messages (yellow)
- ❌ Error messages (red)
- 📊 Progress indicators
- 📄 Page numbers
- 🔍 Current sector being processed

---

## Usage

### Prerequisites
```bash
# Install required packages
pip install selenium webdriver-manager python-dotenv --break-system-packages
```

### Environment Variables
Create a `.env` file with:
```
USERNAME_GITHUB=your_github_username
TOKEN_GITHUB=your_personal_access_token
REPO_GITHUB=Nepal_Stock_Data
USER_EMAIL_GITHUB=your_email@example.com
```

### Run the Script
```bash
python listed_company_update.py
```

---

## Key Differences from nepse_data_update.py

| Aspect | nepse_data_update.py | listed_company_update.py |
|--------|---------------------|-------------------------|
| **Target File** | Multiple CSV files in Nepse_Data/ | Single file: other_nepse_detail/listed_company.csv |
| **Git Commits** | One per sector | One for entire update |
| **Data Type** | Price history data | Company symbols |
| **Update Frequency** | Daily (stock prices) | As needed (company listings) |
| **Pagination** | Price history pages | Company list pages |
| **Processing** | Sequential by company | Sequential by sector |

---

## Expected Output Example

```
📂 Root path set to: /home/user/Nepal_Stock_Data
============================================================
🔄 Starting Listed Company Update Process
============================================================
✅ Found 17 sectors to process

============================================================
🔍 Processing Sector: Commercial Bank
============================================================
⏳ Waiting for data to load...
✅ Set display to 50 entries
📄 Scraping page 1...
✅ Found 19 symbols on page 1
⏹️ Reached last page (page 1)
✅ Total symbols collected for Commercial_Banks: 19
📊 Symbols: ADBL, CZBIL, EBL, GBIME, HBL, KBL, LSL, MBL, NABIL, NBL...

============================================================
🔍 Processing Sector: Corporate Debentures
============================================================
⏳ Waiting for data to load...
✅ Set display to 50 entries
📄 Scraping page 1...
✅ Found 50 symbols on page 1
➡️ Moving to next page...
📄 Scraping page 2...
✅ Found 27 symbols on page 2
⏹️ No more pages available
✅ Total symbols collected for Corporate_Debentures: 77
📊 Symbols: BOKD86KA, CBLD88, CZBILP, EBLD85, EBLD86, ...

[... continues for all sectors ...]

============================================================
📝 Writing data to CSV file
============================================================
✅ Found 17 sectors with data
✅ Maximum rows needed: 123
✅ Successfully wrote data to other_nepse_detail/listed_company.csv

============================================================
📊 Summary
============================================================
  Commercial_Banks: 19 companies
  Corporate_Debentures: 77 companies
  Development_Bank_Limited: 16 companies
  Finance: 16 companies
  ... [all sectors]

============================================================
💾 Committing changes to Git
============================================================
Git add output: 
Git commit output: [main abc1234] Updated listed company data
Git push output: 

============================================================
🎉 Listed Company Update Completed Successfully!
============================================================
```

---

## Troubleshooting

### Issue: "Network error" or timeout
**Solution**: The script includes wait times, but you can increase them if needed

### Issue: "Next button not found"
**Solution**: This is normal for single-page sectors - the script handles it gracefully

### Issue: "Sector not in mapping"
**Solution**: New sectors are automatically handled with underscore replacement

### Issue: Git push fails
**Solution**: Check your GitHub token has write permissions and is not expired

---

## Maintenance

### Adding New Sector Mappings
If a new sector needs a specific mapping, add it to the `SECTOR_MAPPING` dictionary:

```python
SECTOR_MAPPING = {
    "New Sector Name": "New_Sector_CSV_Name",
    # ... existing mappings
}
```

### Adjusting Wait Times
If the website becomes slower/faster, adjust the `time.sleep()` values:

```python
time.sleep(3)  # Increase for slower networks
```

---

## Integration with GitHub Actions

This script can be scheduled to run periodically (e.g., weekly) to keep company listings up-to-date:

```yaml
# Example workflow (not included in this update)
schedule:
  - cron: '0 0 * * 0'  # Run every Sunday at midnight
```

---

**Version:** 1.0  
**Last Updated:** February 2026  
**Compatibility:** Python 3.7+, Selenium 4.x
