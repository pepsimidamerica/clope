import asyncio
import sys

sys.path.insert(0, "")

from clope.spotlight.spotlight import async_run_report, run_report
from dotenv import load_dotenv

load_dotenv()


async def test_async_run_report():
    df = await async_run_report("26312")
    return df


if __name__ == "__main__":
    df = run_report("26312")
    df_async = asyncio.run(test_async_run_report())
    print(df.head())
    print(df_async.head())
    pass
