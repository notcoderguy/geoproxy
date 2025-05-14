import time
import os
import sys
import logging
from dotenv import load_dotenv
from colorama import init
import modules.scrape
import modules.check
import modules.export

# Initialize colorama
init()

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv('APP_DEBUG', 'false').lower() == 'true' else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def scrapeController():
    modules.scrape.app()

def checkController():
    modules.check.app()

def exportController():
    modules.export.app()

def main():
    try:
        if len(sys.argv) > 1:
            command = sys.argv[1]
            if command == 'scrape':
                while True:
                    scrapeController()
                    logger.info('Sleeping for 6 hours...')
                    time.sleep(21600)
            elif command == 'check':
                checkController()
                logger.info('Sleeping for 6 hours...')
                time.sleep(21600)
            elif command == 'export':
                exportController()
                logger.info('Sleeping for 6 hours...')
                time.sleep(21600)
            else:
                while True:
                    scrapeController()
                    checkController()
                    logger.info('Sleeping for 6 hours...')
                    time.sleep(21600)
        else:
            while True:
                scrapeController()
                checkController()
                exportController()
                logger.info('Sleeping for 6 hours...')
                time.sleep(21600)
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")

if __name__ == '__main__':
    main()
