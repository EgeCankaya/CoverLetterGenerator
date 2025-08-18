.PHONY: help install install-dev test lint format type-check run clean

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode
	uv sync

install-dev: ## Install development dependencies
	uv sync --group dev

test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov=coverlettergenerator --cov-report=html --cov-report=term

lint: ## Run linting
	uv run ruff check .

format: ## Format code
	uv run ruff format .

type-check: ## Run type checking
	uv run mypy coverlettergenerator

run: ## Run the application
	uv run python -m coverlettergenerator

run-dev: ## Run the application in development mode
	FLASK_ENV=development FLASK_DEBUG=True uv run python -m coverlettergenerator

clean: ## Clean up generated files
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

setup: install-dev ## Set up development environment
	@echo "Setting up development environment..."
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		cp env.example .env; \
		echo "Please edit .env file and add your OpenAI API key"; \
	else \
		echo ".env file already exists"; \
	fi

check-env: ## Check if environment is properly configured
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found. Run 'make setup' to create it."; \
		exit 1; \
	fi
	@if ! grep -q "OPENAI_API_KEY=your_openai_api_key_here" .env; then \
		echo "✅ .env file appears to be configured"; \
	else \
		echo "❌ Please update your OpenAI API key in .env file"; \
		exit 1; \
	fi

all: install-dev format lint type-check test ## Run all checks and tests

# Target used by CI quality job
check: lint type-check ## Run linting and type checks
