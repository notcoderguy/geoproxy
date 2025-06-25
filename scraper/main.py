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
                scrapeController()
            elif command == 'check':
                checkController()
            elif command == 'export':
                exportController()
            else:
                scrapeController()
                checkController()
        else:
            scrapeController()
            checkController()
            exportController()
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")

if __name__ == '__main__':
    main()
