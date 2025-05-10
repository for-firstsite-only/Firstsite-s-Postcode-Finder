import streamlit as st
import pandas as pd
from PIL import Image


# Load and display the logo
image = Image.open("image.png")  
st.image(image, width=150)

# Load Colchester postcode data
@st.cache_data
def load_postcode_data():
    df = pd.read_csv("Colchester postcodes.csv")
    df["Postcode"] = df["Postcode"].str.upper().str.strip()
    df["LSOA Code"] = df["LSOA Code"].str.strip()
    return df

# Load IMD decile data
@st.cache_data
def load_imd_data():
    imd_df = pd.read_csv("imd_scores.csv")
    imd_df = imd_df[[
        "LSOA code (2011)", 
        "Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"
    ]]
    imd_df.columns = ["LSOA Code", "IMD Decile"]
    imd_df["LSOA Code"] = imd_df["LSOA Code"].str.strip()
    return imd_df


# Merge postcode data with IMD decile
def merge_data(postcodes, imd):
    return postcodes.merge(imd, on="LSOA Code", how="left")

# Load and merge data
postcode_df = load_postcode_data()
imd_df = load_imd_data()
df = merge_data(postcode_df, imd_df)

# Streamlit UI
st.title("Colchester Postcode Finder for Firstsite")
st.markdown("Enter a postcode (full or partial) to find the Ward and IMD decile (1 = most deprived, 10 = least deprived).")

postcode_input = st.text_input("Enter postcode (e.g., CO1, 1JH, CO1 1JH):").upper().strip()

if postcode_input:
    # Match any part of postcode (not just prefix)
    match = df[df["Postcode"].str.contains(postcode_input, na=False)]

    if not match.empty:
        top = match.head(1)
        st.success("Most relevant match found:")
        st.dataframe(top[["Postcode", "Ward", "IMD Decile"]])
    else:
        st.warning("No matching postcodes found.")

st.markdown("---")
st.caption("Sources: Colchester Postcode Dataset & English Indices of Deprivation 2019")
