#!/bin/env python
# _*_ coding: utf-8 _*_


#----------------------------------------------------------------------------
# Name:                 acis_at.py
#
# Goal:                 Contains all API functions, in order to create scenarii
#               The most used are AcisOpen, AcisSend and AcisWaitnMatchResp
#
# Author:               refer below
#
# Version:              refer below
#
# Date:                 refer below
#----------------------------------------------------------------------------

#date              who                 version                 modification
#06-04-2018       Shawn Wu              1.0                     creation
#07-26-2018       Shawn Wu              1.1                     Linux system opend the com port based on usb port(busid+hubid+port+ifid).

import time
import serial
import sys
from output import *
from   datetime                  import datetime
import fnmatch
import re
import configparser

# Constant for execution type : Normal, Demo
NORMAL_MODE = 0
DEMO_MODE = 1
MODE = NORMAL_MODE	# normal mode

# AT Send receive time stamp
SndRcvTimestamp = True
RcvTimespent = True

#Variable for status
statOfItem = ''

# Variable for log
#numOfCommand = 0.0
#numOfTest = 0.0
#numOfSuccessfulTest = 0.0 
#numOfFailedTest = 0.0
#numOfCommand = 0.0
#numOfResponse = 0.0
numOfSuccessfulResponse = 0.0 
#numOfFailedResponse = 0.0

# Variable pour process
#process_stat = ''

# for ascii2print(), mode="symbol"
ascii_symbol = {}
ascii_symbol['\x00'] = "<NULL>"
ascii_symbol['\x01'] = "<SOH>"
ascii_symbol['\x02'] = "<STX>"
ascii_symbol['\x03'] = "<ETX>"
ascii_symbol['\x04'] = "<EOT>"
ascii_symbol['\x05'] = "<ENQ>"
ascii_symbol['\x06'] = "<ACK>"
ascii_symbol['\x07'] = "<BEL>"
ascii_symbol['\x08'] = "<BS>"
ascii_symbol['\x09'] = "<TAB>"
ascii_symbol['\x0a'] = "<LF>"
ascii_symbol['\x0b'] = "<VT>"
ascii_symbol['\x0c'] = "<FF>"
ascii_symbol['\x0d'] = "<CR>"
ascii_symbol['\x0e'] = "<SO>"
ascii_symbol['\x0f'] = "<SI>"
ascii_symbol['\x10'] = "<DLE>"
ascii_symbol['\x11'] = "<DC1>"
ascii_symbol['\x12'] = "<DC2>"
ascii_symbol['\x13'] = "<DC3>"
ascii_symbol['\x14'] = "<DC4>"
ascii_symbol['\x15'] = "<NAK>"
ascii_symbol['\x16'] = "<SYN>"
ascii_symbol['\x17'] = "<ETB>"
ascii_symbol['\x18'] = "<CAN>"
ascii_symbol['\x19'] = "<EM>"
ascii_symbol['\x1a'] = "<SUB>"
ascii_symbol['\x1b'] = "<ESC>"
ascii_symbol['\x1c'] = "<FS>"
ascii_symbol['\x1d'] = "<GS>"
ascii_symbol['\x1e'] = "<RS>"
ascii_symbol['\x1f'] = "<US>"

ascii_symbol['\x7f'] = "<DEL>"

ascii_symbol['\x80'] = "<0x80>"
ascii_symbol['\x81'] = "<0x81>"
ascii_symbol['\x82'] = "<0x82>"
ascii_symbol['\x83'] = "<0x83>"
ascii_symbol['\x84'] = "<0x84>"
ascii_symbol['\x85'] = "<0x85>"
ascii_symbol['\x86'] = "<0x86>"
ascii_symbol['\x87'] = "<0x87>"
ascii_symbol['\x88'] = "<0x88>"
ascii_symbol['\x89'] = "<0x89>"
ascii_symbol['\x8A'] = "<0x8A>"
ascii_symbol['\x8B'] = "<0x8B>"
ascii_symbol['\x8C'] = "<0x8C>"
ascii_symbol['\x8D'] = "<0x8D>"
ascii_symbol['\x8E'] = "<0x8E>"
ascii_symbol['\x8F'] = "<0x8F>"
ascii_symbol['\x90'] = "<0x90>"
ascii_symbol['\x91'] = "<0x91>"
ascii_symbol['\x92'] = "<0x92>"
ascii_symbol['\x93'] = "<0x93>"
ascii_symbol['\x94'] = "<0x94>"
ascii_symbol['\x95'] = "<0x95>"
ascii_symbol['\x96'] = "<0x96>"
ascii_symbol['\x97'] = "<0x97>"
ascii_symbol['\x98'] = "<0x98>"
ascii_symbol['\x99'] = "<0x99>"
ascii_symbol['\x9A'] = "<0x9A>"
ascii_symbol['\x9B'] = "<0x9B>"
ascii_symbol['\x9C'] = "<0x9C>"
ascii_symbol['\x9D'] = "<0x9D>"
ascii_symbol['\x9E'] = "<0x9E>"
ascii_symbol['\x9F'] = "<0x9F>"
ascii_symbol['\xA0'] = "<0xA0>"
ascii_symbol['\xA1'] = "<0xA1>"
ascii_symbol['\xA2'] = "<0xA2>"
ascii_symbol['\xA3'] = "<0xA3>"
ascii_symbol['\xA4'] = "<0xA4>"
ascii_symbol['\xA5'] = "<0xA5>"
ascii_symbol['\xA6'] = "<0xA6>"
ascii_symbol['\xA7'] = "<0xA7>"
ascii_symbol['\xA8'] = "<0xA8>"
ascii_symbol['\xA9'] = "<0xA9>"
ascii_symbol['\xAA'] = "<0xAA>"
ascii_symbol['\xAB'] = "<0xAB>"
ascii_symbol['\xAC'] = "<0xAC>"
ascii_symbol['\xAD'] = "<0xAD>"
ascii_symbol['\xAE'] = "<0xAE>"
ascii_symbol['\xAF'] = "<0xAF>"
ascii_symbol['\xB0'] = "<0xB0>"
ascii_symbol['\xB1'] = "<0xB1>"
ascii_symbol['\xB2'] = "<0xB2>"
ascii_symbol['\xB3'] = "<0xB3>"
ascii_symbol['\xB4'] = "<0xB4>"
ascii_symbol['\xB5'] = "<0xB5>"
ascii_symbol['\xB6'] = "<0xB6>"
ascii_symbol['\xB7'] = "<0xB7>"
ascii_symbol['\xB8'] = "<0xB8>"
ascii_symbol['\xB9'] = "<0xB9>"
ascii_symbol['\xBA'] = "<0xBA>"
ascii_symbol['\xBB'] = "<0xBB>"
ascii_symbol['\xBC'] = "<0xBC>"
ascii_symbol['\xBD'] = "<0xBD>"
ascii_symbol['\xBE'] = "<0xBE>"
ascii_symbol['\xBF'] = "<0xBF>"
ascii_symbol['\xC0'] = "<0xC0>"
ascii_symbol['\xC1'] = "<0xC1>"
ascii_symbol['\xC2'] = "<0xC2>"
ascii_symbol['\xC3'] = "<0xC3>"
ascii_symbol['\xC4'] = "<0xC4>"
ascii_symbol['\xC5'] = "<0xC5>"
ascii_symbol['\xC6'] = "<0xC6>"
ascii_symbol['\xC7'] = "<0xC7>"
ascii_symbol['\xC8'] = "<0xC8>"
ascii_symbol['\xC9'] = "<0xC9>"
ascii_symbol['\xCA'] = "<0xCA>"
ascii_symbol['\xCB'] = "<0xCB>"
ascii_symbol['\xCC'] = "<0xCC>"
ascii_symbol['\xCD'] = "<0xCD>"
ascii_symbol['\xCE'] = "<0xCE>"
ascii_symbol['\xCF'] = "<0xCF>"
ascii_symbol['\xD0'] = "<0xD0>"
ascii_symbol['\xD1'] = "<0xD1>"
ascii_symbol['\xD2'] = "<0xD2>"
ascii_symbol['\xD3'] = "<0xD3>"
ascii_symbol['\xD4'] = "<0xD4>"
ascii_symbol['\xD5'] = "<0xD5>"
ascii_symbol['\xD6'] = "<0xD6>"
ascii_symbol['\xD7'] = "<0xD7>"
ascii_symbol['\xD8'] = "<0xD8>"
ascii_symbol['\xD9'] = "<0xD9>"
ascii_symbol['\xDA'] = "<0xDA>"
ascii_symbol['\xDB'] = "<0xDB>"
ascii_symbol['\xDC'] = "<0xDC>"
ascii_symbol['\xDD'] = "<0xDD>"
ascii_symbol['\xDE'] = "<0xDE>"
ascii_symbol['\xDF'] = "<0xDF>"
ascii_symbol['\xE0'] = "<0xE0>"
ascii_symbol['\xE1'] = "<0xE1>"
ascii_symbol['\xE2'] = "<0xE2>"
ascii_symbol['\xE3'] = "<0xE3>"
ascii_symbol['\xE4'] = "<0xE4>"
ascii_symbol['\xE5'] = "<0xE5>"
ascii_symbol['\xE6'] = "<0xE6>"
ascii_symbol['\xE7'] = "<0xE7>"
ascii_symbol['\xE8'] = "<0xE8>"
ascii_symbol['\xE9'] = "<0xE9>"
ascii_symbol['\xEA'] = "<0xEA>"
ascii_symbol['\xEB'] = "<0xEB>"
ascii_symbol['\xEC'] = "<0xEC>"
ascii_symbol['\xED'] = "<0xED>"
ascii_symbol['\xEE'] = "<0xEE>"
ascii_symbol['\xEF'] = "<0xEF>"
ascii_symbol['\xF0'] = "<0xF0>"
ascii_symbol['\xF1'] = "<0xF1>"
ascii_symbol['\xF2'] = "<0xF2>"
ascii_symbol['\xF3'] = "<0xF3>"
ascii_symbol['\xF4'] = "<0xF4>"
ascii_symbol['\xF5'] = "<0xF5>"
ascii_symbol['\xF6'] = "<0xF6>"
ascii_symbol['\xF7'] = "<0xF7>"
ascii_symbol['\xF8'] = "<0xF8>"
ascii_symbol['\xF9'] = "<0xF9>"
ascii_symbol['\xFA'] = "<0xFA>"
ascii_symbol['\xFB'] = "<0xFB>"
ascii_symbol['\xFC'] = "<0xFC>"
ascii_symbol['\xFD'] = "<0xFD>"
ascii_symbol['\xFE'] = "<0xFE>"
ascii_symbol['\xFF'] = "<0xFF>"


