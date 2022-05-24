#!/usr/bin/python

"""
eth_saver.py
this scripts allows to run a continuous ethanalyzer and
export the traffic off via tftp or ftp.  There will need to be two
instances of the script running.  The first instance runs in 'capture' mode
to continuously run ethanalyzer and save the files to the local bootflash.  
The second instance will run in 'export' mode and copy the captured files
off the bootflash via ftp or tftp.  

Step (1) Copy the script into default VDC bootflash:/scripts/ directory
Step (2) Execute one instance of the script in 'capture' mode
Step (3) Execute a second instance of the script in 'export' mode

Example:
    'capture' mode
    N7K# source eth_saver.py --capture

    'export' mode
    N7K# source eth_saver.py --export --server <ftp_server> --username <username> --password <password>

Use -h for more options

Usage: eth_saver.py [--capture|--export] [options]

Options:
  -h, --help           show this help message and exit
  -c, --capture        run this program in capture mode
  -e, --export         run this program in export mode
  --server=SERVER      server name for export mode
  --protocol=PROTOCOL  protocol for export mode (can be ftp or tftp)
  --username=USERNAME  username for ftp export
  --password=secrets.nx_pass  password for ftp export
  --frames=MAX_FRAMES  maximum number of frames per capture
  --files=MAX_FILES    maximum number of files to capture/export

@author agossett@cisco.com
@version 05/27/2014
"""

import cisco
import time, os, re

class ethSaver(object):
    MAX_FRAMES = 100000
    MAX_FILES = 5000
    PP_NAME = "ethsaver"

    def __init__(self):
        self.max_frames = ethSaver.MAX_FRAMES
        self.max_files = ethSaver.MAX_FILES
        self.pp_name = ethSaver.PP_NAME
        self.protocol = "ftp"
        self.server = ""
        self.username = ""
        self.password = ""
        self.vrf = "management"

    def execute_export(self):
        print "running in export mode"
        file_count = 0
        while file_count < self.max_files:
            # get the first file off the bootflash matching pp_name filter
            files = []
            # s = cli("dir bootflash: | grep %s | grep .pcap" % self.pp_name)
            for l in os.listdir("/bootflash/"):
                r1 = re.search("(?P<filename>%s_[\d_]+\.pcap)" % self.pp_name, l, re.IGNORECASE)
                if r1 is not None:
                    files.append(r1.group("filename"))
    
            files.sort()
            # ensure that there are at least two matching files present
            # this guarantees that the file we're examining is not the same file
            # that is currently being captured
            if len(files) >= 2:
                # copy the file to configured tftp_server   
                print "exporting %s" % files[0]

                # quick gzip of the file first and update filename (no error checking for this...)
                cli("gzip bootflash:%s" % files[0])
                files[0] = files[0]+".gz"
            
                # ftp or tftp pending on provided protocol
                try:
                    if self.protocol == "ftp":
                        s = cli("copy bootflash:%s ftp://%s:%s@%s/%s vrf %s" % (files[0], self.username, self.password, self.server, files[0], self.vrf))
                    else:
                        s = cli("copy bootflash:%s tftp://%s/%s vrf %s" % (files[0], self.server, files[0], self.vrf))
                except Exception as e:
                    print e
                    s = "failed"

                # validate that file was successfully copied, if not don't delete it
                if "Completed Successfully" in s:
                    # delete the file
                    os.remove("/bootflash/%s" % files[0])
                print "\n"

            # wait 5 seconds between each cycle
            print "waiting 5 seconds..."
            time.sleep(5)

    def execute_capture(self):
        print "running in capture mode"
        file_count = 0
        while file_count < self.max_files:
            file_count += 1
            timestamp = int(time.time())
            file_name = "%s_%s_%d.pcap" % (self.pp_name, str(file_count).zfill(6), timestamp)
            print "Running capture %d" % file_count
            cli("ethanalyzer local interface inband limit-captured-frames %d write bootflash:%s" % (self.max_frames, file_name))
            

if __name__ == "__main__":

    from optparse import OptionParser, OptionGroup

    usage = "%prog [--capture|--export] [options]"
    parser = OptionParser(usage)
    parser.add_option("-c","--capture", action="store_true", dest="mode_capture", help="run this program in capture mode", default=False)
    parser.add_option("-e","--export", action="store_true", dest="mode_export", help="run this program in export mode", default=None)
    parser.add_option("--server", action="store", type="string", dest="server", help="server name for export mode", default=None)
    parser.add_option("--protocol", action="store", type="string", dest="protocol", help="protocol for export mode (can be ftp or tftp)", default="ftp")
    parser.add_option("--username", action="store", type="string", dest="username", help="username for ftp export", default=None)
    parser.add_option("--password", action="store", type="string", dest="password", help="password for ftp export", default=None)
    parser.add_option("--frames", action="store", type="int", dest="max_frames", help="maximum number of frames per capture", default=ethSaver.MAX_FRAMES)
    parser.add_option("--files", action="store", type="int", dest="max_files", help="maximum number of files to capture/export", default=ethSaver.MAX_FILES)
    (options, args) = parser.parse_args() 

    # initialize ethSaver object with user provided fields
    es = ethSaver()
    es.max_frames = options.max_frames
    es.max_files = options.max_files

    if options.mode_capture:
        # execute in capture mode
        es.execute_capture()
    elif options.mode_export:
        # execute in export mode
        # determine protocol is ftp or tftp
        options.protocol = options.protocol.lower()
        if options.protocol != "tftp" and options.protocol != "ftp":
            print "Invalid protocol, please specify ftp or tftp"
            parser.print_help()
        elif options.server is None:
            print "Please provide an ftp or tftp server to export captures (use the --server option)"
            parser.print_help()
        else:
            es.protocol = "ftp"
            es.server = options.server
            # if ftp, then ensure username and password are provided, else
            # will use default anonymous/<empty>
            if options.username is None:
                print "no username provided, using 'anonymous'"
                options.username = "anonymous"
            if options.password is None:
                print "no password provided, using 'anonymous'"
                options.password = "anonymous"
            es.username = options.username
            es.password = options.password
            es.execute_export()
    else:
        print "Please enter a mode"
        parser.print_help()