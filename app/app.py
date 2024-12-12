import traceback
import streamlit as st
import subprocess
import os
import sys

# Set page configuration
st.set_page_config(page_title="Note Taker", layout="centered")

# Title
st.title("Note Taker")

# Create tabs for YouTube and Web Page note takers
tab1, tab2 = st.tabs(["YouTube Note Taker", "Web Page Note Taker"])

# Function to clean input data
def clean_input_data(input_text):
    # Split the input into lines
    lines = input_text.splitlines()
    # Remove lines that contain unwanted text
    unwanted_patterns = [
        "Please figure out the best possible answer",
        "Important: Reward for correct answer",
        # Add any other patterns you want to exclude
    ]
    cleaned_lines = []
    for line in lines:
        if any(pattern in line for pattern in unwanted_patterns):
            continue  # Skip lines with unwanted patterns
        cleaned_lines.append(line)
    # Rejoin the cleaned lines
    cleaned_text = "\n".join(cleaned_lines)
    return cleaned_text


# --- YouTube Note Taker ---
with tab1:
    st.header("YouTube Note Taker")

    # Input fields
    youtube_url = st.text_input("Enter YouTube URL")

    # Destination folder within Obsidian vault
    vault_subfolder = st.text_input("Enter Obsidian Subfolder (relative path)", key='youtube_vault_subfolder')

    # Pattern selection
    pattern = st.selectbox("Choose a Pattern", options=["summarize", "extract_wisdom"], key='youtube_pattern')

    # Button to execute
    if st.button("Run", key='youtube_run_button'):
        if not youtube_url or not vault_subfolder:
            st.error("Please provide both a YouTube URL and a destination folder.")
        else:
            with st.spinner("Processing..."):
                try:
                    # Path to your script
                    script_path = "/app/scripts/yt_extract_and_save.sh"

                    # Ensure the script is executable
                    if not os.access(script_path, os.X_OK):
                        st.error(f"Script not executable: {script_path}")
                        sys.exit(1)

                    # Prepare the environment variables
                    env = os.environ.copy()
                    env["VAULT_PATH"] = "/mnt/c/someTestTB/ObsidianVault/ObsidianVault"

                    # Add directories to PATH
                    env["PATH"] = "/home/tsogounix/.local/bin:" + env["PATH"]

                    # Call the script
                    process = subprocess.Popen(
                        [script_path, vault_subfolder, youtube_url, pattern],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        env=env
                    )

                    # Capture output and errors
                    stdout, stderr = process.communicate()

                    # Check for errors
                    if process.returncode != 0:
                        st.error(f"Script failed with error:\n{stderr}")
                    else:
                        # Display the output
                        st.success("Script executed successfully.")

                        # Extract the summary from the output
                        summary_lines = []
                        capture = False
                        for line in stdout.splitlines():
                            if line.startswith("Summary for"):
                                capture = True
                                continue
                            if line.startswith("---------------------------------------------------"):
                                capture = False
                            if capture:
                                summary_lines.append(line)

                        summary = '\n'.join(summary_lines)

                        st.subheader("Summary:")
                        st.write(summary)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.text(traceback.format_exc())

# --- Web Page Note Taker ---
with tab2:
    st.header("Web Page Note Taker")

    # Reminder message
    st.info("Please copy the text from the website (Ctrl+A and Ctrl+C), then paste it into the text area below.")

    # Text area for the user to paste the copied content
    input_data_raw = st.text_area("Paste the copied text here", height=300)

    # Clean the input data
    input_data = clean_input_data(input_data_raw)

    # Add this to display the input data length and content    
    # Modified input data check section
    if st.button("Check Input Data", key='check_input_data'):
        # Clean the input data to remove any potential row number artifacts
        def clean_line(line):
            # Remove leading numbers and colons
            cleaned = line.strip()
            while cleaned and cleaned[0].isdigit():
                cleaned = cleaned.lstrip('0123456789: ')
            return cleaned

        # Process input lines
        input_lines = input_data.splitlines()
        cleaned_lines = [clean_line(line) for line in input_lines]
        
        # Remove any completely empty lines
        cleaned_lines = [line for line in cleaned_lines if line]
        
        # Truncate to first 20 rows
        truncated_lines = cleaned_lines[:20]
        
        # Prepare display information
        st.write(f"Total input data length: {len(input_data)} characters")
        st.write(f"Total number of rows: {len(cleaned_lines)}")
        
        # Display first 20 rows
        st.subheader("First 20 Rows:")
        display_text = '\n'.join(truncated_lines)
        st.text(display_text)
    
        # Add an indication if the text was truncated
        if len(cleaned_lines) > 20:
            st.warning(f"... and {len(cleaned_lines) - 20} more rows (not shown)")

    # Destination folder within Obsidian vault
    vault_subfolder = st.text_input("Enter Obsidian Subfolder (relative path)", key='web_vault_subfolder')

    # Pattern selection
    pattern = st.selectbox("Choose a Pattern", options=["summarize", "extract_wisdom"], key='web_pattern')

    # Web Page URL (optional)
    web_url = st.text_input("Enter Web Page URL (optional)", key='web_url')

    # Button to execute
    if st.button("Run", key='web_run_button'):
        if not input_data or not vault_subfolder:
            st.error("Please provide both the text content and a destination folder.")
        else:
            # Debug: Display the input data length and content with line numbers
            # st.write(f"Input data length before script: {len(input_data)}")
            # st.write("Input data content before script:")
            # st.text('\n'.join(f"{idx+1}: {line}" for idx, line in enumerate(input_data.splitlines())))

            with st.spinner("Processing..."):
                try:
                    # Path to your script
                    script_path = "/app/scripts/web_extract_and_save.sh"

                    # Ensure the script is executable
                    if not os.access(script_path, os.X_OK):
                        st.error(f"Script not executable: {script_path}")
                        sys.exit(1)

                    # Prepare the environment variables
                    env = os.environ.copy()
                    env["VAULT_PATH"] = "/mnt/c/someTestTB/ObsidianVault/ObsidianVault"

                    # Add directories to PATH
                    env["PATH"] = "/home/tsogounix/.local/bin:" + env["PATH"]

                    # Call the script, passing the input_data via stdin
                    process = subprocess.Popen(
                        [script_path, "llama2:latest", vault_subfolder, pattern, web_url],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        env=env,
                        #bufsize=1  # Line buffered
                    )

                    # Send input_data to the script via stdin
                    stdout, stderr = process.communicate(input=input_data)

                    # Check for errors
                    if process.returncode != 0:
                        st.error(f"Script failed with error:\n{stderr}\nStandard Output:\n{stdout}")
                    else:
                        # Display the output
                        st.success("Script executed successfully.")

                        # Extract the summary from the output
                        summary_start = stdout.find("Summary saved to")
                        summary = stdout[:summary_start].strip()

                         # Add the web URL to the summary if provided
                        if web_url:
                            summary = f"Source URL: {web_url}\n\n{summary}"

                        # Display the summary
                        st.subheader("Summary:")
                        st.write(summary)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.text(traceback.format_exc())
