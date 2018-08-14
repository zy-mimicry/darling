#! /usr/bin/env python
# coding=utf-8

"""
"""

import os

def tree_from_abs_dir(rootdir):
    tree = {}
    if os.path.basename(rootdir) == "":
        rootdir = os.path.dirname(rootdir)
    for dirname, subdirname, filelist_noused in os.walk(rootdir):
        if dirname == rootdir and len(subdirname) == 0:
            return tree
        tree[os.path.basename(dirname)] = subdirname
    return tree

def deal_tree_dict(tree_dict, name, string, list_path):
    if len(tree_dict[name]) == 0:
        list_path.append(string + "/" + name)
    string += "/" + name
    for _name in tree_dict[name]:
        deal_tree_dict(tree_dict, _name, string, list_path)

def makedirs_by_list(dest, list_path):
    os.chdir(dest) # dest can't be empty.
    for p in list_path:
        os.makedirs(p)

def mimicry_dir(src, dst):
    """
    Usage: mimicry_dir('/home/yang/__mzPython__/darling/testcases/','../')
    """
    _list = []
    tree = tree_from_abs_dir(src)
    deal_tree_dict(tree, 'testcases', '.', _list)
    makedirs_by_list(dst, _list)

def darling_head_fall(item):
    return "./darling" + item[2:]

def darling_mimicry_dir(src, dst):
    _list = []
    tree = tree_from_abs_dir(src)
    _i_tree = map(darling_head_fall, tree)
    tree = [i for i in _i_tree]
    deal_tree_dict(tree, 'testcases', '.', _list)
    makedirs_by_list(dst, _list)

if __name__ == "__main__":
    darling_mimicry_dir('/home/yang/__mzPython__/darling/testcases/','../')
