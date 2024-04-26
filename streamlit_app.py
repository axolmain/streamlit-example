import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


def load_data(file):
    if file is not None:
        if file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(file)
        elif file.type == 'text/csv':
            df = pd.read_csv(file, low_memory=False)
        else:
            st.error("Unsupported file format. Please upload an Excel file or a CSV.")
            return None
        return df
    else:
        return None


def get_desired_columns(df):
    st.markdown("""
    ## Select the columns from your spreadsheet which match the following criteria:
    - First Name
    - Last Name
    - Email (if available)
    - Phone Number (max 3 numbers, NO LANDLINES)
    - Address (all address fields)
    """)

    columns = st.multiselect("Select Columns", df.columns.tolist())
    return df[columns]


def download_new_csv(df, file_name):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Press to Download",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
    )


def main():
    st.title("File Uploader to DataFrame")
    st.write("Upload a file (Excel, CSV, or Numbers) to create a Pandas DataFrame.")

    file = st.file_uploader("Upload File", type=['xlsx', 'csv'])
    cleaned_df = None

    if file is not None:
        df = load_data(file)
        if df is not None:
            cleaned_df = get_desired_columns(df)
            st.write(cleaned_df)

        else:
            st.error("Failed to load data.")

    if cleaned_df is not None and len(cleaned_df.columns) >= 5:
        download_new_csv(cleaned_df, 'file.csv')


if __name__ == "__main__":
    main()
