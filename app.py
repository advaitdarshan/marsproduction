import streamlit as st
import pandas as pd
import os
import glob
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, UpdateMode

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

    st.sidebar.info("💡 Tip: Table ke columns par click karke Excel jaisa filter lagayein.")

    # ==========================================
    # GLOBAL SEARCH & TOTAL ROWS
    # ==========================================
    search_query = st.text_input("🔍 Global Search (Puri table mein kuch bhi dhoondein)", "")
    st.success(f"Total Original Rows: {len(df)}")

    # ==========================================
    # AG-GRID SETUP (Advanced Filterable Table)
    # ==========================================
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        editable=False, 
        groupable=True, 
        value=True, 
        enableRowGroup=True, 
        aggFunc='sum', 
        sortable=True, 
        filter=True, # Excel jaisa column filter
        resizable=True # Columns ko lamba-chauda karne ke liye
    )
    
    # Global Search box ko table se connect karna
    gb.configure_grid_options(quickFilterText=search_query)
    
    gridOptions = gb.build()

    # Table Display karna aur Filtered data ko ek variable mein save karna
    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        enable_enterprise_modules=True, 
        fit_columns_on_grid_load=True, # Auto-Fit Columns
        height=550, 
        width='100%',
        theme='streamlit',
        update_mode=UpdateMode.MODEL_CHANGED, # Jab bhi user filter lagaye, app ko batao
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED # Sirf Filtered data return karo
    )

    # ==========================================
    # DOWNLOAD BUTTON (Sirf Filter kiye hue Data ke liye)
    # ==========================================
    
    # Jo data filter ho kar aaya hai, use naye dataframe mein convert karna
    filtered_df = pd.DataFrame(grid_response['data'])

    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.info(f"Showing {len(filtered_df)} rows after applying filters.")
        
    with col2:
        # Sirf tabhi download button dikhaye jab table mein koi data ho
        if not filtered_df.empty:
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Filtered Data",
                data=csv,
                file_name=f"Filtered_{selected_file}_{sheet}.csv",
                mime='text/csv',
            )
