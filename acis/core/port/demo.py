#SUBSYSTEMS=="usb", DRIVERS=="GobiSerial", SYMLINK+="acis/slave/AT", ATTRS{bInterfaceNumber}=="03"

import re

f = open('./rules.txt', mode = 'r')

for line in f:
    print(line)
    #g = re.match(r"\s*SUBSYSTEMS==.*ATTRS{bInterfaceNumber}==\"03.*\"", line)
    #g = re.match(r"\s*SUBSYSTEMS==\"usb\",\s*DRIVERS==\"GobiSerial\",\s*SYMLINK\+=\"acis/slave/AT\",\s*ATTRS{bInterfaceNumber}==\"03\"\s*", line)
    g = re.match(r"\s*SUBSYSTEMS==\"usb\",\s*DRIVERS==\"GobiSerial\",\s*SYMLINK\+=\"(acis/(.*))/(.*)\",\s*ATTRS{bInterfaceNumber}==\"(.*)\"\s*",line)
    if g:
        print(">>>>>>>>>>>>")
        print(
        g.group(1),
        g.group(2),
        g.group(3),
        g.group(4))
        print("yes")
    else:
        print("no")
