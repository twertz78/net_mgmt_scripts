""" Used to correctly add VLANs to devices.
Use: Manual modification of both the 'switches' and the 'vlans' variables is required.
local topology identifier is set to topology 6
TODO: changes to make the local topology more dynamic where needed
"""


from netmiko import ConnectHandler

from py import nodes, secrets

# this is imported in case we want to add time.sleep() to anything
# this should be a list of all switches that are in topology 6
switches = nodes.e63b31 + nodes.b31e63 + nodes.b11c12 + \
           nodes.c12b11 + nodes.m22e01 + nodes.e01m22 + \
           nodes.s07h13 + nodes.b31nx5 + nodes.be + \
           nodes.core + nodes.datacenterdevices

# this is the VLAN config that is normalized across the DC switches
# format ['vlan id', 'vlan name', [if fabricpath, have 'mode fabricpath', if classic ethernet have blank], 'TRUE' =
#          vlan is in local topology OR 'FALSE' if VLAN is in topology 0]
vlans = [
    ['410', 'ITNET_OOB_MGMT', 'mode fabricpath', 'FALSE'],
]

# first for loop cycles through all switches in list

j = 0

for switch in switches:
    # Have to set the value of i outside of the loop
    i = 0
    # netmiko connection line
    device = ConnectHandler(
        device_type='cisco_nxos',
        ip=switches[j][0],
        username=secrets.nx_uid,
        password=secrets.nx_pass
    )
    print("Starting %s." % switches[j][1])
    # opening a log file to verify vlan config after the changes
    logfile = file('%s.txt' % switches[j][1], 'w')
    # get initial topology configuration to compare as it changes.
    output = device.send_command_expect('show fabricpath isis vlan-range')
    logfile.write(output)
    # second for loop cycles through the vlan multidimensional array. Note that
    # we are using "send_command_expect", this will not process the next step until
    # the first step finishes (netmiko waits to see the correct prompt).
    for vlan in vlans:

        # apparently you have to build a configuration set in netmiko to make
        # child configurations...
        vlan_config = [
            'vlan ' + vlans[i][0],
            'name ' + vlans[i][1],
            vlans[i][2]
        ]

        device.send_config_set(vlan_config)

        # config of VLAN complete, now doing a show command to verify accuracy
        output = device.send_command_expect('show vlan id ' + vlans[i][0])
        logfile.write(output)

        # This if statement checks if the array states the VLAN should be in topology 6
        # if it is, it adds that vlan to topology 6 on the switch. if not, the loop is
        # skipped.
        if vlans[i][3] == 'TRUE':
            fp_config = [
                'fabricpath topology 6',
                'member vlan ' + vlans[i][0]
            ]

            device.send_config_set(fp_config)

        # config of topology should now have the vlan added if it wasn't right,
        # should be able to compare to previous
        output = device.send_command_expect('show fabricpath isis vlan-range')
        logfile.write(output)

        # Change reference in array to next VLAN config before loop starts over
        i += 1

    # close logfile before opening next logfile

    j += 1

    logfile.close()
