import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("Data Sweeper")
st.write("Transform your files between CSV and Excel fromats with built-in data cleaning and visualizaiton!")

uploaded_file = st.file_uploader("Upload your files (CSV , Excel):", type=["csv","xlsx"], accept_multiple_files=True)

if uploaded_file is not None:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()


        if file_ext == ".csv":
            df = pd.read_csv(file)
            st.write(df)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        
        else:
            st.write(f"Unsupported file type: {file_ext}")
            continue

        #  display info about the file
        st.write(f"File name: {file.name}")
        st.write(f"File size: {file.size/1024} bytes")
        st.write(f"File type: {file_ext}")

        # Show 5 rows of our df
        st.write("Preview the head of the Dataframe")
        st.dataframe(df.head())

        # Options for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1,col2 = st.columns(2)

            with col1:
                if st.button(f"Delete Duplicates from {file.name}"):
                    df = df.drop_duplicates(inplace=True)
                    st.write(f"Duplicates deleted from {file.name}")

            with col2:
                if st.button(f"Remove Null Values from {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns   
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missiing values has been filled!")      

        # Choose Specific Columns to Keep or Covert
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns from {file.name}",df.columns, default=df.columns)
        df = df[columns]

        # Create Some Visualizations
        st.subheader("Data Visualizations")
        if st.checkbox(f"Shwo Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include = "number").iloc[:,:2])

        # Convert the File -> CSV to Excel
        conversion_type = st.radio(f"Convert {file.name} to:",["CSV","Excel"],key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer,index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mine_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer,index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mine_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # download button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mine_type
            )
st.success("All files processed")