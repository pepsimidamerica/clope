"""
Module contains a function for interacting with the Cantaloupe Spotlight API.
"""

import io
import logging
import os

import aiohttp
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

logger = logging.getLogger(__name__)


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
    report_id: str,
    params: list[tuple[str, str]] | None = None,
    dtype: dict | None = None,
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
        excel_data = response.content
    except requests.exceptions.HTTPError as e:
        logger.error(
            f"Error, could not run report: {e.response.status_code} - {e.response.content}"
        )
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Error, could not run report: {e}")
        raise

    try:
        buf = io.BytesIO(excel_data)
        report_df = pandas.read_excel(buf, sheet_name="Report", dtype=dtype)
    except Exception as e:
        logger.error(f"Error reading excel file: {e}")
        raise Exception(f"Error reading excel file: {e}")

    return report_df


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(
        (
            aiohttp.ClientConnectionError,
            aiohttp.ClientResponseError,
            aiohttp.ClientPayloadError,
            aiohttp.ServerTimeoutError,
        )
    ),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.INFO),
)
async def async_run_report(
    report_id: str,
    params: list[tuple[str, str]] | None = None,
    dtype: dict | None = None,
) -> pandas.DataFrame:
    """
    Asynchronous version of run_report.
    Sends GET request to Cantaloupe API to run report and receive excel file data.
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

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                os.environ.get("CLO_BASE_URL", "https://api.mycantaloupe.com")
                + "/Reports/Run",
                auth=aiohttp.BasicAuth(
                    os.environ["CLO_USERNAME"], os.environ["CLO_PASSWORD"]
                ),
                params=current_params,
                timeout=aiohttp.ClientTimeout(total=600),
            ) as response:
                response.raise_for_status()
                excel_data = await response.read()
        except aiohttp.ClientError as e:
            logger.error(f"Error, could not run report: {e}")
            raise

    try:
        buf = io.BytesIO(excel_data)
        report_df = pandas.read_excel(buf, sheet_name="Report", dtype=dtype)
    except Exception as e:
        logger.error(f"Error reading excel file: {e}")
        raise Exception(f"Error reading excel file: {e}")

    return report_df
