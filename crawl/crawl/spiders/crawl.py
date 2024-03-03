import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from collections import deque
from ..items import LinkItem

class MySpider(CrawlSpider):
    def __init__(self, allowed_domains=None, start_urls=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        
        self.allowed_domains = [allowed_domains]
        self.start_urls = [start_urls]
        self.item_count = 0
        self.max_item_count = 50
    
    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        
        settings.set('DEPTH_PRIORITY', 1)
        settings.set('SCHEDULER_DISK_QUEUE', "scrapy.squeues.MarshalFifoDiskQueue")
        settings.set('SCHEDULER_MEMORY_QUEUE', "scrapy.squeues.FifoMemoryQueue")
        settings.set('CONCURRENT_REQUESTS', 64)
        settings.set('CONCURRENT_REQUESTS_PER_DOMAIN', 64)
        settings.set('LOG_ENABLED ', False)
        settings.set('HTTPCACHE_ENABLED  ', True)


    # ---

    name = "crawl"
    
    rules = (Rule(LinkExtractor(), callback='parse_item', follow=True),)

    keywords = {
        "programs": ["program", "degree", "course", "major", "school", "faculty", "faculties"],
        "tuition": ["tuition", "cost", "fees", "finaid", "financialaid", "financial"],
        "calendar": ["calendar", "intake", "term", "start"],
        "deadlines": ["apply", "deadline", "application", "admission"],
        "requirements": ["req", "requirements"],
        "english": ["english", "language", "proficiency", "ielts", "toefl"]
    }

    def parse_item(self, response):
        # Calculate the depth of the URL
        if self.item_count >= self.max_item_count:
            raise scrapy.exceptions.CloseSpider("Reached maximum item count")
        depth = response.meta['depth']

        content_type = response.headers.get('Content-Type', b'').decode('utf-8')
        if not content_type.startswith('text/html'):
            return  # Skip non-HTML content

        # print("Visited url: ", response.url)

        # Check if any keyword is present in the URL
        for type_, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in response.url:
                    self.item_count += 1

                    link_item = LinkItem()
                    link_item["url"] =      response.url
                    link_item["type"] =     type_
                    link_item["keyword"] =  keyword
                    link_item["depth"] =    depth

                    print(f"{self.item_count}. Found url: {response.url} with keyword {keyword}")

                    yield link_item
   