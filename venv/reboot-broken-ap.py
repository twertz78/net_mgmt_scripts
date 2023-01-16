import dns.resolver
from dns import reversename,resolver
import sys,time
import re
import pexpect
import requests
import csv
from netaddr import *
import argparse
from netmiko import ConnectHandler

# cisco-prime-api-getMAC.py
# takes an IP and returns its MAC.

TOUT=30
APIURL='https://cisco-prime.tele.iastate.edu/webacs/api/v2/data/ClientDetails.json'
USERNAME='tcalman'
PASSWORD='RHi7Q1uAsgcTBg0msVfl'

def getHostInfo (macaddress):
	#payload = {'macAddress': macaddress, '.full': 'true', '.case_sensitive': 'false', 'securityPolicyStatus': 'PASSED'}
	payload = {'macAddress': "contains(\"" + macaddress + "\")", '.full': 'true', '.case_sensitive': 'false', 'securityPolicyStatus': 'PASSED'}
	try:                                                                                                                                              
		r = requests.get(APIURL, params=payload, auth=(USERNAME , PASSWORD))
		r.raise_for_status()                                                                                                                      
	except requests.exceptions.Timeout:                                                                                                               
		# Maybe set up for a retry, or continue in a retry loop                                                                                   
		print("Timeout.")
		sys.exit(1)
	except requests.exceptions.TooManyRedirects:                                                                                                      
		# Tell the user their URL was bad and try a different oneA                                                                                
		print("Too many redirects")
		sys.exit(1)
	except requests.exceptions.HTTPError as e:                                                                                                        
		print("HTTP response " + str(e))
		print(r.json())
		sys.exit(1)
	except requests.exceptions.RequestException as e:                                                                                                 
		# catastrophic error. bail.                                                                                                               
		print(e)
		sys.exit(1)
		#this whole deal of getting all this is because prime returns a nested json structure
        clients = r.json() #loads the reply into a varible
#	print r.json()
        #print clients
        queryResponse =  clients.get('queryResponse')
		#print queryResponse
        entity =  queryResponse.get('entity')
		#print entity
        ClientDetailsDTO = entity[0]
		#print ClientDetailsDTO
        ClientDetailsDTO1 = ClientDetailsDTO.get('clientDetailsDTO')
		#print ClientDetailsDTO1
        switchName = ClientDetailsDTO1.get('deviceName')
		switchPort = ClientDetailsDTO1.get('clientInterface')
		return switchName, switchPort

MACAddress = str(sys.argv[1])

parser=argparse.ArgumentParser()
parser.add_argument("MACADDRESS", help='MAC address of the Access Point')
args=parser.parse_args()
MACAddress=args.MACADDRESS
MAC=args.MACADDRESS
MAC_VALID=re.compile(r""" (^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$) """,re.VERBOSE|re.IGNORECASE)

if MAC_VALID.match(MAC) is None:
	print("\033[91mInvalid MAC format.\033[0m")
	print(parser.print_help())
	exit()
else:
	try:
		switch_name, switch_port = getHostInfo(MAC)
		print(str(MAC) + " was found on " + str(switch_name) + " on " + str(switch_port), end=' ')
	#net_connect=ConnectHandler(device_type='cisco_ios', ip=switch_name, username=USERNAME, password=PASSWORD)
		#net_connect.send_config_set("interface " + switch_port)
		#net_connect.send_config_set("shut")
		#time.sleep(3)
		#net_connect.send_config_set("no shut")
		#net_connect.disconnect()
		
	except:
		print(str(MAC) + " was not found in the Prime API.")
		exit(1)


logfile=open("/tmp/"+ switch_name, 'a+')
shutcommands = ['interface ' + switch_port, 'shut']
noshutcommands = ['interface ' + switch_port, 'no shut']


net_connect=ConnectHandler(
	device_type='cisco_ios',
	ip=switch_name,
	username=USERNAME,
	password=PASSWORD,
	secret='xB1iWoMlYQ0Qv9awLNOM1'
)
net_connect.enable()
#output = net_connect.send_config_set("interface " + switch_port)
output = net_connect.send_config_set(shutcommands)
logfile.write(output)
#output = net_connect.send_config_set("shut")
#logfile.write(output)

time.sleep(3)

output = net_connect.send_config_set(noshutcommands)
logfile.write(output)
output = net_connect.disconnect()
print("\033[92m Rebooted. \033[0m")

exit(0)
