import logging
import tempfile
import tarfile
from os.path import (
    abspath, realpath, dirname, join, relpath, exists,
    isdir, isfile
)
import os


log = logging.getLogger(__name__)


resolved = lambda x: realpath(abspath(x))


def badpath(path, base):
    # join will ignore base if path is absolute
    return not resolved(join(base, path)).startswith(base)


def badlink(info, base):
    # Links are interpreted relative to the directory containing the link
    tip = resolved(join(base, dirname(info.name)))
    return badpath(info.linkname, base=tip)


def safemembers(members):
    base = resolved(".")
    for finfo in members:
        if badpath(finfo.name, base):
            log.error('%s BAD PATH', finfo.name)
        elif finfo.issym() and badlink(finfo,base):
            log.error('%s BAD PATH', finfo.name)
        elif finfo.islnk() and badlink(finfo,base):
            log.error('%s BAD PATH', finfo.name)
        else:
            yield finfo


def extract_all(tarpath, destpath):
    with tarfile.open(name=tarpath, mode='r') as tf:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tf, path=destpath, members=safemembers(tf))


def targz(tarpath, source, prefix=None, addprefix=None):
    """
    creates a tar.gz at tarpath(tarpath will be the path of the resulting file.
    it should not be a directory).

    walks source, and adds all files into the tar.gz

    if prefix is specified, the arcname is taken relative to prefix.
    otherwise, prefix is taken to be the source directory

    if addprefix is specified, the arcname <addprefix>/<relpath to prefix>
    """

    if prefix is None:
        prefix = source
    assert not isdir(tarpath)
    with tarfile.open(tarpath, mode='w:gz') as tarf:
        for root, dirs, files in os.walk(source):
            for f in files:
                fpath = join(root, f)
                arcname = relpath(fpath, prefix)
                if addprefix:
                    arcname = join(addprefix, arcname)
                tarf.add(fpath, arcname=arcname)


def find_prefix(source, level=0):
    """
    We walk the source to and
    find a common prefix for all files in the directory.
    the smallest prefix possible, is the first prefix that
    contains more than 1 child.  If level is 0.  If level is 1,
    1 directory outside that is returned, and so on.  Empty
    directories are ignored


    imagine
    foo/bar/baz/foo.py
    foo/bar/bork.py

    The common prefix is foo/bar, since that path contains baz/foo.py and bork.py

    if level = 1, then the common prefix is foo

    We can always solve for level 0.  If the level requires us to return a prefix
    which is outside (one level up from) the source, we throw a ValueError

    Only works for unix
    """
    source = abspath(source)
    current = source
    traversal = []
    while True:
        paths = os.listdir(current)
        if len(paths) == 1:
            candidate = join(current, paths[0])
            if isfile(candidate):
                break
            traversal.append(paths[0])
            current = join(current, paths[0])
        else:
            break
    if level > len(traversal):
        msg = 'find_prefix called with level %s, largest common prefix is %s'
        msg = msg % (level, traversal)
        raise ValueError(msg)
    if level > 0:
        traversal = traversal[:-level]
    return join(source, *traversal)

    # prefixes = set()
    # for root, dirs, files in os.walk(source):
    #     for f in files:
    #         rpath = relpath(root, source)
    #         prefixes.add(rpath)

    # tree = {}
    # for prefix in prefixes:
    #     current = tree
    #     paths = prefix.split(os.sep)
    #     for p in paths:
    #         current = current.setdefault(p, {})
    # path = []
    # current = tree
    # while True:
    #     if len(current.keys()) == 1:
    #         key = list(current.keys())[0]
    #         path.append(key)
    #         current = current[key]
    #     else:
    #         break
    # if level > len(path):
    #     msg = 'find_prefix called with level %s, largest common prefix is %s'
    #     msg = msg % (level, path)
    #     raise ValueError(msg)
    # if level > 0:
    #     path = path[:-level]
    # return join(source, *path)


def ensure_directory(fpath, isdir=False):
    if not isdir:
        path = dirname(fpath)
    else:
        path = fpath
    if not exists(path):
        os.makedirs(path)


def repackage_tar_with_one_level(in_tarpath, out_tarpath, addprefix):
    """
    takes in_tarpath, but rewrites it so that there is alwyas
    1 top level directory before all the crap. If the input
    tar file directory hierarchy is deep enough, we strip
    excess directories until there is one parent.

    if the input tar file directory hierarchy is not deep enough,
    we add <addprefix>
    """
    with tempfile.TemporaryDirectory() as target:
        extract_all(in_tarpath, target)
        try:
            prefix = find_prefix(target, level=1)
        except ValueError:
            prefix = find_prefix(target)
        else:
            # we don't need or want it if
            # the directoyr hierarchy is deep enough
            addprefix = None
        targz(out_tarpath, target, prefix=prefix, addprefix=addprefix)
