from acis_slave_at_testplan_generator import Slave_at_testplan_prepare
from acis_slave_qmi_testplan_generator import Slave_QMI_testplan_prepare
from acis_slave_envs_parser import Slave_envs_parser


slave_test_envs = Slave_envs_parser()

if slave_test_envs.enable_qmi_test():
    print("start qmi test")
    test_plan = Slave_QMI_testplan_prepare()
    test_plan.push_testapp_to_dut()
    test_plan.push_config_to_dut()
else:
    test_plan = Slave_at_testplan_prepare()
    test_plan.search_case()
    test_plan.create_dynamic_cfg()

if slave_test_envs.enable_update_fw():
    test_plan.set_fw_image_file()
    test_plan.fw_image_update()


test_plan.create_auto_generate_script_directory()
test_plan.create_pytest_format_script()

test_plan.run_pytest()


