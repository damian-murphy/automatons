#!/usr/bin/python3
# Copyright (c) 2022 damian@orchestrating-automatons.eu
# Watcher: Observe a process and restart or alert as required
# Licensed under the GNU GPL v3
#
import argparse
import os
import time
import yaml

CONFIGFILE = "watcher-config.yml"
CONFPATH = "/usr/local/etc/"
DEBUG = False

# TODO: Logging of output
def logger():
    # TODO: standardise the logging
    return True

def parse_cmdline():
    # Parse any command line options. Currently, we only support one.
    # Argparse seems nice.
    parser = argparse.ArgumentParser(description="Watches a process, restarting if not running."
                                                 "Settings can be changed in the watcher-config.yml file.")
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
    print("Ya, I ran.")