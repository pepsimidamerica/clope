"""
Module contains a function for interacting with the Cantaloupe Spotlight API.
"""

import io
import logging
import os

import httpx2
import pandas as pd
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
            httpx2.TimeoutException,
            httpx2.NetworkError,
        )
    ),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.INFO),
)
def run_report(
    report_id: str,
    params: list[tuple[str, str]] | None = None,
    dtype: dict | None = None,
) -> pd.DataFrame:
    """
    Send GET request to Cantaloupe API to run report and receive excel file data.
    Uses Basic authentication with username and password.
    Returns a pd dataframe of the report data.

    :param report_id: The ID of the report to run.
    :type report_id: str
    :param params: A list of tuples to pass as parameters in the GET request. Usually date ranges.
    :type params: list[tuple[str, str]] | None
    :param dtype: Dictionary of column names and data types to cast columns to.
    :type dtype: dict | None
    :return: pd DataFrame containing the report data.
    :rtype: pd.DataFrame
    """
    # Check for environment variables
    if "CLO_USERNAME" not in os.environ:
        raise OSError("CLO_USERNAME environment variable not set")
    if "CLO_PASSWORD" not in os.environ:
        raise OSError("CLO_PASSWORD environment variable not set")

    # Create a copy of the params list to avoid modifying the original during retries
    current_params = list(params) if params is not None else []
    current_params.append(("ReportId", report_id))

    # Convert params to a dictionary for the request
    params_dict = {}
    for key, value in current_params:
        params_dict.setdefault(key, []).append(value)

    try:
        response = httpx2.get(
            os.environ.get("CLO_BASE_URL", "https://api.mycantaloupe.com")
            + "/Reports/Run",
            auth=(os.environ["CLO_USERNAME"], os.environ["CLO_PASSWORD"]),
            params=params_dict,
            timeout=600,
        )
        response.raise_for_status()
        excel_data = response.content
    except httpx2.HTTPError as e:
        logger.error(f"Error, could not run report: {e.request.url} - {e}")
        raise
    except httpx2.RequestError as e:
        logger.error(f"Error, could not run report: {e}")
        raise

    try:
        buf = io.BytesIO(excel_data)
        report_df = pd.read_excel(buf, sheet_name="Report", dtype=dtype)
    except Exception as e:
        logger.error(f"Error reading excel file: {e}")
        raise Exception(f"Error reading excel file: {e}") from e

    return report_df


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(
        (
            httpx2.TimeoutException,
            httpx2.NetworkError,
        )
    ),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.INFO),
)
async def async_run_report(
    report_id: str,
    params: list[tuple[str, str]] | None = None,
    dtype: dict | None = None,
) -> pd.DataFrame:
    """
    Asynchronous version of run_report.
    Sends GET request to Cantaloupe API to run report and receive excel file data.
    Uses Basic authentication with username and password.
    Returns a pd dataframe of the report data.

    :param report_id: The ID of the report to run.
    :type report_id: str
    :param params: A list of tuples to pass as parameters in the GET request. Usually date ranges.
    :type params: list[tuple[str, str]] | None
    :param dtype: Dictionary of column names and data types to cast columns to.
    :type dtype: dict | None
    :return: pd DataFrame containing the report data.
    :rtype: pd.DataFrame
    """
    # Check for environment variables
    if "CLO_USERNAME" not in os.environ:
        raise OSError("CLO_USERNAME environment variable not set")
    if "CLO_PASSWORD" not in os.environ:
        raise OSError("CLO_PASSWORD environment variable not set")

    # Create a copy of the params list to avoid modifying the original during retries
    current_params = list(params) if params is not None else []
    current_params.append(("ReportId", report_id))

    # Convert params to a dictionary for the request
    params_dict = {}
    for key, value in current_params:
        params_dict.setdefault(key, []).append(value)

    async with httpx2.AsyncClient() as client:
        try:
            res = await client.get(
                os.environ.get("CLO_BASE_URL", "https://api.mycantaloupe.com")
                + "/Reports/Run",
                auth=(os.environ["CLO_USERNAME"], os.environ["CLO_PASSWORD"]),
                params=params_dict,
                timeout=600,
            )
            res.raise_for_status()
            excel_data = await res.aread()
        except httpx2.HTTPError as e:
            logger.error(f"Error, could not run report: {e}")
            raise

    try:
        buf = io.BytesIO(excel_data)
        report_df = pd.read_excel(buf, sheet_name="Report", dtype=dtype)
    except Exception as e:
        logger.error(f"Error reading excel file: {e}")
        raise Exception(f"Error reading excel file: {e}") from e

    return report_df


# if __name__ == "__main__":
#     from dotenv import load_dotenv

#     load_dotenv()
#     df_delivery_prepick = run_report(
#         "36626",
#         [
#             ("filter0", "2026-08-14"),
#             ("filter0", "2026-08-18"),
#             ("filter16", "Delivery"),
#         ],
#         {"Item Code": str, "Customer Code": str},
#     )
#     # Save to Excel
#     df_delivery_prepick.to_excel("delivery_prepick.xlsx", index=False)
