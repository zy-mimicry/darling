#!/bin/env python
# _*_ coding: utf-8 _*_

import os, sys
import time
import serial
import VarGlobal 
from output import *
from datetime          import datetime
from acis_at           import *



# read all files(include subdir) from a directory
def readDir(dirPath):
    if os.name == "nt":
        if dirPath[-1] == '\\':
            dirPath = dirPath[:-1]
    elif os.name == "posix":
        if dirPath[-1] == '/':
            dirPath = dirPath[:-1]
    else:
        raise Exception("Sorry: no implementation for your platform ('%s') available" % os.name)
        
    allFiles = []
    if os.path.isdir(dirPath):
        fileList = os.listdir(dirPath)
        for f in fileList:
            if os.name == "nt":
                f = dirPath+'\\'+f
            elif os.name == "posix":
                f = dirPath+'/'+f
            else:
                raise Exception("Sorry: no implementation for your platform ('%s') available" % os.name)
            if os.path.isdir(f):
                subFiles = readDir(f)
                allFiles = subFiles + allFiles 
            else:
                allFiles.append(f)
        return allFiles
    else:
        return 'Error,not a dir'

def list_python_program_in_dir(dir):
    python_program = []
    files_in_dir = readDir(dir)
    
    if files_in_dir == 'Error,not a dir':
        return python_program

    for file in files_in_dir:
        if os.path.isfile(file):
            if file[-3:] == '.py':
                python_program.append(file)
            else:
                VarGlobal.SUMMARY_LOGGING.write("Message: The indicated test file name is not .py")
    return python_program

