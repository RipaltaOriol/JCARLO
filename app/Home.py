import streamlit as st

st.set_page_config(
    page_title="JCarlo",
    page_icon="📝",
)

st.write("# Welcome to JCarlo! 👋")

st.sidebar.success("Select a model from above.")

st.markdown(
    """
    JCarlo aims to be an AI tool able to find research sources from user prompts.
"""
)