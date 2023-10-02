import logging

log = logging

log.basicConfig(filename='app.log', filemode='w',
                format='%(levelname)s - %(asctime)s - %(message)s', level=logging.INFO)
log.basicConfig(filename='app.log', filemode='w',
                format='%(levelname)s - %(asctime)s - %(message)s', level=logging.ERROR)
