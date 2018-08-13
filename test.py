#! /usr/bin/env python
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

def deal_tree_dict(tree_dict, name, string, list_of_path):
    if len(tree_dict[name]) == 0:
        print(string + "/" + name)
    string += "/" + name
    for i in tree_dict[name]:
        deal_tree_dict(tree_dict, i, string)

if __name__ == "__main__":
    tree = tree_from_abs_dir("../test/testcases/")

