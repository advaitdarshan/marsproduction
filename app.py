import streamlit as st
import pandas as pd
import os
import glob

# Page Configuration
st.set_page_config(page_title="Factory Dashboard", layout="wide")
st.title("📊 Factory Master Dashboard")

excel_files = glob.glob("*.xlsx")

if not excel_files:
    st.error("⚠️ Yahan koi Excel file nahi mili. Kripya pehle `.bat` file chala kar data upload karein.")
else:
    # Sidebar mein file selection
    selected_file = st.sidebar.selectbox("📂 Select Department / File", excel_files)
    
    # Excel read karna
    xls = pd.ExcelFile(selected_file)
    sheet = st.sidebar.selectbox("📑 Select Sheet", xls.sheet_names)
    
    # Header logic
    temp_df = pd.read_excel(selected_file, sheet_name=sheet, nrows=2)
    unnamed_count = sum('Unnamed' in str(col) for col in temp_df.columns)
    
    # Agar 5 se zyada unnamed hain, toh actual header row 1 pe hai
    header_row = 1 if unnamed_count > 5 else 0 
    df = pd.read_excel(selected_file, sheet_name=sheet, header=header_row)

    # ==========================================
    # NEW DATA CLEANING & MERGED HEADER FIX
    # ==========================================
    
    # 1. Jo columns sach mein puri tarah khali (100% blank) hain, sirf unhe hatao
    df = df.dropna(how='all', axis=1)

    # 2. Merged headers ko delete karne ki jagah, unhe numbering dena
    new_cols = []
    last_valid_col = "Column"
    col_count = 1

    for col in df.columns:
        if "Unnamed" in str(col):
            col_count += 1
            new_cols.append(f"{last_valid_col} ({col_count})")
        else:
            last_valid_col = str(col)
            col_count = 1
            new_cols.append(last_valid_col)
            
    df.columns = new_cols

    # 3. Khali cells mein 'Blank' likhna
    for col in df.columns:
        df[col] = df[col].fillna("Blank").astype(str)

    # ==========================================
    # SMART FILTERS (Mobile Friendly Expander)
    # ==========================================
    with st.expander("🔽 Click here to apply Filters"):
        st.markdown("Yahan se aap kisi bhi column par filter laga sakte hain:")
        cols = st.columns(4) 
        selected_filters = {}
        
        for i, col in enumerate(df.columns):
            unique_vals = ["All"] + sorted(df[col].unique().tolist())
            selected_val = cols[i % 4].selectbox(f"{col}", unique_vals, key=col)
            
            if selected_val != "All":
                selected_filters[col] = selected_val

    # ==========================================
    # FILTERING LOGIC
    # ==========================================
    filtered_df = df.copy()
    for col, val in selected_filters.items():
        filtered_df = filtered_df[filtered_df[col] == val]

    st.success(f"Total Rows: {len(filtered_df)} (Original: {len(df)})")
    
    # ==========================================
    # NATIVE DATAFRAME
    # ==========================================
    st.dataframe(filtered_df, use_container_width=True, height=600)
