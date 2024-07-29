"""
clope is a package for pulling data from the Cantaloupe/Seed Office system.
Primarily via the Spotlight API.
"""

import os
from typing import List, Tuple

import pandas
import snowflake.connector
from dotenv import load_dotenv

from snow.connection_handling import _get_snowflake_connection
from snow.dates import *
from snow.dimensions import *
from snow.facts import *
from spotlight.spotlight import run_report

if __name__ == "__main__":
    """
    Example usage
    """
    # Load env vars from .env file
    load_dotenv()

    res = get_sales_revenue_by_visit_fact(
        branch=2990,
        date_range=(
            date_to_datekey(datetime(2024, 7, 1)),
            date_to_datekey(datetime(2024, 7, 23)),
        ),
    )

    pass
