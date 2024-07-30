import pandas

from clope.snow.connection_handling import _get_snowflake_connection


def get_operators() -> pandas.DataFrame:
    """
    Get list of Seed databases an operator uses. For most, will be 1.
    """
    conn = _get_snowflake_connection()
    try:
        query = f"SELECT * FROM DIMOPERATOR_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
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
        query = f"SELECT * FROM DIMLINEOFBUSINESS_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
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
        query = f"SELECT * FROM DIMBRANCH_V WHERE BRANCHID != -1"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_routes() -> pandas.DataFrame:
    """
    Get list of routes.
    """
    conn = _get_snowflake_connection()
    try:
        query = f"SELECT * FROM DIMROUTE_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_customers(current: bool = False) -> pandas.DataFrame:
    """
    Get list of customers.
    Implements SCD Type 2, so use current=True to get only current rows of
    information and filter out historical data.
    """
    conn = _get_snowflake_connection()
    try:
        query = f"SELECT * FROM DIMCUSTOMER_V"
        conditions = []
        if current:
            conditions.append("CURRENTROWINDICATOR = 'Current'")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_locations(current: bool = False) -> pandas.DataFrame:
    """
    Get list of locations.
    Implements SCD Type 2, so use current=True to get only current rows of
    information and filter out historical data.
    """
    conn = _get_snowflake_connection()
    try:
        query = f"SELECT * FROM DIMLOCATION_V"
        conditions = []
        if current:
            conditions.append("CURRENTROWINDICATOR = 'Current'")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_machines(current: bool = False) -> pandas.DataFrame:
    """
    Get list of machines.
    Implements SCD Type 2, so use current=True to get only current rows of
    information and filter out historical data.
    """
    conn = _get_snowflake_connection()
    try:
        query = f"SELECT * FROM DIMMACHINE_V"
        conditions = []
        if current:
            conditions.append("CURRENTROWINDICATOR = 'Current'")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_coils(current: bool = False) -> pandas.DataFrame:
    """
    Get list of coils. I.E. every coil in every machine planogram.
    Quite a lot of data, but tells you which product is where.
    Implements SCD Type 2, so use current=True to get only current rows of
    information and filter out historical data.
    """
    conn = _get_snowflake_connection()
    try:
        query = f"SELECT * FROM DIMMACHINEPLANOGRAMCOIL_V"
        conditions = []
        if current:
            conditions.append("CURRENTROWINDICATOR = 'Current'")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_micromarkets(current: bool = False) -> pandas.DataFrame:
    """
    Get list of micromarkets.
    Implements SCD Type 2, so use current=True to get only current rows of
    information and filter out historical data.
    """
    conn = _get_snowflake_connection()
    try:
        query = f"SELECT * FROM DIMMICROMARKET_V"
        conditions = []
        if current:
            conditions.append("CURRENTROWINDICATOR = 'Current'")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
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
        query = f"SELECT * FROM DIMDEVICE_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
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
        query = f"SELECT * FROM DIMITEM_V"
        conditions = []
        if current:
            conditions.append("CURRENTROWINDICATOR = 'Current'")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_item_packs() -> pandas.DataFrame:
    """
    Get list of item packs.
    """
    conn = _get_snowflake_connection()
    try:
        query = f"SELECT * FROM DIMITEMPACK_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_item_pack_barcodes() -> pandas.DataFrame:
    """
    Get list of item pack barcodes.
    """
    conn = _get_snowflake_connection()
    try:
        query = f"SELECT * FROM DIMITEMPACKBARCODE_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
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
        query = f"SELECT * FROM DIMSUPPLIER_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
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
        query = f"SELECT * FROM DIMSUPPLIERBRANCH_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
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
        query = f"SELECT * FROM DIMSUPPLIERITEM_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


def get_warehouses() -> pandas.DataFrame:
    """
    Get list of warehouses.
    """
    conn = _get_snowflake_connection()
    try:
        query = f"SELECT * FROM DIMWAREHOUSE_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df
