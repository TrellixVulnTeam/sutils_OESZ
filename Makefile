include .env_deps

.PHONY: build_test_image
build_test_image:
	docker build -t saturncloud/sutils-test:latest dev-docker

.PHONY: push_test_image
push_test_image: build_test_image
	docker push saturncloud/sutils-test:latest

.PHONY: test
test:
	py.test sutils

.PHONY: test_in_docker
test_in_docker:
	docker run --rm -v $(shell pwd):/app --workdir /app \
		saturncloud/sutils-test:latest \
		/opt/conda/bin/conda run -n base make test

.PHONY: build
build:
	mkdir -p saturn-bld
	conda build --output-folder=./saturn-bld --prefix-length 80 -c conda-forge -c saturncloud conda.recipe

.PHONY: build_in_docker
build_in_docker:
	docker run --rm -v $(shell pwd):/app --workdir /app \
		saturncloud/sutils-test:latest \
		/opt/conda/bin/conda run -n base make build
