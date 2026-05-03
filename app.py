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

    # ERROR FIX: Sabhi Heat No. aur Grade ko String (Text) mein convert karna
    df['HEAT NO.'] = df['HEAT NO.'].astype(str)
    df['GRADE'] = df['GRADE'].astype(str)

    # 2. Search & Filter Section
    st.sidebar.header("Filters")
    
    # Heat No Search 
    heat_no_list = ["All"] + sorted(df['HEAT NO.'].dropna().unique().tolist())
    selected_heat = st.sidebar.selectbox("Filter by Heat No", heat_no_list)
    
    # Grade Filter
    grade_list = ["All"] + sorted(df['GRADE'].dropna().unique().tolist())
    selected_grade = st.sidebar.selectbox("Filter by Grade", grade_list)

    # General Search Bar
    search_query = st.text_input("🔍 Search anything (Item Name, Drg No, Heat No...)", "")

    # 3. Filtering Logic
    filtered_df = df.copy()
    
    if selected_heat != "All":
        filtered_df = filtered_df[filtered_df['HEAT NO.'] == selected_heat]
    
    if selected_grade != "All":
        filtered_df = filtered_df[filtered_df['GRADE'] == selected_grade]
        
    if search_query:
        # Pura row check karega search query ke liye
        filtered_df = filtered_df[filtered_df.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)]

    # 4. Results Display
    st.success(f"Total Rows Found: {len(filtered_df)}")
    
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("Waiting for file upload...")
