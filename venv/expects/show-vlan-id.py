import pexpect
import re
import sys
import os

switch_ip=str(sys.argv[1])
switch_vlan=str(sys.argv[2])
switch_un='lmon'
switch_pw='H0rt0nH3rd?'

logfile=file('%s.log' % switch_ip, 'w')

child = pexpect.spawn('telnet %s' % switch_ip)
child.timeout=90
#child.logfile= logfile

devnull = open(os.devnull, 'w')
child.logfile = devnull

#child.logfile= sys.stdout


child.expect('USERNAME:')
child.sendline('lmon')
child.expect('PASSWORD:')
child.sendline('H0rt0nH3rd?')
child.expect('>')

child.sendline('terminal length 0')
child.expect('>')

child.sendline('show vlan id ' + switch_vlan)
child.expect('>')
data = ""
data = child.before

print data
next
print "----------------------------------------------------------------------------------------"

child.sendline('exit')
child.expect('Connection closed by foreign host.')

# child.interact()  give control of the child to the user

