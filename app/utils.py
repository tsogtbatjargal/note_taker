import os
import subprocess
import traceback
import streamlit as st


# Set paths dynamically
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
VAULT_PATH = "/mnt/c/someTestTB/ObsidianVault/ObsidianVault"

def execute_script(script_name, args, input_data=None):
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Script not found: {script_path}")
    if not os.access(script_path, os.X_OK):
        raise PermissionError(f"Script not executable: {script_path}")
    
    env = os.environ.copy()
    env["VAULT_PATH"] = VAULT_PATH

    process = subprocess.Popen(
        [script_path] + args,
        stdin=subprocess.PIPE if input_data else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )

    stdout, stderr = process.communicate(input=input_data)

    if process.returncode != 0:
        raise RuntimeError(f"Script execution failed:\n{stderr}")
    
    return stdout

def clean_input_data(input_text):
    """
    Cleans the raw input text by removing unwanted patterns, empty lines,
    and leading/trailing whitespace.

    Args:
        input_text (str): Raw input text.

    Returns:
        str: Cleaned input text.
    """
    unwanted_patterns = [
        "Please figure out the best possible answer",
        "Important: Reward for correct answer",
    ]

    lines = input_text.splitlines()
    cleaned_lines = []

    for line in lines:
        if any(pattern in line for pattern in unwanted_patterns):
            continue
        cleaned_line = line.strip()
        if cleaned_line:
            cleaned_lines.append(cleaned_line)

    cleaned_text = "\n".join(cleaned_lines)
    return cleaned_text


def load_css(file_name):
    with open(file_name) as f:
        css_content = f.read()
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)