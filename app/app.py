import sys
import os
import streamlit as st

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.utils import load_css
from app.components.logo import display_logo
from app.components.tabs.youtube_tab import youtube_tab
from app.components.tabs.web_page_tab import web_page_tab
from app.config import APP_TITLE, LOGO_PATH

# Set page configuration - MUST BE FIRST!
st.set_page_config(page_title=APP_TITLE, layout="wide")

# Load CSS
css_file_path = os.path.join(os.path.dirname(__file__), '..', 'styles', 'main.css')
load_css(css_file_path)


# Display the logo
display_logo(LOGO_PATH)

st.title(APP_TITLE)

# Tabs for YouTube and Web Page Note Takers
tab1, tab2 = st.tabs(["YouTube Note Taker", "Web Page Note Taker"])

# --- YouTube Note Taker ---
with tab1:
    youtube_tab()

# --- Web Page Note Taker ---
with tab2:
    web_page_tab()
