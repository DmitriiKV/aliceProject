import logging

logging.basicConfig(filename='log.log',
                    format="%(asctime)s, %(levelname)s, "
                           "%(name)s, %(message)s", level=logging.DEBUG)
def log():
    i = 0
    while i < 10:
        logging.debug(i)
        i += 1

if __name__ == '__main__':
    log()