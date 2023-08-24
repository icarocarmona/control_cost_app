import pandas as pd
import snowflake.connector
import streamlit as st
import toml
from snowflake.connector.cursor import SnowflakeCursor


class Snowflake:
    def _get_config(self):
        with open('.streamlit/secrets.toml', 'r') as f:
            conf = toml.load(f)
        return conf

    def _get_connection(self):
        config = self._get_config()
        connection = snowflake.connector.connect(**config['snowflake'])
        return connection

    def _parse_data(self, cursor: SnowflakeCursor):
        data = cursor.fetchall()
        col_names = []
        for metadata in cursor.description:
            col_names.append(metadata.name)

        df = pd.DataFrame(data, columns=col_names)
        return df

    def run_query(self, query) -> pd.DataFrame:
        connction = self._get_connection()
        cursor = connction.cursor()

        try:
            cursor.execute(query)
            df_data = self._parse_data(cursor)

        finally:
            cursor.close()
            connction.close()
        return df_data
