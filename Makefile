.PHONY: pex deps

pex: deps
	pex -v . -r requirements.txt -c main.py -o pt

.venv:
	virtualenv .venv

deps: .venv
	. .venv/bin/activate
	pip install -r requirements.txt
