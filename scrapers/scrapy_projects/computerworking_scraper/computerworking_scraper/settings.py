# Scrapy settings for computerworking_scraper project

BOT_NAME = "computerworking_scraper"

SPIDER_MODULES = ["computerworking_scraper.spiders"]
NEWSPIDER_MODULE = "computerworking_scraper.spiders"

ADDONS = {}

# USER AGENT (opcional pero recomendado)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Concurrency y control (bien para no ser bloqueado)
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1

# Cookies (puedes dejarlo así)
#COOKIES_ENABLED = False

# Headers opcionales
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es",
}

# Pipelines (si luego conectas Mongo aquí va)
ITEM_PIPELINES = {
    'computerworking_scraper.pipelines.MongoPipeline': 300,
}
# Encoding
FEED_EXPORT_ENCODING = "utf-8"