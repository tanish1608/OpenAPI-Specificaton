import json
import yaml
from urllib.parse import urlparse, parse_qs

def thunder_to_openapi(thunder_json):
    openapi = {
        "openapi": "3.0.0",
        "info": {
            "title": thunder_json['collectionName'],
            "version": thunder_json['version']
        },
        "paths": {},
        "components": {
            "schemas": {}
        }
    }

    for request in thunder_json['requests']:
        url = request['url']
        parsed_url = urlparse(url)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        method = request['method'].lower()

        if path not in openapi['paths']:
            openapi['paths'][path] = {}

        openapi['paths'][path][method] = {
            "summary": request['name'],
            "parameters": [],
            "responses": {
                "200": {
                    "description": "Success"
                }
            }
        }

        if 'params' in request and request['params']:
            for param in request['params']:
                param_spec = {
                    "name": param['name'],
                    "in": "query" if not param['isPath'] else "path",
                    "required": param['isPath'],
                    "schema": {
                        "type": "string"
                    }
                }
                openapi['paths'][path][method]['parameters'].append(param_spec)

        # # Add query parameters from URL
        # for key, values in query_params.items():
        #     param_spec = {
        #         "name": key,
        #         "in": "query",
        #         "required": False,  # Query parameters are generally optional
        #         "schema": {
        #             "type": "string"
        #         }
        #     }
        #     openapi['paths'][path][method]['parameters'].append(param_spec)

        if 'body' in request and request['body']:
            openapi['paths'][path][method]['requestBody'] = {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "example": json.loads(request['body']['raw'])
                        }
                    }
                }
            }

    return openapi

# Load Thunder Client JSON
with open('thunder-collection_Swagger Petstore - OpenAPI 3.0.json', 'r') as file:
    thunder_json = json.load(file)

# Convert to OpenAPI
openapi_spec = thunder_to_openapi(thunder_json)

# Save as YAML
with open('openapi_spec.yaml', 'w') as file:
    yaml.dump(openapi_spec, file, sort_keys=False)

# Optionally, save as JSON
with open('openapi_spec.json', 'w') as file:
    json.dump(openapi_spec, file, indent=2)