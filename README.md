# Vehicle Registration Dashboard (Investor View)

An interactive Streamlit dashboard built on public Vahan data to analyze registrations by vehicle category and manufacturer, with YoY and QoQ growth.

## 🔧 Setup Instructions
1) Clone & install
```bash
git clone <your-repo-url>
cd vehicle-reg-dashboard
pip install -r requirements.txt
Run the app

streamlit run app.py

Load data

Click “Upload Vehicle Data” in the app and upload your Excel/CSV.

Expected columns:

Year, Category Group, Vehicle Class (manufacturer or class), Subcategory, Registrations

Optional for QoQ: Month or Quarter (Q1/Q2/Q3/Q4)

📊 Features

Filters: Date range, Category, Manufacturer/Vehicle Class

KPIs: Total Registrations, YoY %, QoQ % (if quarter data available)

Charts: Yearly trends, Quarterly trends, Manufacturer breakdown

Investor-friendly layout

📐 Calculations

YoY% = (CurrentYear - PreviousYear) / PreviousYear * 100

QoQ% = (CurrentQuarter - PreviousQuarter) / PreviousQuarter * 100

QoQ is shown only when quarter/month data is provided.

🗂️ Data Assumptions

“Vehicle Class” serves as manufacturer/class depending on Vahan export.

Missing/invalid numerics are coerced to 0 for aggregation.

If quarter data is unavailable, QoQ will display N/A.


📓 Data Collection 

Source: Vahan Dashboard public pages


Cleaning: header fixes, type coercion, deduplication

🧭 How to Use (in the video)

Upload dataset → pick year & category → read KPIs

Toggle manufacturers to compare market share

Check YoY trend line; if quarters exist, review QoQ line

Use date range to focus on a period and observe % change

💡 Key Investor Insights (examples to look for)

Fastest-growing category YoY (e.g., 2W vs 4W)

Manufacturer gaining/losing share QoQ

Seasonality (festive quarter spikes)

🎥 Video Walkthrough

Video link: https://drive.google.com/file/d/1HlLMNDXow2UFtGsSd_tXohViLjprHZkM/view?usp=sharing
