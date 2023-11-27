import logging

log = logging

log.basicConfig(
    format='%(levelname)s - %(asctime)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ])

log.basicConfig(
    format='%(levelname)s - %(asctime)s - %(message)s',
    level=logging.ERROR,
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ])

log.basicConfig(
    format='%(levelname)s - %(asctime)s - %(message)s',
    level=logging.CRITICAL,
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ])
