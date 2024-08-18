# Thunder Client to OpenAPI Specification Converter

This project provides a utility script to convert Thunder Client JSON collections into OpenAPI 3.0 specifications. The script translates Thunder Client requests, parameters, and folder structures into the corresponding OpenAPI format, making it easier to document and share API specifications.

## Features

- **Folder-Based Tagging:** Automatically map Thunder Client folder structures to OpenAPI tags.
- **Path and Query Parameters:** Properly handles and converts query and path parameters.
- **Request Body Conversion:** Converts JSON request bodies to OpenAPI-compliant `requestBody` objects.
- **Response Codes:** Supports defining multiple response codes for each endpoint.
- **Authentication Support:** Basic authentication details from Thunder Client are translated into OpenAPI security schemes.
- **Inline Documentation:** Supports descriptions and documentation for each request and parameter.
- **Output Formats:** Generates OpenAPI specifications in both YAML and JSON formats.

## Requirements

- Python 3.x
- `PyYAML` package - pip install pyyaml

## Example

- Given a Thunder Client collection, the script will produce an OpenAPI file with structured endpoints, tagged by folders, complete with parameter definitions, request bodies, and response schemas.

## Contributing

- Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

- This project is licensed under the MIT License.