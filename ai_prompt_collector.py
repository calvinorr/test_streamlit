import streamlit as st
import pandas as pd

def main():
    st.title("AI Prompt Collector")

    # Initialize session state
    if 'prompts' not in st.session_state:
        st.session_state.prompts = []
    if 'links' not in st.session_state:
        st.session_state.links = []

    # Input fields
    prompt = st.text_area("Enter your AI prompt:")
    link = st.text_input("Enter a useful article link:")

    if st.button("Add"):
        if prompt:
            st.session_state.prompts.append(prompt)
        if link:
            st.session_state.links.append(link)

    # Display saved prompts and links
    st.subheader("Saved Prompts")
    for p in st.session_state.prompts:
        st.write(p)

    st.subheader("Saved Links")
    for l in st.session_state.links:
        st.write(l)

if __name__ == "__main__":
    main()
