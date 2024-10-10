import yaml
import json 
from datacontract import DataContract
from jsonschema import validate
from jsonschema.exceptions import ValidationError

data_contract = DataContract('customer.yml')

events = [
    # Valid events
    {"id": "DC12", "name" : "Andrew", "email" : "andrew@data-contracts.com", "language": "en"},
    {"id": "DC13", "name" : "Deborah", "email" : "deborah@data-contracts.com"},
    # Missing email, which is a required field
    {"id": "DC14", "name" : "Bukayo", "language": "en"},
    # Email does not pass regex validation
    {"id": "DC15", "name" : "Bukayo", "email" : "bukayo", "language": "en"},
    # `nl` is not a valid language code
    {"id": "DC16", "name" : "Vivianne", "email" : "vivianne@data-contracts.com", "language": "nl"}
]

for event in events:
    try:
        validate(event, data_contract.json_schema())
        print(f"✅ Successfully validated event {event}")
    except ValidationError as e:
        # Improved error handling for regex mismatches
        if e.validator == 'pattern':
            print(f"❗ Error validating event {event}: '{e.instance}' does not match the expected pattern for '{e.path[0]}'")
        else:
            print(f"❗ Error validating event {event}\n{e}")



# # Anonymize the event based on the rules specified in the data contract
# def anonymize(event: dict, data_contract: DataContract):
#     anonymized = event.copy()
#     for name, metadata in data_contract.fields().items():
#         if 'anonymization_strategy' in metadata:
#             if metadata['anonymization_strategy'] == 'email':
#                 anonymized[name] = f"anonymized+{event['id']}@data-contracts.com"
#             if metadata['anonymization_strategy'] == 'hex':
#                 anonymized[name] = event[name].encode("utf-8").hex()

#     return anonymized

# events = [
#     {"id": "DC12", "name" : "Andrew", "email" : "andrew@data-contracts.com", "language": "en"},
#     {"id": "DC13", "name" : "Deborah", "email" : "deborah@data-contracts.com"},
#     {"id": "DC14", "name" : "Bukayo", "email" : "bukayo@data-contracts.com", "language": "en"},
# ]

# for event in events:
#     anonymized = anonymize(event, data_contract)
#     print(f"Anonymizing:\t{event}\n\t\t{anonymized}")

