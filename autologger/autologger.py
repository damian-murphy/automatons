"""
    Logger class for automatons
    Uses the python logging class for use with automatons in order to provide standardised
    logging.
    We're extending the class here with a wrapper, so we could replace the logger 'back end'
    in the future.
    We will write execution info to syslog, and details to the program log.
    If we're running from a console, duplicate the syslog data to console.
"""

import logging
import sys
from pathlib import Path
from logging import handlers


class AutoLogger:
    """
       Extend the logging class with some wrapping
       Takes config parameter as a dict
       :param myconfig: dict containing [loglevel, logfile, logfileretention]
    """

    def __init__(self, myconfig):

        self.logger = logging.getLogger(sys.argv[0])
        self.msgformat = '%(asctime)s %(name)s %(levelname)s: %(message)s'
        self.datefmt = '%Y-%m-%d %H:%M:%S'
        alformat = logging.Formatter(self.msgformat, self.datefmt)
        self.loglevel = myconfig['loglevel']
        self.logpath = Path(myconfig['logfile'])

        # Set the basic config for our logger
        # Basic config takes a string for format, not a formatter object, unlike the handlers.
        # Probably some reason for this, but anyway.
        logging.basicConfig(format=self.msgformat, level=myconfig['loglevel'], datefmt=self.datefmt)
        slh = handlers.SysLogHandler()
        flh = handlers.TimedRotatingFileHandler(self.logpath,
                                                backupCount=myconfig['logfileretention'],
                                                atTime='midnight')
        clh = logging.StreamHandler()  # console logger

        if sys.stdout.isatty():
            clh.setLevel(logging.NOTSET)  # catch anything and copy to the console
        else:
            clh.setLevel(logging.CRITICAL)  # or only send critical errors to the console

        clh.setFormatter(alformat)
        slh.setFormatter(alformat)
        flh.setFormatter(alformat)

        # Remove any default handlers before adding the ones we want
        self.logger.handlers = []
        self.logger.addHandler(slh)
        self.logger.addHandler(flh)
        self.logger.addHandler(clh)

    def syslog(self, level, message):
        """
        :param message
        :param level
        :return:
            Write some input to the system log.
            If running from a console, duplicate there.
        """

        return True

    def setloglevel(self, loglevel):
        """
        :param loglevel:
        :return:

        Change the log level to 'loglevel'

        """
        self.loglevel = loglevel

        return True
