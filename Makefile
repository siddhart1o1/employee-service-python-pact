test:
	@echo Running pytest...
	PYTHONPATH=$(PWD) pytest

start-employee-service:
	@echo Starting employee-service...
	uvicorn employee-service.main:app --reload

verify-pact: test
	@echo Running pact-verifier...
	pact-verifier --provider-base-url=http://localhost:8000 --pact-url=./pact/dashboard-employeeservice.json --provider-states-setup-url=http://localhost:8000/_pact/provider_states

.PHONY: test start-employee-service verify-pact
