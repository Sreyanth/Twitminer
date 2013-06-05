import json
from pprint import pprint
json_data=open('output')

data = json.load(json_data)

for obj in data:
	print(obj['id'])
	pprint(obj['text'])
json_data.close()