# for ascii2print(), mode="hexstring"

# hardcode for ascii2hexstring  >> very fast
# symbol
ascii2hexstring_symbol = {}
ascii2hexstring_symbol['\x00'] = "<0x00>"
ascii2hexstring_symbol['\x01'] = "<0x01>"
ascii2hexstring_symbol['\x02'] = "<0x02>"
ascii2hexstring_symbol['\x03'] = "<0x03>"
ascii2hexstring_symbol['\x04'] = "<0x04>"
ascii2hexstring_symbol['\x05'] = "<0x05>"
ascii2hexstring_symbol['\x06'] = "<0x06>"
ascii2hexstring_symbol['\x07'] = "<0x07>"
ascii2hexstring_symbol['\x08'] = "<0x08>"
ascii2hexstring_symbol['\x09'] = "<0x09>"
ascii2hexstring_symbol['\x0A'] = "<0x0A>"
ascii2hexstring_symbol['\x0B'] = "<0x0B>"
ascii2hexstring_symbol['\x0C'] = "<0x0C>"
ascii2hexstring_symbol['\x0D'] = "<0x0D>"
ascii2hexstring_symbol['\x0E'] = "<0x0E>"
ascii2hexstring_symbol['\x0F'] = "<0x0F>"
ascii2hexstring_symbol['\x10'] = "<0x10>"
ascii2hexstring_symbol['\x11'] = "<0x11>"
ascii2hexstring_symbol['\x12'] = "<0x12>"
ascii2hexstring_symbol['\x13'] = "<0x13>"
ascii2hexstring_symbol['\x14'] = "<0x14>"
ascii2hexstring_symbol['\x15'] = "<0x15>"
ascii2hexstring_symbol['\x16'] = "<0x16>"
ascii2hexstring_symbol['\x17'] = "<0x17>"
ascii2hexstring_symbol['\x18'] = "<0x18>"
ascii2hexstring_symbol['\x19'] = "<0x19>"
ascii2hexstring_symbol['\x1A'] = "<0x1A>"
ascii2hexstring_symbol['\x1B'] = "<0x1B>"
ascii2hexstring_symbol['\x1C'] = "<0x1C>"
ascii2hexstring_symbol['\x1D'] = "<0x1D>"
ascii2hexstring_symbol['\x1E'] = "<0x1E>"
ascii2hexstring_symbol['\x1F'] = "<0x1F>"

#printable
ascii2hexstring_printable = {}
ascii2hexstring_printable['\x20'] = "<0x20>"
ascii2hexstring_printable['\x21'] = "<0x21>"
ascii2hexstring_printable['\x22'] = "<0x22>"
ascii2hexstring_printable['\x23'] = "<0x23>"
ascii2hexstring_printable['\x24'] = "<0x24>"
ascii2hexstring_printable['\x25'] = "<0x25>"
ascii2hexstring_printable['\x26'] = "<0x26>"
ascii2hexstring_printable['\x27'] = "<0x27>"
ascii2hexstring_printable['\x28'] = "<0x28>"
ascii2hexstring_printable['\x29'] = "<0x29>"
ascii2hexstring_printable['\x2A'] = "<0x2A>"
ascii2hexstring_printable['\x2B'] = "<0x2B>"
ascii2hexstring_printable['\x2C'] = "<0x2C>"
ascii2hexstring_printable['\x2D'] = "<0x2D>"
ascii2hexstring_printable['\x2E'] = "<0x2E>"
ascii2hexstring_printable['\x2F'] = "<0x2F>"
ascii2hexstring_printable['\x30'] = "<0x30>"
ascii2hexstring_printable['\x31'] = "<0x31>"
ascii2hexstring_printable['\x32'] = "<0x32>"
ascii2hexstring_printable['\x33'] = "<0x33>"
ascii2hexstring_printable['\x34'] = "<0x34>"
ascii2hexstring_printable['\x35'] = "<0x35>"
ascii2hexstring_printable['\x36'] = "<0x36>"
ascii2hexstring_printable['\x37'] = "<0x37>"
ascii2hexstring_printable['\x38'] = "<0x38>"
ascii2hexstring_printable['\x39'] = "<0x39>"
ascii2hexstring_printable['\x3A'] = "<0x3A>"
ascii2hexstring_printable['\x3B'] = "<0x3B>"
ascii2hexstring_printable['\x3C'] = "<0x3C>"
ascii2hexstring_printable['\x3D'] = "<0x3D>"
ascii2hexstring_printable['\x3E'] = "<0x3E>"
ascii2hexstring_printable['\x3F'] = "<0x3F>"
ascii2hexstring_printable['\x40'] = "<0x40>"
ascii2hexstring_printable['\x41'] = "<0x41>"
ascii2hexstring_printable['\x42'] = "<0x42>"
ascii2hexstring_printable['\x43'] = "<0x43>"
ascii2hexstring_printable['\x44'] = "<0x44>"
ascii2hexstring_printable['\x45'] = "<0x45>"
ascii2hexstring_printable['\x46'] = "<0x46>"
ascii2hexstring_printable['\x47'] = "<0x47>"
ascii2hexstring_printable['\x48'] = "<0x48>"
ascii2hexstring_printable['\x49'] = "<0x49>"
ascii2hexstring_printable['\x4A'] = "<0x4A>"
ascii2hexstring_printable['\x4B'] = "<0x4B>"
ascii2hexstring_printable['\x4C'] = "<0x4C>"
ascii2hexstring_printable['\x4D'] = "<0x4D>"
ascii2hexstring_printable['\x4E'] = "<0x4E>"
ascii2hexstring_printable['\x4F'] = "<0x4F>"
ascii2hexstring_printable['\x50'] = "<0x50>"
ascii2hexstring_printable['\x51'] = "<0x51>"
ascii2hexstring_printable['\x52'] = "<0x52>"
ascii2hexstring_printable['\x53'] = "<0x53>"
ascii2hexstring_printable['\x54'] = "<0x54>"
ascii2hexstring_printable['\x55'] = "<0x55>"
ascii2hexstring_printable['\x56'] = "<0x56>"
ascii2hexstring_printable['\x57'] = "<0x57>"
ascii2hexstring_printable['\x58'] = "<0x58>"
ascii2hexstring_printable['\x59'] = "<0x59>"
ascii2hexstring_printable['\x5A'] = "<0x5A>"
ascii2hexstring_printable['\x5B'] = "<0x5B>"
ascii2hexstring_printable['\x5C'] = "<0x5C>"
ascii2hexstring_printable['\x5D'] = "<0x5D>"
ascii2hexstring_printable['\x5E'] = "<0x5E>"
ascii2hexstring_printable['\x5F'] = "<0x5F>"
ascii2hexstring_printable['\x60'] = "<0x60>"
ascii2hexstring_printable['\x61'] = "<0x61>"
ascii2hexstring_printable['\x62'] = "<0x62>"
ascii2hexstring_printable['\x63'] = "<0x63>"
ascii2hexstring_printable['\x64'] = "<0x64>"
ascii2hexstring_printable['\x65'] = "<0x65>"
ascii2hexstring_printable['\x66'] = "<0x66>"
ascii2hexstring_printable['\x67'] = "<0x67>"
ascii2hexstring_printable['\x68'] = "<0x68>"
ascii2hexstring_printable['\x69'] = "<0x69>"
ascii2hexstring_printable['\x6A'] = "<0x6A>"
ascii2hexstring_printable['\x6B'] = "<0x6B>"
ascii2hexstring_printable['\x6C'] = "<0x6C>"
ascii2hexstring_printable['\x6D'] = "<0x6D>"
ascii2hexstring_printable['\x6E'] = "<0x6E>"
ascii2hexstring_printable['\x6F'] = "<0x6F>"
ascii2hexstring_printable['\x70'] = "<0x70>"
ascii2hexstring_printable['\x71'] = "<0x71>"
ascii2hexstring_printable['\x72'] = "<0x72>"
ascii2hexstring_printable['\x73'] = "<0x73>"
ascii2hexstring_printable['\x74'] = "<0x74>"
ascii2hexstring_printable['\x75'] = "<0x75>"
ascii2hexstring_printable['\x76'] = "<0x76>"
ascii2hexstring_printable['\x77'] = "<0x77>"
ascii2hexstring_printable['\x78'] = "<0x78>"
ascii2hexstring_printable['\x79'] = "<0x79>"
ascii2hexstring_printable['\x7A'] = "<0x7A>"
ascii2hexstring_printable['\x7B'] = "<0x7B>"
ascii2hexstring_printable['\x7C'] = "<0x7C>"
ascii2hexstring_printable['\x7D'] = "<0x7D>"
ascii2hexstring_printable['\x7E'] = "<0x7E>"
ascii2hexstring_printable['\x7F'] = "<0x7F>"

