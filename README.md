# 📈 Nepal_Stock_Data Repository

This repository contains structured datasets of companies listed in the **Nepal Stock Exchange (NEPSE)**. The data is categorized by industry sectors and scraped from public websites. It is ideal for:

- 🧠 Machine Learning & AI model training  
- 📊 Financial & statistical analysis  
- 🎓 Academic research and education  

> ⚠️ **Disclaimer:**  
> The data is scraped from public sources without formal permission. If you're the rightful owner and object to its usage, I sincerely apologize and will remove the content upon request.

---

## 📁 Folder Structure

```bash
Nepal_Stock_Data/
│
├── Nepse_Data/                 # Main dataset files categorized by sectors
├── other_nepse_detail/        # listed company and holiday list
├── Nepse_Data_Update.ipynb    # Notebook to update all data
├── nepse_data_update.py       # Python script for scraping latest data
├── requirements.txt           # Required Python packages
├── .env.example               # Example environment config (optional)
├── .gitignore                 # Git ignored files/folders
└── README.md                  # Project documentation
```

**🔍 About the Project**
The goal of this project is to make NEPSE data more accessible and machine-readable for:

Developers 👨‍💻
Data analysts 📈
Researchers 🧑‍🔬
Students 📚

**📌 What's Included:**
✅ Company-wise historical data
✅ Sector-wise categorization
✅ Year-wise CSV files per company
✅ Machine-learning-ready format

All data is in .csv format, scraped using Python scripts and Jupyter notebooks.

**🌐 Data Sources**
The data is scraped from the following public websites:
🔗 https://nepalstock.com.np
🔗 https://www.sharesansar.com

⚠️ No official affiliation with these platforms.

# **🛠 How It Works**
**▶️ nepse_data_update.py**
Automates scraping of all listed company data.
Iterates over companies and downloads their data
Categorizes by sector and stores in Nepse_Data/

Run it using:
```bash 
python nepse_data_update.py
```
***📓 Nepse_Data_Update.ipynb*** 
This notebook is the visual version of the script. Use it for:
✅ Manual inspection and debugging
✅ Step-by-step learning
✅ Cleaning and saving intermediate data

**🗃️ other_nepse_detail/**
This folder contains all listed company and holiday list.

**Useful for:**
📉 Time-series modeling
🏢 Company-level analysis
📅 Historical trend tracking

**Features**
✅ Sector-based data classification
✅ Easy-to-use CSV format
✅ Ready for ML/DL projects
✅ Free for research & academic use
✅ Fully open-source 🚀

**⚙️ Installation & Setup**
```bash
git clone https://github.com/sudipsudip5250/Nepal_Stock_Data.git
pip install -r requirements.txt
```
simple clone its in your project folder and after that you can bring python folder out in your project folder if you didnt bring and execute its inside then its will again clone repo inside its and update the things inside the new clone. so always try to execute its from outside only one step outside like nepse_data_update.py and Nepal_Stock_Data folder should be in same directory.

**📊 Example Use Cases**
📈 Train LSTM/Transformer models on NEPSE time-series data
🔍 Analyze financial health by sector
📊 Create dashboards using Plotly, Seaborn
🎓 Conduct academic research in economics/finance

📃 License & Usage Terms
You are free to use, modify, and share the datasets for educational or non-commercial purposes.

If you're from the original data sources and object to this usage, please contact me at:📩 sudipsudip5250@gmail.com

I will remove the content immediately upon request.

**🙏 Acknowledgements**
Thanks to the owner of:
***Nepal Stock Exchange
sharesansar***
Their public data platforms made this project possible.

👤 Author
Sudip Bhattarai
GitHub: @sudipsudip5250

**📌 Final Note**
This is part of an open data initiative to promote:

📚 Financial literacy
💹 Stock market understanding
🤖 Machine learning in finance

The Interactive Python Notebook(ipynb) execution didn't face any problem with Google Colab so try it's when you face any problem with executing locally. Feel free to contribute and improve this project! 💡

Let me know if you'd have any question or any other problem/solution or new idea.


<p align="center"><strong> ***THANK YOU ***</strong></p>

