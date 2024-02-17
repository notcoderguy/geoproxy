import time
import os
import sys
from colorama import init, Fore, Style 
import modules.scrape
import modules.check

init()

def scrapeController():
    modules.scrape.app()

def checkController():
    modules.check.app()

def main():
    if not os.path.exists('data'):
        os.mkdir('data')
    try:
        if sys.argv[1] == 'scrape':
            while True:
                scrapeController()
                print(Fore.CYAN + '--------------------------' + Style.RESET_ALL)
                print(Fore.CYAN + 'Sleeping for 30 minutes...' + Style.RESET_ALL)
                print(Fore.CYAN + '--------------------------' + Style.RESET_ALL)
                time.sleep(1800)
        elif sys.argv[1] == 'check':
            checkController()
            print(Fore.CYAN + '--------------------------' + Style.RESET_ALL)
            print(Fore.CYAN + 'Sleeping for 30 minutes...' + Style.RESET_ALL)
            print(Fore.CYAN + '--------------------------' + Style.RESET_ALL)
            time.sleep(600)
        else:
            while True:
                scrapeController()
                checkController()
                print(Fore.CYAN + '--------------------------' + Style.RESET_ALL)
                print(Fore.CYAN + 'Sleeping for 30 minutes...' + Style.RESET_ALL)
                print(Fore.CYAN + '--------------------------' + Style.RESET_ALL)
                time.sleep(1800)
    except IndexError:
        while True:
            scrapeController()
            checkController()
            print(Fore.CYAN + '--------------------------' + Style.RESET_ALL)
            print(Fore.CYAN + 'Sleeping for 30 minutes...' + Style.RESET_ALL)
            print(Fore.CYAN + '--------------------------' + Style.RESET_ALL)
            time.sleep(1800)

if __name__ == '__main__':
    main()