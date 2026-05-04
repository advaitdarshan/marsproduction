import streamlit as st
import pandas as pd
import os
import glob
from st_aggrid import AgGrid, GridOptionsBuilder

# Page Configuration
st.set_page_config(page_title="Factory Dashboard", layout="wide")
st.title("📊 Factory Master Dashboard")

excel_files = glob.glob("*.xlsx")

if not excel_files:
    st.error("⚠️ Yahan koi Excel file nahi mili. Kripya pehle `.bat` file chala kar data upload karein.")
else:
    selected_file = st.sidebar.selectbox("📂 Select Department / File", excel_files)
    
    # Excel read karna
    xls = pd.ExcelFile(selected_file)
    sheet = st.sidebar.selectbox("📑 Select Sheet", xls.sheet_names)
    
    # Header logic (Pehle jaisa)
    temp_df = pd.read_excel(selected_file, sheet_name=sheet, nrows=2)
    unnamed_count = sum('Unnamed' in str(col) for col in temp_df.columns)
    
    header_row = 1 if unnamed_count > 2 else 0
    df = pd.read_excel(selected_file, sheet_name=sheet, header=header_row)

    # Data Cleaning
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    for col in df.columns:
        df[col] = df[col].fillna("Blank").astype(str)

    # Sidebar Filters hata diye gaye hain taaki table mein hi filter ho sake
    st.sidebar.info("💡 Tip: Filter and Search directly within the table headers!")

    # ==========================================
    # AG-GRID SETUP (Advance Excel-like Table)
    # ==========================================
    st.success(f"Total Rows: {len(df)}")
    
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        editable=False, 
        groupable=True, 
        value=True, 
        enableRowGroup=True, 
        aggFunc='sum', 
        sortable=True, 
        filter=True # Ye column filter enable karega
    )
    
    gridOptions = gb.build()

    AgGrid(
        df,
        gridOptions=gridOptions,
        enable_enterprise_modules=True, # Advance filtering ke liye
        fit_columns_on_grid_load=False, # Columns apne hisab se width lenge
        height=600, # Table ki height
        width='100%',
        theme='streamlit' # Theme ('light', 'dark', 'streamlit' etc.)
    )
