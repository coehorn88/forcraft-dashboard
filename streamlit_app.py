import pandas as pd
import streamlit as st

# Streamlit App
st.title("CSV File Parser")

st.write(
    """
    This app allows you to upload a semicolon-separated CSV file. 
    It processes the file to extract specific columns ('EAN' and 'Liczba sztuk') 
    and generates a new CSV file with 'ean' and 'quantity'.
    """
)

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    try:
        # Load the uploaded CSV file using semicolon as a delimiter
        df = pd.read_csv(uploaded_file, delimiter=";", encoding="utf-8")
        
        # Check if required columns exist
        if 'EAN' in df.columns and 'Liczba sztuk' in df.columns:
            # Extract the relevant columns and rename them
            parsed_df = df[['EAN', 'Liczba sztuk']].rename(columns={'EAN': 'ean', 'Liczba sztuk': 'quantity'})
            
            # Ensure the 'ean' column is treated as a string to avoid displaying with commas
            parsed_df['ean'] = parsed_df['ean'].astype(str)
            
            # Show the processed DataFrame
            st.write("Processed Data:")
            st.dataframe(parsed_df)
            
            # Provide download button for the processed file
            csv = parsed_df.to_csv(sep=";", index=False, encoding="utf-8")
            st.download_button(
                label="Download Processed CSV",
                data=csv,
                file_name="parsed_output.csv",
                mime="text/csv"
            )
        else:
            st.error("The uploaded file must contain 'EAN' and 'Liczba sztuk' columns.")
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
