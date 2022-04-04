from planet import api
import json
import sys

sys.exit("breaker triggered")

client = api.ClientV1()

with open("clusters/10/cluster10.json") as f:
    data = json.load(f)

client.create_order(data)