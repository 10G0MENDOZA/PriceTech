BOT_NAME = "compulago_scraper"

SPIDER_MODULES = ["compulago_scraper.spiders"]
NEWSPIDER_MODULE = "compulago_scraper.spiders"

ROBOTSTXT_OBEY = False  # importante para scraping

DOWNLOAD_DELAY = 1

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

ITEM_PIPELINES = {
    "compulago_scraper.pipelines.MongoPipeline": 300,
}

FEED_EXPORT_ENCODING = "utf-8"