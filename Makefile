.DEFAULT_GOAL := help

.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Targets:"
	@echo "  run         - Запуск приложения"
	@echo "  debug       - Запуск приложения в режиме отладки"
	@echo "  conda run   - Запуск приложения в окружении conda"
	@echo "  conda debug - Запуск приложения в режиме отладки в окружении conda"
	@echo ""
	@echo "Flags:"
	@echo "  no-arduino - Запуск без Arduino"
	@echo ""


ENV := source $$(conda info --base)/etc/profile.d/conda.sh && conda activate highflyer

.PHONY: run debug
run debug: ## Запуск приложения / Запуск приложения в режиме отладки
ifeq ($(filter conda,$@),conda)
	@$(ENV) && python main.py $(if $(filter debug,$@),--debug,) $(if $(filter no-arduino,$(MAKECMDGOALS)),--no-arduino,)
else
	@python main.py $(if $(filter debug,$@),--debug,) $(if $(filter no-arduino,$(MAKECMDGOALS)),--no-arduino,)
endif
