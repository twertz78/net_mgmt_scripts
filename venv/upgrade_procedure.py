"""
2018-7-18
Built to automate uploading and checking for inconsistincies, etc.
"""

from datetime import datetime
from netmiko import ConnectHandler, file_transfer
from py import secrets

# FQDN name and a "common" name for each switch. the "common" name helps shorten output,
# whereas the FQDN name is needed for the connection
switches = [
    ['b06nx1.tele.iastate.edu', 'b06nx1'],
]

system_file = 'xxx.bin'
kickstart_file = 'xxx_kickstart.bin'
epld_file = 'xxx.img'

commands = [
    ("show incompatibility system bootflash:///%s" % system_file),
    ("show install all impact epld bootflash:///%s" % epld_file),
    ("show install all impact kickstart bootflash:///%s system bootflash:///%s" % (kickstart_file, system_file))
]

# ------------------------------------------------------------------------------------
# The following three lines are for time calculation
start_time = datetime.now()
total_parts = len(switches) * len(commands)
completed_parts = 0
# ------------------------------------------------------------------------------------
# i is needed to iterate through the multidimensional switches array
i = 0
# iterate through the switches that need to be fixed

direction = 'put'

for switch in switches:

    # Create logfile
    logfile = file('%s.txt', 'w' % switches[i][1])

    # provides the user screen info
    print("******************************")
    print("Starting switch %s." % switches[i][1])
    print("******************************")
    # delineation/separator for switches in log file
    logfile.write("===================================================\n")

    device = {
        'device_type': 'cisco_nxos',
        'host': switches[i][0],
        'username': secrets.nx_uid,
        'password': secrets.nx_pass,
        'file_system': 'bootflash:'
    }

    for current_file in (system_file, kickstart_file, epld_file):

        source_file = current_file
        dest_file = current_file

        file_system = switch.pop('file_system')
        ssh_conn = ConnectHandler(**device)
        transfer_dict = file_transfer(
            ssh_conn,
            source_file=source_file,
            dest_file=dest_file,
            file_system=file_system,
            direction=direction,
            overwrite_file=True
        )

        print(transfer_dict)
        pause = input("Hit enter to continue: ")

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
    logfile.close()
