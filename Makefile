test:
	python -u -m unittest discover ansible_tests_tests/

lint:
	flake8 --ignore=E501

publish:
	twine upload dist/*

release:
	python setup.py sdist bdist_wheel

clean:
	rm dist/*
