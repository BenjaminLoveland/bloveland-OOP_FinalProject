#Makefile for connect-four program

# Variables
PYTHON=python3
TEST_DIR=tests/test_project.py
UML_DIR=uml_diagrams
SOURCE_FILES=ai.py game.py app.py
UML_FILES=$(UML_DIR)/ai.uml $(UML_DIR)/game.uml $(UML_DIR)/app.uml

# Targets
all: style type uml test

style:
	flake8 $(SOURCE_FILES)

type:
	mypy $(SOURCE_FILES)

uml:
	mkdir -p $(UML_DIR)
	java -jar /home/codespace/.vscode-remote/extensions/jebbs.plantuml-2.18.1/plantuml.jar -o $(UML_DIR) $(SOURCE_FILES)

test:
	PYTHONPATH=. pytest --cov=ai --cov=game --cov=app --cov-report=term-missing tests/test_project.py

run:
	python3 app.py

.PHONY: all style type uml run