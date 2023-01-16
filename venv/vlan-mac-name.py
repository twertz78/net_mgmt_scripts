from netmiko import ConnectHandler

from py import secrets

vlans = [
    '3',
    '13',
    '15',
    '22',
    '24',
    '45',
    '90',
    '96',
    '150',
    '155',
    '183',
    '184',
    '185',
    '186',
    '187',
    '193',
    '194',
    '198',
    '200',
    '201',
    '204',
    '207',
    '208',
    '213',
    '219'
]

logfile = open('vlan-output.txt', 'w')

device = ConnectHandler(
    device_type='cisco_nxos',
    ip='switch-b0695at46nx56128-01.tele.iastate.edu',
    username=secrets.nx_uid,
    password=secrets.nx_pass
)

for vlan in vlans:
    output1 = device.send_command("sho vlan id %s" % vlan)
    output2 = device.send_command("sho mac address-table vlan %s" % vlan)
    logfile.write(output1)
    logfile.write("MAC count:" + output2)


logfile.close()
