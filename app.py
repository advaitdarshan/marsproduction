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
    
    # Header logic (Aapki files ke liye)
    temp_df = pd.read_excel(selected_file, sheet_name=sheet, nrows=2)
    unnamed_count = sum('Unnamed' in str(col) for col in temp_df.columns)
    
    header_row = 1 if unnamed_count > 2 else 0
    df = pd.read_excel(selected_file, sheet_name=sheet, header=header_row)

    # Data Cleaning
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    for col in df.columns:
        df[col] = df[col].fillna("Blank").astype(str)

    # ==========================================
    # SMART FILTERS (Mobile Friendly Expander)
    # ==========================================
    # Ye ek box banayega jise aap mobile par click karke khol ya band kar sakte hain
    with st.expander("🔽 Click here to apply Filters (PO#, ITEM, STATUS etc.)"):
        st.markdown("Yahan se aap kisi bhi column par filter laga sakte hain:")
        
        # Screen ko 4 columns mein baantna taaki filters sundar dikhein
        cols = st.columns(4) 
        selected_filters = {}
        
        for i, col in enumerate(df.columns):
            unique_vals = ["All"] + sorted(df[col].unique().tolist())
            # Har filter ko ek column mein fit karna
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
    # NATIVE DATAFRAME (With Fullscreen & Download)
    # ==========================================
    # Ye Streamlit ka asli table hai. Iske top-right corner par hover karne se aapko
    # 1. Search (Magnifying Glass)
    # 2. Download (CSV) - Jo sirf filtered data download karega!
    # 3. Fullscreen (Arrows) - Mobile ke liye best!
    # Ye teeno options milenge.
    
    st.dataframe(filtered_df, use_container_width=True, height=600)
