from netmiko import ConnectHandler
from py import nodes, secrets

switches = nodes.alldevices

i = 0
for switch in switches:

    print("Starting switch %s." % switches[i][1])

    device = ConnectHandler(
        device_type='cisco_nxos',
        ip=switches[i][0],
        username=secrets.nx_uid,
        password=secrets.nx_pass
    )

    vlan = [
        'vlan 2409',
        'mode fabricpath',
        'name F50_Aastra_GW'
    ]

    device.send_config_set(vlan)
    i += 1
