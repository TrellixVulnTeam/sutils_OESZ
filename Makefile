include .env_deps

push_test_image:
	docker build -t saturncloud/sutils-test:latest dev-docker
	docker push saturncloud/sutils-test:latest
test:
	py.test sutils
test_in_docker:
	docker run --rm -v $(shell pwd):/app --workdir /app \
		saturncloud/sutils-test:latest \
		/opt/conda/bin/conda run -n base make test
build:
	mkdir -p saturn-bld
	conda build --output-folder=./saturn-bld --prefix-length 80 -c conda-forge -c saturncloud conda.recipe
