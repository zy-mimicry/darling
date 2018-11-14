#! /usr/bin/env python
# coding=utf-8

"""

"""

# Encoding Dictionary.
from .encoding_format import (
    ascii2hexstring_printable_revert,
    ascii2hexstring_printable_tempsymbol,
    ascii2hexstring_extended,
    ascii2hexstring_printable,
    ascii2hexstring_symbol,
    ascii_symbol)

import time, re, sys, datetime
import platform, fnmatch
import serial
import configparser



class _AT():

    def __init__(self, conf):

        self.conf = conf

        # AT Send receive time stamp
        self.SndRcvTimestamp = True
        self.RcvTimespent = True

        #Variable for status
        self.statOfItem = ''

        # Variable for log
        self.numOfSuccessfulResponse = 0.0

        #list of opened COM ports
        self.uartbuffer = {}

        #self.open()

        print("_AT instance init.")

    def info(self):
        print("I'm _AT")

    def open(self,
             port=None,
             baudrate=115200,
             bytesize=8,
             parity='N',
             stopbits=1,
             rtscts=False,
             OpenPortTimeout=2000,
             timeout=1,
             dsrdtr=False,
             xonxoff=False,
             interCharTimeout=None,
             write_timeout=None):

        # "goal of the method : This function opens the serial port"
        # "INPUT : port : string including the COM port (e.g. COM9), for linux system, this is usbport(e.g. 1-1.4:1.3)"
        # "        baudrate : communication speed"
        # "        OpenPortTimeout: Set a open port timeout value"
        # "        timeout : Set a read timeout value."
        # "        DTRDSR : Enable hardware (DSR/DTR) flow control."
        # "        rtscts : enable RTS/CTS flow control"
        # "        xonxoff : enable software flow control"
        # "        interCharTimeout : Inter-character timeout, None to disable"
        # "OUTPUT : COM port object"

        # for linux system AT port will be changed random, so we use the usbport(this is fixed) to find the AT port every time.
        # if os.name == 'posix':
        #     start_time = datetime.now()
        #     while 1:
        #         try:
        #             ttyusbcom = AcisGetUsbttyport(port)
        #             #SafePrint(None, None, "ttyUSB com port : %s"%ttyusbcom)
        #             diff_time = datetime.now() - start_time
        #             diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
        #             OpenPortTimeout = OpenPortTimeout - diff_time_ms
        #             break
        #         except Exception as e:
        #             #SafePrint(None, None, "Find ttyUSB com port failed : %s"%e)
        #             time.sleep(1)
        #             sys.stdout.write("*")
        #             time.sleep(1)
        #             sys.stdout.write("*")
        #             flag_linebreak = 1
        #             # Count timeout
        #         diff_time = datetime.now() - start_time
        #         diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
        #         if diff_time_ms > OpenPortTimeout:
        #             if flag_linebreak:
        #                 #acis_print("")
        #                 #acis_print(port+" - port not found"+" <"+str(timeout)+" ms")
        #             raise Exception(port+"-port not found"+" <"+str(timeout)+" ms")
        #         usbport2ttycom[port] = ttyusbcom
        #         port = ttyusbcom


        # validate parameter - rtscts
        flowcontrol = "Hardware"
        if type(rtscts) == type("string"):
            if rtscts not in ["Hardware", "None"]:
                print("Invalid parameter for AcisOpen() - rtscts")
                print("Option:")
                print("\"Hardware\"", "\"None\"")
                print("")
                rtscts = 1
                flowcontrol = "Hardware"
            if rtscts == "Hardware":
                rtscts = 1
                flowcontrol = "Hardware"
            if rtscts == "None":
                rtscts = 0
                flowcontrol = "None"
        self.detect_port(port,OpenPortTimeout, "nologmsg")
        try:
            hCom=None
            hCom = serial.Serial(port,
                                 baudrate,
                                 bytesize,
                                 parity,
                                 stopbits,
                                 timeout,
                                 xonxoff,
                                 rtscts,
                                 write_timeout,
                                 dsrdtr,
                                 interCharTimeout)
            #add the new opened COM port to the list including all opened COM port
            #list_hCom.append(hCom)
            print(hCom, "OPEN: Open the "+hCom.port+" @"+str(baudrate)+" "+str(bytesize)+str(parity)+str(stopbits)+" "+str(flowcontrol))
            time.sleep(1)

            self.uartbuffer[hCom.port] = ""

            return hCom

        except serial.SerialException as val:
            print(val)
            if ("%s"%val).startswith("could not open port "):
                print(None, None, "ERROR Could not open COM%d !"%(port))
                print("hCom" + str(hCom))
            else:
                print(None, None, "ERROR : %s"%val)

        except AttributeError:
            print(None, None, "OPEN: Busy for "+hCom.port+"!")

    def detect_port(self, port, timeout=2000, logmsg="logmsg"):

        start_time = datetime.now()
        flag_linebreak = 0
        while 1:
            try:
                s = serial.Serial(port,
                                  baudrate=115200,
                                  bytesize=8,
                                  parity='N',
                                  stopbits=1,
                                  timeout=1,
                                  xonxoff=False,
                                  rtscts=False,
                                  writeTimeout=None,
                                  dsrdtr=False)
                if logmsg=="logmsg":
                    if flag_linebreak:
                        print("")
                    print(port+" - port found")
                # display time spent in receive
                diff_time = datetime.now() - start_time
                diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
                if logmsg=="logmsg":
                    print(" <"+str(timeout)+" @"+str(diff_time_ms)+"ms")
                s.close()
                break
            except serial.SerialException:
                pass
            time.sleep(1)
            sys.stdout.write("*")
            flag_linebreak = 1
            # Count timeout
            diff_time = datetime.now() - start_time
            diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
            if diff_time_ms > timeout:
                if logmsg=="logmsg":
                    if flag_linebreak:
                        print("")
                    print(port+" - port not found"+" <"+str(timeout)+" ms")
                break

    def sleep(self, millisecond, silent=False):
        "goal of the method : this method sleep during x milliseconds"
        "INPUT : milliseconds (ms), sleep duration"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : none"
        try:
            if not(silent):
                print(None, None, "SLEEP: Start sleep for %d milliseconds" % millisecond)
            time.sleep(millisecond/1000.0)
            if not(silent):
                print(None, None, "SLEEP: End sleep")
        except SystemExit:
            raise SystemExit
        except Exception as e:
            print(e)

    def close(self, hCom):
        "goal of the method : This method closes a COM port"
        "INPUT : hCom : COM port object"
        "OUTPUT : none"
        try:
        #print "close com port ", hCom.port
            #hCom.setDTR(0)
            #hCom.setDTR(1)
            #ComPort = hCom.port
            hCom.close()
            #list_hCom.remove(hCom)

            # for linux system, delete the usbport in dict usbport2ttycom.
            # if os.name == 'posix':
            #     for key, value in usbport2ttycom.items():
            #         if value == ComPort:
            #             find_usbport = key
            #             break
            #     usbport2ttycom.pop(find_usbport)

            print(None, hCom, "CLOSE: Close the "+hCom.port)
        except Exception as e:
            print(e)
            print(None, hCom, "CLOSE: Error for "+hCom.port)

    def timeDisplay(self, dt = None):
        "Display the time ; if dt is empty retrun actual date time under format, otherless return dt under format"
        "INPUT  : (optionnal) dt : date Time"
        "OUTPUT : date Time under format hh:mm:ss:???"
        if dt == None:
            dt = datetime.now()
        return "(%0.2d:%0.2d:%0.2d:%0.3d)"%(dt.hour, dt.minute, dt.second, dt.microsecond/1000)

    def send_cmd(hCom, cmd, printmode="symbol"):
        "goal of the method : this method sends an AT command on a COM port"
        "INPUT : hCom : COM port object"
        "        cmd : AT command to send"
        "OUTPUT : none"
        hCom.write(cmd.encode('utf-8'))
        time.sleep(0.1)

        timestamp = self.timeDisplay()+" "
        LogMsg = timestamp+"Snd COM "+ hCom.port+" ["+self.ascii2print(cmd,printmode)+"]"
        print(LogMsg)

    def ascii2print(self, inputstring, mode="symbol"):

        if mode=="symbol":
            # direct convert value to string by Dictionary >> very fast
            string_raw = inputstring
            # convert raw data to <symbol> for \x00 - \x1F
            #                     <0x??>   for \x80 - \xFF
            for key, value in ascii_symbol.items():
                string_raw = string_raw.replace(key,value)
                outputstring = string_raw

        if mode=="hexstring":
            # direct convert value to string by Dictionary >> very fast
            string_raw = inputstring
            for key, value in ascii2hexstring_printable_tempsymbol.items():
                string_raw = string_raw.replace(key,value)
            for key, value in ascii2hexstring_printable_revert.items():
                string_raw = string_raw.replace(key,value)
            for key, value in ascii2hexstring_symbol.items():
                string_raw = string_raw.replace(key,value)
            for key, value in ascii2hexstring_extended.items():
                string_raw = string_raw.replace(key,value)
                outputstring = string_raw

        if mode=="raw":
            string_raw = inputstring
            # convert <symbol> to raw data
            for key, value in ascii_symbol.items():
                string_raw = string_raw.replace(value,key)
                # convert <0x??> to raw data
            for key, value in ascii2hexstring_printable.items():
                string_raw = string_raw.replace(value,key)
            for key, value in ascii2hexstring_symbol.items():
                string_raw = string_raw.replace(value,key)
            for key, value in ascii2hexstring_extended.items():
                string_raw = string_raw.replace(value,key)
                outputstring = string_raw

        return outputstring

    def clean_buffer(self,hCom):
            "goal of the method : this method clears the input buffer of hCom COM port instance"
            "INPUT : hCom, COM port instance"
            "OUTPUT : none"
            try:
                    hCom.flushInput()

            except SystemExit:
                    raise SystemExit

            except Exception as e:
                    hCom.close()
                    print("CLEAR_BUFFER: Error!")
                    print(e)

    def waitn_match_resp(self,hCom, waitpattern, timeout, condition="wildcard", update_result="critical", log_msg="logmsg", printmode="symbol"):
        "goal of the method : combine AcisWaitResp() and AcisMatchResp()"
        "INPUT : hCom : COM port object"
        "        waitpattern : the matching pattern for the received data"
        "        timeout : timeout value in second"
        "OUTPUT : None"

        #myColor = colorLsit[8]

        # validate parameter - condition
        if condition not in ["wildcard"]:
            print("Invalid parameter for AcisWaitnMatchResp() - condition")
            print("Option:")
            print("\"wildcard\"")
            print("")
            print("AcisWaitnMatchResp() only support \"wildcard\" in \"condition\"")
            print("")
            condition = "wildcard"

        AcisWaitResp_response = self.wait_resp(hCom, waitpattern, timeout, log_msg, printmode)
        match_result = self.match_resp(AcisWaitResp_response, waitpattern, condition, update_result, log_msg, printmode)
        return match_result

    def match_resp(self, resp, keywords, condition="wildcard", update_result="critical", log_msg="logmsg", printmode="symbol"):
        "goal of the method : this method compares the received command to the expected command and Display the comparison result"
        "INPUT :  resp : Response object or a string"
        "         keywords (list) : expected response"
        "         condition : matching condition, 1.wildcard"
        "                                        2.match_all_order"
        "                                        3.match_all_disorder"
        "                                        4.contain_all_order"
        "                                        5.contain_all_disorder"
        "                                        6.contain_anyone"
        "                                        7.not_contain_anyone"
        "         update_result : 1. critical, update result to global variable statOfItem"
        "                         2. not_critical, do nothing for the result"
        "         log_msg : 1. logmsg, print with log message"
        "                   2. debug, print with log and debug message"
        "                   3. nologmsg, print without any message"
        "OUTPUT : Boolean >> True:response matched, False:repsonse mis-matched"

        #myColor = colorLsit[8]

        # If resp is Response() >> assign .tabData to resp
        if type(resp) != type("string"):
            #print "This is not a string"
            resp = resp.tabData

        # If keywords is None >> assign empty string
        if keywords == None:
            keywords = [""]

        # validate parameter - condition
        if condition not in ["wildcard", "match_all_order", "match_all_disorder", "contain_all_order", "contain_all_disorder", "contain_anyone", "not_contain_anyone"]:
            print( "Invalid parameter for AcisMatchResp() - condition")
            print( "Option:" )
            print( "\"wildcard\"", "\"match_all_order\"", "\"match_all_disorder\"", "\"contain_all_order\"", "\"contain_all_disorder\"", "\"contain_anyone\"", "\"not_contain_anyone\"" )
            print( "" )
            condition = "wildcard"

        # validate parameter - update_result
        if update_result not in ["critical", "not_critical"]:
            print("Invalid parameter for AcisMatchResp() - update_result")
            print("Option:")
            print("\"critical\"", "\"not_critical\"")
            print("")
            update_result = "critical"

        # validate parameter - log_msg
        if log_msg not in ["logmsg", "nologmsg", "debug"]:
            print("Invalid parameter for AcisMatchResp() - log_msg")
            print("Option:")
            print("\"logmsg\"", "\"nologmsg\"", "\"debug\"")
            print("")
            log_msg = "logmsg"

        # 1
        # Default - matching with wildcard character
        if condition=="wildcard":
            flag_matchstring = False
            matched = False
            for (each_elem) in keywords:
                receivedResp = resp
                expectedResp = each_elem
                if fnmatch.fnmatchcase(receivedResp, expectedResp):
                    flag_matchstring = True
                    matched = True
                    break

            if matched == 0 :
                if log_msg == "logmsg" or log_msg == "debug":
                    if len(keywords)==1:
                        print("")
                        print("Expected Response: %s" % self.ascii2print(expectedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                        print("Received Response: %s" % self.ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                        print("")
                    if len(keywords)>1:
                        print("")
                        print("Expected Response: %s" % self.ascii2print(keywords[0],printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                        for (i,each_elem) in enumerate(keywords):
                            if i == 0:
                                pass
                            if i >0:
                                SafePrintLog("Expected Response: %s" % self.ascii2print(each_elem,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                        SafePrintLog("Received Response: %s" % self.ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                        SafePrintLog("")
        # 2
        if condition=="match_all_order":
            if log_msg == "debug":
                print("Check if response match all keywords in order: ( match without extra char. )")
            receivedResp = resp
            expectedResp = ""
            for (i,each_keyword) in enumerate(keywords) :
                expectedResp += keywords[i]
            matched = fnmatch.fnmatchcase(receivedResp, expectedResp)
            if matched == 0 :
                if log_msg == "logmsg" or log_msg == "debug":
                    print("")
                    print("No Match!! (match_all_order)")
                    print("")
                    print("Expected Response: %s" % self.ascii2print(expectedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                    print("Received Response: %s" % self.ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                    print("")

        # 3
        if condition=="match_all_disorder":
            debug_msg = ""
            debug_msg += "Check if response contains all keywords ( without extra character, dis-order ): \n"
            # differcuit to code , code later

            itemlist = keywords
            #itemlist = ["A","B","C"]
            permutation_list = list(itertools.permutations(itemlist, len(itemlist)))
            permutation_concat_list = []
            for each_elem in permutation_list:
                tempstring = ""
                for eachchar in each_elem:
                    tempstring += eachchar
                permutation_concat_list.append(tempstring)

            debug_msg += "\nConbination of keywords: \n"

            for (i,each_conbination) in enumerate(permutation_concat_list) :
                # print i+1, ascii2print(each_conbination,printmode).replace("<CR>","\\r").replace("<LF>","\\n")

                receivedResp = resp
                expectedResp = each_conbination
                matched = fnmatch.fnmatchcase(receivedResp, expectedResp)

                # debug message
                if matched == 0 :
                    debug_msg += str(i+1) + " " + self.ascii2print(each_conbination,printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- no match\n"
                else:
                    debug_msg += str(i+1) + " " + self.ascii2print(each_conbination,printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- matched\n"

                # break in normal mode when result matched
                # normal mode >> matched result and break, debug mode >> list all conbination and result
                if matched == 1 :
                    if log_msg != "debug":
                        break

            # display "No Match" when matching failed
            if matched == 1 :
                if log_msg == "debug":
                    print( debug_msg)
            else:
                if log_msg == "logmsg" or log_msg == "debug":
                    print("")
                    print("No Match!! (match_all_disorder)")
                    print("")
                    print( debug_msg)

        # 4
        if condition=="contain_all_order":
            debug_msg = ""
            debug_msg += "Check if response contains all keywords in order:"
            receivedResp = resp
            expectedResp = "*"
            for (i,each_keyword) in enumerate(keywords) :
                if i == 0 :
                    expectedResp += keywords[i]
                else:
                    expectedResp += "*" + keywords[i]
            expectedResp += "*"
            matched = fnmatch.fnmatchcase(receivedResp, expectedResp)
            if matched == 1 :
                if log_msg == "debug":
                    print("")
                    print( debug_msg)
                    print( "Expected Response: %s" % self.ascii2print(expectedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                    print("")
            else:
                if log_msg == "logmsg" or log_msg == "debug":
                    print("")
                    print("No Match!! (contain_all_order)")
                    print("")
                    print("Expected Response: %s" % self.ascii2print(expectedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                    print("Received Response: %s" % self.ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                    print("")

        # 5
        if condition=="contain_all_disorder":
            debug_msg = ""
            debug_msg += "\nCheck if response contains all keywords without order:\n\n"
            #for (i,each_keyword) in enumerate(keywords) :
            #    print ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n")
            receivedResp = resp
            expectedResp = ""

            debug_msg += "Response: " + self.ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "\n"
            debug_msg += "Keywords:\n"
            flag_notfound = 0
            matched = 1

            for (i,each_keyword) in enumerate(keywords) :
                if resp.find(keywords[i]) >= 0:
                    debug_msg += self.ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- found\n"
                else:
                    debug_msg += self.ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- not found\n"
                    flag_notfound = 1


            if flag_notfound == 0:
                matched = 1
                if log_msg == "debug":
                    print( debug_msg)

            if flag_notfound == 1:
                matched = 0
                if log_msg == "logmsg" or log_msg == "debug":
                    print("")
                    print( "No Match!! (contain_all_disorder)")
                    print("")
                    print(debug_msg)

        # 6
        if condition=="contain_anyone":
            debug_msg = ""
            debug_msg += "\nCheck if response contains anyone of keywords: \n\n"
            #for (i,each_keyword) in enumerate(keywords) :
            #    print ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n")
            receivedResp = resp
            expectedResp = ""

            debug_msg += "Response: " + self.ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "\n"
            debug_msg += "Keywords:\n"
            flag_found = 0
            matched = 0
            for (i,each_keyword) in enumerate(keywords) :
                if resp.find(keywords[i]) >= 0:
                    debug_msg += self.ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- found\n"
                    flag_found = 1
                else:
                    debug_msg += self.ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- not found\n"

            if flag_found == 1:
                matched = 1
                if log_msg == "debug":
                    print(debug_msg)

            if flag_found == 0:
                matched = 0
                if log_msg == "logmsg" or log_msg == "debug":
                    print("")
                    print("No Match!! (contain_anyone)")
                    print("")
                    print( debug_msg)

        # 7
        if condition=="not_contain_anyone":
            debug_msg = ""
            debug_msg += "\nCheck that response do not contains anyone of keywords: \n\n"
            #for (i,each_keyword) in enumerate(keywords) :
            #    print ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n")
            receivedResp = resp
            expectedResp = ""

            debug_msg += "Response: " + self.ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "\n"
            debug_msg += "Keywords:\n"
            flag_found = 0
            matched = 1

            for (i,each_keyword) in enumerate(keywords) :
                if resp.find(keywords[i]) >= 0:
                    debug_msg += self.ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- found\n"
                    flag_found = 1
                else:
                    debug_msg += self.ascii2print(keywords[i],printmode) + "      <-- not found\n"


            if flag_found == 0:
                matched = 1
                if log_msg == "debug":
                    print( debug_msg)

            if flag_found == 1:
                matched = 0
                if log_msg == "logmsg" or log_msg == "debug":
                    print("")
                    print("No Match!! (not_contain_anyone)")
                    print("")
                    print( debug_msg)

        # udpate result to statOfItem
        if update_result == "critical":
            if matched == 0:
                self.statOfItem = 'NOK'
            else:
                self.numOfSuccessfulResponse += 1.0
                pass
        else:
            if log_msg == "logmsg":
                print("\nNot Critical command\n")

        return matched

    def wait_resp(self, hCom, waitpattern, timeout=60000, log_msg="logmsg", printmode="symbol"): 
        "goal of the method : this method waits for the data received from Com port"
        "INPUT : hCom : COM port object"
        "        waitpattern : the matching pattern for the received data"
        "        timeout (ms) : timeout between each received packet"
        "        log_msg : option for log message"
        "OUTPUT : Received data (String)"

        start_time = datetime.now()
        com_port_name = hCom.port
        if log_msg == "debug":
            print(start_time)
        flag_matchrsp = False
        flag_matchstring = False
        flag_timeout = False
        flag_wait_until_timeout = False
        flag_printline = False
        LogMsg = ""
        timestamp = ""

        # wait until timeout mode
        if waitpattern == None or waitpattern[0] == "":
            flag_wait_until_timeout = True
            waitpattern = [""]
            print("")
            print("Wait responses in %s ms" % str(timeout))
            print("")

        displaybuffer = ""
        displaypointer = 0
        while 1:
            # Read data from UART Buffer
            if hCom.in_waiting>0:
                self.uartbuffer[hCom.port] += hCom.read(hCom.in_waiting).decode('utf-8','ignore')
                if log_msg == "debug":
                    #myColor = colorLsit[7]
                    #print "Read data from UART buffer:", self.uartbuffer[hCom.port].replace("\r","<CR>").replace("\n","<LF>")
                    #print "Read data from UART buffer:", self.ascii2print(self.uartbuffer[hCom.port],printmode)
                    LogMsg = "Read data from UART buffer: "+ self.ascii2print(self.uartbuffer[hCom.port],printmode)
                    print(LogMsg)
            # Match response
            # Loop for each character
            for (i,each_char) in enumerate(self.uartbuffer[hCom.port]) :
                if log_msg == "debug":
                    #myColor = colorLsit[7]
                    #print i, self.uartbuffer[hCom.port][:i+1].replace("\r","<CR>").replace("\n","<LF>").replace("\n","<LF>")
                    #print i, ascii2print(self.uartbuffer[hCom.port][:i+1],printmode)
                    LogMsg = str(i)+" "+self.ascii2print(self.uartbuffer[hCom.port][:i+1],printmode)
                    print(LogMsg)
                # display if matched with a line syntax
                displaybuffer = self.uartbuffer[hCom.port][displaypointer:i+1]
                line_syntax1 = "*\r\n*\r\n"
                line_syntax2 = "+*\r\n"
                line_syntax3 = "\r\n> "
                if fnmatch.fnmatchcase(displaybuffer, line_syntax1) or \
                    fnmatch.fnmatchcase(displaybuffer, line_syntax2) or \
                    fnmatch.fnmatchcase(displaybuffer, line_syntax3) :
                    # display timestamp
                    if self.SndRcvTimestamp:
                        timestamp = self.timeDisplay() + " "
                    # display data
                    #myColor = colorLsit[7]
                    #received_data = displaybuffer.replace("\r","<CR>").replace("\n","<LF>").replace("\x15","<NAK>").replace("\x06","<ACK>").replace("\x00","<NULL>")
                    received_data = self.ascii2print(displaybuffer,printmode)
                    #print timestamp+"Rcv COM", com_port_name, "["+received_data+"]",
                    LogMsg = timestamp+"Rcv COM "+com_port_name+" ["+received_data+"] "
                    displaypointer = i+1
                    flag_printline = True

                # match received response with waitpattern
                for (each_elem) in waitpattern:
                    receivedResp = self.uartbuffer[hCom.port][:i+1]
                    expectedResp = each_elem
                    if fnmatch.fnmatchcase(receivedResp, expectedResp):
                        flag_matchstring = True
                        break
                if flag_matchstring:
                    # display the remaining matched response when waitpettern is found
                    displaybuffer = self.uartbuffer[hCom.port][displaypointer:i+1]
                    if len(displaybuffer)>0:
                        # display timestamp
                        if self.SndRcvTimestamp:
                            timestamp = self.timeDisplay() + " "
                        # display data
                        #myColor = colorLsit[7]
                        #received_data = displaybuffer.replace("\r","<CR>").replace("\n","<LF>").replace("\x15","<NAK>").replace("\x06","<ACK>").replace("\x00","<NULL>")
                        received_data = self.ascii2print(displaybuffer,printmode)
                        #print "Rcv COM", com_port_name, "["+received_data+"]",
                        LogMsg = timestamp+"Rcv COM "+str(com_port_name)+" ["+received_data+"] "
                        pass

                    # display time spent in receive
                    if self.RcvTimespent:
                        diff_time = datetime.now() - start_time
                        diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
                        #print " <"+str(timeout), " @"+str(diff_time_ms), "ms",
                        LogMsg += " <"+str(timeout)+" @"+str(diff_time_ms)+" ms "

                    flag_printline = True

                    # clear matched resposne in UART Buffer
                    uartbuffer[hCom.port] = self.uartbuffer[hCom.port][i+1:]
                    flag_matchrsp = True

                    # break for Match response
                    flag_matchrsp = True

                # print linebreak for EOL
                if flag_printline:
                    flag_printline = False
                    #print ""
                    print(LogMsg)

                # break for Match response
                if flag_matchrsp:
                    break


            # Count timeout
            diff_time = datetime.now() - start_time
            diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
            if diff_time_ms > timeout:
                if log_msg == "debug":
                    #print "Timeout: ", diff_time, "diff_time_ms:", diff_time_ms
                    LogMsg = "Timeout: "+str(diff_time)+" diff_time_ms: "+str(diff_time_ms)
                    print(LogMsg)
                # display the remaining response when timeout
                displaybuffer = self.uartbuffer[hCom.port][displaypointer:]
                if len(displaybuffer)>0:
                    # display timestamp
                    if self.SndRcvTimestamp:
                        #myColor = colorLsit[7]
                        #print TimeDisplay(),
                        timestamp = self.timeDisplay() + " "
                    # display data
                    #myColor = colorLsit[7]
                    #received_data = receivedResp.replace("\r","<CR>").replace("\n","<LF>").replace("\x15","<NAK>").replace("\x06","<ACK>").replace("\x00","<NULL>")
                    received_data = self.ascii2print(receivedResp,printmode)
                    #print "Rcv COM", com_port_name, " ["+received_data+"]"
                    LogMsg = "Rcv COM "+str(com_port_name)+" ["+received_data+"]"
                    print(LogMsg)
                    pass

                # clear all resposne in UART Buffer
                #myColor = colorLsit[8]
                receivedResp = self.uartbuffer[hCom.port]

                if flag_wait_until_timeout != True:
                    if log_msg == "logmsg" or log_msg == "debug":
                        if len(receivedResp) > 0:
                            #print "\nNo Match! "+"@COM"+com_port_name+ " <"+str(timeout)+" ms\n"
                            LogMsg = "\nNo Match! "+"@COM"+com_port_name+" <"+str(timeout)+" ms\n"
                            print(LogMsg)
                        if len(receivedResp) == 0:
                            #print "\nNo Response! "+"@COM"+com_port_name+ " <"+str(timeout)+" ms\n"
                            LogMsg = "\nNo Response! "+"@COM"+com_port_name+ " <"+str(timeout)+" ms\n"
                            print(LogMsg)
                self.uartbuffer[hCom.port] = ""
                flag_timeout = True


            if flag_matchrsp:
                break
            if flag_timeout:
                break


        if log_msg == "debug":
            #print ""
            #print len(self.uartbuffer[hCom.port])
            #print "The remaining data in uartbuffer " + str((hCom.port + 1))  + " : [", self.uartbuffer[hCom.port].replace("\r","<CR>").replace("\n","<LF>"), "]"
            #print "The remaining data in uartbuffer " + str((hCom.port + 1))  + " : [", self.ascii2print(self.uartbuffer[hCom.port],printmode), "]"
            print("")
            print(str(len(self.uartbuffer[hCom.port])))
            LogMsg = "The remaining data in uartbuffer " + str((hCom.port + 1))  + " : [", self.ascii2print(self.uartbuffer[hCom.port],printmode), "]"
            print(LogMsg)
        return receivedResp


class AT():

    name = "AT"

    def __init__(self, obj, conf):

        self.conf = conf

        if obj == "master":
            self.master = _AT(conf[0]); return
        elif obj == "slave":
            self.slave = _AT(conf[0]); return
        elif obj == "any":
            self.any = _AT(conf[0]); return

    def reinit(self, obj, conf):
        print("re-init.")
        self.conf.extend(conf)

        if obj == "master":
            self.master = _AT(conf[0])
        else:
            self.slave = _AT(conf[0])
        return self

    def whoami(self):
        print("My name is : {name}\n- conf: <{conf}>".format(name = AT.name, conf = self.conf))