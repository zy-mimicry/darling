import pytest
import allure
from acis.core.report import report
import os

"""
"""

@report.fixture(scope="module")
def m(request, misc):
    mz =  misc(__file__,
               logger_name = 'ACIS.System.ATcmd.volt',
               mail_to     = 'rzheng@sierrawireless.com',
               port_names  = [
                   # 'AT..master',
                   # 'AT..slave',
                   # 'ADB..master',
                   # 'ADB..slave',
                   'AT..any',
                   'ADB..any',
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
@report.feature("ATcommand")
@report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440",name = ">JIRA: ADC Body<")
class ACISsystemReset():
    """
    Something you want to descript for this test. (can't display)
    """

    @report.step("[Stage] <Pre-Condition>")
    def pre(self, m):
        m.log("\n------------Test Environment check: Start------------")
        # UART Init
        m.log("\nTest Environment Step 2: Open AT Command port:")

        m.log("\nTest Environment Step 3: Initiate DUT:")
        m.at.any.send_cmd( "AT\r")
        m.at.any.waitn_match_resp( ["*\r\nOK\r\n"], 4000)

        m.at.any.send_cmd( "AT&F;&W\r")
        m.at.any.waitn_match_resp( ["*\r\nOK\r\n"], 4000)

        m.at.any.send_cmd( "ATE0\r")
        m.at.any.waitn_match_resp( ["*\r\nOK\r\n"], 4000)

        m.at.any.send_cmd( "AT+CMEE=1\r\n")
        m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 2000)

        m.at.any.send_cmd( 'ATI3\r')
        m.at.any.waitn_match_resp( ['*\r\n*\r\n\r\nOK\r\n'], 4000)

        m.at.any.send_cmd( 'AT!PACKAGE?\r')
        m.at.any.waitn_match_resp( ['*\r\n*\r\nOK\r\n'], 4000)

        m.at.any.send_cmd( 'ATI8\r')
        m.at.any.waitn_match_resp( ['*\r\n*\r\n\r\nOK\r\n'], 4000)

        m.at.any.send_cmd( 'AT!SKU?\r')
        m.at.any.waitn_match_resp( ['*\r\n*\r\n\r\nOK\r\n'], 4000)

        m.log("\nGet device model")
        m.at.any.send_cmd( 'AT+GMM\r\n')
        model = m.at.any.wait_resp( ["*\r\nOK\r\n"], 5000).split('\r\n')[1].strip()

        m.log("\nRead CCID number from SIM:")
        # m.at.any.send_cmd( 'AT+ICCID\r')
        # m.at.any.waitn_match_resp( ['*ICCID: *\r\n'], 4000)
        # m.at.any.waitn_match_resp( ['\r\nOK\r\n'], 4000)

        m.log("\nConfigure unsolicited response:")
        m.at.any.send_cmd( 'AT+WUSLMSK=00000000,0\r\n')
        m.at.any.waitn_match_resp( ["*\r\nOK\r\n"], 5000)

        m.at.any.send_cmd( 'AT+WUSLMSK=00000000,1\r\n')
        m.at.any.waitn_match_resp( ["*\r\nOK\r\n"], 5000)

        m.log("\nUnlock module")
        m.at.any.send_cmd( 'AT!UNLOCK="A710"\r')
        m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 5000)

        m.log("\nAT!GCCLR")
        m.at.any.send_cmd( "AT!GCCLR\r")
        m.at.any.waitn_match_resp( ["*\r\nCrash data cleared\r\n"], 4000)
        m.at.any.waitn_match_resp( ["\r\nOK\r\n"], 4000)

        m.log("\nCheck whether enter download mode")
        m.at.any.send_cmd( "AT!EROPTION?\r\n")
        resp = m.at.any.wait_resp(['*\r\nOK\r\n'], 2000)
        if "Reset" not in resp:
            m.at.any.send_cmd( "AT!EROPTION=1\r\n")
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 2000)

            m.log("\nReset module:")
            m.at.any.send_cmd( "AT!RESET\r\n")
            m.at.any.waitn_match_resp( ['\r\nOK\r\n'], 30000)
            m.at.any.reopen(30000)

        m.log("\nCancel Echo:")
        m.at.any.send_cmd( "ATE0\r\n")
        m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 2000)

    @report.step("[Stage] <Real-Test-Body>")
    def body(self, m):
        m.log("*****************************************************************")
        m.log("%s: To test some at cmd function" % m.test_ID)
        m.log("*****************************************************************")

        for i in range(1):
            m.log("\nUnlock module")
            m.at.any.send_cmd( 'AT!UNLOCK="A710"\r')
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 5000)

            m.log("\nat!pctemp?")
            m.at.any.send_cmd( 'at!pctemp?\r')
            m.at.any.waitn_match_resp( ["*\r\nOK\r\n"], 4000)

            m.log("\nat!patemp?")
            m.at.any.send_cmd( 'at!patemp?\r')
            m.at.any.waitn_match_resp( ["*\r\nOK\r\n"], 4000)

            m.log("\nat!pcvolt?")
            m.at.any.send_cmd( 'at!pcvolt?\r')
            resp = m.at.any.wait_resp( ["*\r\nOK\r\n"], 4000).split('\r\n')
            volt = resp[2].split(': ')[1].split(' mV')[0]
            m.log("\nat!pcvoltlimits?")
            m.at.any.send_cmd( 'at!pcvoltlimits?\r')
            resp = m.at.any.wait_resp( ["*\r\nOK\r\n"], 4000).split('\r\n')
            hi_crit = resp[1].split(': ')[1]
            hi_norm = resp[2].split(': ')[1]
            lo_norm = resp[3].split(': ')[1]
            lo_warn = resp[4].split(': ')[1]
            lo_crit = resp[5].split(': ')[1]
            #m.log("", hi_crit, hi_norm, hi_norm, lo_warn,lo_crit)

            #Low Critical
            m.log("\nat!pcvoltlimits=")
            m.at.any.send_cmd( 'at!pcvoltlimits='+str(int(volt)+500)+','+str(int(volt)+400)+','+str(int(volt)+300)+','+str(int(volt)+200)+','+str(int(volt)+100)+'\r')
            m.at.any.waitn_match_resp( ["*\r\nOK\r\n"], 4000)
            m.log("\nReset module:")
            m.at.any.send_cmd( "AT!RESET\r\n")
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 2000)
            m.at.any.reopen( 30000)
            m.at.any.sleep(10000)
            m.log("\nCancel Echo:")
            m.at.any.send_cmd( "ATE0\r\n")
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 2000)
            m.at.any.send_cmd( 'AT!UNLOCK="A710"\r')
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 5000)
            m.at.any.send_cmd( 'at!pcvolt?\r')
            m.at.any.waitn_match_resp( ['*\r\nVolt state: Low Critical\r\n'], 4000)
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 4000)

            #Low Warning
            m.log("\nat!pcvoltlimits=")
            m.at.any.send_cmd( 'at!pcvoltlimits='+str(int(volt)+400)+','+str(int(volt)+300)+','+str(int(volt)+200)+','+str(int(volt)+100)+','+str(int(volt)-100)+'\r')
            m.at.any.waitn_match_resp( ["*\r\nOK\r\n"], 4000)
            m.log("\nReset module:")
            m.at.any.send_cmd( "AT!RESET\r\n")
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 2000)
            m.at.any.reopen( 30000)
            m.at.any.sleep(10000)
            m.log("\nCancel Echo:")
            m.at.any.send_cmd( "ATE0\r\n")
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 2000)
            m.at.any.send_cmd( 'AT!UNLOCK="A710"\r')
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 5000)
            m.at.any.send_cmd( 'at!pcvolt?\r')
            m.at.any.waitn_match_resp( ['*\r\nVolt state: Low Warning\r\n'], 4000)
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 4000)

            #High Warning
            m.log("\nat!pcvoltlimits=")
            m.at.any.send_cmd( 'at!pcvoltlimits='+str(int(volt)+100)+','+str(int(volt)-100)+','+str(int(volt)-200)+','+str(int(volt)-300)+','+str(int(volt)-400)+'\r')
            m.at.any.waitn_match_resp( ["*\r\nOK\r\n"], 4000)
            m.log("\nReset module:")
            m.at.any.send_cmd( "AT!RESET\r\n")
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 2000)
            m.at.any.reopen( 30000)
            m.at.any.sleep(10000)
            m.log("\nCancel Echo:")
            m.at.any.send_cmd( "ATE0\r\n")
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 2000)
            m.at.any.send_cmd( 'AT!UNLOCK="A710"\r')
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 5000)
            m.at.any.send_cmd( 'at!pcvolt?\r')
            m.at.any.waitn_match_resp( ['*\r\nVolt state: High Warning\r\n'], 4000)
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 4000)

            #Normal
            m.log("\nat!pcvoltlimits=")
            m.at.any.send_cmd( 'at!pcvoltlimits='+str(int(volt)+200)+','+str(int(volt)+100)+','+str(int(volt)-100)+','+str(int(volt)-200)+','+str(int(volt)-300)+'\r')
            m.at.any.waitn_match_resp( ["*\r\nOK\r\n"], 4000)
            m.log("\nReset module:")
            m.at.any.send_cmd( "AT!RESET\r\n")
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 2000)
            m.at.any.reopen( 30000)
            m.at.any.sleep(10000)
            m.log("\nCancel Echo:")
            m.at.any.send_cmd( "ATE0\r\n")
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 2000)
            m.at.any.send_cmd( 'AT!UNLOCK="A710"\r')
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 5000)
            m.at.any.send_cmd( 'at!pcvolt?\r')
            m.at.any.waitn_match_resp( ['*\r\nVolt state: Normal\r\n'], 4000)
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 4000)

            #High Critical
            m.log("\nat!pcvoltlimits=")
            m.at.any.send_cmd( 'at!pcvoltlimits='+str(int(volt)-100)+','+str(int(volt)-200)+','+str(int(volt)-300)+','+str(int(volt)-400)+','+str(int(volt)-500)+'\r')
            m.at.any.waitn_match_resp( ["*\r\nOK\r\n"], 4000)
            m.log("\nReset module:")
            m.at.any.send_cmd( "AT!RESET\r\n")
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 2000)
            m.at.any.reopen( 30000)
            m.at.any.sleep(10000)
            m.log("\nCancel Echo:")
            m.at.any.send_cmd( "ATE0\r\n")
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 2000)
            m.at.any.send_cmd( 'AT!UNLOCK="A710"\r')
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 5000)
            m.at.any.send_cmd( 'at!pcvolt?\r')
            m.at.any.waitn_match_resp( ['*\r\nVolt state: High Critical\r\n'], 4000)
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 4000)

            #restore
            m.log("\nat!pcvoltlimits=")
            m.at.any.send_cmd( 'at!pcvoltlimits='+hi_crit+','+hi_norm+','+lo_norm+','+lo_warn+','+lo_crit+'\r')
            m.at.any.waitn_match_resp( ["*\r\nOK\r\n"], 4000)
            m.log("\nReset module:")
            m.at.any.send_cmd( "AT!RESET\r\n")
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 2000)
            m.at.any.reopen( 30000)
            m.at.any.sleep(10000)
            m.log("\nCancel Echo:")
            m.at.any.send_cmd( "ATE0\r\n")
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 2000)
            m.at.any.send_cmd( 'AT!UNLOCK="A710"\r')
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 5000)

            m.at.any.send_cmd( 'at!pcvoltlimits?\r')
            m.at.any.waitn_match_resp( ['*\r\nOK\r\n'], 4000)

        m.log("\n----- Test Body End -----\n")
        m.log("\n***************************************************************\n")

    @report.step("[Stage] <Restore-Module>")
    def restore(self, m):
        m.at.any.send_cmd( "AT&F;&W\r")
        m.at.any.waitn_match_resp( ["*\r\nOK\r\n"], 4000)
        out_of_class_function(m)


    @report.story("Volt")
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

        m.log("\n>> Welcome use ACIS ! ^_^")
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
            raise e

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
