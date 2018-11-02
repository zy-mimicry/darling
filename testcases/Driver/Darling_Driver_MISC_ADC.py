import pytest
import allure
from ..report import report

"""
Now, please don't care the package imported.
Later, only import 'darling' package for test
"""

@report.fixture(scope="function")
def mydarling(darling_misc):
    return darling_misc(__file__,
                        logger_name = 'DACIS.Driver.ADC',
                        mail_to     = 'rzheng@sierrawireless.com',
                        port_names  = [
                            'pi-slave-01..AT',
                            'pi-slave-02..ADB',
                        ])


@report.epic("Driver")
@report.feature("Driver Misc ADC")
@report.link("https://issues.sierrawireless.com/browse/QTI9X28-4442", name=">JIRA: DACIS<")
class DarlingDriverMiscADC():
    """
    Something you want to descript for this test. (can't display)
    """

    @report.step("body step 01")
    def adc_body_deal_01(self,mydarling):
        mydarling.log("I'm stage 02 << body")

    @report.step("body step 02")
    def adc_body_deal_02(self,mydarling):
        mydarling.log("I'm stage 02 << body")

    @report.step("body step 03")
    def adc_body_deal_03(self,mydarling):
        mydarling.log("I'm stage 03 << body")

    @report.link("https://issues.sierrawireless.com/browse/QTI9X28-4440", name = "=Gerrit: commit 02=")
    @report.link("https://issues.sierrawireless.com/browse/QTI9X28-4443", name = "=Gerrit: commit 01=")
    @report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440",name = ">JIRA: ADC Body<")
    @report.story("DACIS >> maybe test body, crazy...")
    @report.order(order=2)
    def darling_real_body(self, mydarling):
        """
        This is a description
        """
        self.adc_body_deal_01(mydarling)
        self.adc_body_deal_02(mydarling)
        self.adc_body_deal_03(mydarling)


    @report.step("pre step 01")
    def adc_pre_deal_01(self, mydarling):
        mydarling.log("I'm stage 02 << pre")

    @report.step("pre step 02")
    def adc_pre_deal_02(self, mydarling):
        mydarling.log("I'm stage 02 << pre")

    @report.step("pre step 03")
    def adc_pre_deal_03(self, mydarling):
        mydarling.log("I'm stage 03 << pre")


    @report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440",name = ">JIRA: ADC Init<")
    @report.story("DACIS >> maybe pre-condition")
    @report.order(order=1)
    def darling_stage_entrance(self, mydarling):
        """
        The test entrance.

        Please descript more information for this testcase.

        balabala....

        For example:
        ADC test information should be here.

        """

        mydarling.log(">> Darling! ^_^")
        mydarling.log(mydarling.at.whoami())

        mydarling.at.show_conf()
        mydarling.adb.show_conf()

        self.adc_pre_deal_01(mydarling)
        self.adc_pre_deal_02(mydarling)
        self.adc_pre_deal_03(mydarling)


    @report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440",name = ">JIRA: ADC Init<")
    @report.story("DACIS >> maybe dance finished")
    @report.order(order=3)
    def darling_stage_finish(self, mydarling):

        self.adc_late_deal_01(mydarling)
        self.adc_late_deal_02(mydarling)
        self.adc_late_deal_03(mydarling)

    @report.step("late step 01")
    def adc_late_deal_01(self, mydarling):
        mydarling.log("I'm stage 02 << late")

    @report.step("late step 02")
    def adc_late_deal_02(self, mydarling):
        mydarling.log("I'm stage 02 << late")

    @report.step("late step 03")
    def adc_late_deal_03(self, mydarling):
        mydarling.log("I'm stage 03 << late")
