push_test_image:
	docker build -t saturncloud/sutils-test:latest dev-docker
	docker push saturncloud/sutils-test:latest
test:
	py.test sutils
dev_package:
	bash ./dev_package.sh
package:
	bash ./package.sh
