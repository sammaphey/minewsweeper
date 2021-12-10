import errno
import inspect
import logging
import os

from board import Board

ROOTLOGGER = logging.getLogger(inspect.getmodule(__name__))
LOGGER = logging.getLogger(__name__)
LOG_FORMAT = "%(asctime)s - %(name)s:%(funcName)s:%(lineno)s - " \
             "%(levelname)s - %(message)s"
DEFAULT_LOG_PATH = os.path.join(
    os.path.expanduser('~'),
    'Documents/projects/minesweeper/minesweeper.log'
)
DEFAULT_LOG_LEVEL = 'DEBUG'


def create_file(path):
    """
    Check if a file exists.

    If it does not, creates an empty file with the given path. Will create directories that don't
    exist in the path.

    :param path: The path to create.
    :raises OSError: This shouldn't happen, but unexpected OSErrors will get raised (we catch
        EEXist already).
    :returns: ``None``.
    """
    LOGGER.debug('Creating new file: {}'.format(path))
    if not os.path.exists(path):
        # Make directory
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as err:
            if err.errno == errno.EEXIST:
                msg = ('Directory already created, or race condition? Check '
                       'path: {}'.format(path))
                LOGGER.error(msg)
            else:
                msg = 'Unexpected OSError: {}'.format(err)
                LOGGER.error(msg)
                raise OSError(msg)
        # Make file
        with open(path, 'a+') as f:
            f.close()


def setup_logging():
    """
    Set up logging based on provided log params.

    :returns: The looger to be passed into subsequent classes/functions.
    """
    logpath = DEFAULT_LOG_PATH
    loglevel = DEFAULT_LOG_LEVEL

    create_file(logpath)

    formatter = logging.Formatter(LOG_FORMAT)
    ROOTLOGGER.setLevel(loglevel)

    # Setup file handler
    fh = logging.FileHandler(logpath)
    fh.setLevel(loglevel)
    fh.setFormatter(formatter)
    ROOTLOGGER.addHandler(fh)

    LOGGER.info("-------------------------STARTING-------------------------")
    LOGGER.info("INFO Logging Level -- Enabled")
    LOGGER.warning("WARNING Logging Level -- Enabled")
    LOGGER.critical("CRITICAL Logging Level -- Enabled")
    LOGGER.debug("DEBUG Logging Level -- Enabled")
    return LOGGER


logger = setup_logging()
board = Board.beginner()
board.run_game(logger=logger)
