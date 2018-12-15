
from urllib.parse import urlparse, parse_qs
import json
from collections import ChainMap
url1 = "http://www.abc.com/?x=6&z=4&h=66&d=ss"

url2 = "http://www.abc.com/?x=62&z=11&y=14&c=hi&h=49"


def spot_difference(url1, url2):
    u1 =parse_qs((urlparse(url1)).query)
    #print(u1)
    
    u2 =parse_qs((urlparse(url2)).query)

    shared = dict()
    shared_keys = [k for k in [u1.keys() & u2.keys()]]

    for i in shared_keys[0]:
        shared.update({i:
            [u1[i], u2[i]]
        })

    #shared_ = {k:v for k,v in u1.items() if k,v in u2.items()}
    in_url2 = {k:v for k, v in u2.items() if k not in u1.keys()}
    in_url1 = {k:v for k, v in u1.items() if k not in u2.keys()}
    schema = dict()
    schema = {
        "shared": shared,
        "in_url1": in_url1,
        "in_url2": in_url2
    }
    return schema
    #return ChainMap(u1,u2).#.fromkeys(['a', 14])
print(spot_difference(url1, url2))
#u1 =parse_qs((urlparse(url1)).query)
#print(u1)

#u2 =parse_qs((urlparse(url2)).query)

#print(ChainMap(u1, u2).items())

