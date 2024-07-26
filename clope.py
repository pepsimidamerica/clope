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
from snow.dimensions import *
from spotlight.spotlight import run_report

if __name__ == "__main__":
    """
    Example usage
    """
    # Load env vars from .env file
    load_dotenv()

    pass
