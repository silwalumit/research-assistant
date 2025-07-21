# Makefile for research-assistant

# Project variables
PROJECT_NAME := research-assistant
PACKAGE_DIR := src/research_assistant
DOCKER_IMAGE := $(PROJECT_NAME):latest
DOCKER_COMPOSE := docker compose

# Help
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make dev          - Start development server with auto-reload"
	@echo "  make cli          - Run CLI entrypoint"
	@echo "  make install      - Install dependencies"
	@echo "  make docker-build - Build Docker image"
	@echo "  make up           - Start Docker Compose"
	@echo "  make down         - Stop Docker Compose"

# Commands using Rye
dev:
	rye run dev

cli:
	rye run cli

install:
	rye sync

# Docker commands
docker-build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up

down:
	$(DOCKER_COMPOSE) down