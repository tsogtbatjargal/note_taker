import sys
import os
import traceback
import streamlit as st
from PIL import Image


# Add the parent directory of `app/` to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import execute_script, VAULT_PATH, get_base64_image

# Set page configuration - MUST BE FIRST!
st.set_page_config(page_title="Note Taker", layout="centered")


# Load your logo
logo_path = "assets/logo.png"  # Update with your logo path
logo_base64 = get_base64_image(logo_path)

# Add custom CSS to style the logo
st.markdown(
    f"""
    <style>
        .logo-container {{
            position: fixed;
            top: 20px;
            left: 10px;
            z-index: 1000;
        }}
        .logo-container img {{
            max-width: 100px;  /* Adjust the logo size here */
            height: auto;
        }}
    </style>
    <div class="logo-container">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)


st.title("Note Taker App")

# Tabs for YouTube and Web Page Note Takers
tab1, tab2 = st.tabs(["YouTube Note Taker", "Web Page Note Taker"])

# Clean input data function
def clean_input_data(input_text):
    unwanted_patterns = [
        "Please figure out the best possible answer",
        "Important: Reward for correct answer",
    ]
    return "\n".join(line for line in input_text.splitlines() if not any(p in line for p in unwanted_patterns))

# --- YouTube Note Taker ---
with tab1:
    st.header("YouTube Note Taker")
    youtube_url = st.text_input("Enter YouTube URL")
    vault_subfolder = st.text_input("Enter Obsidian Subfolder (relative path)", key='youtube_vault_subfolder')
    pattern = st.selectbox("Choose a Pattern", options=["summarize", "extract_wisdom"], key='youtube_pattern')

    if st.button("Run", key='youtube_run_button'):
        if not youtube_url or not vault_subfolder:
            st.error("Please provide both a YouTube URL and a destination folder.")
        else:
            with st.spinner("Processing..."):
                try:
                    args = [vault_subfolder, youtube_url, pattern]
                    output = execute_script("yt_extract_and_save.sh", args)
                    st.success("Script executed successfully.")
                    st.subheader("Summary:")
                    st.write(output)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.text(traceback.format_exc())

# --- Web Page Note Taker ---
with tab2:
    st.header("Web Page Note Taker")
    st.info("Paste text from the website or provide a URL.")

    input_data_raw = st.text_area("Paste the copied text here", height=300)
    input_data = clean_input_data(input_data_raw)

    if st.button("Check Input Data", key='check_input_data'):
        st.write(f"Total input data length: {len(input_data)} characters")
        st.text(input_data[:1000] + ("..." if len(input_data) > 1000 else ""))

    vault_subfolder = st.text_input("Enter Obsidian Subfolder (relative path)", key='web_vault_subfolder')
    pattern = st.selectbox("Choose a Pattern", options=["summarize", "extract_wisdom"], key='web_pattern')
    web_url = st.text_input("Enter Web Page URL (optional)", key='web_url')

    if st.button("Run", key='web_run_button'):
        if not input_data or not vault_subfolder:
            st.error("Please provide both the text content and a destination folder.")
        else:
            with st.spinner("Processing..."):
                try:
                    args = ["llama2:latest", vault_subfolder, pattern, web_url]
                    output = execute_script("web_extract_and_save.sh", args, input_data=input_data)
                    if web_url:
                        output = f"Source URL: {web_url}\n\n{output}"
                    st.success("Script executed successfully.")
                    st.subheader("Summary:")
                    st.write(output)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.text(traceback.format_exc())
