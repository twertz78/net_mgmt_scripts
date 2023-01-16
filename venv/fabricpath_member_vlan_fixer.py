
from datetime import datetime
from netmiko import ConnectHandler
from py import nodes, secrets

# FQDN name and a "common" name for each switch. the "common" name helps shorten output,
# whereas the FQDN name is needed for the connection
switches = nodes.datacenterdevices
# vlans that need to be removed from the fabricpath membership

vlans = [
    3078
]

# Create logfile
logfile = open('fabricpath_member_vlan_fixed.txt', 'w')
# ------------------------------------------------------------------------------------
# The following three lines are for time calculation
start_time = datetime.now()
total_parts = len(switches) * len(vlans)
completed_parts = 0
# ------------------------------------------------------------------------------------
# i is needed to iterate through the multidimensional switches array
i = 0
# iterate through the switches that need to be fixed
for switch in switches:
    # provides the user screen info
    print("******************************")
    print("Starting switch %s." % switches[i][1])
    print("******************************")
    # delineation/separator for switches in log file
    logfile.write("===================================================\n")

    # Just initiates the connection to the switch
    device = ConnectHandler(
        device_type='cisco_nxos',
        ip=switches[i][0],
        username=secrets.nx_uid,
        password=secrets.nx_pass
    )
    # iterate through the vlans that need to be checked/fixed
    for vlan in vlans:

        # runs the command to the switch, stores in temp variable
        test_vlan = device.send_command_expect("sho vlan id %s" % vlan)
        # separates the vlans in the log file, then adds the output
        logfile.write("*********************\n")
        logfile.write(test_vlan)
        # checks to see if the VLAN is or is not in database
        if "not found in current VLAN database" in test_vlan:
            # stores necessary commands to remove the vlan from local topology fabricpath membership
            remove_vlan = [
                'fabricpath topology 6',
                ('no member vlan %s' % vlan)
            ]
            # runs the commands
            device.send_config_set(remove_vlan)
            # adds changes to logfile
            logfile.write("VLAN %s removed.\n" % vlan)

        else:
            # screen alert and logfile message if vlan does exist
            print("vlan %s configured on device" % vlan)
            logfile.write("@@@@@*****-----vlan %s not removed, exists on device-----*****@@@@@" % vlan)
        logfile.write("*********************\n")
        # following 10 lines for calculating/displaying time remaining
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
    # increment to next block in the switch array
    i += 1
