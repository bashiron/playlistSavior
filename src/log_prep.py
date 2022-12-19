import sys
from loguru import logger


# LOG FILTERS
def reg_filter(record):
    return record['extra']['kind'] == 'regular'


def dir_filter(record):
    return record['extra']['kind'] == 'directory'


def pl_filter(record):
    return record['extra']['kind'] == 'playlist'


def disp_filter(record):
    return record['extra']['kind'] == 'display'


# configure loggers
logger.remove()
logger.add(sys.stderr,
           format='<w><green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level></w>',
           filter=reg_filter, level=0)
logger.add(sys.stderr,
           format='<w><green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <y>{message}</y></w>',
           filter=dir_filter, level=0)
logger.add(sys.stderr,
           format='<w><green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <m>{message}</m></w>',
           filter=pl_filter, level=0)
logger.add(sys.stderr,
           format='<w><green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <fg #6C66BA>{message}</fg #6C66BA></w>',
           filter=disp_filter, level=0)
