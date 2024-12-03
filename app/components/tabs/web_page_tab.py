import streamlit as st
import streamlit.components.v1 as components
from app.utils import execute_script, clean_input_data

def web_page_tab():
    st.header("Web Page Note Taker")
    input_data_raw = st.text_area("Paste the copied text here", height=300, key='web_input_data')
    input_data = clean_input_data(input_data_raw)
    vault_subfolder = st.text_input("Enter Obsidian Subfolder (relative path)", key='web_vault_subfolder')
    pattern = st.selectbox("Choose a Pattern", options=["summarize", "extract_wisdom"], key='web_pattern')
    web_url = st.text_input("Enter Web Page URL (optional)", key='web_web_url')

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
