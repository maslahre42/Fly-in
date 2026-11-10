PYTHON = uv run
MAIN = main.py
MAP ?= maps/challenger/01_the_impossible_dream.txt
ARGS ?=
.PHONY: all install run debug clean lint lint-strict

all:
	$(PYTHON) $(MAIN) $(MAP) $(ARGS)

install:
	uv sync

run:
	$(PYTHON) $(MAIN) $(MAP) $(ARGS)

debug:
	$(PYTHON) -m pdb $(MAIN) $(MAP)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".venv" -exec rm -rf {} +


lint:
	uv run flake8 .
	uv run mypy .

lint-strict:
	uv run flake8 .
	uv run mypy . --strict
