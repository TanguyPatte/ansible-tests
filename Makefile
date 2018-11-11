test:
	python -u -m unittest discover ansible_tests_tests/

lint:
	flake8 --ignore=E501
