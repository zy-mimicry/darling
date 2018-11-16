import pytest
import allure
from acis.core.report import report

"""
Now, please don't care the package imported.
Later, only import 'darling' package for test
"""

@report.fixture(scope="module")
def m(darling_misc):
    return darling_misc(__file__,
                        logger_name = 'ACIS.System.demo',
                        mail_to     = 'rzheng@sierrawireless.com',
                        port_names  = [
                            'AT..master',
                            'AT..slave',
                            'ADB..master',
                            'ADB..slave',
                        ])


@report.epic("System")
@report.feature("System Reset Poweroff")
@report.link("https://issues.sierrawireless.com/browse/QTI9X28-4442", name=">JIRA: DACIS<")
class ACISsystemReset():
    """
    Something you want to descript for this test. (can't display)
    """

    @report.step("body step 01")
    def adc_body_deal_01(self,m):
        m.log("I'm stage 01 << body")

    @report.step("body step 02")
    def adc_body_deal_02(self,m):
        m.log("I'm stage 02 << body")

    @report.step("body step 03")
    def adc_body_deal_03(self,m):
        m.log("I'm stage 03 << body")

    @report.link("https://issues.sierrawireless.com/browse/QTI9X28-4440", name = "=Gerrit: commit 02=")
    @report.link("https://issues.sierrawireless.com/browse/QTI9X28-4443", name = "=Gerrit: commit 01=")
    @report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440",name = ">JIRA: ADC Body<")
    @report.story("DACIS >> maybe test body, crazy...")
    @pytest.mark.run(order=2)
    def acis_mreal_body(self, m):
        """
        This is a description
        """
        self.adc_body_deal_01(m)
        self.adc_body_deal_02(m)
        self.adc_body_deal_03(m)


        # = SagOpen(UART1_COM)
        m.at.master.send_cmd("AT\r")
        m.at.master.waitn_match_resp(["*\r\nOK\r\n"], 4000)

        m.at.master.send_cmd("AT&F;&W\r")
        m.at.master.waitn_match_resp(["*\r\nOK\r\n"], 4000)

        m.at.master.send_cmd("ATE0\r")
        m.at.master.waitn_match_resp(["*\r\nOK\r\n"], 4000)

        m.at.master.send_cmd("AT+CMEE=1\r\n")
        m.at.master.waitn_match_resp(['*\r\nOK\r\n'], 2000)

        m.at.master.send_cmd('ATI3\r')
        m.at.master.waitn_match_resp(['*\r\n*\r\n\r\nOK\r\n'], 4000)

        m.at.master.send_cmd('AT!PACKAGE?\r')
        m.at.master.waitn_match_resp(['*\r\n*\r\nOK\r\n'], 4000)

        m.at.master.send_cmd('ATI8\r')
        m.at.master.waitn_match_resp(['*\r\n*\r\n\r\nOK\r\n'], 4000)

        m.at.master.send_cmd('AT!SKU?\r')
        m.at.master.waitn_match_resp(['*\r\n*\r\n\r\nOK\r\n'], 4000)

        m.at.master.send_cmd('AT+GMM\r\n')
        model = m.at.master.wait_resp(["*\r\nOK\r\n"], 5000).split('\r\n')[1].strip()

        # m.at.master.send_cmd('AT+ICCID\r')
        # m.at.master.waitn_match_resp(['*ICCID: *\r\n'], 4000)
        # m.at.master.waitn_match_resp(['\r\nOK\r\n'], 4000)

        m.at.master.send_cmd('AT+WUSLMSK=00000000,0\r\n')
        m.at.master.waitn_match_resp(["*\r\nOK\r\n"], 5000)

        m.at.master.send_cmd('AT+WUSLMSK=00000000,1\r\n')
        m.at.master.waitn_match_resp(["*\r\nOK\r\n"], 5000)

        m.at.master.send_cmd('AT!UNLOCK="A710"\r')
        m.at.master.waitn_match_resp(['*\r\nOK\r\n'], 5000)

        m.at.master.send_cmd( "AT!GCCLR\r")
        m.at.master.waitn_match_resp( ["*\r\nCrash data cleared\r\n"], 4000)
        m.at.master.waitn_match_resp( ["\r\nOK\r\n"], 4000)

        m.at.master.send_cmd("AT!EROPTION?\r\n")
        resp = m.at.master.wait_resp(['*\r\nOK\r\n'], 2000)
        if "Reset" in resp:
            m.at.master.send_cmd("AT!EROPTION=0,1\r\n")
            m.at.master.waitn_match_resp(['*\r\nOK\r\n'], 2000)

            m.at.master.send_cmd("AT!RESET\r\n")
            m.at.master.waitn_match_resp(['\r\nOK\r\n'], 2000)
            m.at.master.sleep(C_TIMER_MEDIUM)

        m.at.master.send_cmd("ATE0\r\n")
        m.at.master.waitn_match_resp(['*\r\nOK\r\n'], 2000)


    @report.step("pre step 01")
    def adc_pre_deal_01(self, m):
        m.log("I'm stage 01 << pre")

    @report.step("pre step 02")
    def adc_pre_deal_02(self, m):
        m.log("I'm stage 02 << pre")

    @report.step("pre step 03")
    def adc_pre_deal_03(self, m):
        m.log("I'm stage 03 << pre")


    @report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440",name = ">JIRA: ADC Init<")
    @report.story("DACIS >> maybe pre-condition")
    @pytest.mark.run(order=1)
    def acis_mstage_entrance(self, m):
        """
        The test entrance.

        Please descript more information for this testcase.

        balabala....

        For example:
        ADC test information should be here.

        """

        m.log(">> Darling! ^_^")

        self.adc_pre_deal_01(m)
        self.adc_pre_deal_02(m)
        self.adc_pre_deal_03(m)

    @report.story("DACIS >> maybe log-condition")
    @pytest.mark.run(order=4)
    def acis_lstage_entrance(self, m):
        allure.attach('/home/jenkins/hello.txt', attachment_type = allure.attachment_type.TEXT)
        allure.attach.file(source = '/home/jenkins/hello.txt', attachment_type = allure.attachment_type.TEXT)

    @report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440",name = ">JIRA: ADC Init<")
    @report.story("DACIS >> maybe dance finished")
    @pytest.mark.run(order=3)
    def acis_mstage_finish(self, m):

        self.adc_late_deal_01(m)
        self.adc_late_deal_02(m)
        self.adc_late_deal_03(m)

    @report.step("late step 01")
    def adc_late_deal_01(self, m):
        m.log("I'm stage 01 << late")

    @report.step("late step 02")
    def adc_late_deal_02(self, m):
        m.log("I'm stage 02 << late")

    @report.step("late step 03")
    def adc_late_deal_03(self, m):
        m.log("I'm stage 03 << late")


# @pytest.mark.xfail(condition=lambda: True, reason='this test is expecting failure')
# def test_xfail_expected_failure():
#     """this test is an xfail that will be marked as expected failure"""
#     assert False

# @pytest.mark.xfail(condition=lambda: True, reason='this test is expecting failure')
# def test_xfail_unexpected_pass():
#     """this test is an xfail that will be marked as unexpected success"""
#     assert True


# def test_success():
#     """this test succeeds"""
#     assert True


# def test_failure():
#     """this test fails"""
#     assert False


# def test_skip():
#     """this test is skipped"""
#     pytest.skip('for a reason!')


# def test_broken():
#     raise Exception('oops')


# @pytest.mark.skipif('2 + 2 != 5', reason='This test is skipped by a triggered condition in @pytest.mark.skipif')
# def test_skip_by_triggered_condition():
#     pass

