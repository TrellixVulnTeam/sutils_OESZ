push_test_image:
	docker build -t saturncloud/sutils-test:latest dev-docker
	docker push saturncloud/sutils-test:latest
test:
	py.test sutils
dev_package:
	CONDA_OUTPUT=/tmp/output
	rm -rf ${CONDA_OUTPUT}
	mkdir ${CONDA_OUTPUT}
	conda build --output-folder=$CONDA_OUTPUT --prefix-length 80 -c conda-forge -c saturncloud conda.recipe
	TARGET=`ls /tmp/output/noarch/sutils*.bz2`
	anaconda -t ${ANACONDA_TOKEN} upload -u saturncloud -l dev --force --no-progress
main_package:
	CONDA_OUTPUT=/tmp/output
	rm -rf ${CONDA_OUTPUT}
	mkdir ${CONDA_OUTPUT}
	conda build --output-folder=$CONDA_OUTPUT --prefix-length 80 -c conda-forge -c saturncloud conda.recipe
	TARGET=`ls /tmp/output/noarch/sutils*.bz2`
	anaconda -t ${ANACONDA_TOKEN} upload -u saturncloud -l dev -l main --force --no-progress
