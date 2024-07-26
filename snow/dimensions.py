import pandas

from snow.connection_handling import _get_snowflake_connection


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
        query = f"SELECT * FROM DIMBRANCH_V"
        cur = conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
    except Exception as e:
        raise Exception("Error reading Snowflake table", e)
    finally:
        conn.close()
    return df


# Routes
# Customers
# Locations
# Machines
# Machine planogram coils
# Micromarkets
# Devices

# Items
# Item packs
# item pack barcodes

# Suppliers
# Warehouses
