import logging

# Configure the logger
logging.basicConfig(
    filename='error_log.txt',
    level=logging.ERROR,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def log_error(message):
    logging.error(message)

def log_info(message):
    logging.info(message)