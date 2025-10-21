import asyncio

from dotenv import load_dotenv

from clope.snow import get_items
from clope.spotlight.spotlight import async_run_report, run_report

load_dotenv()


async def test_async_run_report():
    df = await async_run_report("26312")
    return df


if __name__ == "__main__":
    df = run_report("26312")
    print(df.head())

    df2 = get_items()
    print(df2.head())
    df.to_excel("spotlight_report.xlsx")
    pass
