import logging

logging.basicConfig(filename='errors.log',
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.ERROR)
