from netmiko import ConnectHandler

from py import secrets

switches = [
    'b06dc1.tele.iastate.edu',
    'm22dc1.tele.iastate.edu',
    'switch-b0695ay36u26nx56128.tele.iastate.edu',
    'switch-b0695au36u26nx56128.tele.iastate.edu',
    'switch-b0695bm27nx56128.tele.iastate.edu',
    'switch-b0695bg27nx56128.tele.iastate.edu',
    'switch-b0695at46nx56128-01.tele.iastate.edu',
    'switch-b0695ax46nx56128-01.tele.iastate.edu',
    'switch-b0695at49nx56128-01.tele.iastate.edu',
    'switch-b0695az49nx56128-01.tele.iastate.edu',
    'switch-b0695aw23nx6001-01.tele.iastate.edu',
    'switch-b0695az23nx6001-01.tele.iastate.edu',
    'switch-b0695ay36nx6001-01.tele.iastate.edu',
    'switch-b0695au36nx5596-01.tele.iastate.edu',
    'switch-m222175nx6001-01.tele.iastate.edu',
    'switch-m222175nx6001-02.tele.iastate.edu',
    'switch-m222175ag26nx56128.tele.iastate.edu',
    'switch-m222175ag28nx56128.tele.iastate.edu'
]

logfile = file('output.txt', 'w')


for switch in switches:
    device = ConnectHandler(device_type='cisco_nxos', ip=switch, username=secrets.nx_uid, password=secrets.nx_pass)
    output = device.send_command("sho vlan | sed 's/ .*//'")
    logfile.write(switch)
    logfile.write(output)

logfile.close()
