import pandas as pd
import streamlit as st


def load_data(file):
    # Check for file format and load data accordingly
    if file is not None:
        if file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(file)
        elif file.type == 'text/csv':
            df = pd.read_csv(file, low_memory=False)
        else:
            st.error("Unsupported file format. Please upload an Excel file or a CSV.")
            return None
        # Capitalize columns that contain 'name'
        df = capitalize_name_columns(df)
        return df
    else:
        return None


def capitalize_name_columns(df):
    # Iterate over the columns of the dataframe
    for col in df.columns:
        # Check if 'name' is in the column name
        if 'name' in col.lower():
            # Apply .title() to each value in the column
            df[col] = df[col].apply(lambda x: x.title() if isinstance(x, str) else x)
    return df


def get_desired_columns(df):
    st.markdown("""
    ## Select the columns from your spreadsheet which match the following criteria:
    - First Name
    - Last Name
    - Email (if available)
    - Phone Number (max 3 numbers, NO LANDLINES)
    - Address (all address fields)
    """)
    # User selects columns to retain in the cleaned dataframe
    columns = st.multiselect("Select Columns", df.columns.tolist())
    # add button to clean data
    st.write("Press to clean data.")
    if st.button("Clean Data"):
        df = capitalize_name_columns(df)

    return df[columns]


def download_new_csv(df, file_name):
    # Convert dataframe to CSV and create download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Press to Download",
        csv,
        file_name,
        "text/csv",
        key='download-csv'
    )


def main():
    st.title("File Uploader to DataFrame")
    st.write("Upload a file (Excel or CSV) to create a Pandas DataFrame.")
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
        download_new_csv(cleaned_df, 'cleaned_data.csv')


if __name__ == "__main__":
    main()
