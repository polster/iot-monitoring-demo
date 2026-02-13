#!makefile

COMPOSE_FILE = "docker-compose.yaml"

include .envrc

.PHONY: docker-infra-up
docker-infra-up:
		docker compose -f ${COMPOSE_FILE} up -d

.PHONY: docker-infra-down
docker-infra-down:
		docker compose -f ${COMPOSE_FILE} down

.PHONY: docker-infra-status
docker-infra-status:
		docker ps -a \
				--filter "name=${COMPOSE_PROJECT_NAME}*" \
				--format "table {{.ID}}\t{{.Names}}\t{{.Status}}"

.PHONY: docker-infra-logs
docker-infra-logs:
		docker compose logs -f

.PHONY: pre-commit-install
pre-commit-install:
		pre-commit install

.PHONY: pre-commit-uninstall
pre-commit-uninstall:
		pre-commit uninstall

.PHONY: pre-commit-run
pre-commit-run:
		pre-commit run --all-files
