#!/usr/bin/python3
# Copyright (c) 2020 damian@orchestrating-automatons.eu
# Furthering my Learning Python series, I now try to manage my backups
# Licensed under the GNU GPL v3
#
import argparse
import os
import time
import yaml

CONFIGFILE = "cleanup-config.yml"
CONFPATH = "/usr/local/etc/"
DEBUG = False

# TODO: Logging of output
def logger():
    # TODO: standardise the logging
    return True

def parse_cmdline():
    # Parse any command line options. Currently, we only support one.
    # Argparse seems nice.
    parser = argparse.ArgumentParser(description="cleans up a defined set of directories, removing files older than X "
                                                 "days. "
                                                 "Settings can be changed in the cleanup-config.yml file.")
    parser.add_argument("-d", "--debug", action="store_true", help="print out some extra debugging info")
    parser.add_argument("-n", "--dry-run", action="store_true", help="show what would be done, but don't do anything")
    args = parser.parse_args()
    return args


def load_config(configfile):
    # Let's be nice and look for the config file in a few places.
    global DEBUG

    if os.path.exists(CONFIGFILE):
        confpath = os.getcwd() + "/"
        if DEBUG:
            print("Using config: " + confpath + CONFIGFILE)
    elif os.path.exists(os.path.dirname(os.path.realpath(__file__)) + "/" + CONFIGFILE):
        confpath = os.path.dirname(os.path.realpath(__file__))
        if DEBUG:
            print("Using config: " + confpath + "/" + CONFIGFILE)
    elif os.path.exists("../etc/" + CONFIGFILE):
        confpath = "../etc/"
        if DEBUG:
            print("Using config: " + confpath + "/" + CONFIGFILE)
    elif os.path.exists(CONFPATH + CONFIGFILE):
        confpath = CONFPATH
        if DEBUG:
            print("Using config: " + confpath + "/" + CONFIGFILE)
    else:
        print("Q - Parameter error, " + configfile +
              " not found or readable in ../etc, " + CONFPATH + ", " + os.getcwd() + " or " + os.path.dirname(os.path.realpath(__file__)))
        exit(2)

    # Load the config file
    try:
        config = yaml.safe_load(open(confpath + "/" + configfile, 'r'))
        # TODO: Put in checks here so that the config is confirmed or set to some defaults.
        return config
    except (yaml.YAMLError, IOError) as e:
        print("R Tape Loading Error, ", e)


def main():
    global DEBUG

    today = time.time()
    count = 0

    cli = parse_cmdline()
    DEBUG = cli.debug
    DRYRUN = cli.dry_run
    config = load_config(CONFIGFILE)

    if DEBUG:
        print(config)

    for item in config['directory_targets']:
        # take a folder at a time, obvs.
        for f in os.listdir(item):
            fpath = os.path.join(item, f)
            if os.stat(fpath).st_mtime < today - config['days'] * 86400:
                if os.path.isfile(fpath):
                    print("Found " + f + ", which is about " + str(round((today - os.stat(fpath).st_mtime) / 86400)) +
                          " days old, deleting.")
                    if not DRYRUN:
                        os.remove(os.path.join(fpath))
                    count = count + 1

        print("Done - removed " + str(count) + " files from " + item + ", hopefully that's what was desired.")
        count = 0

    print("0 OK, 0:1")


if __name__ == "__main__":
    main()
