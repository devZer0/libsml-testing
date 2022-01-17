```
#libsml-testing

this is a collection of SML messages from real-world Smart Meters

The Open-Source Smart-Metering community would like to get some realworld data 
from all those SML Smart Meters out there, so please submit some data from 
your SML capable device.


This is very valuable information to test SML parsers, to know about the 
capabilities of different Smart Meters and to get an impression on how good 
Smart Meters behave according to the specs.

Create dumps in binary and hex format from your smartmeter and submit those as 
follows:

1.  Do proper initialization of the serial interface via stty, vzlogger, 
    <your_favourite_metering_tool> (serial interface should remain initialized 
    after terminating vzlogger etc)

2.  Dump binary data to a file like this:  
    dd if=/dev/ttyUSB0 of=yoursmldump.bin bs=1 count=4096 iflag=fullblock

3.  Convert your .bin file into .hex like this: 
    cat yoursmldump.bin |hexdump -ve '1/1 "%.2X"' >yoursmldump.hex
    
    If you have sml data in hex format already, you can convert it into binary like this:
    cat yoursmldump.hex | xxd -r -p >yoursmldump.bin

4.  Name your files like this: <VENDOR>_<MODEL>-<MODELNR>.bin|hex, e.g. 
    EMH_eHZ-HW8E2AWL0EK2P.bin and EMH_eHZ-HW8E2AWL0EK2P.hex

5.  If you like, add some owner/contact information, so others may contact you 
    about your smart meter and ask questions (see FILES)

6.  Please submit your files via Pull-Request, see 
    https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests 
    If you don't like git or don't understand how to do that, you can send files via mail 
    to devzero AT web.de . 

7.  Discuss about SML with others on volkszaehler-dev@lists.volkszaehler.org.

8.  For decoding the binary sml data you can use the libsml parser example program from 
    https://github.com/volkszaehler/libsml
   
    Use it like this for example:
   
    $ cat ../../libsml-testing/EMH_eHZ-GW8E2A500AK2.bin | ./sml_server - | head -n10
    129-129:199.130.3*255#EMH#
    1-0:0.0.0*255#02280816#
    1-0:1.8.1*255#14798112.9#Wh
    1-0:1.8.2*255#2012.4#Wh
    0-0:96.1.255*255#0002280816#
    1-0:1.7.0*255#13.8#W
    129-129:199.130.3*255#EMH#
    1-0:0.0.0*255#02280816#
    1-0:1.8.1*255#14798113.0#Wh
    1-0:1.8.2*255#2012.4#Wh

9.  Do NOT use libsml from dailab github repo, as this is unmaintained. 
    Please use https://github.com/volkszaehler/libsml , this is the official and maintained version.
    Report Bugs to: https://github.com/volkszaehler/libsml/issues

10. If your sml program which should process binary sml does not support stdin, you can 
    feed binary sml via a serial fake device the following way. use that instead of 
    /dev/ttyUSB0 or /dev/ttyS0 
    Effectively, you simulate a serially attached smart meter this way

    get socat and execute
    # socat -d -d pty,raw,echo=0 pty,raw,echo=0

    socat will connect two pty's and output should look like this:

    # socat -d -d pty,raw,echo=0 pty,raw,echo=0
    2018/01/20 22:08:48 socat[8029] N PTY is /dev/pts/6
    2018/01/20 22:08:48 socat[8029] N PTY is /dev/pts/9
    2018/01/20 22:08:48 socat[8029] N starting data transfer loop with FDs [5,5] and [7,7]

    connect your favourite SML parser/tool to one of the pty's socat did attach to:

    # ./sml_server /dev/pts/6

    now feed a binary sml dump to the other pty's:

    # cat EMH_eHZ-GW8E2A500AK2.bin >/dev/pts/9

    you can throttle the data rate with "pv" (pipe viewer) to simulate serial line slowness:

    # cat EMH_eHZ-GW8E2A500AK2.bin | pv -L 9600 >/dev/pts/9

    now watch output from your favourite SML parser/tool or troubleshoot/debug...


   ```
