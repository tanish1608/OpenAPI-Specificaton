import json
import yaml

def thunder_to_openapi(thunder_json):
    # Create a mapping of folder IDs to folder names
    folder_mapping = {folder['_id']: folder['name'] for folder in thunder_json['folders']}
    
    openapi = {
        "openapi": "3.0.0",
        "info": {
            "title": thunder_json['collectionName'],
            "version": thunder_json['version']
        },
        "servers": [],
        "tags": [],
        "paths": {},
        "components": {
            "schemas": {}
        }
    }
    openapi['servers'].append({"url": thunder_json['settings']['options']['baseUrl']})
    
    # Add tags to OpenAPI spec based on folder names
    for folder in thunder_json['folders']:
        openapi['tags'].append({
            "name": folder['name'],
            "description": f"Operations related to {folder['name']}"
        })

    
    for request in thunder_json['requests']:
        path = request['url']
        method = request['method'].lower()
        description = request.get('docs', 'No description provided')
        # Ensure query strings are stripped from the path
        path = path.split('?')[0]
        
        if path not in openapi['paths']:
            openapi['paths'][path] = {}

        # Assign the tag based on the folder the request belongs to
        tag = folder_mapping.get(request['containerId'], "default")
        
        openapi['paths'][path][method] = {
            "summary": request['name'],
            "tags": [tag],
            "description": description,
            "parameters": [],
            "responses": {
                "200": {
                    "description": ""
                }
            }
        }


        # Process query and path parameters
        if 'params' in request and request['params']:
            for param in request['params']:
                param_spec = {
                    "name": param['name'],
                    "in": "query" if not param['isPath'] else "path",
                    "required": param['isPath'],
                    "description": request.get('description', 'No description provided'),
                    "schema": {
                        "type": "string"
                    }
                }
                openapi['paths'][path][method]['parameters'].append(param_spec)

        # Process the request body if it exists
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
