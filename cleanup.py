#!/usr/bin/python
#  Copyright (c) 2020 damian@orchestrating-automatons.eu
# Furthering my Learning Python series, I now try to manage my backups
#
import os, time, argparse, yaml

CONFIGFILE = "cleanup-config.yml"
CONFPATH = "/usr/local/etc/"
DEBUG = False

def parse_cmdline():
    # Parse any command line options. Currently, we only support one.
    # Argparse seems nice.
    parser = argparse.ArgumentParser(description="cleans up a given directory, removing files older than X days."
                                                 " Settings can be changed in the yaml formatted config file."
    parser.add_argument("-d","--debug", action="store_true", help="print out some extra debugging info")
    args = parser.parse_args()
    return args

# Import the config file
def load_config(configfile):
    # Let's be nice and look for the config file in a few places.

    if os.path.exists(CONFIGFILE):
        confpath = os.getcwd()
        if DEBUG:
            print "Using config: " + confpath + CONFIGFILE
    elif os.path.exists("../etc/" + CONFIGFILE):
        confpath = "../etc/"
        if DEBUG:
            print "Using config: " + confpath + CONFIGFILE
    elif os.path.exists(CONFPATH + CONFIGFILE):
        confpath = CONFPATH
        if DEBUG:
            print "Using config: " + confpath + CONFIGFILE
    else:
        print "Q - Parameter error, " + configfile + \
              " not found or readable in ../etc, /usr/local/etc or " + os.getcwd()
        exit(2)

    # Load the config file
    try:
        config = yaml.safe_load(file(confpath+configfile, 'r'))
        return config
    except (yaml.YAMLError, IOError) as e:
        print "R Tape Loading Error, ", e


def main():
backups = "/backup.dir"
today = time.time()
count = 0
retention_days = 7

for f in os.listdir(backups):
    fpath = os.path.join(backups, f)
    if os.stat(fpath).st_mtime < today - retention_days * 86400:
        if os.path.isfile(fpath):
            print("Found " + f + ", which is about " + str( round((today - os.stat(fpath).st_mtime) / 86400) ) + " days old, deleting.")
            os.remove(os.path.join(fpath))
            count = count + 1

print("Done - removed " + str(count) + " files, hopefully that's what was desired.")
print("0 OK, 0:1")
