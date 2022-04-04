from planet import api
import json
import sys

sys.exit("breaker triggered")

client = api.ClientV1()

with open("clusters/8/cluster8.json") as f:
    data = json.load(f)

client.create_order(data)