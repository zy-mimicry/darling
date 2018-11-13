#! /usr/bin/env python
# coding=utf-8

"""
"""

import os, shutil
from pprint import pprint
#import time

def _tree_from_abs_dir(rootdir):
    tree = {}
    if os.path.basename(rootdir) == "":
        rootdir = os.path.dirname(rootdir)
    for dirname, subdirname, filelist_noused in os.walk(rootdir):
        if dirname == rootdir and len(subdirname) == 0:
            return tree
        tree[os.path.basename(dirname)] = subdirname
    return tree

def _deal_tree(tree_dict, name, string, list_path):
    if len(tree_dict[name]) == 0:
        list_path.append(string + "/" + name)
    string += "/" + name
    for _name in tree_dict[name]:
        _deal_tree(tree_dict, _name, string, list_path)

def _makedirs(dest, list_path):
    mark_workspace = os.getcwd()
    os.chdir(dest) # dest can't be empty.
    for p in list_path:
        try:
            os.makedirs(p)
        except FileExistsError as e:
            shutil.rmtree(p)
    os.chdir(mark_workspace)

different_str = '' # input
def darling_head_fall(item):
    global different_str
    diff = different_str
    dynamic_of_log_path = 'darling_log/' + diff
    return dynamic_of_log_path + '/' + item[2:]

def darling_mimicry_dir(src, dst):
    print("src: {}\ndst: {}".format(src, dst))
    _list = []
    tree = _tree_from_abs_dir(src)
    if os.path.basename(src) == "":
        src = os.path.basename(os.path.dirname(src))
    src = os.path.basename(src)
    print("src(after deal): {}\ntree: {}".format(src, tree))
    _deal_tree(tree, src, '.', _list)
    _list = [i for i in map(darling_head_fall, _list)]
    print(_list)
    _makedirs(dst, _list)

if __name__ == "__main__":
    darling_mimicry_dir('../testcases/','./test_dir')
