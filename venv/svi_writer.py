from py import svis

output_b31 = open('svis_b31.txt', 'w')
output_e63 = open('svis_e63.txt', 'w')
i = 0

for svi in svis.svi_set:

    interface = svis.svi_set[i][0]
    desc = svis.svi_set[i][1]
    bldg_code = svis.svi_set[i][2]
    ip_addr_netreg_a = svis.svi_set[i][3]
    ip_addr_netreg_b = svis.svi_set[i][4]
    ip_addr_netreg_hsrp = svis.svi_set[i][5]
    ip_cidr_netreg = svis.svi_set[i][6]
    ip_addr_guest_a = svis.svi_set[i][7]
    ip_addr_guest_b = svis.svi_set[i][8]
    ip_addr_guest_hsrp = svis.svi_set[i][9]
    ip_cidr_guest = svis.svi_set[i][10]
    ip_addr_nat_a = svis.svi_set[i][11]
    ip_addr_nat_b = svis.svi_set[i][12]
    ip_addr_nat_hsrp = svis.svi_set[i][13]
    ip_cidr_nat = svis.svi_set[i][14]
    ipv6_addr_a = svis.svi_set[i][15]
    ipv6_addr_b = svis.svi_set[i][16]
    ipv6_addr_hsrp = svis.svi_set[i][17]
    ipv6_cidr = svis.svi_set[i][18]

    output_b31.write("interface %s\n" % interface)
    output_b31.write("  description -- (%s) %s [STUDENT][PRIMARY] --\n" % (bldg_code, desc))
    output_b31.write("  shutdown\n")
    output_b31.write("  ip access-group std-isu-v4-pkt-filter in\n")
    output_b31.write("  no ip redirects\n")
    output_b31.write("  ip address %s/%s\n" % (ip_addr_netreg_a, ip_cidr_netreg))
    output_b31.write("  ip address %s/%s secondary\n" % (ip_addr_guest_a, ip_cidr_guest))
    output_b31.write("  ip address %s/%s secondary\n" % (ip_addr_nat_a, ip_cidr_nat))
    output_b31.write("  ip directed-broadcast wake-on-lan-acl\n")
    output_b31.write("  ip verify unicast source reachable-via any\n")
    output_b31.write("  ipv6 address %s/%s\n" % (ipv6_addr_a, ipv6_cidr))
    output_b31.write("  ipv6 verify unicast source reachable-via rx\n")
    output_b31.write("  ipv6 nd ns-interval 10000\n")
    output_b31.write("  ipv6 nd reachable-time 90000\n")
    output_b31.write("  ip router eigrp 196\n")
    output_b31.write("  ipv6 router ospfv3 2698 area 0.0.0.0\n")
    output_b31.write("  ip pim sparse-mode\n")
    output_b31.write("  ip arp timeout 300\n")
    output_b31.write("  ip policy route-map guest-access-policy-route\n")
    output_b31.write("  hsrp version 2\n")
    output_b31.write("  hsrp 1\n")
    output_b31.write("    preempt delay minimum 600\n")
    output_b31.write("    priority 110\n")
    output_b31.write("    ip %s\n" % ip_addr_nat_hsrp)
    output_b31.write("    ip %s secondary\n" % ip_addr_guest_hsrp)
    output_b31.write("    ip %s secondary\n" % ip_addr_nat_hsrp)
    output_b31.write("  hsrp 6 ipv6\n")
    output_b31.write("    preempt delay minimum 600\n")
    output_b31.write("    priority 110\n")
    output_b31.write("    ip %s\n" % ipv6_addr_hsrp)
    output_b31.write("    ip fe80::1\n")
    output_b31.write("  ip dhcp relay address 10.10.67.136\n")
    output_b31.write("  ip dhcp relay address 10.10.67.166\n")
    output_b31.write("\n")
    output_b31.write("\n")

    output_e63.write("interface %s\n" % interface)
    output_e63.write("  description -- (%s) %s [STUDENT][BACKUP] --\n" % (bldg_code, desc))
    output_e63.write("  shutdown\n")
    output_e63.write("  ip access-group std-isu-v4-pkt-filter in\n")
    output_e63.write("  no ip redirects\n")
    output_e63.write("  ip address %s/%s\n" % (ip_addr_netreg_b, ip_cidr_netreg))
    output_e63.write("  ip address %s/%s secondary\n" % (ip_addr_guest_b, ip_cidr_guest))
    output_e63.write("  ip address %s/%s secondary\n" % (ip_addr_nat_b, ip_cidr_nat))
    output_e63.write("  ip directed-broadcast wake-on-lan-acl\n")
    output_e63.write("  ip verify unicast source reachable-via any\n")
    output_e63.write("  ipv6 address %s/%s\n" % (ipv6_addr_b, ipv6_cidr))
    output_e63.write("  ipv6 verify unicast source reachable-via rx\n")
    output_e63.write("  ipv6 nd ns-interval 10000\n")
    output_e63.write("  ipv6 nd reachable-time 90000\n")
    output_e63.write("  ip router eigrp 196\n")
    output_e63.write("  ipv6 router ospfv3 2698 area 0.0.0.0\n")
    output_e63.write("  ip pim sparse-mode\n")
    output_e63.write("  ip arp timeout 300\n")
    output_e63.write("  ip policy route-map guest-access-policy-route\n")
    output_e63.write("  hsrp version 2\n")
    output_e63.write("  hsrp 1\n")
    output_e63.write("    preempt delay minimum 600\n")
    output_e63.write("    priority 90\n")
    output_e63.write("    ip %s\n" % ip_addr_nat_hsrp)
    output_e63.write("    ip %s secondary\n" % ip_addr_guest_hsrp)
    output_e63.write("    ip %s secondary\n" % ip_addr_nat_hsrp)
    output_e63.write("  hsrp 6 ipv6\n")
    output_e63.write("    preempt delay minimum 600\n")
    output_e63.write("    priority 90\n")
    output_e63.write("    ip %s\n" % ipv6_addr_hsrp)
    output_e63.write("    ip fe80::1\n")
    output_e63.write("  ip dhcp relay address 10.10.67.136\n")
    output_e63.write("  ip dhcp relay address 10.10.67.166\n")
    output_e63.write("\n")
    output_e63.write("\n")

    i += 1

output_b31.close()
output_e63.close()
