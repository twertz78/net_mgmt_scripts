from netmiko import ConnectHandler

from py import secrets

logfile = file('vlan-ID-test.txt', 'w')

device = ConnectHandler(
    device_type = 'cisco_nxos',
    ip = 'switch-b0695at46nx56128-01.tele.iastate.edu',
    username = secrets.nx_uid,
    password = secrets.nx_pass
)

i = 1

while i < 10:
    output = device.send_command("sho vlan ID %s | inc active | cut -c -37" % i)
    logfile.write(output + "\n")
    i += 1

logfile.close()
