#!/usr/bin/python3
# Copyright (c) 2020 damian@orchestrating-automatons.eu
# Furthering my Learning Python series, I now try to manage my backups
# Licensed under the GNU GPL v3
#
"""
    Backup file cleaning automaton.
    Maintains a set of files within a certain number.
"""

import argparse
import os
import sys
import time
import yaml

# Set global DEBUG to false by default, can be changed with CLI flag
DEBUG = False
DEFAULT_CONFIGNAME = "cleanup-config.yml"
DEFAULT_CONFIGPATH = "/usr/local/etc"


def logger():
    # TODO: standardise the logging
    # Need to output to screen if it's a tty (so check isatty())
    # Log the files to a specific log and then log activity to syslog
    # standardise this into a module
    """
    Instantiate the logger
    :return:
    """
    return True


def parse_cmdline():
    """
    Parse the command line options:
        -d (debug mode on)
        -n (dry run mode on)
    :return:
    """
    # Parse any command line options.
    # Argparse seems nice.
    parser = \
        argparse.ArgumentParser(description="cleans up a defined set of directories, "
                                            "removing files older than X "
                                            "days. Settings can be changed in the "
                                            "cleanup-config.yml file.")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="print out some extra debugging info")
    parser.add_argument("-n", "--dry-run", action="store_true",
                        help="show what would be done, but don't do anything")
    args = parser.parse_args()
    return args


def load_config(confpath, configfile):
    """
    Load the configuration options yaml file.
    :param confpath: Path to the config file
    :param configfile: Name of the config file
    :return: Configuration in dict format
    """
    # Let's be nice and look for the config file in a few places.
    global DEBUG

    if os.path.exists(configfile):
        searchpath = os.getcwd() + "/"
        if DEBUG:
            print("Using config: " + searchpath + configfile)
    elif os.path.exists(os.path.dirname(os.path.realpath(__file__)) + "/" + configfile):
        searchpath = os.path.dirname(os.path.realpath(__file__))
        if DEBUG:
            print("Using config: " + searchpath + "/" + configfile)
    elif os.path.exists("../etc/" + configfile):
        searchpath = "../etc/"
        if DEBUG:
            print("Using config: " + searchpath + "/" + configfile)
    elif os.path.exists(confpath + configfile):
        searchpath = confpath
        if DEBUG:
            print("Using config: " + searchpath + "/" + configfile)
    else:
        print("Q - Parameter error, " + configfile +
              " not found or readable in ../etc, " + confpath + ", " + os.getcwd() + " or "
              + os.path.dirname(os.path.realpath(__file__)))
        sys.exit(2)

    # Load the config file
    try:
        config = yaml.safe_load(open(searchpath + "/" + configfile, 'r'))
        # TODO: Put in checks here so that the config is confirmed or set to some defaults.
        return config
    except (yaml.YAMLError, IOError) as err:
        print("R Tape Loading Error, ", err)
        return False


def main():
    """
    Main - Do all the work here
    :return: Nothing
    """
    global DEBUG

    # Set standard defaults here
    configfile_name = DEFAULT_CONFIGNAME
    configfile_path = DEFAULT_CONFIGPATH

    today = time.time()
    count = 0

    cli = parse_cmdline()
    DEBUG = cli.debug
    dryrun_mode = cli.dry_run
    config = load_config(configfile_path, configfile_name)
    # stop if the config file fails to load
    if not config:
        sys.exit(2)

    if DEBUG:
        print(config)

    for item in config['directory_targets']:
        # take a folder at a time, obvs.
        for f_name in os.listdir(item):
            fpath = os.path.join(item, f_name)
            if os.stat(fpath).st_mtime < today - config['days'] * 86400:
                if os.path.isfile(fpath):
                    print("Found " + f_name + ", which is about "
                          + str(round((today - os.stat(fpath).st_mtime) / 86400)) +
                          " days old, deleting.")
                    if not dryrun_mode:
                        os.remove(os.path.join(fpath))
                    count = count + 1

        print("Done - removed " + str(count) + " files from " + item
              + ", hopefully that's what was desired.")
        count = 0

    print("0 OK, 0:1")


if __name__ == "__main__":
    main()
