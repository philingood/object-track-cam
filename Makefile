.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

.PHONY: run
run: ## Run application
	python main.py

.PHONY: debug
debug: ## Run application in debug mode
	python main.py DEBUG

.PHONY: conda run
run: ## Run application
	source $$(conda info --base)/etc/profile.d/conda.sh && conda activate highflyer && python main.py

.PHONY: conda debug
debug: ## Run application in debug mode
	source $$(conda info --base)/etc/profile.d/conda.sh && conda activate highflyer && python main.py DEBUG
