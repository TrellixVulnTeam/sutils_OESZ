import json
from typing import List, Dict

from subprocess import run


def query_conda(package_name:str, version:str, channels=List[str]) -> Dict:
    """
    Execute a conda search command and return the results
    """
    if channels is None:
        channels = []
    cmd = ["conda", "search"]
    for channel in channels:
        cmd += ["-c", channel]
    cmd.append('--json')
    cmd.append('--override-channels')
    cmd.append(f"{package_name}={version}")
    output = run(cmd, capture_output=True, text=True).stdout
    return json.loads(output)


def search_conda_results(package_name:str, version:str, results:Dict) -> bool:
    """
    processes the results of query_conda, and tells us if we found the package or not
    """
    if "exception_name" in results:
        if results["exception_name"] == "PackagesNotFoundError":
            return False
        else:
            raise ValueError(f'unknown results {results}')
    if package_name in results:
        for packages in results[package_name]:
            if packages["version"] == version:
                return True
    return False
