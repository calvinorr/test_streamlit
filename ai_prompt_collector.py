import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import plotly.express as px

# Database setup
def init_db():
    conn = sqlite3.connect('ai_prompts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS prompts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  prompt TEXT,
                  link TEXT,
                  tags TEXT,
                  category TEXT,
                  ai_model TEXT,
                  date_added TEXT)''')
    conn.commit()
    return conn

def add_entry(conn, prompt, link, tags, category, ai_model):
    c = conn.cursor()
    c.execute('''INSERT INTO prompts (prompt, link, tags, category, ai_model, date_added)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (prompt, link, tags, category, ai_model, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

def get_all_entries(conn):
    return pd.read_sql_query("SELECT * from prompts", conn)

def main():
    st.set_page_config(page_title="AI Prompt Collector", page_icon="🤖", layout="wide")

    # Custom CSS for dark mode
    st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stButton>button {
        color: #0E1117;
        background-color: #00FFFF;
        border-radius: 5px;
    }
    .stTextInput>div>div>input, .stTextArea textarea {
        background-color: #262730;
        color: #FAFAFA;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🤖 AI Prompt Collector")

    # Initialize database connection
    conn = init_db()

    # Sidebar for input
    st.sidebar.header("Add New Entry")
    prompt = st.sidebar.text_area("Enter your AI prompt:")
    link = st.sidebar.text_input("Enter a useful article link:")
    tags = st.sidebar.text_input("Enter tags (comma-separated):")
    category = st.sidebar.selectbox("Select a category:", ["General", "Code", "Writing", "Image", "Other"])
    ai_model = st.sidebar.selectbox("Select AI Model:", ["ChatGPT", "Claude", "DALL-E", "Midjourney", "Stable Diffusion", "Other"])

    if st.sidebar.button("Add Entry"):
        if prompt or link:
            add_entry(conn, prompt, link, tags, category, ai_model)
            st.sidebar.success("Entry added successfully!")

    # Main content area
    tab1, tab2, tab3 = st.tabs(["📚 Entries", "🔍 Search & Filter", "📊 Analytics"])

    with tab1:
        st.header("Saved Prompts and Links")
        data = get_all_entries(conn)
        st.dataframe(data)  # Simplified dataframe display

    with tab2:
        st.header("Search and Filter")
        search_term = st.text_input("Search prompts and links:")
        col1, col2 = st.columns(2)
        with col1:
            filter_category = st.multiselect("Filter by category:", data['category'].unique())
        with col2:
            filter_model = st.multiselect("Filter by AI Model:", data['ai_model'].unique())

        filtered_data = data

        if search_term:
            filtered_data = filtered_data[filtered_data['prompt'].str.contains(search_term, case=False, na=False) | 
                                          filtered_data['link'].str.contains(search_term, case=False, na=False) |
                                          filtered_data['tags'].str.contains(search_term, case=False, na=False)]

        if filter_category:
            filtered_data = filtered_data[filtered_data['category'].isin(filter_category)]

        if filter_model:
            filtered_data = filtered_data[filtered_data['ai_model'].isin(filter_model)]

        st.dataframe(filtered_data)  # Simplified dataframe display

        if st.button("Export Filtered Data"):
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="ai_prompts_and_links.csv",
                mime="text/csv"
            )

    with tab3:
        st.header("Analytics")
        col1, col2 = st.columns(2)
        with col1:
            category_counts = data['category'].value_counts()
            fig1 = px.pie(values=category_counts.values, names=category_counts.index, title="Prompts by Category", template="plotly_dark")
            st.plotly_chart(fig1)
        with col2:
            model_counts = data['ai_model'].value_counts()
            fig2 = px.bar(x=model_counts.index, y=model_counts.values, title="Prompts by AI Model", template="plotly_dark")
            st.plotly_chart(fig2)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
