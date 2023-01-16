import re
import subprocess
from datetime import datetime
from netmiko import ConnectHandler
from py import nodes, secrets

# FQDN name and a "common" name for each switch. the "common" name helps shorten output,
# whereas the FQDN name is needed for the connection

switches = nodes.alldevices

vlans = [
    ['6', 'Durham_mach_room'],
    ['78', 'asb_78'],
    ['98', 'black_98'],
    # ['216', 'Stu_Health_IENET'],
    # ['217', 'Stu_Health_Private_IENET'],
    # ['239', 'DPS_POLICE_DESKTOP_IENET'],
    # ['254', 'Backbone_254'],
    # ['341', 'CycloneTV'],
    # ['408', 'mgmt_net_408'],
    # ['409', 'console_IENET'],
    # ['428', 'B31_Aastra_Ext_Lvl3'],
    # ['429', 'E63_Aastra_Ext_Lvl3'],
    # ['431', 'B31_Aastra_Ext'],
    # ['432', 'E63_Aastra_Ext'],
    # ['498', 'Aastra_FW'],
    # ['499', 'Aastra_FW_HA'],
    # ['501', 'bookstore_register_IENET'],
    # ['504', 'silonet'],
    # ['505', 'Foundation_Adv_Center_IENET'],
    # ['508', 'NorthChiller_IENET'],
    # ['526', 'Power_Plant_IENET'],
    ['529', 'B06_Forensics'],
    ['534', 'Ticketmaster_CYSte'],
    ['537', 'WomensBBall_IENET_537'],
    ['538', 'MensBBall_IENET_538'],
    # ['539', 'DPS_POLICE_L3_IENET'],
    # ['540', 'K60-B31_WOI-ICN_IENET'],
    # ['549', 'Power_Plant_2_IENET'],
    # ['560', 'VMWARE_STORAGE'],
    # ['570', 'B06_M22_Shared_iso_0'],
    # ['572', 'B06_M22_Shared_iso_2'],
    # ['573', 'B06_M22_Shared_iso_3'],
    # ['594', 'OCS-GW_IENET'],
    # ['601', 'PLantIntro_Ienet'],
    # ['608', 'foundation_isu_serv'],
    # ['609', 'foundation_pci'],
    # ['612', 'PCI_CLIENT_1'],
    # ['613', 'PCI_CLIENT_2'],
    # ['614', 'PCI_CLIENT_3'],
    # ['625', 'IaDOT-INTRANS_IENET'],
    # ['666', 'TicketMaster_IENET'],
    # ['898', 'BOREAS-mgmt-inside'],
    # ['910', 'Police_StateRTR_ICN'],
    # ['995', 'Compco_995'],
    # ['2254', 'Backbone_Aastra'],
    # ['2255', 'FW_Aastra'],
    # ['2400', 'E63_Aastra_GW'],
    ['2401', 'B31_Aastra_GW'],
    ['2409', 'F50_Aastra_GW'],
    ['2410', 'Lync_Aastra_GW'],
    ['2421', 'Durham_UC_Voice_Application_1'],
    # ['2422', 'ASB_UC_Voice_Application_2'],
    # ['2450', 'SBC_GRP1_HA'],
    # ['2451', 'SBC_GRP2_HA'],
    # ['2452', 'SBC_GRP3_HA'],
    # ['2453', 'SBC_GRP4_HA'],
    # ['3207', 'ResPark_Wilson_Netcom_managed'],
    # ['3211', 'Library_Gilman_Netcom_managed'],
    # ['3222', 'ASB_GenSvcs_Netcom_managed'],
    ['3231', 'Black_Linden_Netcom_managed']
]

i = 0

logfile = open('Topology_0_cleanup.txt', 'w')

percent = float(100)/float(len(switches))
percentage = percent/float(len(vlans))
y = 0

start_time = datetime.now()

total_parts = len(switches) * len(vlans)
completed_parts = 0

# iterate through the switches to get the arrays built with the
for switch in switches:

    print("******************************")
    print("Starting switch %s." % switches[i][1])
    print("******************************")

    # Just initiates the connection to the switch
    nxos_config = {
        'device_type': 'cisco_nxos',
        'ip': switches[i][0],
        'username': secrets.nx_uid,
        'password': secrets.nx_pass,
        'global_delay_factor': 0.25,
    }

    device = ConnectHandler(**nxos_config)

    logfile.write('------------------------------------------------------------------- \n')
    logfile.write('%s vlan\n' % (switches[i][1]))
    logfile.write('------------------------------------------------------------------- \n')

    z = 0

    for vlan in vlans:

        y = y + percentage
        print('progress: %f' % y)

        # runs the command to the switch, stores in temp variable
        port = device.send_command_expect("sho vlan id %s" % vlans[z][0], delay_factor=0.25)

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

        pattern = re.compile("^\s+|\s*,\s*|\\n|\s+$")

        port_array = [x for x in pattern.split(port14.communicate()[0]) if x]

        fp_ports = []
        ce_ports = []

        for port in port_array:
            output = device.send_command_expect("show run interface %s" % port, delay_factor=0.25)
            if "mode fabricpath" in output:
                fp_ports.append(port)
            else:
                ce_ports.append(port)

        # if not fp_ports:
            # logfile.write("For VLAN %s on %s, no Fabricpath ports exist. \n" % (vlan, switches[i][1]))
        # else:
            # logfile.write(
                # "For VLAN %s on %s, Fabricpath ports exist on %s \n" % (vlan, switches[i][1], fp_ports)
                # )
        if not ce_ports:
            print("no CE ports for VLAN %s on %s" % (vlans[z][0], switches[i][1]))
            # logfile.write("For VLAN %s on %s, no Classic Ethernet Ports \n" % (vlan, switches[i][1]))
        else:
            logfile.write(
                "VLAN %s %s on %s, Classic Ethernet ports exist on %s \n"
                % (vlans[z][0], vlans[z][1], switches[i][1], ce_ports)
            )

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

        z += 1

    i += 1
