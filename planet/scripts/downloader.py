from planet import api
import json
import requests
from requests.auth import HTTPBasicAuth
import sys
import os

client = api.ClientV1()
order_ids = []


API_KEY = sys.argv[1]
name_prefix = sys.argv[2] #I've used "cluster"
out_dir = sys.argv[2]

for order in client.get_orders().get()["orders"]:
    if f"{name_prefix}" in order["name"]:
        order_ids.append(order["id"])

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

order_id = order_ids[0]

for order_id in order_ids:
    ortho = True
    downloads = requests.get(f"https://api.planet.com/compute/ops/orders/v2/{order_id}", auth=HTTPBasicAuth(API_KEY, ''))

    print(order_id)
    #print(downloads.json()["_links"]["results"][0]["name"])

    counter = 0
    for download in downloads.json()["_links"]["results"]:
        print(f"downloading {counter}")
        counter += 1
        filename = out_dir + download["name"].split("/")[-1]
        print(filename)
        r = requests.get(download["location"], auth=HTTPBasicAuth(API_KEY, ''))
        with open(filename, "wb") as f:
            f.write(r.content)
    if ortho_only and not ortho:
        continue