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
from py import secrets

switches = [
    ['b31fpe.tele.iastate.edu', 'b31fpe'],
    ['e63fpe.tele.iastate.edu', 'e63fpe']
]

# hosts are the IPs to add or remove from the ACL. Format is x.x.x.x/xx
hosts = [

    '10.100.34.0/24',

]

start_time = datetime.now()
total_parts = len(switches) * len(hosts)
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

    for host in hosts:

        # ===========================================
        add_mgmtacl = [
            'ip access-list mgmtacl',
            ('permit ip %s any' % host)
         ]

        remove_mgmtacl = [
            'ip access-list mgmtacl',
            ('no permit ip %s any' % host)
         ]

        resequence_mgmtacl = [
            'resequence ip access-list mgmtacl 10 10'
        ]

        # ===========================================

        add_vtyacl = [
            'ip access-list vtyacl',
            ('permit ip %s any' % host)
        ]

        remove_vtyacl = [
            'ip access-list vtyacl',
            ('no permit ip %s any' % host)
        ]

        resequence_vtyacl = [
            'resequence ip access-list vtyacl 10 10'
        ]

        # ===========================================

        add_snmp_ro = [
            'ip access-list snmp-ro-acl',
            ('permit ip %s any' % host)
        ]

        remove_snmp_ro = [
            'ip access-list snmp-ro-acl',
            ('no permit ip %s any' % host)
        ]

        resequence_snmp_ro = [
            'resequence ip access-list snmp-ro-acl 10 10'
        ]

        # ===========================================

        add_snmp_rw = [
            'ip access-list snmp-rw-acl',
            ('permit ip %s any' % host)
        ]

        remove_snmp_rw = [
            'ip access-list snmp-rw-acl',
            ('no permit ip %s any' % host)
        ]

        resequence_snmp_rw = [
            'resequence ip access-list snmp-rw-acl 10 10'
        ]

        # comment out add lines or remove lines of commands based on what we are doing...
        # =====ADD===================================
        print("Adding %s to mgmtacl" % host)
        device.send_config_set(add_mgmtacl)
        print("Adding %s to vtyacl" % host)
        device.send_config_set(add_vtyacl)
        print("Adding %s to snmp_ro" % host)
        device.send_config_set(add_snmp_ro)
        print("Adding %s to snmp_rw" % host)
        device.send_config_set(add_snmp_rw)

        # =====REMOVE================================
        # print("Removing %s from mgmtacl" % host)
        # device.send_config_set(remove_mgmtacl)
        # print("Removing %s to vtyacl" % host)
        # device.send_config_set(remove_vtyacl)
        # print("Removing %s to snmp_ro" % host)
        # device.send_config_set(remove_snmp_ro)
        # print("Adding %s to snmp_rw" % host)
        # device.send_config_set(add_snmp_rw)

        # =====RESEQUENCE============================
        # print("Resequencing ACL")
        # device.send_config_set(resequence_mgmtacl)
        # print("Resequencing ACL")
        # device.send_config_set(resequence_vtyacl)
        # print("Resequencing ACL")
        # device.send_config_set(resequence_snmp_ro)
        # print("Resequencing ACL")
        # device.send_config_set(resequence_snmp_rw)

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
