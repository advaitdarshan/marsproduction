import streamlit as st
import pandas as pd
import os
import glob

# Page Configuration
st.set_page_config(page_title="Factory Dashboard", layout="wide")

# ==========================================
# CSS MAGIC: Margin Khatam Karna aur Font Chota Karna
# ==========================================
st.markdown("""
    <style>
        /* Main screen ki left aur right blank space (margin) ko hatana */
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1rem !important;
            max-width: 100% !important;
        }
        
        /* Table ke andar text ko thoda chota aur compact karna */
        [data-testid="stDataFrame"] {
            font-size: 13px !important;
        }
    </style>
""", unsafe_allow_html=True)

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
    # DATA CLEANING & MERGED HEADER FIX
    # ==========================================
    
    df = df.dropna(how='all', axis=1)

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

    for col in df.columns:
        df[col] = df[col].fillna("Blank").astype(str)

    # ==========================================
    # SMART FILTERS
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
    st.dataframe(filtered_df, use_container_width=True, height=650)
