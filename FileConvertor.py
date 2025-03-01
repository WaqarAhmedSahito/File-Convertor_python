import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="📊 Data Wizard", layout="wide", page_icon="🔮")
st.markdown("""
    <style>
    .main {background-color: #f9f9f9;}
    .stButton>button {border-radius: 5px; padding: 0.5rem 1rem;}
    .stDownloadButton>button {background-color: #4CAF50; color: white;}
    .st-emotion-cache-1qg05tj {border-radius: 5px;}
    </style>
    """, unsafe_allow_html=True)

with st.container():
    st.title("🔮 Data Wizard")
    st.markdown("""
    **Your all-in-one solution for data conversion & cleaning!**  
    Upload CSV/Excel files ➡️ Clean & Transform ➡️ Download in desired format  
    """)
    st.divider()

with st.expander("📤 UPLOAD FILES", expanded=True):
    files = st.file_uploader(
        "Drag & drop files here (CSV/Excel)",
        type=["csv", "xlsx"],
        accept_multiple_files=True,
        help="Maximum file size: 200MB"
    )

if files:
    for file in files:
        with st.container():
            st.subheader(f"📄 {file.name}")
            col1, col2 = st.columns([2, 1], gap="medium")
            
            with col1:
               
                ext = file.name.split(".")[-1]
                df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
                
                # Preview section
                with st.expander("🔍 Data Preview", expanded=True):
                    st.dataframe(df.head(8), use_container_width=True)

            with col2:
                # Processing options
                with st.container(border=True):
                    st.markdown("🛠️ **Data Cleaning Tools**")
                    
                    if st.checkbox(f"Remove Duplicates", key=f"dup_{file.name}"):
                        df = df.drop_duplicates()
                        st.success("✅ Duplicates removed!")
                    
                    if st.checkbox(f"Fill Missing Values", key=f"fill_{file.name}"):
                        df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
                        st.success("✅ Missing values filled with mean!")

                # Column selection
                with st.container(border=True):
                    selected_columns = st.multiselect(
                        "🔧 Select Columns to Keep",
                        df.columns,
                        default=df.columns,
                        key=f"cols_{file.name}"
                    )
                    df = df[selected_columns]

                # Visualization
                if not df.select_dtypes(include="number").empty:
                    with st.container(border=True):
                        st.markdown("📈 Quick Visualization")
                        st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

            # Conversion & Download
            st.divider()
            with st.container():
                col3, col4 = st.columns([1, 3])
                with col3:
                    format_choice = st.radio(
                        f"Convert {file.name} to:",
                        ["CSV", "Excel"],
                        key=f"format_{file.name}",
                        horizontal=True
                    )
                
                with col4:
                    if st.button(f"⬇️ Download Processed {file.name}", key=f"btn_{file.name}"):
                        output = BytesIO()
                        if format_choice == "CSV":
                            df.to_csv(output, index=False)
                            mime_type = "text/csv"
                            new_name = file.name.replace(ext, "csv")
                        else:
                            df.to_excel(output, index=False, engine="openpyxl")
                            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            new_name = file.name.replace(ext, "xlsx")

                        output.seek(0)
                        st.download_button(
                            label=f"Save {new_name}",
                            data=output,
                            file_name=new_name,
                            mime=mime_type,
                            key=f"dwn_{file.name}"
                        )
                        st.balloons()
            
            st.divider()