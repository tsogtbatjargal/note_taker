import os
import subprocess
import traceback
import streamlit as st
import base64

# Set paths dynamically
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
VAULT_PATH = "/mnt/c/someTestTB/ObsidianVault/ObsidianVault"

# Utility to execute shell scripts
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


# Function to encode the image as a base64 string for embedding
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
