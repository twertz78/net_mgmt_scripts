import pexpect
import re
import sys
import os

SWITCH_IP=str(sys.argv[1])
SWITCH_UN='YOURUSERNAMEHERE'
SWITCH_PW='YOURPASSWORDHERE'
TOUT=60


logfile=file('%s.log' % SWITCH_IP, 'w')

child = pexpect.spawn('ssh %s@%s' % (SWITCH_UN,SWITCH_IP))
#child = pexpect.spawn('ssh %s' % SWITCH_IP)
child.timeout=90

child.logfile= logfile
output = open('show-cdp-neighbors.out', 'a')
#devnull = open(os.devnull, 'w')
#child.logfile = devnull

#child.logfile= sys.stdout

while True:
	i=child.expect(['Are you sure you want to continue connecting*','.*assword:.*|.*ASSWORD:.*','.*#.*',pexpect.EOF,pexpect.TIMEOUT],timeout=TOUT)
	if i==0:
       		child.logfile.write("\n*** New SSH key detected, auto accepting. ***\n")
       		child.sendline('yes')
	elif i==1:
        	child.logfile.write("Sending SSH Password to " + SWITCH_IP,)
        	child.sendline(SWITCH_PW)
        elif i==2: #we have an interactive shell
                child.logfile.write("connection done.")
                child.sendline('terminal length 0')
                break
	elif i==3:
        	child.logfile.write("Connection to " + SWITCH_IP + " Dropped")
        	exit()
	elif i==4: #timeout
        	child.logfile.write("Connection to " + SWITCH_IP + " Timeout")
        	exit()

child.expect('#')
child.sendline('show cdp neighbors')
child.expect('#')

data = ""
data = child.before

print
print '\033[92m' + SWITCH_IP + "'s" + '\033[0m' +" CDP neighbors, excluding APs"
print "----------------------------------------------------------------------------------------"

# take the output and build a python list for each CDP entry.  Had to get creative since Cisco outputs two lines for each CDP entry.
last_line = sum(1 for line in data.splitlines())
i = 0
cdp_line_part_two_regex = re.compile('^                 ')
cdp_device_is_an_ap_regex = re.compile('^ap-')
last_header_line = 7
for line in data.splitlines():
	i += 1
	if line == 'Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID':
		last_header_line = i
	if not (i > 0 and i < last_header_line or i == last_line):
		if cdp_line_part_two_regex.search(line) is not None:
			single_line = single_line + line
			line_list = single_line.split()
			if not cdp_device_is_an_ap_regex.search(line_list[0]):
				#print "#######"+str(line_list)+"#######"
				#this split routine is ghetto.  I wanted to have this output the far-end's interface but its location in the output isn't splittable on whitespace.  I'm going to defer splitting this until I need it.  The following line works 95% of the time though.
				#print line_list[0]+"\t"+line_list[1]+line_list[2]+"\t"+line_list[6]+"\t"+line_list[7]+line_list[8]
				#print line_list[0]+"\t"+line_list[1]+line_list[2]
				# set the first field to 40 characters for better formatting
				print "%-40s" % line_list[0]+"\t"+line_list[1]+line_list[2]
				output.write("%-40s" % line_list[0]+"\t"+line_list[1]+line_list[2] + "\n")
		else:
			single_line = ""
			single_line = line
next

print "----------------------------------------------------------------------------------------"
child.sendline('exit')

output.close()
