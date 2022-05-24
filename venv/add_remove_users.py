"""
Script runs slowly (have not taken time to figure out why, suspect its a Netmiko
thing) HIGHLY suggest running it in a "screen" window.

Adds or removes users
ACL entries are in the "hosts" field.

Author, TJ Wertz
twertz@iastate.edu 2019
"""

from datetime import datetime
from netmiko import ConnectHandler
from py import nodes, secrets

# devices to run commands against, first part is FQDN, second part is for a "common" name
switches = nodes.admin_VDC + nodes.nonproductiondevices + nodes.be + nodes.core

users_to_remove = [
    'ldean',
    'lchad',
    'lpsailor',
    'psailor'
]

users_to_add = [
    ['sirius1', '$1$TPYjKxLK$tQ5cYzhgZmCx4ON8diTmC0', 'network-admin'],
    ['sirius2', '$1$jSgSgvoY$LczMyuMTnksqhmtOk66fu/', 'network-admin'],
    ['sirius3', '$1$1wV5Utr0$Truo5j.PFPjVhVojTJ1Lj0', 'network-admin'],
    ['sirius4', '$1$x98Ugf6j$/pahfaGXzgGd5QvV41bYT0', 'network-admin'],
]

# ---------------------------------------------------------------------------------------
# initial time settings
start_time = datetime.now()
total_parts = len(switches) * len(users_to_add)
completed_parts = 0
# ---------------------------------------------------------------------------------------

logfile = open('users.txt', 'w')

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

    # ------- remove comments below to have user config printed to screen ---------
    # for user_a in users_to_remove:
    #     output = device.send_command("show user-account | i %s" % user_a)
    #     print(output)

    # logfile.write(output)

    logfile.write("************************************************************** \n")
    # iterate through the commands on each switch

    # for users_r in users_to_remove:

    #     remove_user = [
    #         'no username ' + users_r
    #     ]
    #     # ------- comment out line below to stop removing -------
    #     device.send_config_set(remove_user)
    #     # ------- remove comment below to have command printed to screen --------
    #     print(remove_user)

    j = 0
    for users_a in users_to_add:

        add_user = (
                'username %s password 5 %s role %s' % (users_to_add[j][0], users_to_add[j][1], users_to_add[j][2])
        )

        # ------- comment out line below to stop adding -------
        device.send_config_set(add_user)
        # ------- remove comment below to have command printed to screen --------
        print(add_user)
        j += 1

    # ------- remove comments below to changes to user config ---------
    # for user_b in users_to_remove:
    #     output = device.send_command("show user-account | i %s" % user_b)
    #     print(output)

    # logfile.write(output)

    logfile.write("============================================================== \n")

    i += 1

logfile.write("************************************************************** \n")

logfile.close()
