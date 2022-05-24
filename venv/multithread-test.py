import re
import fileinput
import os
from netmiko import ConnectHandler
import subprocess
import threading
import time
import logging
import random


switches = [
    'm22dc1.tele.iastate.edu',
    'b06dc1.tele.iastate.edu',
    'switch-b0695ay36u26nx56128.tele.iastate.edu',
    'switch-b0695au36u26nx56128.tele.iastate.edu',
    'switch-b0695bg27nx56128.tele.iastate.edu',
    'switch-b0695bm27nx56128.tele.iastate.edu',
    'switch-b0695aw23nx6001-01.tele.iastate.edu',
    'switch-b0695az23nx6001-01.tele.iastate.edu',
    'switch-b0695ax46nx56128-01.tele.iastate.edu',
    'switch-b0695at46nx56128-01.tele.iastate.edu',
    'switch-b0695az49nx56128-01.tele.iastate.edu',
    'switch-b0695at49nx56128-01.tele.iastate.edu',
    'switch-b0695ay36nx6001-01.tele.iastate.edu',
    'switch-b0695au36nx5596-01.tele.iastate.edu',
    'switch-m222175nx6001-01.tele.iastate.edu',
    'switch-m222175nx6001-02.tele.iastate.edu',
    'switch-m222175ag26nx56128.tele.iastate.edu',
    'switch-m222175ag28nx56128.tele.iastate.edu',
    'b31nx1.tele.iastate.edu',
    'b31nx2.tele.iastate.edu',
    'b31core.tele.iastate.edu',
    'e63nx1.tele.iastate.edu',
    'e63nx2.tele.iastate.edu',
    'e63core.tele.iastate.edu',
    'b11nx2.tele.iastate.edu',
    'b11nx1.tele.iastate.edu',
    'c12nx2.tele.iastate.edu',
    'c12nx1.tele.iastate.edu',
    'e01nx2.tele.iastate.edu',
    'e01nx1.tele.iastate.edu',
    'm22nx2.tele.iastate.edu',
    'm22nx1.tele.iastate.edu',
    'h13nx1.tele.iastate.edu',
    's07nx1.tele.iastate.edu',
    'b31nx3.tele.iastate.edu',
    'e63nx3.tele.iastate.edu',
    'b31nx4.tele.iastate.edu',
    'b31nx5.tele.iastate.edu',
    'b31dmztest.tele.iastate.edu',
    'e63dmztest.tele.iastate.edu',
    'b31nx6.tele.iastate.edu',
    'e63nx6.tele.iastate.edu',
]

# percentage = float(100)/float(len(vlans))
# y = 0


def vlan_script(switch):

    vlans = [
        50,
        53,
        55,
        65,
        70,
        71,
        72,
        73,
        86,
        126,
        127,
        128,
        129,
        130,
        134,
        135,
        137,
        162,
        163,
        164,
        165,
        166,
        167,
        168,
        169,
        170,
        171,
        173,
        175,
        196,
        326,
        343,
        400,
        514,
        524,
        525,
        535,
        536,
        737,
        754,
        755,
        2050,
        2053,
        2055,
        2065,
        2070,
        2071,
        2072,
        2073,
        2086,
        2126,
        2127,
        2128,
        2129,
        2130,
        2134,
        2135,
        2137,
        2162,
        2164,
        2165,
        2166,
        2168,
        2169,
        2173,
        2175,
        2196,
        2257,
        2343,
        2754,
        2755
    ]

    logfile = file('VLAN-Test.txt', 'w')

    # Just initiates the connection to the switch
    device = ConnectHandler(device_type='cisco_nxos', ip=switch, username=secrets.nx_uid, password=secrets.nx_pass)

    for vlan in vlans:

        # print('%s progress: %f' % (switch, y))
        # print('{:%H:%M:%S}'.format(datetime.datetime.now()))

        # runs the command to the switch, stores in temp variable
        port = device.send_command_expect("sho vlan id %i" % vlan)

        # drops output to shell and iterates through via piping, not my favorite process but it works
        port2 = subprocess.Popen(["echo", port], stdout=subprocess.PIPE)
        port3 = subprocess.Popen(["sed", "1,3d"], stdin=port2.stdout, stdout=subprocess.PIPE)
        port4 = subprocess.Popen(["cut", "-c", "49-80"], stdin=port3.stdout, stdout=subprocess.PIPE)
        port5 = subprocess.Popen(["sed", "$d"], stdin=port4.stdout, stdout=subprocess.PIPE)
        port6 = subprocess.Popen(["sed", "$d"], stdin=port5.stdout, stdout=subprocess.PIPE)
        port7 = subprocess.Popen(["sed", "$d"], stdin=port6.stdout, stdout=subprocess.PIPE)
        port8 = subprocess.Popen(["sed", "$d"], stdin=port7.stdout, stdout=subprocess.PIPE)
        port9 = subprocess.Popen(["sed", "$d"], stdin=port8.stdout, stdout=subprocess.PIPE)
        port10 = subprocess.Popen(["sed", "$d"], stdin=port9.stdout, stdout=subprocess.PIPE)
        port11 = subprocess.Popen(["sed", "$d"], stdin=port10.stdout, stdout=subprocess.PIPE)
        port12 = subprocess.Popen(["sed", "$d"], stdin=port11.stdout, stdout=subprocess.PIPE)
        port13 = subprocess.Popen(["sed", "$d"], stdin=port12.stdout, stdout=subprocess.PIPE)
        port14 = subprocess.Popen(["sed", "$d"], stdin=port13.stdout, stdout=subprocess.PIPE)

        # regex to recognize the commas, spaces, and line breaks
        pattern = re.compile("^\s+|\s*,\s*|\\n|\s+$")
        # creates an array where the output above gets split into array elements, including ranges
        # (i.e., 7-9 could exist)
        port_array = [x for x in pattern.split(port14.communicate()[0]) if x]

        fp_ports = []
        ce_ports = []

        for port in port_array:
            output = device.send_command_expect("show run interface %s" % port)
            # logfile.write(output)
            if "mode fabricpath" in output:
                fp_ports.append(port)
            else:
                ce_ports.append(port)

        logfile.write('------------------------------------------------------------------- \n')
        logfile.write('%s vlan %s %s  \n' % (switch, vlan, port_array))
        logfile.write('------------------------------------------------------------------- \n')
        if fp_ports == []:
            logfile.write("No Fabricpath Ports for vlan %s on %s \n" % (vlan, switch))
        else:
            logfile.write("For VLAN %s on %s, Fabricpath ports exists on %s \n" % (vlan, switch, fp_ports))
        if ce_ports == []:
            logfile.write("No Classic Ethernet Ports for vlan %s on %s \n" % (vlan, switch))
        else:
            logfile.write("For VLAN %s on %s, Classic Ethernet ports exists on %s \n" % (vlan, switch, ce_ports))

        # y = y + percentage

    # print('progress: %f' % y)
    # print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    # print('Task Complete!')

threads = []
for line in switches:
    t = threading.Thread(target=vlan_script, args=(line,))
    threads.append(t)
    t.start()
