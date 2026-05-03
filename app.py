import streamlit as st
import pandas as pd

# Page Configuration for Mobile
st.set_page_config(page_title="Production Portal", layout="wide")

st.title("📊 Production Register Dashboard")
st.markdown("Apni updated Excel file yaha upload karein aur details dekhein.")

# 1. File Uploader
uploaded_file = st.file_uploader("Upload 'PRODUCTION REGISTERR.xlsx'", type="xlsx")

if uploaded_file:
    # Excel read karna
    xls = pd.ExcelFile(uploaded_file)
    sheet = st.sidebar.selectbox("Select Sheet", xls.sheet_names)
    
    df = pd.read_excel(uploaded_file, sheet_name=sheet)
    
    # Data Cleaning (Unnamed columns hatana)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # ERROR FIX & DYNAMIC FILTERS SETUP
    # Sabhi data ko Text (String) mein convert karna taaki sorting mein error na aaye
    for col in df.columns:
        # 'nan' (khali cell) ko theek karna
        df[col] = df[col].fillna("Blank")
        df[col] = df[col].astype(str)

    # 2. Search & Filter Section
    st.sidebar.header("Filters")
    
    # DYNAMIC FILTERS: Har column ke liye automatic ek dropdown filter banega
    selected_filters = {}
    for col in df.columns:
        # Har column ki unique values nikal kar sort karna
        unique_vals = ["All"] + sorted(df[col].unique().tolist())
        
        # Dropdown banana
        selected_val = st.sidebar.selectbox(f"Filter by {col}", unique_vals)
        
        # Agar user "All" ke alawa kuch select kare, toh use dictionary mein save karna
        if selected_val != "All":
            selected_filters[col] = selected_val

    # General Search Bar
    st.markdown("---")
    search_query = st.text_input("🔍 Search anything (General search across all columns)", "")

    # 3. Filtering Logic
    filtered_df = df.copy()
    
    # A) Pehle dropdown filters apply karna
    for col, val in selected_filters.items():
        filtered_df = filtered_df[filtered_df[col] == val]
        
    # B) Fir general search box apply karna
    if search_query:
        # Pura row check karega search query ke liye
        filtered_df = filtered_df[filtered_df.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)]

    # 4. Results Display
    st.success(f"Total Rows Found: {len(filtered_df)}")
    
    # Table Show karna
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("Waiting for file upload...")