# extendec ascii
ascii2hexstring_extended = {}
ascii2hexstring_extended['\x80'] = "<0x80>"
ascii2hexstring_extended['\x81'] = "<0x81>"
ascii2hexstring_extended['\x82'] = "<0x82>"
ascii2hexstring_extended['\x83'] = "<0x83>"
ascii2hexstring_extended['\x84'] = "<0x84>"
ascii2hexstring_extended['\x85'] = "<0x85>"
ascii2hexstring_extended['\x86'] = "<0x86>"
ascii2hexstring_extended['\x87'] = "<0x87>"
ascii2hexstring_extended['\x88'] = "<0x88>"
ascii2hexstring_extended['\x89'] = "<0x89>"
ascii2hexstring_extended['\x8A'] = "<0x8A>"
ascii2hexstring_extended['\x8B'] = "<0x8B>"
ascii2hexstring_extended['\x8C'] = "<0x8C>"
ascii2hexstring_extended['\x8D'] = "<0x8D>"
ascii2hexstring_extended['\x8E'] = "<0x8E>"
ascii2hexstring_extended['\x8F'] = "<0x8F>"
ascii2hexstring_extended['\x90'] = "<0x90>"
ascii2hexstring_extended['\x91'] = "<0x91>"
ascii2hexstring_extended['\x92'] = "<0x92>"
ascii2hexstring_extended['\x93'] = "<0x93>"
ascii2hexstring_extended['\x94'] = "<0x94>"
ascii2hexstring_extended['\x95'] = "<0x95>"
ascii2hexstring_extended['\x96'] = "<0x96>"
ascii2hexstring_extended['\x97'] = "<0x97>"
ascii2hexstring_extended['\x98'] = "<0x98>"
ascii2hexstring_extended['\x99'] = "<0x99>"
ascii2hexstring_extended['\x9A'] = "<0x9A>"
ascii2hexstring_extended['\x9B'] = "<0x9B>"
ascii2hexstring_extended['\x9C'] = "<0x9C>"
ascii2hexstring_extended['\x9D'] = "<0x9D>"
ascii2hexstring_extended['\x9E'] = "<0x9E>"
ascii2hexstring_extended['\x9F'] = "<0x9F>"
ascii2hexstring_extended['\xA0'] = "<0xA0>"
ascii2hexstring_extended['\xA1'] = "<0xA1>"
ascii2hexstring_extended['\xA2'] = "<0xA2>"
ascii2hexstring_extended['\xA3'] = "<0xA3>"
ascii2hexstring_extended['\xA4'] = "<0xA4>"
ascii2hexstring_extended['\xA5'] = "<0xA5>"
ascii2hexstring_extended['\xA6'] = "<0xA6>"
ascii2hexstring_extended['\xA7'] = "<0xA7>"
ascii2hexstring_extended['\xA8'] = "<0xA8>"
ascii2hexstring_extended['\xA9'] = "<0xA9>"
ascii2hexstring_extended['\xAA'] = "<0xAA>"
ascii2hexstring_extended['\xAB'] = "<0xAB>"
ascii2hexstring_extended['\xAC'] = "<0xAC>"
ascii2hexstring_extended['\xAD'] = "<0xAD>"
ascii2hexstring_extended['\xAE'] = "<0xAE>"
ascii2hexstring_extended['\xAF'] = "<0xAF>"
ascii2hexstring_extended['\xB0'] = "<0xB0>"
ascii2hexstring_extended['\xB1'] = "<0xB1>"
ascii2hexstring_extended['\xB2'] = "<0xB2>"
ascii2hexstring_extended['\xB3'] = "<0xB3>"
ascii2hexstring_extended['\xB4'] = "<0xB4>"
ascii2hexstring_extended['\xB5'] = "<0xB5>"
ascii2hexstring_extended['\xB6'] = "<0xB6>"
ascii2hexstring_extended['\xB7'] = "<0xB7>"
ascii2hexstring_extended['\xB8'] = "<0xB8>"
ascii2hexstring_extended['\xB9'] = "<0xB9>"
ascii2hexstring_extended['\xBA'] = "<0xBA>"
ascii2hexstring_extended['\xBB'] = "<0xBB>"
ascii2hexstring_extended['\xBC'] = "<0xBC>"
ascii2hexstring_extended['\xBD'] = "<0xBD>"
ascii2hexstring_extended['\xBE'] = "<0xBE>"
ascii2hexstring_extended['\xBF'] = "<0xBF>"
ascii2hexstring_extended['\xC0'] = "<0xC0>"
ascii2hexstring_extended['\xC1'] = "<0xC1>"
ascii2hexstring_extended['\xC2'] = "<0xC2>"
ascii2hexstring_extended['\xC3'] = "<0xC3>"
ascii2hexstring_extended['\xC4'] = "<0xC4>"
ascii2hexstring_extended['\xC5'] = "<0xC5>"
ascii2hexstring_extended['\xC6'] = "<0xC6>"
ascii2hexstring_extended['\xC7'] = "<0xC7>"
ascii2hexstring_extended['\xC8'] = "<0xC8>"
ascii2hexstring_extended['\xC9'] = "<0xC9>"
ascii2hexstring_extended['\xCA'] = "<0xCA>"
ascii2hexstring_extended['\xCB'] = "<0xCB>"
ascii2hexstring_extended['\xCC'] = "<0xCC>"
ascii2hexstring_extended['\xCD'] = "<0xCD>"
ascii2hexstring_extended['\xCE'] = "<0xCE>"
ascii2hexstring_extended['\xCF'] = "<0xCF>"
ascii2hexstring_extended['\xD0'] = "<0xD0>"
ascii2hexstring_extended['\xD1'] = "<0xD1>"
ascii2hexstring_extended['\xD2'] = "<0xD2>"
ascii2hexstring_extended['\xD3'] = "<0xD3>"
ascii2hexstring_extended['\xD4'] = "<0xD4>"
ascii2hexstring_extended['\xD5'] = "<0xD5>"
ascii2hexstring_extended['\xD6'] = "<0xD6>"
ascii2hexstring_extended['\xD7'] = "<0xD7>"
ascii2hexstring_extended['\xD8'] = "<0xD8>"
ascii2hexstring_extended['\xD9'] = "<0xD9>"
ascii2hexstring_extended['\xDA'] = "<0xDA>"
ascii2hexstring_extended['\xDB'] = "<0xDB>"
ascii2hexstring_extended['\xDC'] = "<0xDC>"
ascii2hexstring_extended['\xDD'] = "<0xDD>"
ascii2hexstring_extended['\xDE'] = "<0xDE>"
ascii2hexstring_extended['\xDF'] = "<0xDF>"
ascii2hexstring_extended['\xE0'] = "<0xE0>"
ascii2hexstring_extended['\xE1'] = "<0xE1>"
ascii2hexstring_extended['\xE2'] = "<0xE2>"
ascii2hexstring_extended['\xE3'] = "<0xE3>"
ascii2hexstring_extended['\xE4'] = "<0xE4>"
ascii2hexstring_extended['\xE5'] = "<0xE5>"
ascii2hexstring_extended['\xE6'] = "<0xE6>"
ascii2hexstring_extended['\xE7'] = "<0xE7>"
ascii2hexstring_extended['\xE8'] = "<0xE8>"
ascii2hexstring_extended['\xE9'] = "<0xE9>"
ascii2hexstring_extended['\xEA'] = "<0xEA>"
ascii2hexstring_extended['\xEB'] = "<0xEB>"
ascii2hexstring_extended['\xEC'] = "<0xEC>"
ascii2hexstring_extended['\xED'] = "<0xED>"
ascii2hexstring_extended['\xEE'] = "<0xEE>"
ascii2hexstring_extended['\xEF'] = "<0xEF>"
ascii2hexstring_extended['\xF0'] = "<0xF0>"
ascii2hexstring_extended['\xF1'] = "<0xF1>"
ascii2hexstring_extended['\xF2'] = "<0xF2>"
ascii2hexstring_extended['\xF3'] = "<0xF3>"
ascii2hexstring_extended['\xF4'] = "<0xF4>"
ascii2hexstring_extended['\xF5'] = "<0xF5>"
ascii2hexstring_extended['\xF6'] = "<0xF6>"
ascii2hexstring_extended['\xF7'] = "<0xF7>"
ascii2hexstring_extended['\xF8'] = "<0xF8>"
ascii2hexstring_extended['\xF9'] = "<0xF9>"
ascii2hexstring_extended['\xFA'] = "<0xFA>"
ascii2hexstring_extended['\xFB'] = "<0xFB>"
ascii2hexstring_extended['\xFC'] = "<0xFC>"
ascii2hexstring_extended['\xFD'] = "<0xFD>"
ascii2hexstring_extended['\xFE'] = "<0xFE>"
ascii2hexstring_extended['\xFF'] = "<0xFF>"

