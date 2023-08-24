from snow import Snowflake
import queries as query
import streamlit as st


@st.cache_data
def get_warehouses():
    return Snowflake().run_query(query.SHOW_WAREHOUSES)


@st.cache_data
def get_cost_by_warehouse():
    return Snowflake().run_query(query.COST_BY_WAREHOUSE)


@st.cache_data
def get_cost_by_account():
    return Snowflake().run_query(query.COST_BY_ACCOUNT)


@st.cache_data
def get_statement_timeouts():
    return Snowflake().run_query(query.STATEMENT_TIMEOUTS)


@st.cache_data
def get_users():
    df = Snowflake().run_query(query.GET_USERS)
    return df[["login_name", "disabled", "last_success_login"]]


@st.cache_data
def get_tables_size_last_updated():
    return Snowflake().run_query(query.TABLES_SIZE)


@st.cache_data
def get_top_10_query():
    return Snowflake().run_query(query.TOP_QUERIES)


@st.cache_data
def get_top_10_query_time():
    return Snowflake().run_query(query.TOP_QUERIES_TIME)


@st.cache_data
def get_top_10_query_queue():
    return Snowflake().run_query(query.TOP_QUERIES_QUEUE)


@st.cache_data
def get_top_10_query_price():
    return Snowflake().run_query(query.TOP_QUERIES_PRICE)
