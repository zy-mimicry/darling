from acis.core.report import report

"""
"""

@report.fixture(scope="module")
def m(request, misc):
    """
    __file__    : logging module record log file.
    logger_name : logger namespace of logging module.
    mail_to     : where the mail to be send.
    port_names  : testcase registers ports [AT or ADB ...] from framework.
                : ? master << map to '/etc/udev/rules.d/11-acis.rules' - 'master'
                : ? slave  << map to '/etc/udev/rules.d/11-acis.rules' - 'slave'
                : ? any    << map to '/etc/udev/rules.d/11-acis.rules' - 'master' or 'slave'
                : eg. port_names  = [
                                    'AT..master',
                                    'AT..slave',
                                    'ADB..master',
                                    'ADB..slave',
                                    ]
    """
    mz =  misc(__file__,
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

@report.step("[Stage] < out of class functions>")
def out_of_class_function(m):
    print("Out of class, get 'm' is :{}".format(m))

@report.epic("System") # << should modify
@report.feature("ATcommand") # << should modify
@report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440",name = ">JIRA: ADC Body<")
class ACISsystemReset(): # << should modify

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


    @report.link("https://issues.sierrawireless.com/browse/QTI9X28-4443", name = "=Gerrit: commit 01=")
    @report.story("Volt") # << should modify
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
