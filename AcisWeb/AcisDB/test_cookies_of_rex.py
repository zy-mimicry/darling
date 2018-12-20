
# 20 items
erd_ids = [
    "04.60.25",
    "04.60.26",
    "04.60.27",
    "04.60.28",
    "04.60.29",
    "04.60.30",
    "04.60.31",
    "04.60.32",
    "04.60.33",
    "04.60.34",
    "04.60.35",
    "04.60.36",
    "04.60.37",
    "04.60.38",
    "04.60.39",
    "04.60.40",
    "04.60.41",
    "04.60.42",
    "04.60.43",
    "04.60.44",
]


category = [
    "07 - Cloud Platform",
    "09 - Performances",
    "10 - Regulatory App. & Env. Compliance ",
]

title = [
    "eUICC support ",
    "Startup Time " ,
    "Spy mode ",
    "WiFi Hotspot ",
]

description = [
    'The module shall support an AT command to configure modem to bootup to SPY mode. ',
    'The module shall support a Legato API to enter spy mode when modem registers on UMTS network, the Legato API will not take effect when modem registers on LTE network. ',
    "The module shall automatically detect the 'FILE' type CWE images, decode and copy to a specific path of EFS. ",
    "The module should automatically detect the NV update file from a specific path in EFS, then parse each NV/EFS item from the file and write it to appropriate NV/EFS location, the parsed file should be deleted automatically after NV update is completed. ",
    "The module firmware design shall not change the NV item structure for a given NV item during the course of development and product maintenance. ",

    "The module shall support eUICC device requirement per GSMA specification Annex G for DEV1, DEV2, DEV3, DEV4, DEV5, DEV6, DEV8 and DEV9. See Document \"Remote Provisioning Architecture for Embedded UICC Technical Specification v1.0 17 December 2013\"",
    ' The module should support eUICC device requirement per GSMA specification Annex G for DEV7. See Document "Remote Provisioning Architecture for Embedded UICC Technical Specification v1.0 17 December 2013"',
    "The module shall support local SIM profile switch for following SIM manufacturer, including VALID, Gemalto, G&D, Oberthur and Morpho. ",

    "The module's Legato framework and service shall be ready to use in 20s from power on or reset. ",
    "blank ",
    "The module shall complete loading kernel image (i.e. to start launching \"init\" process) within 4.5s after power-on or reset, even with security signed images. ",
    "blank ",
    "The module shall support USB ready (i.e. USB enumeration complete on device side) within 10s after power-on/reset, even with security signed images. ",
    "The module shall support full emergency call functionality within 20s from module power-on or reset, even with security signed images. ",
    "Legato start-up time itself shall not be greater than 4s (i.e. from rootfs starts loading Legato to all Legato services are functional). ",
    "The module shall support an AT command to exit spy mode. ",
    "The module shall support an AT command to configure if module can exit spy mode by AT command. ",
    "The module shall support an AT command to enter spy mode when modem registers on UMTS network, and the AT command will not take effect when modem registers on LTE network. ",
]

product_priority = ['MUST', 'SHOULD']

status = ['DONE', "UNDO"]

author = ["Cassie Sheng", "Victor He", "Joe Liu",]

version = ["01.00", "01.01", "01.02", "01.03", "01.04",]

HLD = ['https://link_to_HLD_01', "https://link_to_HLD_02"]

l1_jira = ['https://issues.sierrawireless.com/browse/QTI9X28-4000']
l2_jira = ['https://issues.sierrawireless.com/browse/QTI9X28-3077']

bug_jiras = ['https://issues.sierrawireless.com/browse/QTI9X28-4072',
             'https://issues.sierrawireless.com/browse/QTI9X28-4077',
             'https://issues.sierrawireless.com/browse/QTI9X28-4007',]

platform = ['SD55']

workload = ['1d', '2d', '1w', '4h']

case_name = ["ACIS_A_S_Test_Temp_Volt","ACIS_A_S_PowerOff_Linux","ACIS_A_S_Reset_Linux_HW"]

case_age = ['2018-11-25', '2017-11-24', '2011-1-1']

test_result = ['PASS', "FAIL"]

test_log = ['ftp://acis_testcase_log_path01', "ftp://acis_testcase_log_path03","ftp://acis_testcase_log_path02"]

report_path = ['ftp://report_path_01','ftp://report_path_02','ftp://report_path_03' ]

fw_version = ['SWI9X28A_00.19.02.13','SWI9X28A_00.19.01.13','SWI9X28A_00.19.02.12']

test_date = ['2011-2-22', '2015-12-1', '2014-11-9']

def random_gen_cookies():
    """
    out_cookies = [{
                    'ERD_ID'  : "",
                    'excel'   : {},
                    'jira'    : {},
                    'jenkins' : {},
                    'UIform'  : {}},
                    ...]
    """

    import random
    out_cookies = []

    for e in erd_ids:
        out = {}
        out['ERD_ID'] = e
        out['excel'] = {
            'erd_id' : e,
            'category' : random.choice(category),
            'title' : random.choice(title),
            'description' : random.choice(description),
            'product_priority' : random.choice(product_priority),
            'author' : random.choice(author),
            'version' : random.choice(version),
        }
        out['jira'] = {
            'HLD' : random.choice(HLD),
            'status' : random.choice(status),
            'l1_jira' : random.choice(l1_jira),
            'l2_jira' : random.choice(l2_jira),
            'bug_jiras' : random.choice(bug_jiras),
            'platform' : random.choice(platform),
            'workload' : random.choice(workload),
            'case_name' : random.choice(case_name),
            'case_age' : random.choice(case_age),
            'report_path' : random.choice(report_path),
        }
        out['jenkins'] = {
            'fw_version' : random.choice(fw_version),
            'test_result' : random.choice(test_result),
            'test_log' : random.choice(test_log),
            'date' : random.choice(test_date),
        }
        out['UIform'] = {
            'UItest' : "I Love This Game.",
        }
        out_cookies.append(out)

    return out_cookies
