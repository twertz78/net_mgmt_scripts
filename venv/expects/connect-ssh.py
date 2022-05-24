#!/usr/bin/python
import pexpect
import re
import sys
import os
import time
import base64

SWITCH_IP = str(sys.argv[1])
SWITCH_UN = 'ttwertz'
SWITCH_PW = base64.b64decode("RHVyaGFtMjM4LURlc2s=")
ENABLE_PW = 'YOURENABLEHERE'
TOUT = 20

logfile = file('%s.log' % SWITCH_IP, 'w')

child = pexpect.spawn('ssh %s@%s' % (SWITCH_UN, SWITCH_IP))
child.timeout = 90

# child.logfile= sys.stdout
child.logfile = logfile
# child.logfile = devnull

while True:
	child.logfile = sys.stdout
	i = child.expect(['Are you sure you want to continue connecting*','.*assword:.*|.*ASSWORD:.*|Enter PASSCODE*','.*#.*','USERNAME:*','.*>.*',pexpect.EOF,pexpect.TIMEOUT],timeout=TOUT)
	child.logfile = logfile
	if i == 0:
		# child.logfile.write("\n*** New SSH key detected, auto accepting. ***\n")
       	child.sendline('yes')
elif i == 1:
		# child.logfile.write("Sending telnet pw to " + SWITCH_IP,)
        child.sendline(SWITCH_PW)
	elif i == 2: #we have an interactive shell
		# child.logfile.write("connection done.")
		child.sendline('terminal length 0')
		break
	elif i == 3:
		# child.logfile.write("sending username. ")
        child.sendline(SWITCH_UN)
	elif i == 4: #send enable
		# child.logfile.write("enable")
		child.sendline("enable")
		child.sendline(ENABLE_PW)
		break
	elif i == 5: #timeout
		# child.logfile.write("Connection to " + SWITCH_IP + " Dropped")
        exit()
	elif i == 6: #username
		# child.logfile.write("Connection to " + SWITCH_IP + " Timeout")
        exit()

child.logfile = logfile
child.interact()
