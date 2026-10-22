PYTHON = uv run python
MAIN = main1.py
MAP ?= maps/utf8_bom.txt

.PHONY: install run debug clean lint lint-strict all

install:
	uv sync
	
run:
	$(PYTHON) $(MAIN) $(MAP)

debug:
	$(PYTHON) -m pdb $(MAIN) $(MAP)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict

all:
	uv run flake8 .
	uv run mypy . --strict
	$(PYTHON) $(MAIN) $(MAP)
