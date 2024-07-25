"""
clope is a package for pulling data from the Cantaloupe/Seed Office system.
Primarily via the Spotlight API.
"""

import os
import shutil
from datetime import datetime
from typing import List, Tuple

import pandas
import requests
import snowflake.connector
from dotenv import load_dotenv


def run_report(
    report_id: str, params: List[Tuple[str, str]] = None, dtype: dict = None
) -> pandas.DataFrame:
    """
    Send GET request to Cantaloupe API to run report and receive excel file data.
    Uses Basic authentication with username and password.
    Returns a pandas dataframe of the report data.

    Takes two optional parameters:
    - params: List of tuples to pass as parameters in the GET request. Usually date ranges.
    - dtype: Dictionary of column names and data types to cast columns to.
    """
    # Check for environment variables
    # Required
    if "CLO_USERNAME" not in os.environ:
        raise Exception("CLO_USERNAME environment variable not set")
    clo_username = os.environ["CLO_USERNAME"]
    if "CLO_PASSWORD" not in os.environ:
        raise Exception("CLO_PASSWORD environment variable not set")
    clo_password = os.environ["CLO_PASSWORD"]
    # Optional
    if "CLO_BASE_URL" not in os.environ:
        clo_base_url = "https://api.mycantaloupe.com"
    else:
        clo_base_url = os.environ["CLO_BASE_URL"]
    if "CLO_ARCHIVE_FILES" not in os.environ:
        clo_archive_files = False
    else:
        clo_archive_files = os.environ["CLO_ARCHIVE_FILES"].lower() == "true"

    if params is None:
        params = []
    params.append(("ReportId", report_id))

    response = requests.get(
        clo_base_url + "/Reports/Run",
        auth=(clo_username, clo_password),
        params=params,
    )

    if response.status_code != 200:
        print("Error, could not run report: ", response.content)
        raise Exception("Error, could not run report", response.content)

    excel_data = response.content

    try:
        # Save temp excel file to local directory
        with open(f"report{report_id}.xlsx", "wb") as f:
            f.write(excel_data)
    except Exception as e:
        print("Error saving excel file: ", e)
        exit(1)

    try:
        report_df = pandas.read_excel(
            f"report{report_id}.xlsx", sheet_name="Report", dtype=dtype
        )
    except Exception as e:
        print("Error reading excel file: ", e)
        raise Exception("Error reading excel file", e)

    # Delete temp excel file
    if len(report_df) > 0:
        if clo_archive_files:
            try:
                new_dir = os.path.join(
                    os.getcwd(), "Archive", datetime.now().strftime("%Y-%m-%d")
                )
                os.makedirs(new_dir, exist_ok=True)
                shutil.move(
                    f"report{report_id}.xlsx",
                    os.path.join(new_dir, f"report{report_id}.xlsx"),
                )
            except Exception as e:
                print("Error moving excel file: ", e)
                raise Exception("Error moving excel file", e)
        else:
            try:
                os.remove(f"report{report_id}.xlsx")
            except Exception as e:
                print("Error deleting excel file: ", e)
                raise Exception("Error deleting excel file", e)

    # Print message if no data returned
    if len(report_df) == 0:
        print("No data returned from report")

    return report_df


def _get_snowflake_connection():
    """
    Connect to Snowflake data warehouse using environment variables.
    """
    conn = snowflake.connector.connect(
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
    )
    return conn


def list_tables() -> List[str]:
    """
    List all tables in Snowflake database.
    """
    conn = _get_snowflake_connection()
    try:
        cur = conn.cursor()
        cur.execute("SHOW VIEWS")
        tables = cur.fetchall()
    except Exception as e:
        print("Error listing Snowflake tables: ", e)
        raise Exception("Error listing Snowflake tables", e)
    finally:
        conn.close()
    pass
    return [table[1] for table in tables]


def get_table_data(table_name: str) -> pandas.DataFrame:
    """
    Get data from Snowflake table.
    """
    conn = _get_snowflake_connection()
    try:
        query = f"SELECT * FROM {table_name}"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        print("Error reading Snowflake table: ", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


if __name__ == "__main__":
    """
    Example usage
    """
    # Load env vars from .env file
    load_dotenv()

    # table_list = list_tables()
    branches = get_table_data("DIMBRANCH_V")

    pass
