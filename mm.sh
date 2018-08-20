#! /bin/bash

rm -rf ./Dresult/*
pytest -s testcases/ --alluredir ./Dresult/
allure generate ./Dresult -o ./Dreport --clean
