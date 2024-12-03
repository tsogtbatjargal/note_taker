import streamlit as st
#import streamlit.components.v1 as components
from app.utils import execute_script

def youtube_tab():
    st.header("YouTube Note Taker")
    youtube_url = st.text_input("Enter YouTube URL", key='youtube_url')
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

                    # Process the output to make it more readable
                    # Split the output into lines
                    lines = output.strip().split('\n')

                    # Initialize variables
                    title = ''
                    duration = ''
                    summary = ''
                    saving_info = ''
                    in_summary = False

                    # Process each line
                    for line in lines:
                        if line.startswith('Title for'):
                            title = line.replace('Title for ', '')
                        elif line.startswith('Duration for'):
                            duration = line.replace('Duration for ', '')
                        elif 'Summary for' in line:
                            in_summary = True
                            summary = ''  # Reset summary in case of multiple summaries
                        elif line.strip() == '---------------------------------------------------':
                            in_summary = False
                        elif 'Summary saved to' in line:
                            saving_info = line
                        elif in_summary:
                            summary += line + '\n'

                    # Display the title and duration
                    if title:
                        st.markdown(f"<div class='custom-title'>{title}</div>", unsafe_allow_html=True)
                    if duration:
                        st.write(f"**Duration:** {duration}")

                    # Display the summary
                    if summary:
                        st.markdown('### Summary:')
                        st.markdown(summary)
                    
                    # Optionally, display the saving info
                    if saving_info:
                        st.info(saving_info)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
