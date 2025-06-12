"""
The clope spotlight module provides functions for running reports using the
Cantaloupe spotlight API. It includes a synchronous and an asynchronous function.
"""

from .spotlight import async_run_report, run_report

__all__ = ["run_report", "async_run_report"]
