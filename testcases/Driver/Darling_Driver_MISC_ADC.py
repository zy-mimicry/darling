import pytest
import allure
from ..report import report



@report.epic("Driver")
@report.feature("Driver Misc ADC Test")
class DarlingDriverMiscADC():
    """
    helldfjlskjfklsjd
    """

    @report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440","127.0.0.1:8000")
    @report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440",name = "JIRA: DACIS")
    @report.story("This is a entry for test.")
    @pytest.mark.run(order=2)
    def darling_must_late(self):
        print("I'm late.")

    @report.step("This is a step for test.")
    def adc_test_case(self):
        """here is description"""
        print("hello step.")

    @report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440","127.0.0.1:8000")
    @report.story("This is a entry for test.")
    @pytest.mark.run(order=1)
    def darling_entry(self):
        """
        thisjfksjdfkljskljfljsdlfjksdjf
        """
        print("hello story.")
        self.adc_test_case()
        self.mm()
        self.cc()

    @report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440","127.0.0.1:8000")
    @report.step("This is a step for test mm.")
    def mm(self):
        print("hello mm")

    @report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440","127.0.0.1:8000")
    @report.step("This is a step for test cc.")
    def cc(self):
        print("hello cc")


    pass


