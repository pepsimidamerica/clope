import sys
from datetime import datetime, timedelta

sys.path.insert(0, "")

from clope import get_machine_alerts_fact
from clope.snow.dates import date_to_datekey, datekey_to_date

alerts = get_machine_alerts_fact(
    effective_date_range=(
        date_to_datekey(datetime.now() - timedelta(days=1)),
        date_to_datekey(datetime.now()),
    ),
    added_date_range=(
        datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        - timedelta(days=1),
        datetime.now(),
    ),
)

pass
