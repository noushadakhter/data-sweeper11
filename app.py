
import streamlit as st
import pandas as pd
import os
from io import BytesIO 

#set up our app
st.set_page_config(page_title="Data Sweeper", layout='wide')
st.title("Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("Upload Your Files (CSV or Excel Sheet):", type=["csv", "xlsx"],
                                 accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file) 
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)  
        else:
            st.error(f"Unsupported File Type: {file.name}")  
            continue 

        # Display info About The File!
        st.write(f"**File Name :** {file.name}")
        st.write(f"**File Size :** {file.size/1024} KB")

        # Show 5 rows of dataframe
        st.write("Preview The Head Of The Dataframe")
        st.dataframe(df.head())

        # options for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data For {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates From {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values For {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values Have Been Filled!")

        # Choose Specific Columns To Keep Or Convert!
        st.subheader("Select Columns To Convert")
        columns = st.multiselect(f"Choose Columns For {file.name}", df.columns, default=df.columns)  # Fixed 'cloumns' typo
        df = df[columns]

        # Create Some Visualization!
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization For {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])  # Fixed 'df_select_dt' to 'df'

        # Convert The File! -> CSV To Excel
        st.subheader("Conversion Option")
        conversion_type = st.radio(f"Convert {file.name} to :", ["CSV", "Excel"], key=file.name)  # Added comma
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()  # Fixed inconsistent capitalization of 'Buffer'
            if conversion_type == "CSV":  # Fixed '===' to '=='
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"  # Correct MIME type for CSV
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # Correct MIME type for Excel
            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type  # Fixed missing comma here
            )

st.success("All Files Processed!")  # Fixed typo 'succes' to 'success'





#footer
st.write("---")
st.write("**© Created By Noushad Akhter**")






















































































