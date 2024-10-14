import logging
from bot import startBot
logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(filename='myapp.log', level=logging.DEBUG)
    logger.debug('Started')
    startBot()    
    logger.debug('Finished')

if __name__ == '__main__':
    main()