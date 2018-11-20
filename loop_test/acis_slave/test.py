#! /usr/bin/env python3

test_string = """\
# _*_ coding:utf-8 _*_

import pytest
import allure
from acis.core.report import report
import os

@report.fixture(scope="module")
def m(request, misc):
    mz =  misc(__file__,
               logger_name = 'ACIS.QMI.APP.TEST',
               mail_to     = 'rzheng@sierrawireless.com',
               port_names  = [
                   'AT..any',
                   'ADB..any',
               ])

    mz.test_ID = os.path.basename(__file__.split('.')[0])
    mz.errors = {{}}
    mz.flags  = []
    def module_upload_log():
        allure.attach.file(source = mz.which_log,
                           attachment_type = allure.attachment_type.TEXT)
        if mz.at: mz.at.closeall()
    request.addfinalizer(module_upload_log)
    return mz


@report.epic("QMI")
@report.feature("APP")
class ACISQMIAppTest():
    \"\"\"
    Something you want to descript for this test. (can't display)
    \"\"\"

    @report.step("[Stage] <Pre-Condition>")
    def pre(self, m):
        m.log("PUSH : testapp to DUT.")
        m.adb.any.send_cmd("push  {TEST_APP} /tmp/testQaQmi")

        m.log("PUSH : testapp config to DUT.")
        m.adb.any.send_cmd("push {CONFIG_FILE} /tmp")


    @report.step("[Stage] <Real-Test-Body>")
    def body(self, m):

        m.log("***********test {CASENAME} start*************")

        serial_id = m.adb.conf['any']['serial_id']

        returninfo = os.popen('adb -s {{SERIAL_ID}}) shell "cd /tmp&&./testQaQmi -t {CASENAME}"'.format(SERIAL_ID = serial_id))
        while 1:
            try:
                line = returninfo.readline()
            except :
                continue
            if len(line) <= 0:
                break

        os.popen('adb -s {{SERIAL_ID}} pull /tmp/te_log/{CASENAME}.log {LOG_PATH}/{CASENAME}.log'.format(SERIAL_ID = serial_id))
        time.sleep(2)

        fd = open('{LOG_PATH}/{CASENAME}.log', 'r')
        log_read = fd.read()
        if re.findall(r'>>>>>>>RESULT:Passed:\d+/\d+=100%', log_read):
            test_result = True
        else:
            test_result = False

        print(log_read)
        m.adb.any.send_cmd("'cd /tmp&&rm /tmp/te_log/* -rf'")

        print("***********test {CASENAME} end*************\\n")

        fd.close()

    @report.step("[Stage] <Restore-Module>")
    def restore(self, m):


    @report.story("QMI APP TEST")
    @pytest.mark.run(order=1)
    def acis_mstage_entrance(self, m):
        \"\"\"
        TODO: QMI APP TEST.
        \"\"\"

        m.log("\\n>> Welcome use ACIS ! ^_^")

        try:
            try:
                self.pre(m)                    # << Stage | pre
            except Exception as e:
                m.log("<Pre-Stage-Exception> reason: {{}}".format(e))
                m.flags.append('pre')
                m.errors['pre'] = e
                raise e
            self.body(m)                       # << Stage | body
        except Exception as e:
            if not m.flags :
                m.log("<Body-Stage-Exception> reason: {{}}".format(e))
                m.flags.append('body')
                m.errors['body'] = e

        try:
            self.restore(m)                    # << Stage | restore
        except Exception as e:
            m.log("<Restore-Stage-Exception> reason: {{}}".format(e))
            m.flags.append('restore')
            m.errors['restore'] = e

        if m.flags:
            m.log("\\n\\n  <ACIS Exception Stack Information>\\n")
            for f in m.flags:
                m.log("--- {{}} stack info ---\\n{{}}\\n".format(f, m.errors[f]))
            m.log("\\nTESTCASE:[{{}}] Result:[{{}}]\\n".format(m.test_ID, "FAIL"))
            raise Exception("\\n\\n <ACIS Test Exception, Please check stack information.>\\n")
        else:
            m.log("\\nTESTCASE:[{{}}] Result:[{{}}]\\n".format(m.test_ID, "PASS"))
"""

print(test_string)
print("=" * 100)

ss = "{{name}}, {log}"

print(ss.format(name = 'mm', log = 'hello'))

print(test_string.format(TEST_APP = "test app", CONFIG_FILE = "config file", LOG_PATH = 'log_path', CASENAME = "case name"))
