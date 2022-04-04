from planet import api
import json
import requests
from requests.auth import HTTPBasicAuth
import sys

client = api.ClientV1()
order_ids = []

ortho_only = True

API_KEY = sys.argv[1]
name_prefix = sys.argv[2]

for order in client.get_orders().get()["orders"]:
    if f"{name_prefix}" in order["name"]:
        order_ids.append(order["id"])

order_id = order_ids[0]

for order_id in order_ids[0:]:
#    if not order_id == "7f055102-ee98-403c-bd53-bbde6734e3e9":
#        continue
    ortho = True
    downloads = requests.get(f"https://api.planet.com/compute/ops/orders/v2/{order_id}", auth=HTTPBasicAuth(API_KEY, ''))

    print(order_id)
    #print(downloads.json()["_links"]["results"][0]["name"])

    counter = 0
    for download in downloads.json()["_links"]["results"]:
        print(f"downloading {counter}")
        counter += 1
        filename = "boa_planet/" + download["name"].split("/")[-1]
        #if "PSOrthoTile" in filename:
        #    filename = "boa_planet/" + download["name"].split("/")[2]
        #elif filename
        if "tif" in "boa_planet/" + download["name"].split("/")[1]:
            ortho = False
            if ortho_only:
                break
        print(filename)
        #TODO take my damn api key out
        r = requests.get(download["location"], auth=HTTPBasicAuth("d105c141f3a24b27bc90881242b71739", ''))
        with open(filename, "wb") as f:
            f.write(r.content)
    if ortho_only and not ortho:
        continue