# for mode="hexstring", fast convertion for printable ascii , ord()+128
ascii2hexstring_printable_tempsymbol = {}
ascii2hexstring_printable_tempsymbol['\x20'] = "\xBC\xB0\xF8\xA0\xBE"
ascii2hexstring_printable_tempsymbol['\x21'] = "\xBC\xB0\xF8\xA1\xBE"
ascii2hexstring_printable_tempsymbol['\x22'] = "\xBC\xB0\xF8\xA2\xBE"
ascii2hexstring_printable_tempsymbol['\x23'] = "\xBC\xB0\xF8\xA3\xBE"
ascii2hexstring_printable_tempsymbol['\x24'] = "\xBC\xB0\xF8\xA4\xBE"
ascii2hexstring_printable_tempsymbol['\x25'] = "\xBC\xB0\xF8\xA5\xBE"
ascii2hexstring_printable_tempsymbol['\x26'] = "\xBC\xB0\xF8\xA6\xBE"
ascii2hexstring_printable_tempsymbol['\x27'] = "\xBC\xB0\xF8\xA7\xBE"
ascii2hexstring_printable_tempsymbol['\x28'] = "\xBC\xB0\xF8\xA8\xBE"
ascii2hexstring_printable_tempsymbol['\x29'] = "\xBC\xB0\xF8\xA9\xBE"
ascii2hexstring_printable_tempsymbol['\x2A'] = "\xBC\xB0\xF8\xAA\xBE"
ascii2hexstring_printable_tempsymbol['\x2B'] = "\xBC\xB0\xF8\xAB\xBE"
ascii2hexstring_printable_tempsymbol['\x2C'] = "\xBC\xB0\xF8\xAC\xBE"
ascii2hexstring_printable_tempsymbol['\x2D'] = "\xBC\xB0\xF8\xAD\xBE"
ascii2hexstring_printable_tempsymbol['\x2E'] = "\xBC\xB0\xF8\xAE\xBE"
ascii2hexstring_printable_tempsymbol['\x2F'] = "\xBC\xB0\xF8\xAF\xBE"
ascii2hexstring_printable_tempsymbol['\x30'] = "\xBC\xB0\xF8\xB0\xBE"
ascii2hexstring_printable_tempsymbol['\x31'] = "\xBC\xB0\xF8\xB1\xBE"
ascii2hexstring_printable_tempsymbol['\x32'] = "\xBC\xB0\xF8\xB2\xBE"
ascii2hexstring_printable_tempsymbol['\x33'] = "\xBC\xB0\xF8\xB3\xBE"
ascii2hexstring_printable_tempsymbol['\x34'] = "\xBC\xB0\xF8\xB4\xBE"
ascii2hexstring_printable_tempsymbol['\x35'] = "\xBC\xB0\xF8\xB5\xBE"
ascii2hexstring_printable_tempsymbol['\x36'] = "\xBC\xB0\xF8\xB6\xBE"
ascii2hexstring_printable_tempsymbol['\x37'] = "\xBC\xB0\xF8\xB7\xBE"
ascii2hexstring_printable_tempsymbol['\x38'] = "\xBC\xB0\xF8\xB8\xBE"
ascii2hexstring_printable_tempsymbol['\x39'] = "\xBC\xB0\xF8\xB9\xBE"
ascii2hexstring_printable_tempsymbol['\x3A'] = "\xBC\xB0\xF8\xBA\xBE"
ascii2hexstring_printable_tempsymbol['\x3B'] = "\xBC\xB0\xF8\xBB\xBE"
ascii2hexstring_printable_tempsymbol['\x3C'] = "\xBC\xB0\xF8\xBC\xBE"
ascii2hexstring_printable_tempsymbol['\x3D'] = "\xBC\xB0\xF8\xBD\xBE"
ascii2hexstring_printable_tempsymbol['\x3E'] = "\xBC\xB0\xF8\xBE\xBE"
ascii2hexstring_printable_tempsymbol['\x3F'] = "\xBC\xB0\xF8\xBF\xBE"
ascii2hexstring_printable_tempsymbol['\x40'] = "\xBC\xB0\xF8\xC0\xBE"
ascii2hexstring_printable_tempsymbol['\x41'] = "\xBC\xB0\xF8\xC1\xBE"
ascii2hexstring_printable_tempsymbol['\x42'] = "\xBC\xB0\xF8\xC2\xBE"
ascii2hexstring_printable_tempsymbol['\x43'] = "\xBC\xB0\xF8\xC3\xBE"
ascii2hexstring_printable_tempsymbol['\x44'] = "\xBC\xB0\xF8\xC4\xBE"
ascii2hexstring_printable_tempsymbol['\x45'] = "\xBC\xB0\xF8\xC5\xBE"
ascii2hexstring_printable_tempsymbol['\x46'] = "\xBC\xB0\xF8\xC6\xBE"
ascii2hexstring_printable_tempsymbol['\x47'] = "\xBC\xB0\xF8\xC7\xBE"
ascii2hexstring_printable_tempsymbol['\x48'] = "\xBC\xB0\xF8\xC8\xBE"
ascii2hexstring_printable_tempsymbol['\x49'] = "\xBC\xB0\xF8\xC9\xBE"
ascii2hexstring_printable_tempsymbol['\x4A'] = "\xBC\xB0\xF8\xCA\xBE"
ascii2hexstring_printable_tempsymbol['\x4B'] = "\xBC\xB0\xF8\xCB\xBE"
ascii2hexstring_printable_tempsymbol['\x4C'] = "\xBC\xB0\xF8\xCC\xBE"
ascii2hexstring_printable_tempsymbol['\x4D'] = "\xBC\xB0\xF8\xCD\xBE"
ascii2hexstring_printable_tempsymbol['\x4E'] = "\xBC\xB0\xF8\xCE\xBE"
ascii2hexstring_printable_tempsymbol['\x4F'] = "\xBC\xB0\xF8\xCF\xBE"
ascii2hexstring_printable_tempsymbol['\x50'] = "\xBC\xB0\xF8\xD0\xBE"
ascii2hexstring_printable_tempsymbol['\x51'] = "\xBC\xB0\xF8\xD1\xBE"
ascii2hexstring_printable_tempsymbol['\x52'] = "\xBC\xB0\xF8\xD2\xBE"
ascii2hexstring_printable_tempsymbol['\x53'] = "\xBC\xB0\xF8\xD3\xBE"
ascii2hexstring_printable_tempsymbol['\x54'] = "\xBC\xB0\xF8\xD4\xBE"
ascii2hexstring_printable_tempsymbol['\x55'] = "\xBC\xB0\xF8\xD5\xBE"
ascii2hexstring_printable_tempsymbol['\x56'] = "\xBC\xB0\xF8\xD6\xBE"
ascii2hexstring_printable_tempsymbol['\x57'] = "\xBC\xB0\xF8\xD7\xBE"
ascii2hexstring_printable_tempsymbol['\x58'] = "\xBC\xB0\xF8\xD8\xBE"
ascii2hexstring_printable_tempsymbol['\x59'] = "\xBC\xB0\xF8\xD9\xBE"
ascii2hexstring_printable_tempsymbol['\x5A'] = "\xBC\xB0\xF8\xDA\xBE"
ascii2hexstring_printable_tempsymbol['\x5B'] = "\xBC\xB0\xF8\xDB\xBE"
ascii2hexstring_printable_tempsymbol['\x5C'] = "\xBC\xB0\xF8\xDC\xBE"
ascii2hexstring_printable_tempsymbol['\x5D'] = "\xBC\xB0\xF8\xDD\xBE"
ascii2hexstring_printable_tempsymbol['\x5E'] = "\xBC\xB0\xF8\xDE\xBE"
ascii2hexstring_printable_tempsymbol['\x5F'] = "\xBC\xB0\xF8\xDF\xBE"
ascii2hexstring_printable_tempsymbol['\x60'] = "\xBC\xB0\xF8\xE0\xBE"
ascii2hexstring_printable_tempsymbol['\x61'] = "\xBC\xB0\xF8\xE1\xBE"
ascii2hexstring_printable_tempsymbol['\x62'] = "\xBC\xB0\xF8\xE2\xBE"
ascii2hexstring_printable_tempsymbol['\x63'] = "\xBC\xB0\xF8\xE3\xBE"
ascii2hexstring_printable_tempsymbol['\x64'] = "\xBC\xB0\xF8\xE4\xBE"
ascii2hexstring_printable_tempsymbol['\x65'] = "\xBC\xB0\xF8\xE5\xBE"
ascii2hexstring_printable_tempsymbol['\x66'] = "\xBC\xB0\xF8\xE6\xBE"
ascii2hexstring_printable_tempsymbol['\x67'] = "\xBC\xB0\xF8\xE7\xBE"
ascii2hexstring_printable_tempsymbol['\x68'] = "\xBC\xB0\xF8\xE8\xBE"
ascii2hexstring_printable_tempsymbol['\x69'] = "\xBC\xB0\xF8\xE9\xBE"
ascii2hexstring_printable_tempsymbol['\x6A'] = "\xBC\xB0\xF8\xEA\xBE"
ascii2hexstring_printable_tempsymbol['\x6B'] = "\xBC\xB0\xF8\xEB\xBE"
ascii2hexstring_printable_tempsymbol['\x6C'] = "\xBC\xB0\xF8\xEC\xBE"
ascii2hexstring_printable_tempsymbol['\x6D'] = "\xBC\xB0\xF8\xED\xBE"
ascii2hexstring_printable_tempsymbol['\x6E'] = "\xBC\xB0\xF8\xEE\xBE"
ascii2hexstring_printable_tempsymbol['\x6F'] = "\xBC\xB0\xF8\xEF\xBE"
ascii2hexstring_printable_tempsymbol['\x70'] = "\xBC\xB0\xF8\xF0\xBE"
ascii2hexstring_printable_tempsymbol['\x71'] = "\xBC\xB0\xF8\xF1\xBE"
ascii2hexstring_printable_tempsymbol['\x72'] = "\xBC\xB0\xF8\xF2\xBE"
ascii2hexstring_printable_tempsymbol['\x73'] = "\xBC\xB0\xF8\xF3\xBE"
ascii2hexstring_printable_tempsymbol['\x74'] = "\xBC\xB0\xF8\xF4\xBE"
ascii2hexstring_printable_tempsymbol['\x75'] = "\xBC\xB0\xF8\xF5\xBE"
ascii2hexstring_printable_tempsymbol['\x76'] = "\xBC\xB0\xF8\xF6\xBE"
ascii2hexstring_printable_tempsymbol['\x77'] = "\xBC\xB0\xF8\xF7\xBE"
ascii2hexstring_printable_tempsymbol['\x78'] = "\xBC\xB0\xF8\xF8\xBE"
ascii2hexstring_printable_tempsymbol['\x79'] = "\xBC\xB0\xF8\xF9\xBE"
ascii2hexstring_printable_tempsymbol['\x7A'] = "\xBC\xB0\xF8\xFA\xBE"
ascii2hexstring_printable_tempsymbol['\x7B'] = "\xBC\xB0\xF8\xFB\xBE"
ascii2hexstring_printable_tempsymbol['\x7C'] = "\xBC\xB0\xF8\xFC\xBE"
ascii2hexstring_printable_tempsymbol['\x7D'] = "\xBC\xB0\xF8\xFD\xBE"
ascii2hexstring_printable_tempsymbol['\x7E'] = "\xBC\xB0\xF8\xFE\xBE"
ascii2hexstring_printable_tempsymbol['\x7F'] = "\xBC\xB0\xF8\xFF\xBE"

