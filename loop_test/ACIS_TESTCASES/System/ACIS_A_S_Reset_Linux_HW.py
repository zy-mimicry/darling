import pytest
import allure
from acis.core.report import report
import os,re

"""
"""

@report.fixture(scope="module")
def m(request, misc):
    mz =  misc(__file__,
               logger_name = 'ACIS.System.Reset.linux_hw',
               mail_to     = 'rzheng@sierrawireless.com',
               port_names  = [
                   'AT..master',
                   'AT..slave',
                   'ADB..master',
                   'ADB..slave',
               ])

    mz.test_ID = os.path.basename(__file__.split('.')[0])
    mz.errors = {}
    mz.flags  = []
    def module_upload_log():
        allure.attach.file(source = mz.which_log,
                           attachment_type = allure.attachment_type.TEXT)
        mz.at.closeall()
    request.addfinalizer(module_upload_log)
    return mz

@report.step("[Stage] < out of class functions>")
def out_of_class_function(m):
    print("Out of class, get 'm' is :{}".format(m))

@report.epic("System")
@report.feature("Reset")
@report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440",name = ">JIRA: ADC Body<")
class ACISsystemReset():
    """
    Something you want to descript for this test. (can't display)
    """

    @report.step("[Stage] <Pre-Condition>")
    def pre(self, m):

        m.at.slave.send_cmd( "AT\r")
        m.at.slave.waitn_match_resp(  ["*\r\nerror\r\n"], 4000)

        m.at.slave.send_cmd(  "AT&F;&W\r")
        m.at.slave.waitn_match_resp(  ["*\r\nOK\r\n"], 4000)

        m.at.slave.send_cmd(  "ATE0\r")
        m.at.slave.waitn_match_resp(  ["*\r\nOK\r\n"], 4000)

        m.at.slave.send_cmd(  "AT+CMEE=1\r\n")
        m.at.slave.waitn_match_resp(  ['*\r\nOK\r\n'], 2000)

        m.at.slave.send_cmd(  'ATI3\r')
        m.at.slave.waitn_match_resp(  ['*\r\n*\r\n\r\nOK\r\n'], 4000)

        m.at.slave.send_cmd(  'AT!PACKAGE?\r')
        m.at.slave.waitn_match_resp(  ['*\r\n*\r\nOK\r\n'], 4000)

        m.at.slave.send_cmd(  'ATI8\r')
        m.at.slave.waitn_match_resp(  ['*\r\n*\r\n\r\nOK\r\n'], 4000)

        m.at.slave.send_cmd(  'AT!SKU?\r')
        m.at.slave.waitn_match_resp(  ['*\r\n*\r\n\r\nOK\r\n'], 4000)

        m.at.slave.send_cmd(  'AT+GMM\r\n')
        model = m.at.slave.wait_resp(  ["*\r\nOK\r\n"], 5000).split('\r\n')[1].strip()

        # m.at.slave.send_cmd(  'AT+ICCID\r')
        # m.at.slave.waitn_match_resp(  ['*ICCID: *\r\n'], 4000)
        # m.at.slave.waitn_match_resp(  ['\r\nOK\r\n'], 4000)

        m.at.slave.send_cmd(  'AT+WUSLMSK=00000000,0\r\n')
        m.at.slave.waitn_match_resp(  ["*\r\nOK\r\n"], 5000)

        m.at.slave.send_cmd(  'AT+WUSLMSK=00000000,1\r\n')
        m.at.slave.waitn_match_resp(  ["*\r\nOK\r\n"], 5000)

        m.at.slave.send_cmd(  'AT!UNLOCK="A710"\r')
        m.at.slave.waitn_match_resp(  ['*\r\nOK\r\n'], 5000)

        m.at.slave.send_cmd(  "AT!GCCLR\r")
        m.at.slave.waitn_match_resp(  ["*\r\nCrash data cleared\r\n"], 4000)
        m.at.slave.waitn_match_resp(  ["\r\nOK\r\n"], 4000)

        m.at.slave.send_cmd(  "AT!EROPTION?\r\n")
        resp = m.at.slave.wait_resp(  ['*\r\nOK\r\n'], 2000)
        if "Reset" in resp:
            m.at.slave.send_cmd(  "AT!EROPTION=0,1\r\n")
            m.at.slave.waitn_match_resp(  ['*\r\nOK\r\n'], 2000)

            m.at.slave.send_cmd(  "AT!RESET\r\n")
            m.at.slave.waitn_match_resp(  ['\r\nOK\r\n'], 2000)
            m.at.slave.sleep(30000)

        m.at.slave.send_cmd(  "ATE0\r\n")
        m.at.slave.waitn_match_resp(  ['*\r\nOK\r\n'], 2000)


    @report.step("[Stage] <Real-Test-Body>")
    def body(self, m):

        m.log ("*****************************************************************")
        m.log ("%s: To verify Kernel Hard Reset stability" % m.test_ID)
        m.log ("*****************************************************************")

        for i in range(1):
            #print ("\n-----Kern_H %dth loop reset-----\n" % i)

            #print "\nATI"
            m.at.slave.send_cmd(  'ATI\r')
            m.at.slave.waitn_match_resp(  ['*\r\n*\r\n\r\nOK\r\n'], 4000)

            #print "\nAT!PACKAGE?"
            m.at.slave.send_cmd(  'AT!PACKAGE?\r')
            m.at.slave.waitn_match_resp(  ['*\r\n*\r\nOK\r\n'], 4000)

            #print "\nATI8"
            m.at.slave.send_cmd(  'ATI8\r')
            m.at.slave.waitn_match_resp(  ['*\r\n*\r\n\r\nOK\r\n'], 4000)

            #print "\nCheck module is crashed"
            m.at.slave.send_cmd(  "AT!GCDUMP\r")
            m.at.slave.waitn_match_resp(  ["*\r\nNo crash data available\r\n"], 20000)
            m.at.slave.waitn_match_resp(  ["\r\nOK\r\n"], 4000)
            if m.at.slave.statOfItem != "OK":
                raise Exception("Modem crashed...")

            m.adb.slave.send_cmd("reboot")

            if m.at.slave.statOfItem != "OK":
                raise Exception("Reboot failed...")

            m.at.slave.sleep(30000)

            #print "\nAT!gstatus? to check whether module reboot truely"
            m.at.slave.send_cmd(  "AT!GSTATUS?\r")
            resp = m.at.slave.wait_resp( ["*\r\nOK\r\n"], 4000).split('\r\n')[2]
            R_time = int(re.split(':|\t', resp)[1])
            if (R_time > 30000):
                #print "module don't reboot truely, Time From Boot: %d" % R_time
                raise Exception("Kernel hard reset failed...")

        #print "\n----- Test Body End -----\n"
        #print "\n**************************************************************\n"

    @report.step("[Stage] <Restore-Module>")
    def restore(self, m):
        m.log("I'm stage 03 << pre")
        m.log("Nothing to do in this stage.....")
        m.at.slave.send_cmd(  "AT&F;&W\r")
        m.at.slave.waitn_match_resp(  ["*\r\nOK\r\n"], 4000)

        out_of_class_function(m)


    @report.story("linux_hw")
    @pytest.mark.run(order=1)
    @report.link("https://issues.sierrawireless.com/browse/QTI9X28-4443", name = "=Gerrit: commit 01=")
    def acis_mstage_entrance(self, m):
        """
        The test entrance.

        Please descript more information for this testcase.

        balabala....

        For example:
        ADC test information should be here.

        """

        m.log("\n>> Welcome to use ACIS ! ^_^")
        try:
            try:
                self.pre(m)                    # << Stage | pre
            except Exception as e:
                m.log("<Pre-Stage-Exception> reason: {}".format(e))
                m.flags.append('pre')
                m.errors['pre'] = e
                raise e
            self.body(m)                       # << Stage | body
        except Exception as e:
            if not m.flags :
                m.log("<Body-Stage-Exception> reason: {}".format(e))
                m.flags.append('body')
                m.errors['body'] = e
        try:
            self.restore(m)                    # << Stage | restore
        except Exception as e:
            m.log("<Restore-Stage-Exception> reason: {}".format(e))
            m.flags.append('restore')
            m.errors['restore'] = e
        if m.flags:
            m.log("\n\n  <ACIS Exception Stack Information>\n")
            for f in m.flags:
                m.log("--- {} stack info ---\n{}\n".format(f, m.errors[f]))
            m.log("\nTESTCASE:[{}] Result:[{}]\n".format(m.test_ID, "FAIL"))
            raise Exception("\n\n <ACIS Test Exception, Please check stack information.>\n")
        else:
            m.log("\nTESTCASE:[{}] Result:[{}]\n".format(m.test_ID, "PASS"))
