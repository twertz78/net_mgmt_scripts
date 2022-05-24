from datetime import datetime
from netmiko import ConnectHandler
from py import nodes, secrets

# import pexpect
# import re

# devices to run commands against, first part is FQDN, second part is for a "common" name
switches = nodes.datacenterdevices

# commands to run
commands = [
    # !!!!!!!!DO NOT TRY TO USE THIS WITHOUT CLEANING UP THE EXTRA FOR LOOPS BELOW!!!!!!!!
    'show interface status up | grep Eth',
    'show interface description'

]

# ---------------------------------------------------------------------------------------
# initial time settings
start_time = datetime.now()
total_parts = len(switches) * len(commands)
completed_parts = 0
# ---------------------------------------------------------------------------------------

logfile = file('2019_05_08_interface_descriptions.csv', 'w')

i = 0
# iterate through each switch
for switch in switches:

    print("******************************")
    print("Starting switch %s." % switches[i][1])
    print("******************************")

    nxos_config = {
        'device_type': 'cisco_nxos',
        'ip': switches[i][0],
        'username': secrets.nx_uid,
        'password': secrets.nx_pass,
        'global_delay_factor': 0.25,
    }

    device = ConnectHandler(**nxos_config)

    logfile.write("************************************************************** \n")
    # iterate through the commands on each switch

    # for vdc in vdcs:
    device.send_config_set('attach module 5')

    for command in commands:
        # !!!!! EXTRA STUFF HERE!!!!!
        # -----This next 8 lines are for one special run --------
        # The lines put each new line of text into an array so a second command can be ran against it
        # initial_array = device.send_command_expect("%s" % command)
        # pattern = re.compile("\r\n|\r|\n")
        # second_array = [x for x in pattern.split(initial_array) if x]
        # blank_array = []
        # for ele in second_array:
        #     blank_array.append(str(ele))
        # print blank_array
        # -----------------------------
        # line below for troubleshooting
        # wait = input("stopped - any key continues")
        # -----------------------------

        # !!!!! ORIGINAL STUFF HERE!!!!!
        # Uncomment the following line to be back to "normal"
        output = device.send_command_expect("%s" % command)

        logfile.write("%s \n" % switches[i][1])
        logfile.write("%s \n" % command)
        # !!!!! EXTRA STUFF HERE!!!!!
        # -----This for/in statement is for one special run --------
        # for ele in blank_array:
        #     new_command = ('show run int %s' % ele)
        #     output = device.send_command_expect("%s" % new_command)
        #     logfile.write("%s \n" % output)
        # -----------------------------

        # !!!!! ORIGINAL STUFF HERE!!!!!
        # Uncomment the following line to be back to "normal"
        logfile.write("%s \n" % output)
        # un-comment the next line if you want to see the command outputs as they are generated
        # print("%s \n" % output)
        logfile.write("************************************************************** \n")

        # ---------------------------------------------------------------------------------------
        # time to completion script
        completed_parts += 1
        current_time = datetime.now()
        et = current_time - start_time
        elapsed_time = et.seconds
        estimated_time = elapsed_time * total_parts / completed_parts
        time_to_completion = estimated_time - elapsed_time
        hours = time_to_completion / 3600
        minutes = (time_to_completion % 3600) / 60
        seconds = (time_to_completion % 3600) % 60
        print("Time left %i:%i:%i" % (hours, minutes, seconds))
        # ---------------------------------------------------------------------------------------



    logfile.write("============================================================== \n")

    i += 1

logfile.write("************************************************************** \n")

logfile.close()
