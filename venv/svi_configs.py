from netmiko import ConnectHandler
from datetime import datetime
from py import secrets

vlans = [
    '407',
    '1501',
    '1502',
    '1503',
    '1504',
    '1505',
    '1506',
    '1507',
    '1508',
    '1509',
    '1510',
    '1511',
    '1512',
    '1513',
    '1514',
    '1515',
    '1516',
    '1517',
    '1518',
    '1519',
    '1520',
    '1521',
    '1522',
    '1523',
    '1524',
    '1525',
    '1526',
    '1527',
    '1528',
    '1529',
    '1530',
    '1531',
    '1532',
    '1533',
    '1534',
    '1535',
    '1536',
    '1537',
    '1538',
    '1539',
    '1540',
    '1541',
    '1542',
    '1543',
    '1544',
    '1545',
    '1546',
    '1547',
    '1548',
    '1549',
    '1550',
    '1551',
    '1552',
    '1553',
    '1554',
    '1802',
    '1804',
    '1806',
    '1808',
    '1810',
    '1812',
    '1814',
    '1816',
    '1818',
    '1820',
    '1822',
    '1824',
    '1826',
    '1828',
    '1830',
    '1832',
    '1834',
    '1836',
    '1838',
    '1840',
    '1842',
    '1844',
    '1846',
    '1848',
    '1850',
    '1852',
    '1854',
    '1856',
    '1858',
    '1860',
    '1862',
    '1864',
    '1868',
    '1872',
    '1876',
    '1884',
    '1888',
    '1892',
    '1908',
    '1910',
    '1912',
    '1916',
    '1924',
    '1932',
    '1934',
    '1940',
    '1948',
    '1956',
    '1964',
    '1972',
    '1980',
    '1998',
    '1999'
]

switches = [
    ['b31nx6.tele.iastate.edu', 'b31nx6'],
    ['e63nx6.tele.iastate.edu', 'e63nx6'],
]

i = 0

percent = float(100)/float(len(switches))
percentage = percent/float(len(vlans))
y = 0

start_time = datetime.now()

total_parts = len(switches) * len(vlans)
completed_parts = 0

for switch in switches:
    logfile = open('%s.txt' % switches[i][1], 'w')

    print("******************************")
    print("Starting switch %s." % switches[i][1])
    print("******************************")

    device = ConnectHandler(
        device_type='cisco_nxos',
        ip=switches[i][0],
        username=secrets.nx_uid,
        password=secrets.nx_pass
    )

    for vlan in vlans:
        output = device.send_command("sho run int vlan%s" % vlan)
        logfile.write("VLAN %s " % vlan)
        logfile.write("%s : \n " % switches[i][1])
        logfile.write("%s \n" % output)
        logfile.write("********************************************* \n")

        y += percentage
        print('progress: %f' % y)

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

    logfile.close()
