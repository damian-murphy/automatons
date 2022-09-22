"""
    Logger class for automatons
    Uses the python logging class for use with automatons in order to provide standardised logging

"""

import logging
import platform
import os
import sys
from pathlib import Path
from logging import handlers

class AutoLogger:
    """
       Extend the logging class with some wrapping
    """

    def __init__(self,myconfig):

        self.has_tty = sys.stdout.isatty()
        self.myname = sys.argv[0]

        logger = logging.getLogger(sys.argv[0])
        msgformat = '%(asctime)s %(name)s %(levelname)s: %(message)s'
        datefmt = '%Y-%m-%d %H:%M:%S'
        alformat = logging.Formatter(msgformat, datefmt)

        # Work out if we're on windows or not
        if platform.system() == "Windows":
            logpath = Path(os.environ["ProgramFiles"]) / Path(myconfig['logfile'])
        else:
            logpath = Path(myconfig['logfile'])

        # Set the basic config for our logger
        # Basic config takes a string for format, not a formatter object, unlike the handlers.
        # Probably some reason for this, but anyway.
        logging.basicConfig(format=msgformat, level=myconfig['loglevel'], datefmt=datefmt)
        slh = handlers.SysLogHandler()
        flh = handlers.TimedRotatingFileHandler(logpath, backupCount=myconfig['logfileretention'],
                                                atTime='midnight')
        clh = logging.StreamHandler()  # console logger
        clh.setLevel(logging.CRITICAL)  # only send critical errors to the console
        clh.setFormatter(alformat)
        slh.setFormatter(alformat)
        flh.setFormatter(alformat)

        # Remove any default handlers before adding the ones we want
        logger.handlers = []
        logger.addHandler(slh)
        logger.addHandler(flh)
        logger.addHandler(clh)

