build:
	python setup.py sdist
deploy:
	twine upload dist/*.tar.gz