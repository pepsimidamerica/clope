"""
clope is a package for pulling data from the Cantaloupe/Seed Office system.
Primarily via the Spotlight API.
"""

from .snow.dates import *
from .snow.dimensions import *
from .snow.facts import *
from .spotlight.spotlight import run_report

if __name__ == "__main__":
    """
    Example usage
    """
    pass
