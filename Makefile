# DONGOL Makefile
# Convenient commands for development

.PHONY: help install dev test lint format clean build docs

PYTHON := python3
PIP := pip3

help:
	@echo "DONGOL - Available Commands:"
	@echo ""
	@echo "  make install     - Install production dependencies"
	@echo "  make dev         - Install development dependencies"
	@echo "  make test        - Run test suite"
	@echo "  make test-cov    - Run tests with coverage"
	@echo "  make lint        - Run linters"
	@echo "  make format      - Format code with black"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make build       - Build package"
	@echo "  make docs        - Generate documentation"
	@echo "  make run         - Run example"
	@echo ""

install:
	$(PIP) install -e .

dev:
	$(PIP) install -e ".[dev,all]"

test:
	pytest tests/ -v --tb=short

test-cov:
	pytest tests/ -v --cov=dongol --cov-report=html --cov-report=term

lint:
	ruff check dongol/
	mypy dongol/

format:
	black dongol/ tests/ examples/

clean:
	rm -rf build/ dist/ *.egg-info/
	rm -rf .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	$(PYTHON) -m build

docs:
	@echo "Documentation generation not yet implemented"

run:
	$(PYTHON) examples/basic_usage.py

run-agent:
	$(PYTHON) examples/agent_workflow.py

benchmark:
	$(PYTHON) -c "
import asyncio
import time
from core.engine import DongolEngine

async def benchmark():
    engine = DongolEngine({'max_workers': 8})
    await engine.start()
    
    start = time.time()
    tasks = []
    
    for i in range(100):
        task = await engine.create_task(
            name=f'Benchmark {i}',
            content='Test content ' * 100,
            auto_chunk=True
        )
        tasks.append(task)
    
    # Execute all
    for task in tasks:
        await engine.execute_task(task.id)
    
    elapsed = time.time() - start
    print(f'Created and executed 100 tasks in {elapsed:.2f}s')
    print(f'Average: {elapsed/100*1000:.2f}ms per task')
    
    await engine.stop()

asyncio.run(benchmark())
"
