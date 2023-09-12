DOCKER_REPOSITORY := eshin94/laundrydo

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yml
IMAGE_VERSION := 0.0.1

PROJECT_NAME := LaundryDO
MODEL_LOAD_PATTERN_PORT := 8000

.PHONY: build
build :
		docker build \
			-t $(DOCKER_REPOSITORY):$(PROJECT_NAME)_$(IMAGE_VERSION) \
			-f $(DOCKERFILE) \
			.

.PHONY: push
push:
	docker push $(DOCKER_REPOSITORY):$(PROJECT_NAME)_$(IMAGE_VERSION)

.PHONY: build_all
build_all: build

.PHONY: push_all
push_all: push

.PHONY: c_build
c_build: build_all


.PHONY: c_up
c_up :
		docker-compose \
				-f ./$(DOCKER_COMPOSE) \
				up

.PHONY: c_down
c_down:
		docker-compose \
				-f ./$(DOCKER_COMPOSE) \
				down