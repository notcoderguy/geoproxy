import logging
from colorama import init
from rich.progress import Progress, BarColumn, TextColumn
from rich.console import Console
from .sources.monosans import scrape as monosans_scrape
from .sources.spysme import scrape as spysme_scrape 
from .sources.proxyscrape import scrape as proxyscrape_scrape
from .sources.geonode import scrape as geonode_scrape

init()
console = Console()
logger = logging.getLogger(__name__)


def app():
    logger.info("Starting scraping process")
    
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(complete_style="green"),
        TextColumn("[progress.completed]{task.completed}/{task.total}"),
        transient=True,
        console=console
    ) as progress:
        tasks = [
            ("Monosans", monosans_scrape),
            ("Spys.me", spysme_scrape),
            ("ProxyScrape", proxyscrape_scrape),
            ("GeoNode", geonode_scrape)
        ]
        
        main_task = progress.add_task("Overall Progress", total=len(tasks))
        
        for name, scraper in tasks:
            try:
                success = scraper(progress=progress, parent_task=main_task)
                if success:
                    logger.info(f"Successfully scraped {name}")
                else:
                    logger.warning(f"Failed to scrape {name}")
            except Exception as e:
                logger.error(f"Error scraping {name}: {str(e)}")
            progress.update(main_task, advance=1)
    
    logger.info("Scraping process completed")
