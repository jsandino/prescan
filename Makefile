install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
	
format:
	black prescan/*.py tests/*py
	
lint:
	pylint --disable=R,C hello.py
	
test:
	python -m pytest -vv --cov=prescan tests
	
all: install lint test