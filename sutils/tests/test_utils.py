import tempfile
import os
from os.path import join, dirname, exists
import tarfile

from pytest import raises

from ..files import ensure_directory, find_prefix


# def prep_data(dest):
#     source = tempfile.TemporaryDirectory()
#     with source as source:
#         path = join(source, 'foo/bar/baz.py')
#         path1 = path
#         if not exists(dirname(path)):
#             os.makedirs(dirname(path))
#         with open(path, "wb+") as f:
#             f.write("print('hello')\n".encode('utf-8'))
#             f.flush()
#         path = join(source, 'foo/bar/bork/fo.py')
#         path2 = path
#         if not exists(dirname(path)):
#             os.makedirs(dirname(path))
#         with open(path, "wb+") as f:
#             f.write("print('hello2')\n".encode('utf-8'))
#             f.flush()
#         with tarfile.open(dest, mode='w:gz') as ff:
#             ff.add(path1, arcname='foo/bar/baz.py')
#             ff.add(path2, arcname='foo/bar/bork/fo.py')


# def test_extract_all():
#     with tempfile.TemporaryDirectory() as dest:
#         dest = join(dest, 'data.tar.gz')
#         prep_data(dest)
#         with tarfile.open(dest, mode='r') as ff:
#             data = list(ff)
#         import ipdb;ipdb.set_trace()


def test_find_prefix():
    with tempfile.TemporaryDirectory() as source:

        path = join(source, 'foo/bar/baz/foo.py')
        ensure_directory(path)

        prefix = find_prefix(source)
        assert prefix == join(source, 'foo/bar/baz')
        prefix = find_prefix(source, level=1)
        assert prefix == join(source, 'foo/bar')
        prefix = find_prefix(source, level=2)
        assert prefix == join(source, 'foo')
        prefix = find_prefix(source, level=3)
        assert prefix == join(source)
        with raises(ValueError):
            prefix = find_prefix(source, level=4)

        with open(path, "w+") as f:
            f.write('.\n')
        prefix = find_prefix(source)
        assert prefix == join(source, 'foo/bar/baz')
        prefix = find_prefix(source, level=1)
        assert prefix == join(source, 'foo/bar')
        prefix = find_prefix(source, level=2)
        assert prefix == join(source, 'foo')
        prefix = find_prefix(source, level=3)
        assert prefix == join(source)
        with raises(ValueError):
            prefix = find_prefix(source, level=4)

        path = join(source, 'foo/bar/bork.py')
        ensure_directory(path)
        with open(path, "w+") as f:
            f.write('.\n')

        prefix = find_prefix(source)
        assert prefix == join(source, 'foo/bar')
        prefix = find_prefix(source, level=1)
        assert prefix == join(source, 'foo')
        prefix = find_prefix(source, level=2)
        assert prefix == join(source)
        with raises(ValueError):
            prefix = find_prefix(source, level=3)
