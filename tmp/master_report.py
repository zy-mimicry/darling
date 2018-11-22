#! /usr/bin/env python
# coding=utf-8

"""
"""

import sys,re,os
import shutil
import zipfile
import getopt


def iter_report_tree(dest, out):
    """
    Copy dest's *_report files to out.
    """

    if not os.path.exists(dest):
        raise Exception("Report Directry NOT exists.")

    if not os.path.exists(out):
        raise Exception("Report output-dir NOT exists.")

    if os.path.exists(out):
        shutil.rmtree(out)
        os.makedirs(out, mode = 0o775)

    for dirname, subdir, filelist in os.walk(dest):
        if '_report' in dirname:
            for f in filelist:
                shutil.copy(dirname + '/' + f, out +'/' + f )
            for s in subdir:
                shutil.copytree(dirname + '/' + s , out + '/' + s)

def make_zip(source_dir, output_filename):
    """
    Zip source_dir to output file.
    """
    if not os.path.exists(source_dir):
        raise Exception

    if not os.path.exists(os.path.dirname(output_filename)):
        os.makedirs(os.path.dirname(output_filename))

    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)
            zipf.write(pathfile, arcname)
    zipf.close()


def result_link(src, syml):
    os.symlink(src, syml)

def make_workspace_report(out):
    os.makedirs(out, mode=0o775)

def deal_cmdline(argv):
    src  = ''
    dest = ''
    out_zip = ''
    link = ''
    report = ''

    try:
        opts, args = getopt.getopt(argv,"hs:d:z:L:R:",["sfile=","dfile=","zip=","Link=","Report="])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("""\
Usage:
    python demo.py -s [test_log_dir] -d [test_log_root] -z [where_zip] -L [result_link] -R [report_spec]

    - python demo.py -s [test_log_dir]
                     -d [test_log_root]
                     -z [where_zip]
                     -L [result_link]
                     -R [report_spec]
            """)
            sys.exit(0)
        elif opt in ("-s", "--sfile"):
            src  = arg
        elif opt in ("-d", "--dfile"):
            dest = arg
        elif opt in ("-z", "--zip"):
            out_zip = arg
        elif opt in ("-L", "--Link"):
            link = arg
        elif opt in ("-R", "--Report"):
            report = arg

    print("All args:", src, dest, out_zip, link, report)

    print("iter tree")
    iter_report_tree(src, dest)

    print("zip file")
    make_zip(dest, out_zip)

    print("link result")
    result_link(dest, link)

    print("make report dir")
    make_workspace_report(report)

if __name__ == "__main__":
    deal_cmdline(sys.argv[1:])

