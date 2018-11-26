import pytest
import allure
from acis.core.report import report
#import os

"""
"""

@report.fixture(scope="module")
def m(request, misc):
    mz =  misc(__file__,
               logger_name = 'ACIS.SYSTEM.RESET.LINUX',
               mail_to     = 'swi@sierrawireless.com',
               port_names  = [
                   # 'AT..master',
                   # 'AT..slave',
                   # 'ADB..master',
                   # 'ADB..slave',
                   'AT..any',
                   'ADB..any',
               ])

    #mz.test_ID = os.path.basename(__file__.split('.')[0])
    mz.test_ID = __name__
    mz.errors = {}
    mz.flags  = []
    def module_close_AT():
        if mz.at: mz.at.closeall()
        # allure.attach.file(source = mz.which_log,
        #                    attachment_type = allure.attachment_type.TEXT)
    request.addfinalizer(module_close_AT)
    return mz

@report.step("[Stage] < out of class functions>")
def out_of_class_function(m):
    print("Out of class, get 'm' is :{}".format(m))

@report.epic("System") # << should modify
@report.feature("ATcommand") # << should modify
@report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440",name = ">JIRA: ADC Body<")
class ACISsystemReset(): # << should modify
    """
    Something you want to descript for this test. (can't display)
    """

    @report.step("[Stage] <Pre-Condition>")
    def pre(self, m):
        m.log("Stage [pre]")

    @report.step("[Stage] <Real-Test-Body>")
    def body(self, m):
        m.log("Stage [body]")

    @report.step("[Stage] <Restore-Module>")
    def restore(self, m):
        m.log("Stage [restore]")
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

        m.log("\n>> Welcome to use ACIS ! ^_^")
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
                self.restore(m)                    # << Stage | restore
            except Exception as e:
                m.log("<Restore> The restore process should not have an exception.\nBut now NOT,reason:\n{}".format(e))
                m.flags.append('restore')
                m.errors['restore'] = e

            if m.flags:
                m.log("\n\n  <ACIS Exception Stack Information>\n")
                for f in m.flags:
                    m.log("--- {} stack info ---\n{}\n\n".format(f, m.errors[f]))

                m.log("\nTESTCASE:[{}] Result:[{}]\n".format(m.test_ID, "FAIL"))
                allure.attach.file(source = m.which_log, name = __name__ + '.log'
                                   attachment_type = allure.attachment_type.TEXT)
            else:
                m.log("\nTESTCASE:[{}] Result:[{}]\n".format(m.test_ID, "PASS"))
                allure.attach.file(source = m.which_log, name = __name__ + '.log'
                                   attachment_type = allure.attachment_type.TEXT)
