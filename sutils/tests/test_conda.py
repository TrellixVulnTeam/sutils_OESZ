from os.path import dirname, join
import json

from sutils.conda import search_conda_results


def test_search_conda_results_no_package():
    data_file = join(dirname(__file__), "test_data", "conda_no_version_found.json")
    with open(data_file) as f:
        data = json.load(f)
    result = search_conda_results("jupyter_saturn", "1.2.8", data)
    assert not result


def test_search_conda_results_version_found():
    data_file = join(dirname(__file__), "test_data", "conda_version_found.json")
    with open(data_file) as f:
        data = json.load(f)
    result = search_conda_results("jupyter_saturn", "1.2.7", data)
    assert result
