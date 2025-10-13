import os

import snowflake.connector


def _get_snowflake_connection(
    schema: str = "PUBLIC",
) -> snowflake.connector.SnowflakeConnection:
    """
    Connect to Snowflake data warehouse using environment variables. By default,
    connects to the main PUBLIC schema. Can be overridden to connect to others.
    """
    for env in [
        "SNOWFLAKE_USER",
        # "SNOWFLAKE_PASSWORD",
        "SNOWFLAKE_PRIVATE_KEY_FILE",
        "SNOWFLAKE_PRIVATE_KEY_FILE_PWD",
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_WAREHOUSE",
        "SNOWFLAKE_DATABASE",
    ]:
        if env not in os.environ:
            raise Exception(f"Missing required environment variable: {env}")

    # TODO Need to change to private key auth over password
    conn = snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        # password=os.environ["SNOWFLAKE_PASSWORD"],
        authenticator="SNOWFLAKE_JWT",
        private_key_file=os.environ["SNOWFLAKE_PRIVATE_KEY_FILE"],
        private_key_file_pwd=os.environ["SNOWFLAKE_PRIVATE_KEY_FILE_PWD"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=schema,
    )
    return conn
