def parse_branches(branches):
    all_branches = []
    for branch in branches.splitlines():
        if "->" in branch:
            continue
        branch = branch.split()[-1]
        all_branches.append(branch)
    return all_branches


def local_branches(g):
    return parse_branches(g.git.branch())


def remote_branches(g):
    return parse_branches(g.git.branch("-r"))


def remote_tags(g, remote="origin"):
    result = []
    for tag in g.git.ls_remote(remote, tags=True).splitlines():
        if tag:
            result.append(tag.split("refs/tags/")[-1])
    return result
