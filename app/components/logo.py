import streamlit as st
import base64

def display_logo(logo_path):
    """
    Displays a logo in the top-left corner using Streamlit.

    Args:
        logo_path (str): Path to the logo image file.
    """
    def get_base64_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    # Convert the logo image to Base64
    logo_base64 = get_base64_image(logo_path)

    # Add custom CSS to position the logo
    st.markdown(
        f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" alt="Logo">
        </div>
        """,
        unsafe_allow_html=True
    )
