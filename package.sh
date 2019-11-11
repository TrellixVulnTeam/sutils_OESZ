export CONDA_OUTPUT=/tmp/output
rm -rf ${CONDA_OUTPUT}
mkdir ${CONDA_OUTPUT}
conda build --output-folder=$CONDA_OUTPUT --prefix-length 80 -c conda-forge -c saturncloud conda.recipe
export TARGET=`ls ${CONDA_OUTPUT}noarch/sutils*.bz2`
anaconda -t ${ANACONDA_TOKEN} upload -u saturncloud -l dev -l main --force --no-progress
