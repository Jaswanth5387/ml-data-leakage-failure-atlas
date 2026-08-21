.PHONY: validate test summary

validate:
	python scripts/validate_cases.py

test:
	python -m unittest discover -s tests -v

summary:
	python scripts/summarize.py

