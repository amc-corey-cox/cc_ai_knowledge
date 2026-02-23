RUN := uv run
SCHEMA := schema/knowledge-entry.yaml
OAK_CONF := conf/oak_config.yaml

.PHONY: help validate validate-terms validate-all validate-file gen-json-schema check-ontology-versions docs docs-serve

help:
	@echo "validate          Validate all entries against LinkML schema (structure)"
	@echo "validate-terms    Validate topic terms against ontologies (AIO)"
	@echo "validate-all      Run all validators (structure + terms)"
	@echo "validate-file F=  Validate a specific file (structure only)"
	@echo "gen-json-schema   Generate JSON Schema from LinkML (for editor support)"
	@echo "check-ontology-versions  Check if local ontology files are up to date"
	@echo "docs              Build documentation site"
	@echo "docs-serve        Serve documentation site locally"

validate:
	$(RUN) python scripts/validate.py

validate-terms:
	$(RUN) python scripts/validate_terms.py

validate-all: validate validate-terms

validate-file:
	$(RUN) python scripts/validate.py $(F)

gen-json-schema:
	$(RUN) gen-json-schema $(SCHEMA) > schema/knowledge-entry.json

check-ontology-versions:
	$(RUN) python scripts/check_ontology_versions.py

docs:
	$(RUN) mkdocs build --strict

docs-serve:
	$(RUN) mkdocs serve
