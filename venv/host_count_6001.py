import datetime
from netmiko import ConnectHandler
from py import nodes, secrets
import re

switches = nodes.b31wnx1e63wnx1
time_stamp = datetime.datetime.now()
today = datetime.datetime.date(time_stamp)
current_time = datetime.datetime.time(time_stamp)
i = 0

# iterate through the switches
for switch in switches:

    # Just initiates the connection to the switch
    device = ConnectHandler(
        device_type='cisco_nxos',
        ip=switches[i][0],
        username=secrets.nx_uid,
        password=secrets.nx_pass
    )

    h_t1 = device.send_command_expect("show hardware profile status | i i used | i i host4|host6 | ex LPM")
    h_t2 = h_t1
    h_t3 = h_t1
    h_t4 = h_t1

    u4 = re.compile("Used Unicast Host4 Entries in Host = ([0-9]{1,6})\.")
    u6 = re.compile("Used Unicast Host6 Entries in Host = ([0-9]{1,6})\.")
    m4 = re.compile("Used Multicast Host4 Entries in Host = ([0-9]{1,6})\.")
    m6 = re.compile("Used Multicast Host6 Entries in Host = ([0-9]{1,6})\.")

    uni_host4 = int(u4.search(h_t1).group(1))
    uni_host6 = int(u6.search(h_t2).group(1))
    multi_host4 = int(m4.search(h_t3).group(1))
    multi_host6 = int(m6.search(h_t4).group(1))
    total = (uni_host4 + (uni_host6 * 2) + multi_host4 + multi_host6)

    output = open('/home/twertz/%s_%s_host_count.csv' % (today, switches[i][1]), 'a+')
    output.write("%s, %s\n" % (current_time, total))
    output.close()

    i += 1
