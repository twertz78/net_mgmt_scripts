from datetime import datetime
from netmiko import ConnectHandler
from py import nodes, secrets

vlans = [
    410
]

switches = nodes.e63b31 + nodes.b31e63 + nodes.b11c12 + \
           nodes.c12b11 + nodes.m22e01 + nodes.e01m22 + \
           nodes.s07h13 + nodes.b31nx5 + nodes.be + \
           nodes.core + nodes.datacenterdevices

i = 0

# Next three lines are for "time remaining" messages printed to screen as program runs
start_time = datetime.now()
total_parts = len(switches) * len(vlans)
completed_parts = 0

# first for loop cycles through all allfpnodes.switches in list,
# must add password in password variable (encrypted) above.

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

        output = device.send_command("sho run vlan %s" % vlan)  # | inc active | cut -c -37

        print("Removing VLAN %i" % vlan)

        vlan_remove = [
            'no vlan ' + str(vlan)
        ]

        device.send_config_set(vlan_remove)

        logfile.write("*********************\n")
        logfile.write(output)
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