def run(config, test_project, log_path, files): 
    "this method executes the tests cases the one after the others"
    # check the logs directory exit or not, if doesn't this directory, create it.
    if os.path.isdir(log_path) == False:
        os.makedirs(log_path)
    
    if test_project:
        # Set the summary logger object, to log the summary result of all test cases.
        file_time_stamp = time.strftime("__%Y_%m_%d__%H_%M_%S", time.localtime())

        if os.name == "nt":
            test_summary_log = log_path + "\\" + test_project + "_summary" + file_time_stamp + ".log"
            test_summary_log = test_summary_log.replace('\\', '\\\\')
        elif os.name == "posix":
            test_summary_log = log_path + "/" + test_project + "_summary" + file_time_stamp +".log"
        else:
            raise Exception("Sorry: no implementation for your platform ('%s') available" % os.name)
        VarGlobal.SUMMARY_LOGGING.addHandler(test_summary_log)

    # For test report
    VarGlobal.numOfTest = 0.0
    VarGlobal.numOfSuccessfulTest = 0.0 
    VarGlobal.numOfFailedTest = 0.0
    
    # Load the config file
    VarGlobal.SUMMARY_LOGGING.write('CONFIG FILE: %s\n' %config)
    
    try:
        #execute config file content
        exec(compile(open(config).read(), config, 'exec'))
    except IOError:
        VarGlobal.SUMMARY_LOGGING.write("MESSAGE: Error! The config file don't exist.")

    # Traverse all files and find all python program
    test_cases = []
    for file in files:
        if os.path.isfile(file):
            if file[-3:] == '.py':
                test_cases.append(file)
            else:
                VarGlobal.SUMMARY_LOGGING.write("Message: The indicated test file name is not .py")
        elif os.path.isdir(file):
            test_cases = test_cases + list_python_program_in_dir(file)
        else:
            VarGlobal.SUMMARY_LOGGING.write("Message: The indicated test (file or directory) %s don't exist."%test)

    VarGlobal.SUMMARY_LOGGING.write("**********************************************************************")
    VarGlobal.SUMMARY_LOGGING.write("                              Start the Test                          ")
    VarGlobal.SUMMARY_LOGGING.write("  ------------------------------------------------------------------  ")
    
    #run all python script
    for test in test_cases:
        test_case_name = os.path.basename(test)[:-3]   # test_case_name
        logtimestamp = time.strftime("%Y_%m_%d__%H_%M_%S", time.localtime())
        VarGlobal.SUMMARY_LOGGING.write(time.strftime("***********("+logtimestamp+")" + " Start " + test_case_name + "***********"))
        
        # create a test log for a single case
        if os.name == 'nt':
            test_case_log_timestamp = log_path + "\\" + test_case_name + "_" + logtimestamp + ".log"
            test_case_log = log_path + "\\" + test_case_name + ".log"
            test_case_log = test_case_log.replace('\\', '\\\\')
            test_case_log_timestamp = test_case_log_timestamp.replace('\\', '\\\\')
        elif os.name == 'posix':
            test_case_log_timestamp = log_path + "/" + test_case_name + "_" + logtimestamp +".log"
            test_case_log = log_path + '/' + test_case_name + '.log'
        else:
            raise Exception("Sorry: no implementation for your platform ('%s') available" % os.name)
        if os.path.isfile(test_case_log):
            os.remove(test_case_log)
        VarGlobal.SUMMARY_LOGGING.write("LOG: " + test_case_log)
        VarGlobal.TEST_CASE_LOGGING.addHandler(test_case_log)
        VarGlobal.TEST_CASE_LOGGING.addHandler(test_case_log_timestamp)
        VarGlobal.statOfItem = 'OK'

        VarGlobal.SUMMARY_LOGGING.write( "FILE: " + test)

        # execute the test
        try:
            #execute test case file content (as a source Linux)
            exec(compile(open(test).read(), test, 'exec'))  # detecte de NameError dans la fonction qui fait l'appel.
        except Exception as e:
            VarGlobal.statOfItem = 'NOK'
            acis_print(e)

        # For process window at the end of the test execution
        VarGlobal.numOfTest += 1.0
        if VarGlobal.statOfItem == 'OK':
            VarGlobal.numOfSuccessfulTest += 1.0
            logtimestamp = time.strftime("%Y_%m_%d__%H_%M_%S", time.localtime())
            VarGlobal.SUMMARY_LOGGING.write(time.strftime("***********("+logtimestamp+")" + " End " + test_case_name + " Passed***********"))
            VarGlobal.SUMMARY_LOGGING.write("")
        else:
            VarGlobal.numOfFailedTest += 1.0
            logtimestamp = time.strftime("%Y_%m_%d__%H_%M_%S", time.localtime())
            VarGlobal.SUMMARY_LOGGING.write(time.strftime("***********("+logtimestamp+")" + " End " + test_case_name + " Failed***********"))
            VarGlobal.SUMMARY_LOGGING.write("")
        VarGlobal.TEST_CASE_LOGGING.removeHandler(test_case_log)
        VarGlobal.TEST_CASE_LOGGING.removeHandler(test_case_log_timestamp)
    # Sumarrize the test results
    VarGlobal.SUMMARY_LOGGING.write("  ------------------------------------------------------------------  ")
    VarGlobal.SUMMARY_LOGGING.write("Total test cases: %d, Total Passed cases: %d, Total Failed cases: %d" %(VarGlobal.numOfTest, VarGlobal.numOfSuccessfulTest, VarGlobal.numOfFailedTest))
    VarGlobal.SUMMARY_LOGGING.write("                              Finished the Test                          ")
    VarGlobal.SUMMARY_LOGGING.write("**********************************************************************")
    if test_project:
        VarGlobal.SUMMARY_LOGGING.removeHandler(test_summary_log)


def main(argv):
    cfg = ''
    log_fullpath = ''
    test_project_name = ''
    help = False
    list_test = []
    # Get current directory and enter into log directory
    current_directory = os.getcwd()

    # Set the log path
    if os.name == "nt":
        log_fullpath = current_directory+'\logs'
    elif os.name == "posix":
        log_fullpath = current_directory+'/logs'
    else:
        raise Exception("Sorry: no implementation for your platform ('%s') available" % os.name)

    while argv:
        if argv[0] == '-cfg':
            cfg = argv[1]
            argv = argv[2:]
        elif argv[0] == '-logpath':
            log_fullpath = argv[1]
            argv = argv[2:]
        elif argv[0] == '-testproject':
            test_project_name = argv[1]
            argv = argv[2:]
        elif argv[0] == '-h':
            help = True
            argv = argv[1:]
        elif argv[0][0] == '-':
            print("Error: There is not the parameter %s." % argv[0])
            sys.exit()
        else:
            list_test.append(argv[0])
            argv = argv[1:]

    run(cfg, test_project_name, log_fullpath, list_test)


main(sys.argv[1:])
