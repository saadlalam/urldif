
from urllib.parse import urlparse, parse_qs
import json


url1 = "http://www.abc.com/?x=6&z=4&h=66&d=ss"

url2 = "http://www.abc.com/?x=62&z=11&y=14&c=hi&h=49"


def spot_difference(url1, url2):
    u1 =parse_qs((urlparse(url1)).query)
    u2 =parse_qs((urlparse(url2)).query)
    shared_keys = [k for k in [u1.keys() & u2.keys()]]
    shared = {i:[u1[i], u2[i]] for i in shared_keys[0]}
    in_url2 = {k:v for k, v in u2.items() if k not in u1.keys()}
    in_url1 = {k:v for k, v in u1.items() if k not in u2.keys()}
    schema = {
        "shared": shared,
        "in_url1": in_url1,
        "in_url2": in_url2
    }
    return json.dumps(schema, indent=4, sort_keys=True)



print(spot_difference(url1,url2))