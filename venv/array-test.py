# Combine this with fabricpath.py file to get one big output
# Question - how to get a dynamically named array, and then password
# all that info into the if,elif,else statement correctly... multidimensional
# array might work, but not sure how to make that all work right.
# worst case scenario I can copy and paste manually to get the data into the
# script, but that seems ridiculous.

# testing arrays, in prod would have output from
# show fabricpath topology 6 isis vlan-range
# with one array per switch
a = [1, 2, 3, 4, 6]
b = [2, 3, 4, 6]
c = [1, 2, 3, 4, 5, 6]
d = [5, 6]

# converting arrays to set as there is supposed to be a big
# performance improvement
a_set = set(a)
b_set = set(b)
c_set = set(c)
d_set = set(d)


logfile = file('array.txt', 'w')
i = 0

# logic to determine if are in fabricpath on switches
# would need to loop it 4096 times
while i < 8:
    i = i + 1

    if i not in a_set and i not in b_set and i not in c_set and i not in d_set:
        logfile.write("No switches contain VLAN %i" % i)

    elif i in a_set and i in b_set and i in c_set and i in d_set:
        logfile.write("All switches contain VLAN %i" % i)
    else:
        logfile.write("VLAN %i only exists on switches: " % i)
        if i in a_set:
            logfile.write("a ")
        if i in b_set:
            logfile.write("b ")
        if i in c_set:
            logfile.write("c ")
        if i in d_set:
            logfile.write("d ")
    logfile.write("\n")
