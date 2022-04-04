from planet import api
import json

#sys.exit("breaker triggered")

client = api.ClientV1()

with open("clusters/0/cluster0.json") as f:
    data = json.load(f)

client.create_order(data)