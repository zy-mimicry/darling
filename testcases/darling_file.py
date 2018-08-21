#! /usr/bin/env python
# coding=utf-8

"""
"""

import os, shutil
from pprint import pprint
import time

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
        try:
            os.makedirs(p)
        except FileExistsError as e:
            shutil.rmtree(p)

dynamic_of_log_path = ''
def darling_head_fall(item):
    global dynamic_of_log_path
    time_str = time.strftime('%Y_%m_%d_%H_%M_%S')
    dynamic_of_log_path = 'darling_log/' + time_str
    return "./darling_log" + '/' + time_str + '/' + item[1:]

def darling_mimicry_dir(src, dst):
    print("src: {}, dst: {}".format(src, dst))
    _list = []
    tree = tree_from_abs_dir(src)
    if os.path.basename(src) == "":
        src = os.path.basename(os.path.dirname(src))
    src = os.path.basename(src)
    print("src: {}, tree: {}".format(src, tree))
    deal_tree_dict(tree, src, '.', _list)
    _list = [i for i in map(darling_head_fall, _list)]
    print(_list)
    makedirs_by_list(dst, _list)

if __name__ == "__main__":
    darling_mimicry_dir('./testcases/','../', darling_head_fall)
