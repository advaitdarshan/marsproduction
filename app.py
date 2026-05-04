import streamlit as st
import pandas as pd
import os
import glob

# Page Configuration for Mobile
st.set_page_config(page_title="Master Dashboard", layout="wide")

st.title("📊 Factory Master Dashboard")
st.markdown("Apni department file select karein aur details dekhein.")

# GitHub folder (repo) mein jitni bhi .xlsx files hain, sabko dhoondhna
excel_files = glob.glob("*.xlsx")

if not excel_files:
    st.error("⚠️ Yahan koi Excel file nahi mili. Kripya pehle `.bat` file chala kar data upload karein.")
else:
    # 1. FILE SELECTOR DROPDOWN
    selected_file = st.sidebar.selectbox("📂 Select Department / File", excel_files)
    
    # Excel read karna
    xls = pd.ExcelFile(selected_file)
    sheet = st.sidebar.selectbox("📑 Select Sheet", xls.sheet_names)
    
    df = pd.read_excel(selected_file, sheet_name=sheet)
    
    # Data Cleaning 
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    for col in df.columns:
        df[col] = df[col].fillna("Blank").astype(str)

    # 2. DYNAMIC FILTERS SECTION
    st.sidebar.header("🔍 Filters")
    
    selected_filters = {}
    for col in df.columns:
        unique_vals = ["All"] + sorted(df[col].unique().tolist())
        selected_val = st.sidebar.selectbox(f"Filter by {col}", unique_vals)
        
        if selected_val != "All":
            selected_filters[col] = selected_val

    # 3. GENERAL SEARCH BAR
    st.markdown("---")
    search_query = st.text_input(f"🔍 Search anything in {selected_file}", "")

    # Filtering Logic
    filtered_df = df.copy()
    
    for col, val in selected_filters.items():
        filtered_df = filtered_df[filtered_df[col] == val]
        
    if search_query:
        filtered_df = filtered_df[filtered_df.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)]

    # 4. RESULTS DISPLAY
    st.success(f"Total Rows Found: {len(filtered_df)}")
    st.dataframe(filtered_df, use_container_width=True)
