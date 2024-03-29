from netmiko import ConnectHandler

from py import secrets

# this should be a list of all switches that participate in fabricpath
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
    ['b11nx1.tele.iastate.edu', 'b11nx1'],
    ['c12nx2.tele.iastate.edu', 'c12nx2'],
    ['b11nx2.tele.iastate.edu', 'b11nx2'],
    ['c12nx1.tele.iastate.edu', 'c12nx1'],
    ['b31nx1.tele.iastate.edu', 'b31nx1'],
    ['e63nx2.tele.iastate.edu', 'e63nx2'],
    ['b31nx2.tele.iastate.edu', 'b31nx2'],
    ['e63nx1.tele.iastate.edu', 'e63nx1'],
    ['e01nx1.tele.iastate.edu', 'e01nx1'],
    ['m22nx2.tele.iastate.edu', 'm22nx2'],
    ['e01nx2.tele.iastate.edu', 'e01nx2'],
    ['m22nx1.tele.iastate.edu', 'm22nx1'],
    ['h13nx1.tele.iastate.edu', 'h13nx1'],
    ['s07nx1.tele.iastate.edu', 's07nx1'],
    ['b31nx3.tele.iastate.edu', 'b31nx3'],
    ['e63nx3.tele.iastate.edu', 'e63nx3'],
    ['b31nx6.tele.iastate.edu', 'b31nx6'],
    ['e63nx6.tele.iastate.edu', 'e63nx6'],
    # ['rtr-b31nx6-vdc1.tele.iastate.edu', 'b31nx6-M3'],
    # ['rtr-e63nx6-vdc1.tele.iastate.edu', 'e63nx6-M3'],
    ['b31nx4.tele.iastate.edu', 'b31nx4'],
    ['b31nx5.tele.iastate.edu', 'b31nx5'],
    ['b31dmztest.tele.iastate.edu', 'b31dmztest'],
    ['e63dmztest.tele.iastate.edu', 'e63dmztest'],
    ['b31core.tele.iastate.edu', 'b31core'],
    ['e63core.tele.iastate.edu', 'e63core']

]

# first for loop cycles through all switches in list, must add password.
# opening a log file to verify vlan config after the changes
logfile = open('em_switch_ID.txt', 'w')

i = 0

for switch in switches:

    print("Starting switch %s." % switches[i][1])
    # netmiko connection line
    device = ConnectHandler(
        device_type='cisco_nxos',
        ip=switches[i][0],
        username=secrets.nx_uid,
        password=secrets.nx_pass
    )

    logfile.write("===================================================\n")

    logfile.write("%s.\n" % switches[i][1])

    switchid = device.send_command_expect('sho fabricpath switch-id | grep "[E]"')

    logfile.write(switchid + "\n")

    i += 1

# close logfile before opening next logfile
logfile.close()
