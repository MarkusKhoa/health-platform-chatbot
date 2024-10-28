POETRY=poetry
ALEMBIC=alembic

.DEFAULT_GOAL := run

# Create a virtual environment
shell:
	${POETRY} shell

# Install dependencies
install: shell
	${POETRY} install --no-root

# Run the FastAPI server
run: install
	${POETRY} run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

# Help target
help:
	@echo "Available targets:"
	@echo "  make shell        - Create a virtual environment"
	@echo "  make install     - Install project dependencies"
	@echo "  make run         - Run the FastAPI server"

.PHONY: shell install run help