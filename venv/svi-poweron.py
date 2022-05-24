import pexpect
import os
import time
from py import secrets

switch = "10.10.0.175"
timer = 20

logfile = file('%s.log' % switch, 'a')

child = pexpect.spawn('ssh %s@%s' % (secrets.nx_uid, switch))
child.timeout = 90

child.logfile = logfile
# output = open()

while True:

    i = child.expect(
        [
            'Are you sure you want to continue connecting*',
            '.*assword:.*|.*ASSWORD:.*|Enter PASSCODE*',
            '.*#.*',
            'USERNAME:*',
            '.*>.*',
            pexpect.EOF,
            pexpect.TIMEOUT
        ],
        timeout=timer
    )

    if i == 0:
        child.sendline("yes")
    elif i == 1:
        child.sendline(secrets.nx_pass)
    elif i == 2:
        child.sendline("terminal length 0")
        break
    elif i == 3:
        child.sendline(secrets.nx_uid)
    elif i == 4:
        child.sendline("enable")
        child.sendline(secrets.nx_pass)
        break
    elif i == 5:
        exit()
    elif i == 6:
        exit()

# ---------------------------------------------------------------------------------------------------

child.expect('#')
child.sendline("configure")

vlans = open('vlans.csv')

for each_vlan in vlans:

    # separates lines into individual components
    vlan, virt_gw_ip = each_vlan.split(",")

    child.logfile.write("--------------------VLAN %s--------------------" % vlan)

    # no shuts the VLAN, waits 3 seconds for it to come up before moving on
    child.expect('#')
    child.sendline("interface %s" % vlan)
    child.sendline("no shutdown")
    time.sleep(3)

    # looking to see if we can ping the layer 3 SVI address
    child.expect('#')
    ping = os.system("ping -c5 -i 0.2 -W 1 %s" % vlan)
    if ping != 0:
        child.logfile.write("cannot ping %s on vlan %s" % (virt_gw_ip, vlan))
        child.sendline("interface %s" % vlan)
        child.sendline("shutdown")
        break  # leave loop early
    else:
        child.logfile.write("Ping vlan %s successful" % vlan)

    # Looking to see if the HSRP interface is up
    child.expect('#')
    hsrp_down = child.sendline("show hsrp interface vlan %s | grep 'Interface Down' | wc line" % vlan)
    if hsrp_down == 0:
        child.logfile.write("HSRP successfully started for vlan %s" % vlan)
    else:
        child.logfile.write("HSRP not successfully started for vlan %s" % vlan)
        child.sendline("interface %s" % vlan)
        child.sendline("shutdown")

# Let HSRP switch back to B06DC1 as primary (has a 600s timeout)
time.sleep(600)

for each_vlan in vlans:

    vlan, virt_gw_ip = each_vlan.split(",")

    # Logging if B06DC1 is now the active HSRP
    hsrp_local_active = child.sendline("show hsrp interface vlan 6 | grep 'Local state is Active' | wc line")
    if hsrp_local_active == 0:
        child.logfile.write("HSRP not active on B06DC1 for vlan %s" % vlan)
    else:
        child.logfile.write("HSRP active on B06DC1 for vlan %s" % vlan)

child.sendline('exit')

vlans.close()
logfile.close()