ascii2hexstring_printable_revert = {}
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA0\xBE'] = "<0x20>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA1\xBE'] = "<0x21>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA2\xBE'] = "<0x22>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA3\xBE'] = "<0x23>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA4\xBE'] = "<0x24>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA5\xBE'] = "<0x25>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA6\xBE'] = "<0x26>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA7\xBE'] = "<0x27>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA8\xBE'] = "<0x28>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA9\xBE'] = "<0x29>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xAA\xBE'] = "<0x2A>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xAB\xBE'] = "<0x2B>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xAC\xBE'] = "<0x2C>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xAD\xBE'] = "<0x2D>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xAE\xBE'] = "<0x2E>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xAF\xBE'] = "<0x2F>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB0\xBE'] = "<0x30>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB1\xBE'] = "<0x31>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB2\xBE'] = "<0x32>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB3\xBE'] = "<0x33>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB4\xBE'] = "<0x34>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB5\xBE'] = "<0x35>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB6\xBE'] = "<0x36>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB7\xBE'] = "<0x37>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB8\xBE'] = "<0x38>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB9\xBE'] = "<0x39>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xBA\xBE'] = "<0x3A>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xBB\xBE'] = "<0x3B>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xBC\xBE'] = "<0x3C>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xBD\xBE'] = "<0x3D>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xBE\xBE'] = "<0x3E>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xBF\xBE'] = "<0x3F>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC0\xBE'] = "<0x40>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC1\xBE'] = "<0x41>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC2\xBE'] = "<0x42>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC3\xBE'] = "<0x43>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC4\xBE'] = "<0x44>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC5\xBE'] = "<0x45>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC6\xBE'] = "<0x46>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC7\xBE'] = "<0x47>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC8\xBE'] = "<0x48>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC9\xBE'] = "<0x49>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xCA\xBE'] = "<0x4A>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xCB\xBE'] = "<0x4B>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xCC\xBE'] = "<0x4C>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xCD\xBE'] = "<0x4D>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xCE\xBE'] = "<0x4E>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xCF\xBE'] = "<0x4F>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD0\xBE'] = "<0x50>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD1\xBE'] = "<0x51>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD2\xBE'] = "<0x52>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD3\xBE'] = "<0x53>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD4\xBE'] = "<0x54>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD5\xBE'] = "<0x55>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD6\xBE'] = "<0x56>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD7\xBE'] = "<0x57>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD8\xBE'] = "<0x58>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD9\xBE'] = "<0x59>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xDA\xBE'] = "<0x5A>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xDB\xBE'] = "<0x5B>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xDC\xBE'] = "<0x5C>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xDD\xBE'] = "<0x5D>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xDE\xBE'] = "<0x5E>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xDF\xBE'] = "<0x5F>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE0\xBE'] = "<0x60>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE1\xBE'] = "<0x61>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE2\xBE'] = "<0x62>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE3\xBE'] = "<0x63>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE4\xBE'] = "<0x64>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE5\xBE'] = "<0x65>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE6\xBE'] = "<0x66>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE7\xBE'] = "<0x67>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE8\xBE'] = "<0x68>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE9\xBE'] = "<0x69>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xEA\xBE'] = "<0x6A>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xEB\xBE'] = "<0x6B>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xEC\xBE'] = "<0x6C>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xED\xBE'] = "<0x6D>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xEE\xBE'] = "<0x6E>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xEF\xBE'] = "<0x6F>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF0\xBE'] = "<0x70>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF1\xBE'] = "<0x71>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF2\xBE'] = "<0x72>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF3\xBE'] = "<0x73>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF4\xBE'] = "<0x74>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF5\xBE'] = "<0x75>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF6\xBE'] = "<0x76>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF7\xBE'] = "<0x77>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF8\xBE'] = "<0x78>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF9\xBE'] = "<0x79>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xFA\xBE'] = "<0x7A>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xFB\xBE'] = "<0x7B>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xFC\xBE'] = "<0x7C>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xFD\xBE'] = "<0x7D>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xFE\xBE'] = "<0x7E>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xFF\xBE'] = "<0x7F>"



#list of opened COM ports
list_hCom = []
uartbuffer = {}
usbport2ttycom = {}

def TimeDisplay(dt = None):
    "Display the time ; if dt is empty retrun actual date time under format, otherless return dt under format"
    "INPUT  : (optionnal) dt : date Time"
    "OUTPUT : date Time under format hh:mm:ss:???"
    if dt == None:
        dt = datetime.now() 
    return "(%0.2d:%0.2d:%0.2d:%0.3d)"%(dt.hour, dt.minute, dt.second, dt.microsecond/1000)

