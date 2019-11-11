push_test_image:
	docker build -t saturncloud/sutils-test:latest dev-docker
	docker push saturncloud/sutils-test:latest
test:
	py.test sutils
dev_package:
	export OUTPUT=/tmp/output
	rm -rf ${OUTPUT}
	mkdir ${OUTPUT}
	conda build --output-folder=$OUTPUT --prefix-length 80 -c conda-forge -c saturncloud conda.recipe
	export TARGET=`ls /tmp/output/noarch/sutils*.bz2`
	anaconda -t ${ANACONDA_TOKEN} upload -u saturncloud -l dev --force --no-progress
main_package:
	export OUTPUT=/tmp/output
	rm -rf ${OUTPUT}
	mkdir ${OUTPUT}
	conda build --output-folder=$OUTPUT --prefix-length 80 -c conda-forge -c saturncloud conda.recipe
	export TARGET=`ls /tmp/output/noarch/sutils*.bz2`
	anaconda -t ${ANACONDA_TOKEN} upload -u saturncloud -l dev -l main --force --no-progress
