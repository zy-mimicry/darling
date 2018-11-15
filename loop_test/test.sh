#! /bin/bash

export PYTHONPATH=/mnt/sda2/rzheng/__mzPython__/self/darling
export ACIS_DIFF=1234
export REPORT_PATH=/mnt/sda2/rzheng/__mzPython__/self/darling/loop_test/log
export PLATFORM=9X28

rm -rf ./Dresult/*

pytest -s ACIS_TESTCASES/ --alluredir ./Dresult/

#allure generate ./Dresult -o ./Dreport --clean
