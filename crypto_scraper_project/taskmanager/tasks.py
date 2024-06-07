from celery import shared_task
from .scraper import CoinMarketCapScraper
from .models import ScrapingJob

@shared_task
def scrape_coins(job_id, coin):
    scraper = CoinMarketCapScraper()
    data = scraper.scrape_coin_data(coin)
    scraper.close_driver()

    # Update ScrapingJob with the scraped data
    job = ScrapingJob.objects.get(id=job_id)
    job_data = {
        "coin": coin,
        "output": data
    }
    job.results.append(job_data)
    job.save()
