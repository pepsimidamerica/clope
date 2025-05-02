"""
Module contains a function for interacting with the Cantaloupe Spotlight API.
"""

import logging
import os
import shutil
from datetime import datetime
from typing import List, Tuple

import pandas
import requests
from tenacity import (
    after_log,
    before_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from clope._logger import logger


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(
        (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException,
        )
    ),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.INFO),
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

    # Create a copy of the params list to avoid modifying the original during retries
    current_params = list(params) if params is not None else []
    current_params.append(("ReportId", report_id))

    try:
        response = requests.get(
            os.environ.get("CLO_BASE_URL", "https://api.mycantaloupe.com")
            + "/Reports/Run",
            auth=(os.environ["CLO_USERNAME"], os.environ["CLO_PASSWORD"]),
            params=current_params,
            timeout=600,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(
            f"Error, could not run report: {e.response.status_code} - {e.response.content}"
        )
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Error, could not run report: {e}")
        raise

    excel_data = response.content

    try:
        # Save temp excel file to local directory
        with open(f"report{report_id}.xlsx", "wb") as f:
            f.write(excel_data)
    except Exception as e:
        logger.error(f"Error saving excel file: {e}")
        raise Exception(f"Error saving excel file {e}")

    try:
        report_df = pandas.read_excel(
            f"report{report_id}.xlsx", sheet_name="Report", dtype=dtype
        )
    except Exception as e:
        logger.error(f"Error reading excel file: {e}")
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
            logger.error(f"Error moving excel file: {e}")
            raise Exception("Error moving excel file", e)
    else:
        try:
            os.remove(f"report{report_id}.xlsx")
        except Exception as e:
            logger.error(f"Error deleting excel file: {e}")
            raise Exception("Error deleting excel file", e)
