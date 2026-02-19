RUN := uv run

.PHONY: help validate validate-file gen-json-schema

help:
	@echo "validate          Validate all knowledge entries against LinkML schema"
	@echo "validate-file F=  Validate a specific file"
	@echo "gen-json-schema   Generate JSON Schema from LinkML (for editor support)"

validate:
	$(RUN) python scripts/validate.py

validate-file:
	$(RUN) python scripts/validate.py $(F)

gen-json-schema:
	$(RUN) gen-json-schema schema/knowledge-entry.yaml > schema/knowledge-entry.json