def SafePrint(time, hCom, info):
    "goal of the method : This method displays information"
    "INPUT : "
    "OUTPUT : "

    if MODE != DEMO_MODE:
        if type(time)==datetime or time == None:
            timeDisplay = TimeDisplay(time) + " "
        elif type(time)==str and time=="":
            timeDisplay = ""
        else:
            timeDisplay = str(time) + " "
    else:
        timeDisplay = ""
    
    if hCom != None and info.find(hCom.port) == -1 and MODE != DEMO_MODE:
        info = hCom.port+info

    acis_print(timeDisplay + str(info))

def SafePrintLog( Msg ):
    "goal of the method : This method displays information"
    "INPUT : "
    "OUTPUT : "
    
    acis_print(str(Msg))

def ascii2print(inputstring, mode="symbol"):

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

def get_ini_value ( file_path, sections, name ):    
    if os.path.isfile(file_path):
        acis_print("\nRead %s:%s from %s\n" % ( sections, name, file_path ))        
        Parser = configparser.RawConfigParser()
        found = Parser.read(file_path)        
        if not Parser.has_section(sections):
            acis_print("\nNo Section %s in %s  !!!" % ( str(sections), file_path ))
        if not Parser.has_option(sections, name):
            acis_print("\nNo Name %s udner %s in %s  !!!" % ( name, str(sections), file_path ))

        Parser = configparser.ConfigParser()
        found = Parser.read(file_path)
        value = Parser.get(sections, name)
        return value.strip("\"'")
    else:
        acis_print("\%s NOT exits !!!\n" % file_path)
        return ''

def AcisDetectCom(port, timeout=2000, logmsg="logmsg"):
    start_time = datetime.now()
    flag_linebreak = 0
    #print "Detect COM port"
    while 1:
        try:
            s = serial.Serial(port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=False, rtscts=False, writeTimeout=None, dsrdtr=False)
            if logmsg=="logmsg":
                if flag_linebreak:
                    acis_print("")
                acis_print(port+" - port found") 
            # display time spent in receive
            diff_time = datetime.now() - start_time
            diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
            if logmsg=="logmsg":
                acis_print(" <"+str(timeout)+" @"+str(diff_time_ms)+"ms")
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
                    acis_print("")
                acis_print(port+" - port not found"+" <"+str(timeout)+" ms")
            break

def AcisReOpenCom(hCom, cfun_delay_time=2000):
    ComPort = hCom.port
    baudrate = hCom.baudrate
    bytesize = hCom.bytesize
    parity = hCom.parity
    stopbits = hCom.stopbits

    # for linux system, we need to save the usbport(key value) first, since it will delete in AcisClose() in dict usbport2ttycom.
    if os.name == 'posix':
        for key, value in usbport2ttycom.items():
            if value == ComPort:
                save_usbport = key
                break
    AcisClose(hCom)
    AcisSleep(cfun_delay_time)
    
    # for linux system AT port will be changed random, so we use the usbport(this is fixed) to find the AT port every time.
    if os.name == 'posix':
        ComPort = save_usbport
    #AcisDetectCom(ComPort,cfun_timeout)
    hCom = AcisOpen(ComPort,baudrate, bytesize, parity, stopbits) 
    return hCom

def getusbportdir(path, usbport):
    for home, dirs, files in os.walk(path):
        for subdir in dirs:
            if subdir == usbport:
                return os.path.join(home,usbport)
            getusbportdir(subdir, usbport)

def AcisGetUsbttyport(usbport, sysdir = r'/sys/devices/platform'):
    "goal of the method : This function finds the ttyUSB port based on usb busid,hub_id,device port and interface id"
    "INPUT: usbport: busid_hubid_port:deviceid_ifid"
    "       sysdir: /dev/ttyUSB* via the usbport find in sysdir, then we can know the ttyUSB number."
    "OUTPUT: /dev/ttyUSB* which specify the AT port in linux system"
    usbportdir = getusbportdir(sysdir, usbport)
    for home, dirs, file in os.walk(usbportdir):
        for subdir in dirs:
            if re.match('ttyUSB', subdir):
                return '/dev/' + subdir

def AcisOpen( port=None, baudrate=115200, bytesize=8, parity='N', stopbits=1, rtscts=False, OpenPortTimeout=2000, timeout=1, dsrdtr=False, xonxoff=False, interCharTimeout=None, write_timeout=None):
    "goal of the method : This function opens the serial port"
    "INPUT : port : string including the COM port (e.g. COM9), for linux system, this is usbport(e.g. 1-1.4:1.3)"
    "        baudrate : communication speed"
    "        OpenPortTimeout: Set a open port timeout value"
    "        timeout : Set a read timeout value."
    "        DTRDSR : Enable hardware (DSR/DTR) flow control."
    "        rtscts : enable RTS/CTS flow control"
    "        xonxoff : enable software flow control"
    "        interCharTimeout : Inter-character timeout, None to disable"
    "OUTPUT : COM port object"

    # for linux system AT port will be changed random, so we use the usbport(this is fixed) to find the AT port every time.
    if os.name == 'posix':
        start_time = datetime.now()
        while 1:
            try:
                ttyusbcom = AcisGetUsbttyport(port)
                SafePrint(None, None, "ttyUSB com port : %s"%ttyusbcom)
                diff_time = datetime.now() - start_time
                diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
                OpenPortTimeout = OpenPortTimeout - diff_time_ms
                break
            except Exception as e:
                SafePrint(None, None, "Find ttyUSB com port failed : %s"%e)
            time.sleep(1)
            sys.stdout.write("*")
            time.sleep(1)
            sys.stdout.write("*")
            flag_linebreak = 1
            # Count timeout
            diff_time = datetime.now() - start_time
            diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
            if diff_time_ms > OpenPortTimeout:
                if flag_linebreak:
                    acis_print("")
                acis_print(port+" - port not found"+" <"+str(timeout)+" ms")
                raise Exception(port+"-port not found"+" <"+str(timeout)+" ms")
        usbport2ttycom[port] = ttyusbcom
        port = ttyusbcom

    # validate parameter - rtscts
    flowcontrol = "Hardware"
    if type(rtscts) == type("string"):
        if rtscts not in ["Hardware", "None"]:
            acis_print("Invalid parameter for AcisOpen() - rtscts")
            acis_print("Option:")
            acis_print("\"Hardware\"", "\"None\"")
            acis_print("")
            rtscts = 1
            flowcontrol = "Hardware"
        if rtscts == "Hardware":
            rtscts = 1
            flowcontrol = "Hardware"
        if rtscts == "None":
            rtscts = 0
            flowcontrol = "None"
    AcisDetectCom(port,OpenPortTimeout, "nologmsg")
    try:
        hCom=None
        # for pySerial 3.4
        hCom = serial.Serial(port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts, write_timeout, dsrdtr, interCharTimeout)
        #add the new opened COM port to the list including all opened COM port
        list_hCom.append(hCom)
        SafePrint(None, hCom, "OPEN: Open the "+hCom.port+" @"+str(baudrate)+" "+str(bytesize)+str(parity)+str(stopbits)+" "+str(flowcontrol))
        time.sleep(1)

        global uartbuffer
        uartbuffer[hCom.port] = ""

        return hCom
    
    except serial.SerialException as val:
        acis_print(val)
        if ("%s"%val).startswith("could not open port "):
            SafePrint(None, None, "ERROR Could not open COM%d !"%(port))
            acis_print("hCom" + str(hCom))
        else:
            SafePrint(None, None, "ERROR : %s"%val)
            
    except AttributeError:
        SafePrint(None, None, "OPEN: Busy for "+hCom.port+"!")

def AcisSleep(millisecond, silent=False):
    "goal of the method : this method sleep during x milliseconds"
    "INPUT : milliseconds (ms), sleep duration"
    "                silent, flag to know if a comment shall be displayed or not"
    "OUTPUT : none"
    try:
        if not(silent):
            SafePrint(None, None, "SLEEP: Start sleep for %d milliseconds" % millisecond)
        time.sleep(millisecond/1000.0)
        if not(silent):
            SafePrint(None, None, "SLEEP: End sleep")
    
    except SystemExit:
        raise SystemExit
    
    except Exception as e:
        acis_print(e)

def AcisClose(hCom):
    "goal of the method : This method closes a COM port"
    "INPUT : hCom : COM port object"
    "OUTPUT : none"
    try:
    #print "close com port ", hCom.port
        #hCom.setDTR(0)
        #hCom.setDTR(1)
        ComPort = hCom.port
        hCom.close()    
        list_hCom.remove(hCom)

        # for linux system, delete the usbport in dict usbport2ttycom.
        if os.name == 'posix':
            for key, value in usbport2ttycom.items():
                if value == ComPort:
                    find_usbport = key
                    break
            usbport2ttycom.pop(find_usbport)

        SafePrint(None, hCom, "CLOSE: Close the "+hCom.port)
    except Exception as e:                 
        acis_print(e)
        SafePrint(None, hCom, "CLOSE: Error for "+hCom.port)

