from snowflake.connection_handling import _get_snowflake_connection

# Function collections fact
# Function recognize sales revenue fact
# Function telelmetry sales fact


def run_function(function_name: str, function_parameters: dict):
    """
    Run a function defined in the snowflake database and return the results
    """
    conn = _get_snowflake_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            f"SELECT {function_name}({','.join([f'{k}=>{v}' for k,v in function_parameters.items()])})"
        )
        result = cur.fetchall()
    except Exception as e:
        print("Error running Snowflake function: ", e)
        raise Exception("Error running Snowflake function", e)
    finally:
        conn.close()
    return result
