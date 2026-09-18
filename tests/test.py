"""
Random tests.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load env vars from a .env file
load_dotenv()

sys.path.insert(0, "")

from clope.snow import get_lines_of_business

lob = get_lines_of_business()

pass
