from planet import api
import json
import sys

sys.exit("breaker triggered")

client = api.ClientV1()

with open("clusters/3/cluster3.json") as f:
    data = json.load(f)

client.create_order(data)