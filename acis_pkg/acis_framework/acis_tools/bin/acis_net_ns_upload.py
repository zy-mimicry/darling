#! /usr/bin/env python3
#coding=utf-8

import os,sys,re,shutil
import subprocess

def get_cookies(dst):
    """
    """

    which_net = 'wlp3s0'
    # Is exists? (NFS directory)
    if not os.path.exists(dst):
        raise FileNotFoundError("Sorry, '{}' directory is not exists.".format(dst))

    # GET: IP , hostname , mac address
    try:
        ip = subprocess.check_output("ifconfig {net} | grep \"inet addr\" | awk '{{ print $2}}' | awk -F: '{{print $2}}'".
                                     format(net = which_net),
                                     shell=True).decode('utf-8').strip()
        hostname = subprocess.check_output('hostname', shell=True).decode('utf-8').strip()
        mac = subprocess.check_output('cat /sys/class/net/{net}/address'.
                                      format(net = which_net),
                                      shell = True).decode('utf-8').strip()
    except subprocess.SubprocessError as e:
        print(e)
        sys.exit(-1)
    else:
        return { 'ip' : ip,
                 'hostname' : hostname,
                 'mac' : mac}


def iter_file(dst, pattern):
    for root, dirs, filelist in os.walk(dst):
        for f in filelist:
            if f == pattern:
               return (True, root, os.path.basename(root))
        for d in dirs:
            iter_file(root + '/' + d, pattern)
    return (False, "", "")

def find_ipfile(dst, ip):
    return iter_file(dst, ip)

if __name__ == "__main__":

    NFS_dir = './rasp-nodes-ips'
    cookies = get_cookies(NFS_dir)

    obj_file = cookies['ip']
    (exists, root_dir, host) = find_ipfile(NFS_dir, obj_file)

    if exists:
        if parent_dir == cookies['hostname']:
            print('Do nothing.')
            return
        else:
            # 1. rm file
            os.remove(root_dir + '/' + cookies['ip'])
            # 2. if hostname dir exists?
            # 3.1 exists
            if os.path.exists(root_dir):
                pass
            # 3.2 not exists
            else:
                os.makedirs()
                write file
    else:
        # 1. if hostname dir exists?
        # 2. exists: touch file at here
        # 3. not exists: make a dir and touch file at there.
        pass
