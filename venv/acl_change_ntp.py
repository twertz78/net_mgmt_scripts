"""
Script runs slowly (have not taken time to figure out why, suspect its a Netmiko
thing) HIGHLY suggest running it in a "screen" window.

Adds hosts to or removes ACL entries from the ACLs on the switches
ACL entries are in the "hosts" field.

TODO: instead of commenting out the add or remove (and corresponding prints) sub
commands, have the script take an additional field from the bash line. either "add" or
"remove" to get it to work.

Author, TJ Wertz
twertz@iastate.edu 2019
"""

from netmiko import ConnectHandler
from datetime import datetime
from py import nodes, secrets

switches = nodes.datacenterdevices

# hosts are the IPs to add or remove from the ACL. Format is x.x.x.x/xx

start_time = datetime.now()
total_parts = len(switches)
completed_parts = 0

i = 0
for switch in switches:

    print("Starting switch %s." % switches[i][1])

    device = ConnectHandler(
        device_type='cisco_nxos',
        ip=switches[i][0],
        username=secrets.nx_uid,
        password=secrets.nx_pass
    )

    add_mgmtacl = [
        'ip access-list mgmtacl',
        'permit ip 129.186.67.233/32 any'
     ]

    remove_mgmtacl = [
        'ip access-list mgmtacl',
        'no permit ip 129.186.1.244/32 any'
     ]

    add_ntp_peers_acl = [
        'ip access-list ntp-peers-acl',
        'permit ip 129.186.67.233/32 any'
    ]

    remove_ntp_peers_acl = [
        'ip access-list ntp-peers-acl',
        'no permit ip 129.186.1.244/32 any'
    ]

    add_ntp_server = [
        'ntp server 129.186.67.233 use-vrf management',
    ]

    remove_ntp_server = [
        'no ntp server 129.186.1.244 use-vrf management',
    ]

    resequence_mgmtacl = [
        'resequence ip access-list mgmtacl 10 10'
    ]

    resequence_ntp_peers_acl = [
        'resequence ip access-list ntp-peers-acl 10 10'
    ]

    # comment out add lines or remove lines of commands based on what we are doing...

    # print("Adding IP to mgmtacl")
    # device.send_config_set(add_mgmtacl)
    print("Adding IP to ntp-peers-acl")
    device.send_config_set(add_ntp_peers_acl)
    # print("Adding IP to NTP server list")
    # device.send_config_set(add_ntp_server)
    # print("Removing IP from mgmtacl")
    # device.send_config_set(remove_mgmtacl)
    # print("Resequencing ACL")
    # device.send_config_set(resequence_mgmtacl)
    print("Removing IP from ntp-peers-acl")
    device.send_config_set(remove_ntp_peers_acl)
    print("Resequencing ACL")
    device.send_config_set(resequence_ntp_peers_acl)
    # print("Removing IP from NTP server list")
    # device.send_config_set(remove_ntp_server)
    # --------------------------------------------------------------------------------------
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
    # --------------------------------------------------------------------------------------

    i += 1
