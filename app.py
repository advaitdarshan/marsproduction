import streamlit as st
import pandas as pd
import os
import glob

st.set_page_config(page_title="Factory Dashboard", layout="wide")
st.title("📊 Factory Master Dashboard")
st.markdown("Apni file select karein aur details dekhein.")

excel_files = glob.glob("*.xlsx")

if not excel_files:
    st.error("⚠️ Yahan koi Excel file nahi mili. Kripya pehle `.bat` file chala kar data upload karein.")
else:
    selected_file = st.sidebar.selectbox("📂 Select Department / File", excel_files)
    
    # Excel read karna, but temporarily string form mein
    xls = pd.ExcelFile(selected_file)
    sheet = st.sidebar.selectbox("📑 Select Sheet", xls.sheet_names)
    
    # ======= JADOO YAHAN HAI (HEADER DETECTOR) =======
    # Pehle 2 rows padh kar check karte hain ki header kahan hai
    temp_df = pd.read_excel(selected_file, sheet_name=sheet, nrows=2)
    
    # Agar pehli row (Index 0) mein bahut saare 'Unnamed' hain, iska matlab header 2nd row (header=1) pe hai
    unnamed_count = sum('Unnamed' in str(col) for col in temp_df.columns)
    
    if unnamed_count > 2:
        header_row = 1  # 2nd line ko header maano
    else:
        header_row = 0  # 1st line ko header maano
    
    # Ab file ko theek header ke sath read karna
    df = pd.read_excel(selected_file, sheet_name=sheet, header=header_row)
    # =================================================

    # 'Unnamed' columns ko puri tarah hata dena (jo khali merge ki wajah se aate hain)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    for col in df.columns:
        df[col] = df[col].fillna("Blank").astype(str)

    st.sidebar.header("🔍 Filters")
    
    selected_filters = {}
    for col in df.columns:
        unique_vals = ["All"] + sorted(df[col].unique().tolist())
        selected_val = st.sidebar.selectbox(f"Filter by {col}", unique_vals)
        
        if selected_val != "All":
            selected_filters[col] = selected_val

    st.markdown("---")
    search_query = st.text_input(f"🔍 Search anything in {selected_file}", "")

    filtered_df = df.copy()
    
    for col, val in selected_filters.items():
        filtered_df = filtered_df[filtered_df[col] == val]
        
    if search_query:
        filtered_df = filtered_df[filtered_df.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)]

    st.success(f"Total Rows Found: {len(filtered_df)}")
    st.dataframe(filtered_df, use_container_width=True)
