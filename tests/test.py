import sys
from datetime import datetime, timedelta

sys.path.insert(0, "")

from clope import run_report

# from clope.snow.dates import date_to_datekey, datekey_to_date
from dotenv import load_dotenv

load_dotenv()

# alerts = get_machine_alerts_fact(
#     effective_date_range=(
#         date_to_datekey(datetime.now() - timedelta(days=1)),
#         date_to_datekey(datetime.now()),
#     ),
#     added_date_range=(
#         datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
#         - timedelta(days=1),
#         datetime.now(),
#     ),
# )

df = run_report(
    "24128", [("filter3", "2024-09-06T00:00:00Z"), ("filter3", "2024-09-06T23:59:59Z")]
)

pass
