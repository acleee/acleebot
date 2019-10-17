"""Initialize bot module."""
import logging
logger = logging.basicConfig(filename='errors.log',
                            filemode='w',
                            format='%(name)s - %(levelname)s - %(message)s',
                            level=logging.ERROR)

all = ['commands', 'db', 'ch']