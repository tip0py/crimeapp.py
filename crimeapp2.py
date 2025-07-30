import streamlit as st
from PIL import Image
import pandas as pd
import base64

# Load image
bg_image_path = "/mnt/data/918bce7f5032dc7b9baecf310eeefa5d.jpg"
qa_csv_path = "/mnt/data/criminal_justice_qa.csv"

# Set custom page config
st.set_page_config(page_title="Securo - Crime Intelligence Bot", layout="centered")

# Background image setup
def get_base64_bg(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def set_bg(image_path):
    bg_base64 = get_base64_bg(image_path)
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bg_base64}");
            background-size: cover;
            font-family: 'Times New Roman', serif;
            color: white;
        }}
        .main-card {{
            background-color: rgba(0, 0, 0, 0.7);
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 0 10px rgba(255, 0, 0, 0.6);
        }}
        h1, h2, h3 {{
            text-shadow: 2px 2px 4px #000000;
        }}
        .stButton > button {{
            background-color: #8b0000;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            font-size: 18px;
        }}
        </style>
    """, unsafe_allow_html=True)

# Set background image
set_bg(bg_image_path)

# Title and options overlay
st.markdown("<div class='main-card'>", unsafe_allow_html=True)
st.title("🔍 Welcome to Securo")
st.markdown("""
### Your Personal Crime Intelligence Assistant for St. Kitts and Nevis
Helping criminologists, forensic experts, and authorities analyze, solve, and prevent crime.
""")

# Buttons for login and signup
col1, col2 = st.columns(2)
with col1:
    if st.button("🔐 Login"):
        st.info("Login functionality coming soon.")

with col2:
    if st.button("📝 Create Account"):
        st.info("Signup functionality coming soon.")

st.markdown("</div>", unsafe_allow_html=True)

# Load QA CSV (basic stub for now)
df_qa = pd.read_csv(qa_csv_path)
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h4>Sample Knowledge Base Preview</h4>", unsafe_allow_html=True)
st.dataframe(df_qa.head(), use_container_width=True)
