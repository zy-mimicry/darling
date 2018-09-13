import pytest
import allure
from ..report import report

"""
Now, please don't care the package imported.
Later, only import 'darling' package for test
"""


@report.epic("Driver")
@report.feature("Driver Misc ADC Test")
@report.link("https://issues.sierrawireless.com/browse/QTI9X28-4442", name="__TestCaseInitLinks__: ADC")
class DarlingDriverMiscADC():

    @report.link("https://issues.sierrawireless.com/browse/QTI9X28-4440", name = "Gerrit: Fuck here")
    @report.link("https://issues.sierrawireless.com/browse/QTI9X28-4443", name = "Gerrit: list")
    @report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440",name = "JIRA: DACIS")
    @report.story("This is a entry for test2.")
    #@pytest.mark.run(order=2)
    @report.order(order=2)
    def darling_must_late(self):
        """
        This is a description
        """
        print("I'm late.")


    @report.step("This is a step for test.")
    def adc_test_case(self):
        """here is description"""
        print("hello step.")


    @report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440","127.0.0.1:8000")
    @report.story("This is a entry for test.")
    @report.order(order=1)
    def darling_entry(self, mydarling):
        """
        The test entrance.

        Please descript more information for this testcase.

        balabala....

        For example:
        ADC test information should be here.

        """
        darling = mydarling(__file__,
                            logger_name = 'DACIS.Driver.ADC',
                            mail_to  = 'rzheng@sierrawireless.com',
                            port_names = [
                                'pi-slave-01..AT',
                                'pi-slave-02..ADB',
                            ])
        darling.log(">> Darling! ^_^")
        darling.log(darling.at.whoami())

        darling.at.show_conf()
        darling.adb.show_conf()

        self.adc_test_case()
