install:
	python setup.py develop
	pip install -e .[test] 

test: install
	nosetests --with-coverage  --cover-erase --cover-package=postnl.locations --cover-xml --logging-level=INFO --with-doctest
