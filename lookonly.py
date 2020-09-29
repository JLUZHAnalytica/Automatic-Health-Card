from setting import *
from getcookie import get_cookie
from auto_health import query_record
from auto_health import headers

JSESSIONID = get_cookie(username, password)
headers.update({"cookie": "JSESSIONID=" + JSESSIONID})
for num in range(20200101, 20200131):
    if len(query_record(num, headers)) != 0:
        print(str(num) + " OK")
    else:
        print(str(num) + " 未填写")
