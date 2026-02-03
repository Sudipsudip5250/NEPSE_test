# Setup Guide - nepse_data_update.py

## Required .env Variables

Create a `.env` file in the project root directory with the following variables:

```
USERNAME_GITHUB=your_github_username
TOKEN_GITHUB=your_github_token
REPO_GITHUB=Nepal_Stock_Data
USER_EMAIL_GITHUB=your_email@example.com
```

## How to Get These Values

### 1. **GitHub Username**
   - Go to https://github.com/settings/profile
   - Your username is displayed at the top

### 2. **GitHub Token (TOKEN_GITHUB)**
   - Go to https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Give it a name (e.g., "Nepal Stock Data")
   - Select scopes: `repo` (full control)
   - Click "Generate token"
   - **Copy the token** (you won't see it again)
   - Paste it in `.env` as `TOKEN_GITHUB=your_copied_token`

### 3. **GitHub Email**
   - Go to https://github.com/settings/emails
   - Use your primary email address

### 4. **Repo Name**
   - Use: `Nepal_Stock_Data` (this is the repository name)

## .env File Location

Place the `.env` file in the same directory as `nepse_data_update.py`:
```
c:\Users\hp\Desktop\Nepal_Stock_Data\.env
```

## How It Works

1. Script loads `.env` file using `from dotenv import load_dotenv`
2. GitHub credentials are used for:
   - Cloning/pulling the latest data from the repository
   - Updating and committing new NEPSE data
3. The script automatically validates that `TOKEN_GITHUB` exists

## What If TOKEN_GITHUB Is Missing?

Script will show error:
```
❌ Error: GITHUB_TOKEN environment variable is not set.
```

## Installation

Install required package:
```bash
pip install python-dotenv
```

Then run:
```bash
python nepse_data_update.py
```

---

**Note:** Keep your `.env` file private and never commit it to GitHub.