def AcisSendAT(hCom, cmd, printmode="symbol"): 
    "goal of the method : this method sends an AT command on a COM port"
    "INPUT : hCom : COM port object"
    "        cmd : AT command to send"
    "OUTPUT : none"
    hCom.write(cmd.encode('utf-8'))
    time.sleep(0.1)

    if SndRcvTimestamp:
        timestamp = TimeDisplay()+" "
    else:
        timestamp = ""
    # print_mutex.acquire() 
    # myColor = colorLsit[6]  # blue
    # print timestamp+"Snd COM"+ str(hCom.port+1)+" ["+ascii2print(cmd,printmode)+"]"
    # myColor = colorLsit[8]  # black
    # print_mutex.release() 
    LogMsg = timestamp+"Snd COM "+ hCom.port+" ["+ascii2print(cmd,printmode)+"]"
    SafePrintLog(LogMsg)

def AcisWaitResp(hCom, waitpattern, timeout=60000, log_msg="logmsg", printmode="symbol"): 
    "goal of the method : this method waits for the data received from Com port"
    "INPUT : hCom : COM port object"
    "        waitpattern : the matching pattern for the received data"
    "        timeout (ms) : timeout between each received packet"
    "        log_msg : option for log message"
    "OUTPUT : Received data (String)"

    start_time = datetime.now()
    com_port_name = hCom.port
    if log_msg == "debug":
        #print start_time
        print(start_time)
    global uartbuffer
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
        SafePrintLog("")
        SafePrintLog("Wait responses in %s ms" % str(timeout))
        SafePrintLog("")

    displaybuffer = ""
    displaypointer = 0
    while 1:
        # Read data from UART Buffer
        if hCom.in_waiting>0:
            uartbuffer[hCom.port] += hCom.read(hCom.in_waiting).decode('utf-8','ignore')
            if log_msg == "debug":
                #myColor = colorLsit[7]
                #print "Read data from UART buffer:", uartbuffer[hCom.port].replace("\r","<CR>").replace("\n","<LF>")
                #print "Read data from UART buffer:", ascii2print(uartbuffer[hCom.port],printmode)
                LogMsg = "Read data from UART buffer: "+ascii2print(uartbuffer[hCom.port],printmode)
                SafePrintLog(LogMsg)
        # Match response
        # Loop for each character
        for (i,each_char) in enumerate(uartbuffer[hCom.port]) :
            if log_msg == "debug":
                #myColor = colorLsit[7]
                #print i, uartbuffer[hCom.port][:i+1].replace("\r","<CR>").replace("\n","<LF>").replace("\n","<LF>")
                #print i, ascii2print(uartbuffer[hCom.port][:i+1],printmode)
                LogMsg = str(i)+" "+ascii2print(uartbuffer[hCom.port][:i+1],printmode)
                SafePrintLog(LogMsg)
            # display if matched with a line syntax
            displaybuffer = uartbuffer[hCom.port][displaypointer:i+1]
            line_syntax1 = "*\r\n*\r\n"
            line_syntax2 = "+*\r\n"
            line_syntax3 = "\r\n> "
            if fnmatch.fnmatchcase(displaybuffer, line_syntax1) or \
                fnmatch.fnmatchcase(displaybuffer, line_syntax2) or \
                fnmatch.fnmatchcase(displaybuffer, line_syntax3) :
                # display timestamp
                if SndRcvTimestamp:
                    timestamp = TimeDisplay() + " "
                # display data
                #myColor = colorLsit[7]
                #received_data = displaybuffer.replace("\r","<CR>").replace("\n","<LF>").replace("\x15","<NAK>").replace("\x06","<ACK>").replace("\x00","<NULL>")
                received_data = ascii2print(displaybuffer,printmode)
                #print timestamp+"Rcv COM", com_port_name, "["+received_data+"]",
                LogMsg = timestamp+"Rcv COM "+com_port_name+" ["+received_data+"] "
                displaypointer = i+1
                flag_printline = True

            # match received response with waitpattern
            for (each_elem) in waitpattern:
                receivedResp = uartbuffer[hCom.port][:i+1]
                expectedResp = each_elem
                if fnmatch.fnmatchcase(receivedResp, expectedResp):
                    flag_matchstring = True
                    break
            if flag_matchstring:
                # display the remaining matched response when waitpettern is found
                displaybuffer = uartbuffer[hCom.port][displaypointer:i+1]
                if len(displaybuffer)>0:
                    # display timestamp
                    if SndRcvTimestamp:
                        timestamp = TimeDisplay() + " "
                    # display data
                    #myColor = colorLsit[7]
                    #received_data = displaybuffer.replace("\r","<CR>").replace("\n","<LF>").replace("\x15","<NAK>").replace("\x06","<ACK>").replace("\x00","<NULL>")
                    received_data = ascii2print(displaybuffer,printmode)
                    #print "Rcv COM", com_port_name, "["+received_data+"]",
                    LogMsg = timestamp+"Rcv COM "+str(com_port_name)+" ["+received_data+"] "
                    pass

                # display time spent in receive
                if RcvTimespent:
                    diff_time = datetime.now() - start_time
                    diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
                    #print " <"+str(timeout), " @"+str(diff_time_ms), "ms",
                    LogMsg += " <"+str(timeout)+" @"+str(diff_time_ms)+" ms "

                flag_printline = True

                # clear matched resposne in UART Buffer
                uartbuffer[hCom.port] = uartbuffer[hCom.port][i+1:]
                flag_matchrsp = True
                
                # break for Match response
                flag_matchrsp = True

            # print linebreak for EOL
            if flag_printline:
                flag_printline = False
                #print ""
                SafePrintLog(LogMsg)

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
                SafePrintLog(LogMsg)
            # display the remaining response when timeout
            displaybuffer = uartbuffer[hCom.port][displaypointer:]
            if len(displaybuffer)>0:
                # display timestamp
                if SndRcvTimestamp:
                    #myColor = colorLsit[7]
                    #print TimeDisplay(),
                    timestamp = TimeDisplay() + " "
                # display data
                #myColor = colorLsit[7]
                #received_data = receivedResp.replace("\r","<CR>").replace("\n","<LF>").replace("\x15","<NAK>").replace("\x06","<ACK>").replace("\x00","<NULL>")
                received_data = ascii2print(receivedResp,printmode)
                #print "Rcv COM", com_port_name, " ["+received_data+"]"
                LogMsg = "Rcv COM "+str(com_port_name)+" ["+received_data+"]"
                SafePrintLog(LogMsg)
                pass

            # clear all resposne in UART Buffer
            #myColor = colorLsit[8]
            receivedResp = uartbuffer[hCom.port]

            if flag_wait_until_timeout != True:
                if log_msg == "logmsg" or log_msg == "debug":
                    if len(receivedResp) > 0:
                        #print "\nNo Match! "+"@COM"+com_port_name+ " <"+str(timeout)+" ms\n"
                        LogMsg = "\nNo Match! "+"@COM"+com_port_name+" <"+str(timeout)+" ms\n"
                        SafePrintLog(LogMsg)
                    if len(receivedResp) == 0:
                        #print "\nNo Response! "+"@COM"+com_port_name+ " <"+str(timeout)+" ms\n"
                        LogMsg = "\nNo Response! "+"@COM"+com_port_name+ " <"+str(timeout)+" ms\n"
                        SafePrintLog(LogMsg)
            uartbuffer[hCom.port] = ""
            flag_timeout = True
        

        if flag_matchrsp:
            break
        if flag_timeout:
            break


    if log_msg == "debug":
        #print ""
        #print len(uartbuffer[hCom.port])
        #print "The remaining data in uartbuffer " + str((hCom.port + 1))  + " : [", uartbuffer[hCom.port].replace("\r","<CR>").replace("\n","<LF>"), "]"
        #print "The remaining data in uartbuffer " + str((hCom.port + 1))  + " : [", ascii2print(uartbuffer[hCom.port],printmode), "]"
        SafePrintLog("")
        SafePrintLog(str(len(uartbuffer[hCom.port])))
        LogMsg = "The remaining data in uartbuffer " + str((hCom.port + 1))  + " : [", ascii2print(uartbuffer[hCom.port],printmode), "]"
        SafePrintLog(LogMsg)
    return receivedResp

