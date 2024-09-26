"""
Module contains a function for interacting with the Cantaloupe Spotlight API.
"""

import os
import shutil
from datetime import datetime
from typing import List, Tuple

import pandas
import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(
        (requests.exceptions.ConnectionError, requests.exceptions.Timeout)
    ),
)
def run_report(
    report_id: str, params: List[Tuple[str, str]] = None, dtype: dict = None
) -> pandas.DataFrame:
    """
    Send GET request to Cantaloupe API to run report and receive excel file data.
    Uses Basic authentication with username and password.
    Returns a pandas dataframe of the report data.

    :param report_id: The ID of the report to run.
    :param params: A list of tuples to pass as parameters in the GET request. Usually date ranges.
    :param dtype: Dictionary of column names and data types to cast columns to.
    """
    # Check for environment variables
    if "CLO_USERNAME" not in os.environ:
        raise Exception("CLO_USERNAME environment variable not set")
    if "CLO_PASSWORD" not in os.environ:
        raise Exception("CLO_PASSWORD environment variable not set")

    if params is None:
        params = []
    params.append(("ReportId", report_id))

    try:
        response = requests.get(
            os.environ.get("CLO_BASE_URL", "https://api.mycantaloupe.com")
            + "/Reports/Run",
            auth=(os.environ["CLO_USERNAME"], os.environ["CLO_PASSWORD"]),
            params=params,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Error, could not run report: {e.response.status_code} - {e.response.content}"
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error, could not run report: {e}")

    excel_data = response.content

    try:
        # Save temp excel file to local directory
        with open(f"report{report_id}.xlsx", "wb") as f:
            f.write(excel_data)
    except Exception as e:
        raise Exception(f"Error saving excel file {e}")

    try:
        report_df = pandas.read_excel(
            f"report{report_id}.xlsx", sheet_name="Report", dtype=dtype
        )
    except Exception as e:
        raise Exception(f"Error reading excel file: {e}")

    # Delete temp excel file
    if len(report_df) > 0:
        _handle_temp_file(report_id)

    return report_df


def _handle_temp_file(report_id: str):
    """
    Helper function that gets called after the report is run.
    """
    if os.environ.get("CLO_ARCHIVE_FILES", "false").lower() == "true":
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
