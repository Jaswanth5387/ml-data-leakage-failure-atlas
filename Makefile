.PHONY: validate test summary release-check

validate:
	python scripts/validate_cases.py

test:
	python -m unittest discover -s tests -v

summary:
	python scripts/summarize.py

release-check:
	python scripts/check_release.py 0.1.0
