import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Vehicle Registration Dashboard", layout="wide")
st.title("📊 Vehicle Registration Dashboard (Investor View)")

# File uploader
uploaded_file = st.file_uploader("Upload Vehicle Data", type=["xlsx", "xls", "csv"])

if uploaded_file:
    # Detect file type and read
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file, skip_blank_lines=True)
    else:
        df = pd.read_excel(uploaded_file, skip_blank_lines=True)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Remove any header-like rows inside data
    df = df[df['Year'].astype(str).str.isnumeric()]

    # Convert Year & Registrations safely
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype(int)
    df['Registrations'] = pd.to_numeric(df['Registrations'], errors='coerce').fillna(0)

    # --------------------
    # YoY Calculation
    # --------------------
    yearly = df.groupby(['Year', 'Category Group'])['Registrations'].sum().reset_index()
    yearly['YoY%'] = yearly.groupby('Category Group')['Registrations'].pct_change() * 100

    # --------------------
    # QoQ Calculation (only if Month or Quarter column exists)
    # --------------------
    df['Quarter'] = None
    if 'Month' in df.columns:
        df['Date'] = pd.to_datetime(df['Month'] + ' ' + df['Year'].astype(str), errors='coerce')
        df['Quarter'] = df['Date'].dt.to_period('Q')
    elif 'Quarter' in df.columns:
        df['Quarter'] = df['Quarter']

    if df['Quarter'].notna().any():
        quarterly = df.groupby(['Quarter', 'Category Group'])['Registrations'].sum().reset_index()
        quarterly['QoQ%'] = quarterly.groupby('Category Group')['Registrations'].pct_change() * 100
    else:
        quarterly = pd.DataFrame(columns=['Quarter', 'Category Group', 'Registrations', 'QoQ%'])

    # --------------------
    # Sidebar Filters
    # --------------------
    years = sorted(df['Year'].unique())
    categories = df['Category Group'].unique()

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_category = st.sidebar.selectbox("Select Category", categories)

    # Filter for KPIs
    filtered_data = df[(df['Year'] == selected_year) & (df['Category Group'] == selected_category)]
    total_reg = int(filtered_data['Registrations'].sum())

    # YoY Value
    yoy_change = yearly[(yearly['Year'] == selected_year) & 
                        (yearly['Category Group'] == selected_category)]['YoY%'].values
    yoy_display = f"{yoy_change[0]:.2f}%" if len(yoy_change) > 0 and not pd.isna(yoy_change[0]) else "N/A"

    # QoQ Value (latest quarter of selected year)
    if not quarterly.empty:
        q_data = quarterly[(quarterly['Category Group'] == selected_category) & 
                           (quarterly['Quarter'].astype(str).str.startswith(str(selected_year)))]
        if not q_data.empty:
            latest_qoq = q_data.iloc[-1]['QoQ%']
            qoq_display = f"{latest_qoq:.2f}%" if not pd.isna(latest_qoq) else "N/A"
        else:
            qoq_display = "N/A"
    else:
        qoq_display = "N/A"

    # --------------------
    # KPI Cards
    # --------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Registrations", f"{total_reg:,}")
    col2.metric("YoY Growth %", yoy_display)
    col3.metric("QoQ Growth %", qoq_display)

    # --------------------
    # Charts
    # --------------------
    st.subheader(f"📈 Yearly Trend - {selected_category}")
    fig1 = px.line(yearly[yearly['Category Group'] == selected_category],
                   x='Year', y='Registrations', markers=True,
                   title=f"Yearly Registrations - {selected_category}")
    st.plotly_chart(fig1, use_container_width=True)

    if not quarterly.empty:
        st.subheader(f"📉 Quarterly Trend - {selected_category}")
        fig_q = px.line(quarterly[quarterly['Category Group'] == selected_category],
                        x='Quarter', y='Registrations', markers=True,
                        title=f"Quarterly Registrations - {selected_category}")
        st.plotly_chart(fig_q, use_container_width=True)

    # Manufacturer / Vehicle Class breakdown
    st.subheader("🏭 Manufacturer / Vehicle Class Breakdown")
    manu_group = filtered_data.groupby('Vehicle Class')['Registrations'].sum().reset_index()
    fig2 = px.bar(manu_group, x='Vehicle Class', y='Registrations',
                  title=f"Registrations by Vehicle Class - {selected_year}")
    st.plotly_chart(fig2, use_container_width=True)

    st.success("Dashboard Updated Successfully ✅")

else:
    st.info("Please upload an Excel or CSV file to get started.")
