import streamlit as st


st.set_page_config(page_title="Control Cost", page_icon="☃️", layout="wide")


dashboard, data = st.tabs(["📊 Dashboard", "📅 Data"])

with dashboard:
    st.header("📊 Dashboard")
    col1, col2= st.columns(2)

    with col1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg")

    with col2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")

    


with data:
    st.header("📅 Data")
