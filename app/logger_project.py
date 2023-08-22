import logging

def init_logger():
    logging.basicConfig(
        level=logging.INFO,
        filename="py_log.log",
        filemode="w",
        format="%(asctime)s %(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(levelname)s  %(message)s",
    )
    #logging.d
