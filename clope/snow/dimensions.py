import pandas

from clope._logger import logger
from clope.snow.connection_handling import _get_snowflake_connection


def get_operators() -> pandas.DataFrame:
    """
    Get list of Seed databases an operator uses. For most, will be 1.
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMOPERATOR_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_lines_of_business() -> pandas.DataFrame:
    """
    Reference table for the three lines of business.
    Delivery, Micromarket, and Vending
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMLINEOFBUSINESS_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_branches() -> pandas.DataFrame:
    """
    Get list of branches.
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMBRANCH_V WHERE BRANCHID != -1"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_routes(branch: int = None) -> pandas.DataFrame:
    """
    Get list of routes.

    :param branch: Filter by branch key
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMROUTE_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_customers(current: bool = False, branch: int = None) -> pandas.DataFrame:
    """
    Get list of customers.
    Implements SCD Type 2, so use current=True to get only current rows of
    information and filter out historical data.

    :param current: Filter by current row indicator
    :param branch: Filter by branch key
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMCUSTOMER_V"
        conditions = []
        if current:
            conditions.append("CURRENTROWINDICATOR = 'Current'")
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_locations(current: bool = False, customer: int = None) -> pandas.DataFrame:
    """
    Get list of locations.
    Implements SCD Type 2, so use current=True to get only current rows of
    information and filter out historical data.

    :param current: Filter by current row indicator
    :param customer: Filter by customer key
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMLOCATION_V"
        conditions = []
        if current:
            conditions.append("CURRENTROWINDICATOR = 'Current'")
        if customer:
            conditions.append(f"CUSTOMERKEY = {customer}")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_machines(
    current: bool = False, location: int = None, route: int = None
) -> pandas.DataFrame:
    """
    Get list of machines.
    Implements SCD Type 2, so use current=True to get only current rows of
    information and filter out historical data.

    :param current: Filter by current row indicator
    :param location: Filter by location key
    :param route: Filter by route key
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMMACHINE_V"
        conditions = []
        if current:
            conditions.append("CURRENTROWINDICATOR = 'Current'")
        if location:
            conditions.append(f"LOCATIONKEY = {location}")
        if route:
            conditions.append(f"ROUTEKEY = {route}")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_coils(
    current: bool = False,
    machine: int = None,
    item: int = None,
) -> pandas.DataFrame:
    """
    Get list of coils. I.E. every coil in every machine planogram.
    Quite a lot of data, but tells you which product is where.
    Implements SCD Type 2, so use current=True to get only current rows of
    information and filter out historical data.

    :param current: Filter by current row indicator
    :param machine: Filter by machine key
    :param item: Filter by item key
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMMACHINEPLANOGRAMCOIL_V"
        conditions = []
        if current:
            conditions.append("CURRENTROWINDICATOR = 'Current'")
        if machine:
            conditions.append(f"MACHINEKEY = {machine}")
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_micromarkets(
    current: bool = False,
    location: int = None,
    route: int = None,
) -> pandas.DataFrame:
    """
    Get list of micromarkets.
    Implements SCD Type 2, so use current=True to get only current rows of
    information and filter out historical data.

    :param current: Filter by current row indicator
    :param location: Filter by location key
    :param route: Filter by route key
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMMICROMARKET_V"
        conditions = []
        if current:
            conditions.append("CURRENTROWINDICATOR = 'Current'")
        if location:
            conditions.append(f"LOCATIONKEY = {location}")
        if route:
            conditions.append(f"ROUTEKEY = {route}")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_telemetry_devices() -> pandas.DataFrame:
    """
    Get list of telemetry devices.
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMDEVICE_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_items(current: bool = False) -> pandas.DataFrame:
    """
    Get list of items.
    Implements SCD Type 2, so use current=True to get only current rows of
    information and filter out historical data.
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMITEM_V"
        conditions = []
        if current:
            conditions.append("CURRENTROWINDICATOR = 'Current'")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_item_packs(item: int = None) -> pandas.DataFrame:
    """
    Get list of item packs.

    :param item: Filter by item key
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMITEMPACK_V"
        conditions = []
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_item_pack_barcodes(item: int = None, item_pack: int = None) -> pandas.DataFrame:
    """
    Get list of item pack barcodes.

    :param item: Filter by item key
    :param item_pack: Filter by item pack key
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMITEMPACKBARCODE_V"
        conditions = []
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if item_pack:
            conditions.append(f"ITEMPACKKEY = {item_pack}")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_suppliers() -> pandas.DataFrame:
    """
    Get list of suppliers.
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMSUPPLIER_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_supplier_branch() -> pandas.DataFrame:
    """
    Get list of supplier branches.
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMSUPPLIERBRANCH_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_supplier_items() -> pandas.DataFrame:
    """
    Get list of supplier items.
    NOTE: Doesn't seem to be used yet. No rows as of writing.
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMSUPPLIERITEM_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_warehouses(branch: int = None) -> pandas.DataFrame:
    """
    Get list of warehouses.

    :param branch: Filter by branch key
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM DIMWAREHOUSE_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        logger.error("Error reading Snowflake table", e)
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df
