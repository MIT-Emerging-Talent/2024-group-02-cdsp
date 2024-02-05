import re
from datetime import datetime, timezone


text = """11/12/1111

            1/2/2020
            11"""

regex = r"(\d{1,2}\/\d{1,2}\/\d{4})"

is_fount = re.search(regex,text)

print(is_fount)

if is_fount:
    print("True")

print(datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"))