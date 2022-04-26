from planet import api
import json

#sys.exit("breaker triggered")

client = api.ClientV1()

with open("clusters/<n>/cluster<n>.json") as f:
    data = json.load(f)

client.create_order(data)