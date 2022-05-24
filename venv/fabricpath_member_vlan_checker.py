import os
import sys
import re
import time
from netmiko import ConnectHandler
from py import nodes, secrets

topology = int(sys.argv[1])

if topology == 31:
    switches = nodes.b31e63
elif topology == 63:
    switches = nodes.e63b31
elif topology == 11:
    switches = nodes.b11c12
elif topology == 12:
    switches = nodes.c12b11
elif topology == 22:
    switches = nodes.m22e01
elif topology == 1:
    switches = nodes.e01m22
elif topology == 7:
    switches = nodes.s07h13
elif topology == 35:
    switches = nodes.b31nx3e63nx3
elif topology == 20:
    switches = nodes.b31nx5
elif topology == 29:
    switches = nodes.be
elif topology == 0:
    switches = nodes.core
elif topology == 6:
    switches = nodes.datacenterdevices
else:
    sys.exit(
        "Your topology selection was not valid, please use 0 for core or 31, 63, 11, 12, 22, 1, 7, 35, 20, 29, or 6"
    )

# This is the "temporary" script that I have to create dynamically
new_file = file('temp_script.py', 'w')

i = 0

percent = float(100)/float(len(switches))

z = 0

# iterate through the switches to get the arrays built
for switch in switches:
    z = z + percent
    print('progress: %f' % z)

    # Just initiates the connection to the switch
    device = ConnectHandler(
        device_type='cisco_nxos',
        ip=switches[i][0],
        username=secrets.nx_uid,
        password=secrets.nx_pass
    )

    # runs the command to the switch, stores in temp variable
    vlans_in_topo = device.send_command_expect("sho run fabricpath | i 'member vlan' | cut -c 15-")
    # regex to recognize the commas
    pattern = re.compile("^\s+|\s*,\s*|\s+$|\n")
    # creates an array where the output above gets split into array elements, including ranges
    # (i.e., 7-9 could exist)
    vlans = [x for x in pattern.split(vlans_in_topo) if x]

    # empty array where we will put individual numbers into, breaking up ranges (i.e., splits up 7-9 into 7, 8, 9)
    array = []
    # iterates through the elements in the array vlan and adds individual numbers into the empty array
    for ele in vlans:
        if "-" in ele:
            l, r = ele.split("-")
            array.append(int(l))
            p = int(l) + 1
            while p < int(r):
                array.append(int(p))
                p = p + 1
            array.append(int(r))
        else:
            array.append(int(ele))

    array = str(array)

    new_file.write(switches[i][1] + ' = ' + array + '\n')
    new_file.write(switches[i][1] + '_set = set(' + switches[i][1] + ')' + '\n')

    i = i + 1

new_file.write("logfile = file('fabricpath_members.txt', 'w')" + '\n')
new_file.write('i = 0' + '\n')

new_file.write('while i < 4096:' + '\n')
new_file.write('    i = i + 1' + '\n')
i = i - 1

new_file.write('    if i ')
j = 0
while j < i:
    new_file.write('not in ' + switches[j][1] + "_set and i ")
    j = j + 1
new_file.write('not in ' + switches[j][1] + '_set:' + '\n')
new_file.write('        logfile.write("no switches have VLAN %i as a member of the local topology" % i)' + '\n')

new_file.write('    elif i ')
k = 0
while k < i:
    new_file.write('in ' + switches[k][1] + "_set and i ")
    k = k + 1
new_file.write('in ' + switches[k][1] + '_set:' + '\n')
new_file.write('        logfile.write("ALL SWITCHES HAVE VLAN %i AS A MEMBER OF THE LOCAL TOPOLOGY" % i)' + '\n')

new_file.write('    else:' + '\n')
new_file.write('        logfile.write("VLAN %i is a member of the local topology on switches: " % i)' + '\n')
m = 0
while m < i:
    new_file.write('        if i in ' + switches[m][1] + '_set:' + '\n')
    new_file.write('            logfile.write("' + switches[m][1] + ' ")' + '\n')
    m = m + 1
new_file.write('        if i in ' + switches[m][1] + '_set:' + '\n')
new_file.write('            logfile.write("' + switches[m][1] + ' ")' + '\n')

new_file.write('    logfile.write("\\n")')

new_file.close()

os.system('python temp_script.py')

while True:
    try:
        os.remove('temp_script.py')
        break
    except OSError:
        print("Unable to remove temp script, retrying")
        time.sleep(0.5)
