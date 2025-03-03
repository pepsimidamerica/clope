from datetime import datetime

import pandas

from clope._logger import logger
from clope.snow.connection_handling import _get_snowflake_connection


def get_cashless_vending_transaction_fact(
    branch: int = None,
    customer: int = None,
    location: int = None,
    machine: int = None,
    item: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This fact is about the money related to a transaction.
    Pertains to vending and micromarkets lines of business only.

    :param branch: The branch key
    :param customer: The customer key
    :param location: The location key
    :param machine: The machine key
    :param item: The item key
    :param date_range: The date range the item was sold, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM CASHLESSVENDINGTRANSACTIONFACT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if customer:
            conditions.append(f"CUSTOMERKEY = {customer}")
        if location:
            conditions.append(f"LOCATIONKEY = {location}")
        if machine:
            conditions.append(f"MACHINEKEY = {machine}")
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if date_range:
            conditions.append(
                f"TRANSACTIONDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_collection_fact(
    branch: int = None,
    customer: int = None,
    location: int = None,
    machine: int = None,
    micro_market: int = None,
    route: int = None,
    line_of_business: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This fact is about the collection of money at a vend visit.
    Pertains to vending and micromarkets lines of business only.

    :param branch: The branch key
    :param customer: The customer key
    :param location: The location key
    :param machine: The machine key
    :param micro_market: The micro market key
    :param route: The route key
    :param line_of_business: The line of business key
    :param date_range: The date range the item was collected, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM COLLECTIONFACT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if customer:
            conditions.append(f"CUSTOMERKEY = {customer}")
        if location:
            conditions.append(f"LOCATIONKEY = {location}")
        if machine:
            conditions.append(f"MACHINEKEY = {machine}")
        if micro_market:
            conditions.append(f"MICROMARKETKEY = {micro_market}")
        if route:
            conditions.append(f"ROUTEKEY = {route}")
        if line_of_business:
            conditions.append(f"LINEOFBUSINESSKEY = {line_of_business}")
        if date_range:
            conditions.append(
                f"VISITDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_micromarket_salesfact(
    branch: int = None,
    customer: int = None,
    location: int = None,
    machine: int = None,
    micro_market: int = None,
    item: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This fact is about the sales of items at a micromarket.

    :param branch: The branch key
    :param customer: The customer key
    :param location: The location key
    :param machine: The machine key
    :param micro_market: The micro market key
    :param item: The item key
    :param date_range: The date range the item was sold, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM MICROMARKETSALESFACT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if customer:
            conditions.append(f"CUSTOMERKEY = {customer}")
        if location:
            conditions.append(f"LOCATIONKEY = {location}")
        if machine:
            conditions.append(f"MACHINEKEY = {machine}")
        if micro_market:
            conditions.append(f"MICROMARKETKEY = {micro_market}")
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if date_range:
            conditions.append(
                f"TRANSACTIONDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_order_fulfillment_delivery_fact(
    branch: int = None,
    customer: int = None,
    location: int = None,
    line_of_business: int = None,
    machine: int = None,
    item: int = None,
    item_pack: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This fact tracks orders from the intial creation to delivery
    specifically providing details on order quantities at the time of order
    creation, prepick, pick, and delivery.
    PrepickQuantity reflects any changes made to the order after its initial
    creation but before picking.

    :param branch: The branch key
    :param customer: The customer key
    :param location: The location key
    :param line_of_business: The line of business key
    :param machine: The machine key
    :param item: The item key
    :param item_pack: The item pack key
    :param date_range: The date range the item was delivered, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM ORDERFULFILLMENTDELIVERYFACT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if customer:
            conditions.append(f"CUSTOMERKEY = {customer}")
        if location:
            conditions.append(f"LOCATIONKEY = {location}")
        if line_of_business:
            conditions.append(f"LINEOFBUSINESSKEY = {line_of_business}")
        if machine:
            conditions.append(f"MACHINEKEY = {machine}")
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if item_pack:
            conditions.append(f"ITEMPACKKEY = {item_pack}")
        if date_range:
            conditions.append(
                f"ORDERDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_order_fulfillment_vending_market_fact(
    branch: int = None,
    customer: int = None,
    location: int = None,
    machine: int = None,
    line_of_business: int = None,
    micro_market: int = None,
    item: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This fact illustrates the flow of product from prepick to delivery
    for each vending machine and market section.

    :param branch: The branch key
    :param customer: The customer key
    :param location: The location key
    :param machine: The machine key
    :param line_of_business: The line of business key
    :param micro_market: The micro market key
    :param item: The item key
    :param date_range: The date range the item was delivered, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM ORDERFULFILLMENTVENDINGMARKETFACT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if customer:
            conditions.append(f"CUSTOMERKEY = {customer}")
        if location:
            conditions.append(f"LOCATIONKEY = {location}")
        if machine:
            conditions.append(f"MACHINEKEY = {machine}")
        if line_of_business:
            conditions.append(f"LINEOFBUSINESSKEY = {line_of_business}")
        if micro_market:
            conditions.append(f"MICROMARKETKEY = {micro_market}")
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if date_range:
            conditions.append(
                f"TARGETDELIVERYDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_delivery_order_receipt_fact(
    branch: int = None,
    customer: int = None,
    location: int = None,
    machine: int = None,
    item: int = None,
    item_pack: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This face returns information on the receipt of a delivery order and
    the original order details.

    :param branch: The branch key
    :param customer: The customer key
    :param location: The location key
    :param machine: The machine key
    :param item: The item key
    :param item_pack: The item pack key
    :param date_range: The date range the item was received, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM RECEIVEDELIVERYORDERFACT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if customer:
            conditions.append(f"CUSTOMERKEY = {customer}")
        if location:
            conditions.append(f"LOCATIONKEY = {location}")
        if machine:
            conditions.append(f"MACHINEKEY = {machine}")
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if item_pack:
            conditions.append(f"ITEMPACKKEY = {item_pack}")
        if date_range:
            conditions.append(
                f"ORDERDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_sales_revenue_by_day_fact(
    branch: int = None,
    customer: int = None,
    location: int = None,
    machine: int = None,
    item: int = None,
    item_pack: int = None,
    route: int = None,
    line_of_business: int = None,
    micro_market: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    First version of this fact. Provides sales revenue by day.
    For delivery, this is revenue from deliveries made.
    For vending, this is sales and revenue since the prior visit.
    For markets, this is sales revenue recorded from the market for the day.

    Note that for Markets, the Spoils and Commissions are not available in
    this view, as they are tied to the visit.

    :param branch: The branch key
    :param customer: The customer key
    :param location: The location key
    :param machine: The machine key
    :param item: The item key
    :param item_pack: The item pack key
    :param route: The route key
    :param line_of_business: The line of business key
    :param micro_market: The micro market key
    :param date_range: The date range of sales, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM RECOGNIZESALESREVENUEFACTBYDAY_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if customer:
            conditions.append(f"CUSTOMERKEY = {customer}")
        if location:
            conditions.append(f"LOCATIONKEY = {location}")
        if machine:
            conditions.append(f"MACHINEKEY = {machine}")
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if item_pack:
            conditions.append(f"ITEMPACKKEY = {item_pack}")
        if route:
            conditions.append(f"ROUTEKEY = {route}")
        if line_of_business:
            conditions.append(f"LINEOFBUSINESSKEY = {line_of_business}")
        if micro_market:
            conditions.append(f"MICROMARKETKEY = {micro_market}")
        if date_range:
            conditions.append(
                f"VISITDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_sales_revenue_by_visit_fact(
    branch: int = None,
    customer: int = None,
    location: int = None,
    machine: int = None,
    item: int = None,
    item_pack: int = None,
    route: int = None,
    line_of_business: int = None,
    micro_market: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This fact provides sales revenue by visit.
    For delivery, this is revenue for the deliveries made.
    For vending and market, this is sales and revenue since the prior visit.

    :param branch: The branch key
    :param customer: The customer key
    :param location: The location key
    :param machine: The machine key
    :param item: The item key
    :param item_pack: The item pack key
    :param route: The route key
    :param line_of_business: The line of business key
    :param micro_market: The micro market key
    :param date_range: The date range of visits, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM RECOGNIZESALESREVENUEFACTBYVISIT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if customer:
            conditions.append(f"CUSTOMERKEY = {customer}")
        if location:
            conditions.append(f"LOCATIONKEY = {location}")
        if machine:
            conditions.append(f"MACHINEKEY = {machine}")
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if item_pack:
            conditions.append(f"ITEMPACKKEY = {item_pack}")
        if route:
            conditions.append(f"ROUTEKEY = {route}")
        if line_of_business:
            conditions.append(f"LINEOFBUSINESSKEY = {line_of_business}")
        if micro_market:
            conditions.append(f"MICROMARKETKEY = {micro_market}")
        if date_range:
            conditions.append(
                f"VISITDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_sales_by_coil(
    branch: int = None,
    customer: int = None,
    location: int = None,
    line_of_business: int = None,
    machine: int = None,
    item: int = None,
    micro_market: int = None,
    coil: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This fact provides sales by coil for each day.

    :param branch: The branch key
    :param customer: The customer key
    :param location: The location key
    :param line_of_business: The line of business key
    :param machine: The machine key
    :param item: The item key
    :param micro_market: The micro market key
    :param coil: The coil key
    :param date_range: The date range of sales, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM SALESBYCOILFACT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if customer:
            conditions.append(f"CUSTOMERKEY = {customer}")
        if location:
            conditions.append(f"LOCATIONKEY = {location}")
        if line_of_business:
            conditions.append(f"LINEOFBUSINESSKEY = {line_of_business}")
        if machine:
            conditions.append(f"MACHINEKEY = {machine}")
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if micro_market:
            conditions.append(f"MICROMARKETKEY = {micro_market}")
        if coil:
            conditions.append(f"COILKEY = {coil}")
        if date_range:
            conditions.append(
                f"EXTRACTDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_scheduling_machine_fact(
    branch: int = None,
    customer: int = None,
    location: int = None,
    line_of_business: int = None,
    machine: int = None,
    micro_market: int = None,
    route: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This fact provides information on the scheduling of machines, what caused
    it to be scheduled, whether the schedule was edited.

    :param branch: The branch key
    :param customer: The customer key
    :param location: The location key
    :param line_of_business: The line of business key
    :param machine: The machine key
    :param micro_market: The micro market key
    :param route: The route key
    :param date_range: The date range the item was scheduled, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM SCHEDULINGMACHINEFACT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if customer:
            conditions.append(f"CUSTOMERKEY = {customer}")
        if location:
            conditions.append(f"LOCATIONKEY = {location}")
        if line_of_business:
            conditions.append(f"LINEOFBUSINESSKEY = {line_of_business}")
        if machine:
            conditions.append(f"MACHINEKEY = {machine}")
        if micro_market:
            conditions.append(f"MICROMARKETKEY = {micro_market}")
        if route:
            conditions.append(f"ROUTEKEY = {route}")
        if date_range:
            conditions.append(
                f"SCHEDULEDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_scheduling_route_summary_fact(
    branch: int = None,
    route: int = None,
    line_of_business: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This fact is a roll-up view of the statistics associated with schedules.

    :param branch: The branch key
    :param route: The route key
    :param line_of_business: The line of business key
    :param date_range: The date range the item was scheduled, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM SCHEDULINGROUTESUMMARYFACT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if route:
            conditions.append(f"ROUTEKEY = {route}")
        if line_of_business:
            conditions.append(f"LINEOFBUSINESSKEY = {line_of_business}")
        if date_range:
            conditions.append(
                f"SCHEDULINGDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_telemetry_sales_fact(
    location: int = None,
    machine: int = None,
    device: int = None,
    item: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This fact shows the sales reported on each product at each call from a
    telemeter from a vending machine.  All products associated with the
    machine at the time of the call are included.

    :param location: The location key
    :param machine: The machine key
    :param device: The device key
    :param item: The item key
    :param date_range: The date range the item was sold, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM TELEMETRYSALESFACT_V"
        conditions = []
        if location:
            conditions.append(f"LOCATIONKEY = {location}")
        if machine:
            conditions.append(f"MACHINEKEY = {machine}")
        if device:
            conditions.append(f"DEVICEKEY = {device}")
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if date_range:
            conditions.append(
                f"TRANSACTIONDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_vending_micromarket_visit_item_fact(
    branch: int = None,
    customer: int = None,
    location: int = None,
    machine: int = None,
    route: int = None,
    line_of_business: int = None,
    micro_market: int = None,
    item: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This fact provides the item level inventory and delivery information
    for replenishment visits for Vending and Micromarkets.

    :param branch: The branch key
    :param customer: The customer key
    :param location: The location key
    :param machine: The machine key
    :param route: The route key
    :param line_of_business: The line of business key
    :param micro_market: The micro market key
    :param item: The item key
    :param date_range: The date range the item was visited, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM VENDINGMICROMARKETVISITITEMFACT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if customer:
            conditions.append(f"CUSTOMERKEY = {customer}")
        if location:
            conditions.append(f"LOCATIONKEY = {location}")
        if machine:
            conditions.append(f"MACHINEKEY = {machine}")
        if route:
            conditions.append(f"ROUTEKEY = {route}")
        if line_of_business:
            conditions.append(f"LINEOFBUSINESSKEY = {line_of_business}")
        if micro_market:
            conditions.append(f"MICROMARKETKEY = {micro_market}")
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if date_range:
            conditions.append(
                f"VISITDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_warehouse_inventory_fact(
    branch: int = None,
    warehouse: int = None,
    item: int = None,
    item_pack: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This fact provides a view of the start of day inventory for each warehouse.

    :param branch: The branch key
    :param warehouse: The warehouse key
    :param item: The item key
    :param item_pack: The item pack key
    :param date_range: The date range the item was received, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM WAREHOUSEINVENTORYFACT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if warehouse:
            conditions.append(f"WAREHOUSEKEY = {warehouse}")
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if item_pack:
            conditions.append(f"PARPACKKEY = {item_pack}")
        if date_range:
            conditions.append(
                f"INVENTORYDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_warehouse_observed_inventory_fact(
    branch: int = None,
    warehouse: int = None,
    item: int = None,
    item_pack: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This fact provides the view of the observed inventories that were captured.

    :param branch: The branch key
    :param warehouse: The warehouse key
    :param item: The item key
    :param item_pack: The item pack key
    :param date_range: The date range the item was observed, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM WAREHOUSEOBSERVEDINVENTORYFACT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if warehouse:
            conditions.append(f"WAREHOUSEKEY = {warehouse}")
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if item_pack:
            conditions.append(f"ITEMPACKKEY = {item_pack}")
        if date_range:
            conditions.append(
                f"EFFECTIVEDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_warehouse_prod_movement_fact(
    branch: int = None,
    from_warehouse: int = None,
    to_warehouse: int = None,
    item: int = None,
    item_pack: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This fact is for reporting on all product movements.

    :param branch: The branch key
    :param from_warehouse: The warehouse key the product is moving from
    :param to_warehouse: The warehouse key the product is moving to
    :param item: The item key
    :param item_pack: The item pack key
    :param date_range: The date range the item was moved, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM WAREHOUSEPRODUCTMOVEMENTFACT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if from_warehouse:
            conditions.append(f"FROMWAREHOUSEKEY = {from_warehouse}")
        if to_warehouse:
            conditions.append(f"TOWAREHOUSEKEY = {to_warehouse}")
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if item_pack:
            conditions.append(f"ITEMPACKKEY = {item_pack}")
        if date_range:
            conditions.append(
                f"EFFECTIVEDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_warehouse_purchase_fact(
    branch: int = None,
    warehouse: int = None,
    item: int = None,
    item_pack: int = None,
    supplier: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This fact provides the view of the purchases made by the warehouse.

    :param branch: The branch key
    :param warehouse: The warehouse key
    :param item: The item key
    :param item_pack: The item pack key
    :param supplier: The supplier key
    :param date_range: The date range the item was purchased, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM WAREHOUSEPURCHASEFACT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if warehouse:
            conditions.append(f"WAREHOUSEKEY = {warehouse}")
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if item_pack:
            conditions.append(f"ITEMPACKKEY = {item_pack}")
        if supplier:
            conditions.append(f"SUPPLIERKEY = {supplier}")
        if date_range:
            conditions.append(
                f"EFFECTIVEDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_warehouse_receive_fact(
    branch: int = None,
    warehouse: int = None,
    item: int = None,
    item_pack: int = None,
    supplier: int = None,
    date_range: tuple[int, int] = None,
) -> pandas.DataFrame:
    """
    This fact provides info about what was received by the warehouse.

    :param branch: The branch key
    :param warehouse: The warehouse key
    :param item: The item key
    :param item_pack: The item pack key
    :param supplier: The supplier key
    :param date_range: The date range the item was received, as a tuple of date keys
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM WAREHOUSERECEIVEFACT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if warehouse:
            conditions.append(f"WAREHOUSEKEY = {warehouse}")
        if item:
            conditions.append(f"ITEMKEY = {item}")
        if item_pack:
            conditions.append(f"ITEMPACKKEY = {item_pack}")
        if supplier:
            conditions.append(f"SUPPLIERKEY = {supplier}")
        if date_range:
            conditions.append(
                f"EFFECTIVEDATEKEY BETWEEN {date_range[0]} AND {date_range[1]}"
            )
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


def get_machine_alerts_fact(
    branch: int = None,
    customer: int = None,
    location: int = None,
    machine: int = None,
    micro_market: int = None,
    effective_date_range: tuple[int, int] = None,
    added_date_range: tuple[datetime, datetime] = None,
) -> pandas.DataFrame:
    """
    This fact contains info on machine alerts that Cantaloupe has raised.
    Out of order, not dexing, etc.

    :param branch: The branch key
    :param customer: The customer key
    :param location: The location key
    :param machine: The machine key
    :param micro_market: The micro market key
    :param effective_date_range: The date range the alert was effective, as a tuple of date keys
    :param added_date_range: The date range the alert was added, as a tuple of datetime objects
    """
    conn = _get_snowflake_connection()
    try:
        query = "SELECT * FROM MACHINEALERTSFACT_V"
        conditions = []
        if branch:
            conditions.append(f"BRANCHKEY = {branch}")
        if customer:
            conditions.append(f"CUSTOMERKEY = {customer}")
        if location:
            conditions.append(f"LOCATIONKEY = {location}")
        if machine:
            conditions.append(f"MACHINEKEY = {machine}")
        if micro_market:
            conditions.append(f"MICROMARKETKEY = {micro_market}")
        if effective_date_range:
            conditions.append(
                f"CREATEDDATEKEY BETWEEN {effective_date_range[0]} AND {effective_date_range[1]}"
            )
        if added_date_range:
            conditions.append(
                f"INSERTDATETIME BETWEEN '{added_date_range[0]}' AND '{added_date_range[1]}'"
            )
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
