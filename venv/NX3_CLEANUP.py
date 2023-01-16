from datetime import datetime

from netmiko import ConnectHandler

from py import secrets

# this should be a list of all switches that participate in fabricpath
switches = [

    ['b31nx3.tele.iastate.edu', 'b31nx3'],
    ['e63nx3.tele.iastate.edu', 'e63nx3'],
]

vlans = [
    407,
    1501,
    1502,
    1503,
    1504,
    1505,
    1506,
    1507,
    1508,
    1509,
    1510,
    1511,
    1512,
    1513,
    1514,
    1515,
    1516,
    1517,
    1518,
    1519,
    1520,
    1521,
    1522,
    1523,
    1524,
    1525,
    1526,
    1527,
    1528,
    1529,
    1530,
    1531,
    1532,
    1533,
    1534,
    1535,
    1550,
    1551,
    1552,
    1553,
    1554,
    1802,
    1804,
    1806,
    1808,
    1810,
    1812,
    1814,
    1816,
    1818,
    1820,
    1822,
    1824,
    1826,
    1828,
    1830,
    1832,
    1834,
    1836,
    1838,
    1840,
    1842,
    1844,
    1846,
    1848,
    1850,
    1852,
    1854,
    1856,
    1858,
    1860,
    1862,
    1864,
    1868,
    1872,
    1876,
    1884,
    1888,
    1892,
    1908,
    1910,
    1912,
    1916,
    1924,
    1932,
    1934,
    1940,
    1948,
    1956,
    1964,
    1972,
    1980

]

i = 0

# Next three lines are for "time remaining" messages printed to screen as program runs
start_time = datetime.now()
total_parts = len(switches) * len(vlans)
completed_parts = 0

# first for loop cycles through all switches in list, must add password in password variable (encrypted) above.
for switch in switches:

    print("******************************")
    print("Starting switch %s." % switches[i][1])
    print("******************************")

    # netmiko connection line
    device = ConnectHandler(
        device_type='cisco_nxos',
        ip=switches[i][0],
        username=secrets.nx_uid,
        password=secrets.nx_pass
    )
    # opening a log file to verify vlan config after the changes
    logfile = open('%s.txt' % switches[i][1], 'w')

    logfile.write("===================================================\n")

    for vlan in vlans:

        logfile.write("Configuring VLAN %s.\n" % vlan)

        sho_run_vlan = device.send_command("sho run vlan %s" % vlan)  # | inc active | cut -c -37
        sho_int_vlan = device.send_command("sho run interface vlan%s" % vlan)

        # Removing SVI
        print("Removing SVI for VLAN %i" % vlan)
        svi_remove = [
            'no interface vlan ' + str(vlan)
        ]
        device.send_config_set(svi_remove)

        # Removing VLAN
        print("Removing VLAN %i" % vlan)
        vlan_remove = [
            'no vlan ' + str(vlan)
        ]
        device.send_config_set(vlan_remove)

        logfile.write("*********************\n")
        logfile.write(sho_run_vlan)
        logfile.write(sho_int_vlan)
        logfile.write("VLAN %s removed.\n" % vlan)
        logfile.write("*********************\n")

        logfile.write("\n")
        logfile.write("\n")
        logfile.write("===================================================\n")

        # Next block is for "time remaining" messages printed to screen as program runs
        completed_parts += 1
        current_time = datetime.now()
        et = current_time - start_time
        elapsed_time = et.seconds
        estimated_time = elapsed_time * total_parts / completed_parts
        time_to_completion = estimated_time - elapsed_time
        hours = time_to_completion / 3600
        minutes = (time_to_completion % 3600) / 60
        seconds = (time_to_completion % 3600) % 60
        print("Time left %i hours, %i minutes, and %i seconds" % (hours, minutes, seconds))

    i += 1

    # close logfile before opening next logfile
    logfile.close()
