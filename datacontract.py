import yaml
import json

class DataContract:
    '''
    An object containing a data contract.

    Args:
        path (str): The path to the data contract YAML file
    '''
    def __init__(self, path: str):
        with open(path, "r") as stream:
            self.contract = yaml.safe_load(stream)
        
        if 'owner' not in self.contract:
            raise ValueError(f'`{self.name()}` contract does not have an owner')

    def name(self) -> str:
        '''
        Returns:
            The name of the data contract.
        '''
        return self.contract['name']
    
    def fields(self) -> dict:
        '''
        Returns:
            The fields that make up the schema.
        '''
        return self.contract['fields']

    def json_schema(self) -> dict:
        '''
        Generate a JSON Schema from the data contract.

        Returns:
            The JSON Schema
        '''
        properties = {}
        required = []
        for name, metadata in self.fields().items():
            properties[name] = {
                'description': metadata['description'],
                'type': metadata['type'],
            }
            if 'enum' in metadata:
                properties[name]['enum'] = metadata['enum']
            if 'pattern' in metadata:
                properties[name]['pattern'] = metadata['pattern']

            if 'required' in metadata and metadata['required'] is True:
                required.append(name)

        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": self.name(),
            "description": self.contract['description'],
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": True
        }
        return schema
