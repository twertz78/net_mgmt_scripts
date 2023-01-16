from netmiko import ConnectHandler

from py import secrets

switches = [
    ['switch-m222175ag26nx56128.tele.iastate.edu', 'M22AG26'],
    ['switch-m222175ag28nx56128.tele.iastate.edu', 'M22AG28'],
    ['b31nx1.tele.iastate.edu', 'b31nx1'],
    ['b31nx2.tele.iastate.edu', 'b31nx2'],
    ['b31core.tele.iastate.edu', 'b31core'],
]

i = 0
for switch in switches:
    device = ConnectHandler(
        device_type='cisco_nxos',
        ip=switches[i][0],
        username=secrets.nx_uid,
        password=secrets.nx_pass
    )
    vlans_in_topo = device.send_command_expect("show fabricpath isis topology 0 vlan-range")
    if "No VNI configured." in vlans_in_topo:
        print("No VNI")
    else:
        print("VNI")
    i += 1