def AcisMatchResp(resp, keywords, condition="wildcard", update_result="critical", log_msg="logmsg", printmode="symbol"):
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
        SafePrintLog( "Invalid parameter for AcisMatchResp() - condition")
        SafePrintLog( "Option:" )
        SafePrintLog( "\"wildcard\"", "\"match_all_order\"", "\"match_all_disorder\"", "\"contain_all_order\"", "\"contain_all_disorder\"", "\"contain_anyone\"", "\"not_contain_anyone\"" )
        SafePrintLog( "" )
        condition = "wildcard"

    # validate parameter - update_result
    if update_result not in ["critical", "not_critical"]:
        SafePrintLog("Invalid parameter for AcisMatchResp() - update_result")
        SafePrintLog("Option:")
        SafePrintLog("\"critical\"", "\"not_critical\"")
        SafePrintLog("")
        update_result = "critical"

    # validate parameter - log_msg
    if log_msg not in ["logmsg", "nologmsg", "debug"]:
        SafePrintLog("Invalid parameter for AcisMatchResp() - log_msg")
        SafePrintLog("Option:")
        SafePrintLog("\"logmsg\"", "\"nologmsg\"", "\"debug\"")
        SafePrintLog("")
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
                    SafePrintLog("")
                    SafePrintLog("Expected Response: %s" % ascii2print(expectedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                    SafePrintLog("Received Response: %s" % ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                    SafePrintLog("")
                if len(keywords)>1:
                    SafePrintLog("")
                    SafePrintLog("Expected Response: %s" % ascii2print(keywords[0],printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                    for (i,each_elem) in enumerate(keywords):
                        if i == 0:
                            pass
                        if i >0:
                            SafePrintLog("Expected Response: %s" % ascii2print(each_elem,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                    SafePrintLog("Received Response: %s" % ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                    SafePrintLog("")
    # 2
    if condition=="match_all_order":
        if log_msg == "debug":
            SafePrintLog("Check if response match all keywords in order: ( match without extra char. )")
        receivedResp = resp
        expectedResp = ""
        for (i,each_keyword) in enumerate(keywords) :
            expectedResp += keywords[i]
        matched = fnmatch.fnmatchcase(receivedResp, expectedResp)
        if matched == 0 :
            if log_msg == "logmsg" or log_msg == "debug":
                SafePrintLog("")
                SafePrintLog("No Match!! (match_all_order)")
                SafePrintLog("")
                SafePrintLog("Expected Response: %s" % ascii2print(expectedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                SafePrintLog("Received Response: %s" % ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                SafePrintLog("")

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
                debug_msg += str(i+1) + " " + ascii2print(each_conbination,printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- no match\n"
            else:
                debug_msg += str(i+1) + " " + ascii2print(each_conbination,printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- matched\n"

            # break in normal mode when result matched
            # normal mode >> matched result and break, debug mode >> list all conbination and result
            if matched == 1 :
                if log_msg != "debug":
                    break

        # display "No Match" when matching failed
        if matched == 1 :
            if log_msg == "debug":
                SafePrintLog( debug_msg)
        else:
            if log_msg == "logmsg" or log_msg == "debug":
                SafePrintLog("")
                SafePrintLog("No Match!! (match_all_disorder)")
                SafePrintLog("")
                SafePrintLog( debug_msg)

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
                SafePrintLog("")
                SafePrintLog( debug_msg)
                SafePrintLog( "Expected Response: %s" % ascii2print(expectedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                SafePrintLog("")
        else:
            if log_msg == "logmsg" or log_msg == "debug":
                SafePrintLog("")
                SafePrintLog("No Match!! (contain_all_order)")
                SafePrintLog("")
                SafePrintLog("Expected Response: %s" % ascii2print(expectedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                SafePrintLog("Received Response: %s" % ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"))
                SafePrintLog("")

    # 5
    if condition=="contain_all_disorder":
        debug_msg = ""
        debug_msg += "\nCheck if response contains all keywords without order:\n\n"
        #for (i,each_keyword) in enumerate(keywords) :
        #    print ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n")
        receivedResp = resp
        expectedResp = ""

        debug_msg += "Response: " + ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "\n"
        debug_msg += "Keywords:\n"
        flag_notfound = 0
        matched = 1

        for (i,each_keyword) in enumerate(keywords) :
            if resp.find(keywords[i]) >= 0:
                debug_msg += ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- found\n"
            else:
                debug_msg += ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- not found\n"
                flag_notfound = 1


        if flag_notfound == 0:
            matched = 1
            if log_msg == "debug":
                SafePrintLog( debug_msg)

        if flag_notfound == 1:
            matched = 0
            if log_msg == "logmsg" or log_msg == "debug":
                SafePrintLog("")
                SafePrintLog( "No Match!! (contain_all_disorder)")
                SafePrintLog("")
                SafePrintLog(debug_msg)

    # 6
    if condition=="contain_anyone":
        debug_msg = ""
        debug_msg += "\nCheck if response contains anyone of keywords: \n\n"
        #for (i,each_keyword) in enumerate(keywords) :
        #    print ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n")
        receivedResp = resp
        expectedResp = ""

        debug_msg += "Response: " + ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "\n"
        debug_msg += "Keywords:\n"
        flag_found = 0
        matched = 0
        for (i,each_keyword) in enumerate(keywords) :
            if resp.find(keywords[i]) >= 0:
                debug_msg += ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- found\n"
                flag_found = 1
            else:
                debug_msg += ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- not found\n"

        if flag_found == 1:
            matched = 1
            if log_msg == "debug":
                SafePrintLog(debug_msg)

        if flag_found == 0:
            matched = 0
            if log_msg == "logmsg" or log_msg == "debug":
                SafePrintLog("")
                SafePrintLog("No Match!! (contain_anyone)")
                SafePrintLog("")
                SafePrintLog( debug_msg)

    # 7
    if condition=="not_contain_anyone":
        debug_msg = ""
        debug_msg += "\nCheck that response do not contains anyone of keywords: \n\n"
        #for (i,each_keyword) in enumerate(keywords) :
        #    print ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n")
        receivedResp = resp
        expectedResp = ""

        debug_msg += "Response: " + ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "\n"
        debug_msg += "Keywords:\n"
        flag_found = 0
        matched = 1

        for (i,each_keyword) in enumerate(keywords) :
            if resp.find(keywords[i]) >= 0:
                debug_msg += ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- found\n"
                flag_found = 1
            else:
                debug_msg += ascii2print(keywords[i],printmode) + "      <-- not found\n"


        if flag_found == 0:
            matched = 1
            if log_msg == "debug":
                SafePrintLog( debug_msg)

        if flag_found == 1:
            matched = 0
            if log_msg == "logmsg" or log_msg == "debug":
                SafePrintLog("")
                SafePrintLog("No Match!! (not_contain_anyone)")
                SafePrintLog("")
                SafePrintLog( debug_msg)

    # udpate result to statOfItem
    if update_result == "critical":
        if matched == 0:
            global statOfItem
            statOfItem = 'NOK'
        else:
            global numOfSuccessfulResponse
            numOfSuccessfulResponse += 1.0
            pass
    else:
        if log_msg == "logmsg":
            SafePrintLog("\nNot Critical command\n")

    return matched

def AcisWaitnMatchResp(hCom, waitpattern, timeout, condition="wildcard", update_result="critical", log_msg="logmsg", printmode="symbol"):
    "goal of the method : combine AcisWaitResp() and AcisMatchResp()"
    "INPUT : hCom : COM port object"
    "        waitpattern : the matching pattern for the received data"
    "        timeout : timeout value in second"
    "OUTPUT : None"

    #myColor = colorLsit[8]

    # validate parameter - condition
    if condition not in ["wildcard"]:
        SafePrintLog("Invalid parameter for AcisWaitnMatchResp() - condition")
        SafePrintLog("Option:")
        SafePrintLog("\"wildcard\"")
        SafePrintLog("")
        SafePrintLog("AcisWaitnMatchResp() only support \"wildcard\" in \"condition\"")
        SafePrintLog("")
        condition = "wildcard"

    AcisWaitResp_response = AcisWaitResp(hCom, waitpattern, timeout, log_msg, printmode)
    match_result = AcisMatchResp(AcisWaitResp_response, waitpattern, condition, update_result, log_msg, printmode)
    return match_result

def AcisCleanBuffer(hCom):
        "goal of the method : this method clears the input buffer of hCom COM port instance"
        "INPUT : hCom, COM port instance"
        "OUTPUT : none"
        try:
                hCom.flushInput()
        
        except SystemExit:
                raise SystemExit
        
        except Exception as e:
                hCom.close()
                acis_print("CLEAR_BUFFER: Error!")
                acis_print(e)

def PRINT_TEST_RESULT(_test_id, _result=statOfItem):
    "goal of the method : this method displays information"
    "INPUT : _test_id, information to display (test case number)"
    "                _result, result of the test acse execution"
    "OUTPUT : none"
    #myColor = colorLsit[8]
    # if _result == 'OK':
            # print "===> " + str(_test_id) + "was successful"
    # else:
            # print "===> " + str(_test_id) + "was failed"
    acis_print("")
    if _result == 'OK':
        acis_print("Status " + str(_test_id) + ": PASSED")
    else:
        acis_print("Status " + str(_test_id) + ": FAILED")

def PRINT_START_FUNC(_string):
    "goal of the method : this method displays information"
    "INPUT : _string, information to display"
    "OUTPUT : none"
    #statOfItem = 'OK'
    acis_print("----------------------------------------------------------------------")
    acis_print(_string)
    acis_print("----------------------------------------------------------------------")
