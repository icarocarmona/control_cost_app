import streamlit as st
import data as dados

st.set_page_config(page_title='Control Cost', page_icon='☃️', layout='wide')

dashboard, data = st.tabs(['📊 Dashboard', '📅 Data'])

with dashboard:
    st.header('📊 Dashboard')
    col1, col2 = st.columns(2)

    with col1:
        st.header('A cat')
        st.image('https://static.streamlit.io/examples/cat.jpg')

    with col2:
        st.header('A dog')
        st.image('https://static.streamlit.io/examples/dog.jpg')


with data:
    st.header('📅 Data')
    st.markdown("## Warehouses")
    st.write(dados.get_warehouses())

    st.markdown("## Cost by Warehouse")
    st.write(dados.get_cost_by_warehouse())

    st.markdown("## Cost by Account")
    st.write(dados.get_cost_by_account())

    st.markdown("## Statements Timeouts")
    st.write(dados.get_statement_timeouts())

    st.markdown("## Users")
    st.write(dados.get_users())

    st.markdown(
        "## DML from the information schema to identify table sizes and last updated timestamps")
    st.write(dados.get_tables_size_last_updated())

    st.markdown("## Top 10 queries")
    st.write(dados.get_top_10_query())

    st.markdown("## Top 10 queries time executions")
    st.write(dados.get_top_10_query_time())

    st.markdown("## Top 10 queries queue")
    st.write(dados.get_top_10_query_queue())

    st.markdown("## Top 10 queries price")
    st.write(dados.get_top_10_query_price())
