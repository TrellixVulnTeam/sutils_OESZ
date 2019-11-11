push_test_image:
	docker build -t saturncloud/sutils-test:latest dev-docker
	docker push saturncloud/sutils-test:latest
