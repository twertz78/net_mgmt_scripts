import pexpect
import re
import sys
import os

switch_ip=str(sys.argv[1])
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

child.sendline('show cdp neighbors')
child.expect('>')
data = ""
data = child.before

#print data
print
#print "CDP neighbors for " + switch_ip
print '\033[92m' + switch_ip + "'s" + '\033[0m' +" CDP neighbors, excluding APs"
print "----------------------------------------------------------------------------------------"

# take the output and build a python list for each CDP entry.  Had to get creative since Cisco outputs two lines for each CDP entry.
last_line = sum(1 for line in data.splitlines())
i = 0
cdp_line_part_two_regex = re.compile('^                 ')
#cdp_device_is_an_ap_regex = re.compile('^ap-')
#cdp_device_is_an_unconfigured_ap_regex = re.compile('^AP')
last_header_line = 7
for line in data.splitlines():
	i += 1
	if line == 'Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID':
		last_header_line = i
	if not (i > 0 and i < last_header_line or i == last_line):
		if cdp_line_part_two_regex.search(line) is not None:
			single_line = single_line + line
			line_list = single_line.split()
			#if not cdp_device_is_an_ap_regex.search(line_list[0]):
			#if not cdp_device_is_an_ap_regex.search(line_list[0]):
				#print "#######"+str(line_list)+"#######"
				#this split routine is ghetto.  I wanted to have this output the far-end's interface but its location in the output isn't splittable on whitespace.  I'm going to defer splitting this until I need it.  The following line works 95% of the time though.
				#print line_list[0]+"\t"+line_list[1]+line_list[2]+"\t"+line_list[6]+"\t"+line_list[7]+line_list[8]
				#print line_list[0]+"\t"+line_list[1]+line_list[2]
				# set the first field to 40 characters for better formatting
				#print "%-40s" % line_list[0]+"\t"+line_list[1]+line_list[2]
			print "%-40s" % line_list[0]+"\t"+line_list[1]+line_list[2]
		else:
			single_line = ""
			single_line = line
next

print "----------------------------------------------------------------------------------------"

child.sendline('exit')
child.expect('Connection closed by foreign host.')

# child.interact()  give control of the child to the user

