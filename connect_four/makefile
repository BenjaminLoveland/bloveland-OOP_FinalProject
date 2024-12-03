# Makefile for connect-four program

# Variables
PYTHON=python3
TEST_DIR=tests
UML_DIR=uml_diagrams
SOURCE_FILES=ai.py game.py app.py
UML_FILES=$(UML_DIR)/ai.uml $(UML_DIR)/game.uml $(UML_DIR)/app.uml
UML_JAR= # Update this path to the correct PlantUML JAR file location

# Targets
all: style type uml test

style:
	flake8 $(SOURCE_FILES)

type:
	mypy $(SOURCE_FILES)

uml:
	

test:
	PYTHONPATH=. pytest --cov=ai --cov=game --cov=app --cov-report=term-missing tests/test_ai.py tests/test_game.py tests/test_app.py

run:
	$(PYTHON) app.py

.PHONY: all style type uml test run
