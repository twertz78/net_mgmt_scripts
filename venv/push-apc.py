import dns.resolver
from dns import reversename,resolver
import sys,time
import re
import pexpect
import csv
from netaddr import *


TOUT=180
CRED_SEQ=0


def getHostMac(shorthostname):
	with open("/home/twertz/ups-config/for-netreg-ups") as search:
		for line in search:
			line = line.rstrip()  # remove '\n' at end of line
			if shorthostname in line:
				mac = EUI(line.split()[1])
		mac.dialect = mac_unix_expanded
		return re.sub(r":", " ", str(mac)).upper()

def getNextCredential(i):
	with open ("/home/twertz/ups-config/apc-credentials") as search:
		reader = csv.reader(search)
		if reader is None:
			# EOF
			return 1,1
		credentials = list(reader)
	# print "getNextCredential: " + str(i)
	USERNAME = credentials[i][0]
	PASSWORD = credentials[i][1]
	return USERNAME,PASSWORD

# print getNextCredential()

# CREDENTIAL = getNextCredential()

# print
IPADDRESS=str(sys.argv[1])
# print "IPADDRESS:       " + IPADDRESS
REVERSENAME=reversename.from_address(IPADDRESS)
# print "REVERSENAME:     " + str(REVERSENAME)
SHORTHOSTNAME=str(resolver.query(REVERSENAME, "PTR")[0]).split('.')[0]
# print "shorthostname:   " + shorthostname
LOCATION=re.sub(r"-.*","",re.sub(r'ups-','', SHORTHOSTNAME))
# print "LOCATION:        " + LOCATION

MACADDRESS=str(getHostMac(SHORTHOSTNAME))
# print "MACADDRESS:      " + MACADDRESS

# logfile=file('%s.log' % IPADDRESS, 'w')
logfile = open('apc-actions.log', 'a')


# WRITE THE CUSTOMIZED INI FILE TO /TMP
with open("/home/twertz/ups-config/config-template.ini", "r") as sources:
	lines = sources.readlines()
FILENAME = "/tmp/" + SHORTHOSTNAME + "-APC.ini"
with open(FILENAME, "w") as sources:
	for line in lines:
		line = re.sub(r'shorthostname', SHORTHOSTNAME, line)
		line = re.sub(r'LOCATION', LOCATION, line)
		line = re.sub(r'MACADDRESS', MACADDRESS, line)
		sources.write(line)


child = pexpect.spawn('ftp ' + IPADDRESS)

#child.logfile= sys.stdout
child.logfile= logfile

CRED_SEQ=0
while True:
		i = child.expect(
			[
				'530 Not logged in',
			 	'.*assword:.*',
				 '.*username*|.*Name.*',
			 	'.*230 User logged in.*',
			 	pexpect.EOF,pexpect.TIMEOUT
			],
			timeout=TOUT
		)
		if i == 0: # login failed. try something else.
			child.logfile.write("\n*** try different credential. ***\n")
			time.sleep(2)
			CRED_SEQ = CRED_SEQ + 1
			CREDENTIAL = getNextCredential(CRED_SEQ)
		if CREDENTIAL[0] == '999':
			child.logfile.write("\n *** Credential sets exhausted.  Giving up on logging in. *** /n")
			break
			child.logfile.write("\n*** trying: \'" + CREDENTIAL[0] + "' / '" + CREDENTIAL[1] + "'  ***\n")
			child.expect('>')
			child.sendline('user')
			child.logfile.write("Sending username '" + CREDENTIAL[0] + "'\n")
			child.expect('(username)')
			child.sendline(CREDENTIAL[0])
		elif i == 1: #send a password.
			child.logfile.write("\nSending Password '" + CREDENTIAL[1] + "' to " + IPADDRESS + "\n")
			child.sendline(CREDENTIAL[1])
		elif i == 2: #enter a username.
			CREDENTIAL = getNextCredential(CRED_SEQ)
			child.logfile.write("sending username " + CREDENTIAL[0])
			child.sendline(CREDENTIAL[0])
		elif i == 3: #we are logged in, do what we came here to do
			child.sendline ('put ' + FILENAME + ' config.ini')
			child.expect ('bytes sent in')
			time.sleep(1)
			child.sendline ('exit')
			child.expect('221')
			child.logfile.write("\n *** Connection will be gracefully closed. *** /n")
			with open("apc-success.log", "a") as myfile:
			myfile.write(IPADDRESS + "\n")
		elif i == 4:
			child.logfile.write("\nConnection to " + IPADDRESS + " closed")
			exit()
		elif i == 5: #timeout
			child.logfile.write("Connection to " + IPADDRESS + " Timeout")
			exit()




# child.expect ('Name .*: ')
# child.sendline ('apcadmin')
# child.expect ('Password:')
# child.sendline ('Wnttktlo!')
# child.expect ('ftp> ')
# child.sendline ('put /tmp/' + shorthostname + '-APC.ini config.ini')
# child.expect ('bytes sent in')
# child.sendline ('exit')
