"""
clope is a package for pulling data from the Cantaloupe/Seed Office system.
Primarily via the Spotlight API.
"""

import os
from typing import List, Tuple

import pandas
import snowflake.connector
from dotenv import load_dotenv

from connection_handling import _get_snowflake_connection
from dimensions import *
from spotlight import run_report


def list_views() -> List[str]:
    """
    List all views in Snowflake database.
    """
    conn = _get_snowflake_connection()
    try:
        cur = conn.cursor()
        cur.execute("SHOW VIEWS")
        tables = cur.fetchall()
    except Exception as e:
        raise Exception("Error listing Snowflake views", e)
    finally:
        conn.close()
    return [table[1] for table in tables]


# def get_view_data(table_name: str) -> pandas.DataFrame:
#     """
#     Get data from a Snowflake table.
#     """
#     conn = _get_snowflake_connection()
#     try:
#         query = f"SELECT * FROM {table_name}"
#         cur = conn.cursor()
#         cur.execute(query)
#         df = cur.fetch_pandas_all()
#     except Exception as e:
#         print("Error reading Snowflake table: ", e)
#         raise Exception("Error reading Snowflake table", e)
#     finally:
#         conn.close()
#     return df


if __name__ == "__main__":
    """
    Example usage
    """
    # Load env vars from .env file
    load_dotenv()

    list_views()
    pass
