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
    
    # Header logic 
    temp_df = pd.read_excel(selected_file, sheet_name=sheet, nrows=2)
    unnamed_count = sum('Unnamed' in str(col) for col in temp_df.columns)
    
    header_row = 1 if unnamed_count > 2 else 0
    df = pd.read_excel(selected_file, sheet_name=sheet, header=header_row)

    # Data Cleaning
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    for col in df.columns:
        df[col] = df[col].fillna("Blank").astype(str)

    st.sidebar.info("💡 Tip: Use column headers to filter like Excel.")

    # ==========================================
    # CUSTOM TOOLBAR (Search & Download)
    # ==========================================
    col1, col2 = st.columns([3, 1]) # Screen ko 2 hisso mein baantna
    
    with col1:
        # Global Search Box (Ye theek waisa hi kaam karega jaisa default search karta tha)
        search_query = st.text_input("🔍 Global Search (Puri table mein kuch bhi dhoondein)", "")
        
    with col2:
        st.write("") # Thodi spacing ke liye
        st.write("")
        # Download Button (Data ko CSV mein download karne ke liye)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data",
            data=csv,
            file_name=f"{selected_file}_{sheet}.csv",
            mime='text/csv',
        )

    st.success(f"Total Rows: {len(df)}")
    
    # ==========================================
    # AG-GRID SETUP
    # ==========================================
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        editable=False, 
        groupable=True, 
        value=True, 
        enableRowGroup=True, 
        aggFunc='sum', 
        sortable=True, 
        filter=True # Excel jaisa column filter
    )
    
    # Hamare Global Search box ko AgGrid ke sath connect karna
    gb.configure_grid_options(quickFilterText=search_query)
    
    gridOptions = gb.build()

    AgGrid(
        df,
        gridOptions=gridOptions,
        enable_enterprise_modules=True, 
        fit_columns_on_grid_load=False, 
        height=650, # Height badha di hai taaki Fullscreen jaisa feel aaye
        width='100%',
        theme='streamlit' 
    )
