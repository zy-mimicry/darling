#! /usr/bin/env python3
#coding = utf-8

"""
"""

import subprocess
import os,sys,re

rule_template = """\
# ACIS udev conf

# Now, support 'TWO' DUT : master and slave
{rule_master_part_01}
{rule_slave_part_01}

{rule_master_part_02}

{rule_slave_part_02}

LABEL=="acis_end"
# End of Conf.
"""

rule_master_part_01 = """\
ATTRS{{serial}}=="{master_dev}", GOTO="acis_master" \
"""

rule_master_part_02 = """
# Jenkins Slave -- [acis master DUT]
LABEL=="acis_master"
SUBSYSTEMS=="usb", DRIVERS=="GobiSerial", SYMLINK+="acis/master/AT", ATTRS{bInterfaceNumber}=="03"
SUBSYSTEMS=="usb", DRIVERS=="GobiSerial", SYMLINK+="acis/master/DM", ATTRS{bInterfaceNumber}=="00"
GOTO="acis_end"\
"""

rule_slave_part_01 = """\
ATTRS{{serial}}=="{slave_dev}", GOTO="acis_slave"\
"""

rule_slave_part_02 = """\
# Jenkins Slave -- [acis slave DUT]
LABEL=="acis_slave"
SUBSYSTEMS=="usb", DRIVERS=="GobiSerial", SYMLINK+="acis/slave/AT", ATTRS{bInterfaceNumber}=="03"
SUBSYSTEMS=="usb", DRIVERS=="GobiSerial", SYMLINK+="acis/slave/DM", ATTRS{bInterfaceNumber}=="00"
GOTO="acis_end"\
"""


def get_devices():
    try:
        output = subprocess.check_output('adb devices',
                                        shell = True).decode('utf-8').strip()
    except subprocess.CalledProcessError as err:
        print("ERROR: ", err)
        sys.exit(-1)
    else:
        devices = []
        for line in output.split('\n'):
            print(line)
            g = re.match('\s*?(.*)\s*device$', line)
            if g:
                devices.append(g.group(1).strip())
        devices.append("helloworld")
        print(devices)
        return devices

def guide(devices):

    total_nums = 0
    picks = {}

    print("""             \
    >acis.make.rules<\nNote, acis.make.rules tool only support 'master' and 'slave' devices.\n""")
    print("Which would you like to link to </dev/acis/master> ?")

    for n,d in enumerate(devices):
        print("{n}. <{d}>".format(n = n + 1, d = d))
        total_nums += 1
    print("Total devices: [{nums}]\n".format(nums = total_nums))
    if total_nums == 0 or total_nums > 2:
        print("ACIS only support 1-2 devices, but scan [{}] . Please check your USB connection.".format(nums))
        sys.exit(-1)

    while True:
        try:
            which = int(input("Your choice:(number) "))
            if which > total_nums or which <= 0:
                raise ValueError("Outof Range")
        except ValueError:
            print("Please type INT NUMBER(in range 1-2) to pick."); continue
        else:
            print(which)
            picks["master"] = devices[which-1]

            if total_nums < 2:
                print("Now only one device [{}], and that be added to 'master', so there is NO 'slave.'".format(devices[which-1]))
            else:
                print("Due to your choice [{}] as 'master', ".format(
                    devices[which-1]), end = '')
                if which == 1:
                    print("so 'slave' auto-confirmed to [{}]".format(devices[1]))
                    picks["slave"] = devices[1]
                else:
                    print("so 'slave' auto-confirmed to [{}]".format(devices[0]))
                    picks["slave"] = devices[0]
            break
    return picks

# m = guide(get_devices())
# print(m)


def make_rules(_file, devices):

    template = ""

    if len(devices) == 2:
        template = rule_template.format( rule_master_part_01 = rule_master_part_01.format(master_dev = devices["master"]),
                                         rule_master_part_02 = rule_master_part_02,
                                         rule_slave_part_01  = rule_slave_part_01.format(slave_dev = devices["slave"]),
                                         rule_slave_part_02  = rule_slave_part_02)
    elif len(devices) == 1:
        template = rule_template.format( rule_master_part_01 = rule_master_part_01.format(master_dev = devices["master"]),
                                         rule_master_part_02 = rule_master_part_02,
                                         rule_slave_part_01  = "",
                                         rule_slave_part_02  = "")
    print("=================================")
    print(template)
    with open(_file, 'w') as f:
        f.write(template)
        f.flush()
    print("\n[Next Step] >> Hey, Guy! \n >> Now please unplug all USB DEVICEs and Sysmte will auto-enable the NEW rules for udev.")


def check_rules(_file, devices):

    if os.path.exists(_file):
        print("\n\n===== show file contents =====")
        for l in open(_file, 'r'):
            print(l)
        print("===== end of show =====")
        while True:
            choice = str(input("Do you want to overwrite it? (y/n)")).lower()
            if choice not in ("y", "n"):
                print("Please type (y or n) for your choice."); continue
                sys.exit(0)
            if choice == "n":
                print("Your choice is [NOT overwrite rules], so do nothing...")
            else:
                make_rules(_file, devices)
                pass
            break
    else:
        print("File:<{}> not exists, Now new a file to make a rule.".format(_file))
        make_rules(_file, devices)


check_rules('/etc/udev/rules.d/11-acis.rules', guide(get_devices()))


