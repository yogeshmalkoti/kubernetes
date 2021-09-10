import jsonschema
import yaml
import simplejson as json

with open('schema-example.json', 'r') as f:
    schema_data = f.read()
schema = json.loads(schema_data)

json_obj = {"name": "eggs", "price": 21.47, "sku": 2}
jsonschema.validate(json_obj, schema)

json_obj = {"name": "eggs", "price": "blue", "sku": 2}
