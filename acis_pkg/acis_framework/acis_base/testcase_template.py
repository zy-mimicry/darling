#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from acis.core.report import report

"""
@ Information about this case or author, just like:

@ Author:

@ Test Cases TODO:
@ Test Name:
@ Brief:

@ History
Date                    Author                          Modification
2018-June-08            rzheng                          Create file
------------------------------------------------------------------------
"""

@report.fixture(scope="module")
def m(request, minit):
    """
    __file__    : logging module record log file.
    logger_name : logger namespace of logging module.
    mail_to     : where the mail to be send.
    port_names  : testcase registers ports [AT or ADB ...] from framework.
                : ? DUT1   << map to '/etc/udev/rules.d/11-acis.rules' - 'DUT1'
                : ? DUT2   << map to '/etc/udev/rules.d/11-acis.rules' - 'DUT2'
                : ? any    << map to '/etc/udev/rules.d/11-acis.rules' - 'DUT1' or 'DUT2'
                : eg. port_names  = [
                                    'AT..DUT1',
                                    'AT..DUT2',
                                    'ADB..DUT1',
                                    'ADB..DUT2',
                                    ]
    """
    mz =  minit(__file__,
                logger_name = 'ACIS.SYSTEM.RESET.LINUX',
                mail_to     = 'swi@sierrawireless.com',
                port_names  = [
                    'AT..any',
                    'ADB..any',
                ])

    mz.test_ID = __name__
    mz.errors = {}
    mz.flags  = []
    def module_close_AT():
        if mz.at: mz.at.closeall()
    request.addfinalizer(module_close_AT)
    return mz

# Functions defined outside the class can still be used.
@report.step("[Stage] < out of class functions>")
def out_of_class_function(m):
    print("Out of class, get 'm' is :{}".format(m))

# < ACIS report category >
# divide categories according to the directory structure.
# -- For example:
# [directory]    >> testcases/System/ATcommand/ACIS_A_S_Test_Temp_Volt.py
# report.epic    << report.epic("System")
# report.feature << report.feature("ATcommand")
# report.story   << report.story("ACIS_A_S_Test_Temp_Volt")
# report.step    << This represents a series of steps performed.

# < ACIS report links >
# As long as the name URL is different, you can set multiple http links.
# And you can specify the name you want.
# -- For example:
# report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440",name = ">JIRA: beauty<")
# report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4442",name = ">JIRA: Awesome<")
# report.link("https://issues.sierrawireless.com/browse/QTI9X28-4443", name = "=Gerrit: commit 01=")

@report.epic("System")              # << should be modified to category
@report.feature("ATcommand")        # << should be modified to feature
@report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440",name = ">JIRA: ADC Body<")
class ACISsystemReset(): # << should modify

    @report.step("[Stage] <Pre-Condition>")
    def pre(self, m):
        m.log("Stage [pre]")
        sim_ini = m.conf.SIM_INI

    @report.step("[Stage] <Real-Test-Body>")
    def body(self, m):
        m.log("Stage [body]")
        m.at.any.send_cmd("AT\r")
        m.at.any.waitn_match_resp(["*\r\nOK\r\n"], 4000)

    @report.step("[Stage] <Restore-Module>")
    def restore(self, m):
        m.log("Stage [restore]")
        m.adb.any.send_cmd("shell \"poweroff\"")
        out_of_class_function(m)


    @report.link("https://issues.sierrawireless.com/browse/QTI9X28-4443", name = "=Gerrit: commit 01=")
    @report.story("test_case_name")           # << should be modified to test case name
    @report.mark.run(order=1)
    def acis_mstage_entrance(self, m): # << should modify. MUST: testcase ID(file name)
        """
        TODO:
        1. The test entrance.
        2. A functional description of testcase should be added here.
        """

        m.log(">> Welcome to use ACIS ! ^_^\n")
        try:
            try:
                self.pre(m)                    # << Stage | pre
            except Exception as e:
                m.flags.append('pre')
                m.errors['pre'] = e
                raise e
            self.body(m)                       # << Stage | body
        except Exception as e:
            if not m.flags :
                m.flags.append('body')
                m.errors['body'] = e
            raise e

        finally:
            try:
                if m.flags:
                    [ m.at.closeall() for me in m.errors[m.flags[0]].args if 'Input/output error' in me ]
                self.restore(m)                # << Stage | restore
            except Exception as e:
                m.log("<Restore> The restore process should not have an exception.\nBut now NOT,reason:\n{}".format(e))
                m.flags.append('restore')
                m.errors['restore'] = e

            if m.flags:
                m.log("\n\n  <ACIS Exception Stack Information>\n")
                for f in m.flags:
                    m.log("--- {} stack info ---\n{}\n\n".format(f, m.errors[f]))

                m.log("\nTESTCASE:[{}] Result:[{}]\n".format(m.test_ID, "FAIL"))
                report.attach_file(source = m.which_log, name = __name__ + '.log',
                                   attachment_type = report.attachment_type.TEXT)
            else:
                m.log("\nTESTCASE:[{}] Result:[{}]\n".format(m.test_ID, "PASS"))
                report.attach_file(source = m.which_log, name = __name__ + '.log',
                                   attachment_type = report.attachment_type.TEXT)
