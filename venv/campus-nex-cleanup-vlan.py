from netmiko import ConnectHandler

from py import secrets

switches = [
    ['m22dc1.tele.iastate.edu', 'M22DC1'],
    ['b06dc1.tele.iastate.edu', 'B06DC1'],
    ['switch-b0695ay36u26nx56128.tele.iastate.edu', 'B06AY3656128'],
    ['switch-b0695au36u26nx56128.tele.iastate.edu', 'B06AU3656128'],
    ['switch-b0695bg27nx56128.tele.iastate.edu', 'B06BG27'],
    ['switch-b0695bm27nx56128.tele.iastate.edu', 'B06BM27'],
    ['switch-b0695aw23nx6001-01.tele.iastate.edu', 'B06AW23'],
    ['switch-b0695az23nx6001-01.tele.iastate.edu', 'B06AZ23'],
    ['switch-b0695ax46nx56128-01.tele.iastate.edu', 'B06AX46'],
    ['switch-b0695at46nx56128-01.tele.iastate.edu', 'B06AT46'],
    ['switch-b0695az49nx56128-01.tele.iastate.edu', 'B06AZ49'],
    ['switch-b0695at49nx56128-01.tele.iastate.edu', 'B06AT49'],
    ['switch-b0695ay36nx6001-01.tele.iastate.edu', 'B06AY366001'],
    ['switch-b0695au36nx5596-01.tele.iastate.edu', 'B06AU365596'],
    ['switch-m222175nx6001-01.tele.iastate.edu', 'M2201'],
    ['switch-m222175nx6001-02.tele.iastate.edu', 'M2202'],
    ['switch-m222175ag26nx56128.tele.iastate.edu', 'M22AG26'],
    ['switch-m222175ag28nx56128.tele.iastate.edu', 'M22AG28'],
    ['b31nx1.tele.iastate.edu', 'b31nx1'],
    ['b31nx2.tele.iastate.edu', 'b31nx2'],
    ['b31core.tele.iastate.edu', 'b31core'],
    ['e63nx1.tele.iastate.edu', 'e63nx1'],
    ['e63nx2.tele.iastate.edu', 'e63nx2'],
    ['e63core.tele.iastate.edu', 'e63core'],
    ['b11nx2.tele.iastate.edu', 'b11nx2'],
    ['b11nx1.tele.iastate.edu', 'b11nx1'],
    ['c12nx2.tele.iastate.edu', 'c12nx2'],
    ['c12nx1.tele.iastate.edu', 'c12nx1'],
    ['e01nx2.tele.iastate.edu', 'e01nx2'],
    ['e01nx1.tele.iastate.edu', 'e01nx1'],
    ['m22nx2.tele.iastate.edu', 'm22nx2'],
    ['m22nx1.tele.iastate.edu', 'm22nx1'],
    ['h13nx1.tele.iastate.edu', 'h13nx1'],
    ['s07nx1.tele.iastate.edu', 's07nx1'],
    ['b31nx3.tele.iastate.edu', 'b31nx3'],
    ['e63nx3.tele.iastate.edu', 'e63nx3'],
    ['b31nx4.tele.iastate.edu', 'b31nx4'],
    ['b31nx5.tele.iastate.edu', 'b31nx5'],
    ['b31dmztest.tele.iastate.edu', 'b31dmztest'],
    ['e63dmztest.tele.iastate.edu', 'e63dmztest'],
    ['b31nx6.tele.iastate.edu', 'b31nx6'],
    ['e63nx6.tele.iastate.edu', 'e63nx6']
]

vlans = [
    5,
    7,
    8,
    11,
    14,
    16,
    28,
    38,
    39,
    42,
    43,
    67,
    102,
    110,
    114,
    240,
    250,
    402,
    751,
    2005,
    2007,
    2008,
    2011,
    2012,
    2014,
    2016,
    2038,
    2039,
    2042,
    2043,
    2067,
    2102,
    2114,
    2145,
    2240,
    2402,
    2751
]

for switch in switches:
    device = ConnectHandler(device_type='cisco_nxos', ip=switch, username=secrets.nx_uid, password=secrets.nx_pass)
    logfile = file('%s.txt' % switch, 'w')

    for vlan in vlans:

        print("Removing VLAN %i" % vlan)

        output = device.send_command_expect('show vlan %i' % vlan)
        logfile.write(output)

        vlan_remove = [
            'no vlan ' + vlan
        ]
