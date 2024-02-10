# Python Pact Implementation

This project demonstrates the implementation of Python Pact with pact-python. The project involves two components: the client, i.e., Dashboard, and the service provider, i.e., Employee Service.

Tests are present in the `dashboard/test` directory, and states for the provider can be found in `employee-service/states/provider_states.py`.

## Dev Setup
- To install dependencies, use `requirements.txt`.
- To start the Employee Service, use `make start-employee-service`.
- To run tests and generate the Pact file, use `make verify-pact`.
