import snowflake.connector

import streamlit as st
import toml
import pandas as pd
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

with open('.streamlit/secrets.toml', 'r') as f:
    config = toml.load(f)


# Função para listar os warehouses
def listar_warehouses():
    try:
        # Conectando ao Snowflake
        connection = snowflake.connector.connect(**config["snowflake"])

        # Executando a query para listar os warehouses
        cursor = connection.cursor()
        cursor.execute("SHOW WAREHOUSES")

        # Obtendo os resultados e exibindo-os
        # warehouses = [row[0] for row in cursor]
        # st.write("Warehouses disponíveis:")
        # for warehouse in warehouses:
        #     st.write(warehouse)

        # st.write(cursor.description)
        dat = cursor.fetchall()

        df = pd.DataFrame(dat, columns=cursor.description)

        col_names = []
        for elt in cursor.description:
            col_names.append(elt[0])
        df = pd.DataFrame(dat, columns=col_names)
        wh_list = df[df['auto_suspend'] != ''][[
            'name', 'auto_suspend', 'auto_resume']]
        st.write(wh_list)

    except Exception as e:
        st.error(f"Erro ao listar os warehouses: {e}")


if __name__ == "__main__":
    st.title("Listar Warehouses do Snowflake")
    listar_warehouses()
