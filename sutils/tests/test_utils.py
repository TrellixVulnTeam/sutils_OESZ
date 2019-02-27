import tempfile
import os
from os.path import join, dirname, exists
import tarfile

from pytest import raises

from ..files import (
    ensure_directory, find_prefix,
    extract_all, targz
)


def prep_data(dest):
    source = tempfile.TemporaryDirectory()
    with source as source:
        path = join(source, 'foo/bar/baz.py')
        path1 = path
        if not exists(dirname(path)):
            os.makedirs(dirname(path))
        with open(path, "wb+") as f:
            f.write("print('hello')\n".encode('utf-8'))
            f.flush()
        path = join(source, 'foo/bar/bork/fo.py')
        path2 = path
        if not exists(dirname(path)):
            os.makedirs(dirname(path))
        with open(path, "wb+") as f:
            f.write("print('hello2')\n".encode('utf-8'))
            f.flush()
        with tarfile.open(dest, mode='w:gz') as ff:
            ff.add(path1, arcname='foo/bar/baz.py')
            ff.add(path2, arcname='foo/bar/bork/fo.py')


def prep_data2(dest):
    source = tempfile.TemporaryDirectory()
    with source as source:
        path = join(source, 'baz.py')
        path1 = path
        if not exists(dirname(path)):
            os.makedirs(dirname(path))
        with open(path, "wb+") as f:
            f.write("print('hello')\n".encode('utf-8'))
            f.flush()
        path = join(source, 'fo.py')
        path2 = path
        if not exists(dirname(path)):
            os.makedirs(dirname(path))
        with open(path, "wb+") as f:
            f.write("print('hello2')\n".encode('utf-8'))
            f.flush()
        with tarfile.open(dest, mode='w:gz') as ff:
            ff.add(path1, arcname='baz.py')
            ff.add(path2, arcname='fo.py')


def test_extract_all():
    with tempfile.TemporaryDirectory() as dest:
        dest = join(dest, 'data.tar.gz')
        prep_data(dest)
        with tempfile.TemporaryDirectory() as target:
            extract_all(dest, target)
            assert exists(join(target, 'foo/bar/baz.py'))
            assert exists(join(target, 'foo/bar/bork/fo.py'))


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


def test_tar_prefix_cleaning():
    with tempfile.TemporaryDirectory() as dest_dir:
        dest = join(dest_dir, 'data.tar.gz')
        dest2 = join(dest_dir, 'data2.tar.gz')
        prep_data(dest)
        with tempfile.TemporaryDirectory() as target:
            extract_all(dest, target)
            prefix = find_prefix(target, level=1)
            targz(dest2, target, prefix=prefix)
        with tempfile.TemporaryDirectory() as target:
            extract_all(dest2, target)
            assert exists(join(target, 'bar/baz.py'))
            assert exists(join(target, 'bar/bork/fo.py'))


def test_tar_prefix_cleaning2():
    with tempfile.TemporaryDirectory() as dest_dir:
        dest = join(dest_dir, 'data.tar.gz')
        dest2 = join(dest_dir, 'data2.tar.gz')
        prep_data2(dest)
        with tempfile.TemporaryDirectory() as target:
            extract_all(dest, target)
            try:
                prefix = find_prefix(target, level=1)
            except ValueError:
                prefix = find_prefix(target)
            targz(dest2, target, prefix=prefix, addprefix='data')
        with tempfile.TemporaryDirectory() as target:
            extract_all(dest2, target)
            assert exists(join(target, 'data/baz.py'))
            assert exists(join(target, 'data/fo.py'))
