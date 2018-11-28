#! /usr/bin/env python3

import shutil
import os,sys

def do_copy():

    shutil.copytree('./acis_testcasess/', './old')

    for root, dirs, filelist in os.walk('./old'):
        for f in filelist:
            if '__init__' not in f:
                print("delete file: ", os.path.join(root, f))
                os.remove(os.path.join(root, f))

do_copy()
