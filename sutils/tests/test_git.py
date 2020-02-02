import tempfile

from git import Git, Repo, Tag

from sutils.git import (

)


def test_branches():
    path1 = tempfile.TemporaryDirectory()
    path2 = tempfile.TemporaryDirectory()
    with path1 as path1, path2 as path2:
        Repo.init(path1, bare=True)
        g1 = Repo(path1)
        Repo.clone_from(path1, path2)
        g2 = Repo(path2)
        with open(join(path2, 'foo'), "w+") as f:
            f.write('foo')
        g2.add('foo')
        g2.commit('test')
        g2.git.checkout(b='user')
        g2.git.push('origin', 'master')
        g2.git.push('origin', 'user')
        rb = remote_branches(g2)
        assert set(rb) == {'origin/master', 'origin/user'}
        rb = local_branches(g2)
        assert set(rb) == {'master', 'user'}


def test_branches_clone():
    path1 = tempfile.TemporaryDirectory()
    path2 = tempfile.TemporaryDirectory()
    path3 = tempfile.TemporaryDirectory()
    with path1 as path1, path2 as path2, path3 as path3:
        Repo.init(path1, bare=True)
        g1 = Repo(path1)
        Repo.clone_from(path1, path2)
        g2 = Repo(path2)
        with open(join(path2, 'foo'), "w+") as f:
            f.write('foo')
        g2.add('foo')
        g2.commit('test')
        g2.git.checkout(b='user')
        g2.git.push('origin', 'master')
        g2.git.push('origin', 'user')

        Repo.clone_from(path1, path3)
        g3 = Repo(path3)
        g3.git.checkout('origin/user', b='user')
        rb = local_branches(g3)
        assert set(rb) == {'user', 'master'}
