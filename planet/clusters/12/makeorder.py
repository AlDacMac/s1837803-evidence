from planet import api
import json

sys.exit("breaker triggered")

client = api.ClientV1()

with open("clusters/12/cluster12.json") as f:
    data = json.load(f)

client.create_order(data)