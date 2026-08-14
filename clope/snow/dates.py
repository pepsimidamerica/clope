"""
This module contains functionality to translate between datekeys and dates.

Technically there are tables containing this data, but I don't think
it's necessary to actually query them. We can just calculate them directly.
Should be much quicker.
"""

from datetime import datetime, timedelta

import pandas as pd


def datekey_to_date(datekey: int) -> datetime:
    """
    Convert a datekey to a datetime object.
    """
    base_date = datetime(1900, 1, 1)
    return base_date + timedelta(days=datekey - 1)


def date_to_datekey(date: datetime) -> int:
    """
    Convert a datetime object to a datekey.
    """
    base_date = datetime(1900, 1, 1)
    return (date - base_date).days + 1


def get_datekey_range(start_date: datetime, end_date: datetime) -> list[int]:
    """
    Get a list of datekeys between two dates.
    """
    return [date_to_datekey(x) for x in pd.date_range(start_date, end_date)]


def get_date_range(start_datekey: int, end_datekey: int) -> list[datetime]:
    """
    Get a list of dates between two datekeys.
    """
    return [datekey_to_date(x) for x in range(start_datekey, end_datekey + 1)]


def monthkey_to_date(monthkey: int) -> datetime:
    """
    Convert a monthkey to a datetime object representing the first day of the month.
    """
    year = 1900 + (monthkey - 1) // 12
    month = (monthkey - 1) % 12 + 1
    return datetime(year, month, 1)


def date_to_monthkey(date: datetime) -> int:
    """
    Convert a datetime object to a monthkey.
    """
    return (date.year - 1900) * 12 + date.month


def quarterkey_to_date(quarterkey: int) -> datetime:
    """
    Convert a quarterkey to a datetime object representing the first day of the quarter.
    """
    year = 1900 + (quarterkey - 1) // 4
    quarter = (quarterkey - 1) % 4 + 1
    month = (quarter - 1) * 3 + 1
    return datetime(year, month, 1)


def date_to_quarterkey(date: datetime) -> int:
    """
    Convert a datetime object to a quarterkey.
    """
    quarter = (date.month - 1) // 3 + 1
    return (date.year - 1900) * 4 + quarter


def yearkey_to_date(yearkey: int) -> datetime:
    """
    Convert a yearkey to a datetime object representing the first day of the year.
    """
    year = 1900 + yearkey - 1
    return datetime(year, 1, 1)


def date_to_yearkey(date: datetime) -> int:
    """
    Convert a datetime object to a yearkey.
    """
    return date.year - 1900 + 1
