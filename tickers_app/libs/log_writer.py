import logging


def init_logger(log_file_path, app_name):
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.INFO)
    # create the logging file handler
    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(file_handler)
    return logger
