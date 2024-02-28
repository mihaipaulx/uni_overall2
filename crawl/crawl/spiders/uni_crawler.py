# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# from urllib.parse import urlparse
# from ..items import LinkItem

# class CrawlSpider(CrawlSpider):
#     name = 'uni_crawler'
#     # allowed_domains = ['ou.edu']  # Replace with the domain you want to crawl
#     # start_urls = ['https://www.ou.edu']  # Replace with the starting URL
#     def __init__(self, *args, **kwargs):
#         super(CrawlSpider, self).__init__(*args, **kwargs)
#         self.allowed_domains = [kwargs.get('domain')]
#         self.start_urls = [kwargs.get('url')]
#         self.item_count = 0

#     # Rules to horizontally crawl through links
#     rules = (
#         Rule(LinkExtractor(), callback='parse_item', follow=True),
#     )
    
#     # Keywords to search for in URLs
#     keywords = {
#         "programs": ["program", "degree", "course", "major", "school", "faculty", "faculties"],
#         "tuition": ["tuition", "cost", "fees", "finaid", "financialaid", "financial"],
#         "calendar": ["calendar", "intake", "term", "start"],
#         "deadlines": ["apply", "deadline", "application", "admission"],
#         "requirements": ["req", "requirements"],
#         "english": ["english", "language", "proficiency", "ielts", "toefl"]
#     }

#     def parse_item(self, response):
#         # Calculate the depth of the URL
#         parsed_url = urlparse(response.url)
#         depth = parsed_url.path.count('/')  # Count the slashes in the path
        
#         # Check if any keyword is present in the URL
#         for type_, keywords in self.keywords.items():
#             for keyword in keywords:
#                 if keyword in response.url:
#                     self.item_count += 1

#                     if self.item_count > 100:  # Stop yielding items if count reaches 20
#                         raise scrapy.exceptions.CloseSpider("Reached maximum item count")
#                     else:
#                         link_item = LinkItem()
#                         link_item["url"] =      response.url
#                         link_item["type"] =     type_
#                         link_item["keyword"] =  keyword
#                         link_item["depth"] =    depth

#                         yield link_item





import scrapy
from scrapy import signals
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlparse
from collections import deque
from ..items import LinkItem

class CrawlSpider(CrawlSpider):
    name = 'uni_crawler'

    def __init__(self, *args, **kwargs):
        super(CrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = [kwargs.get('domain')]
        self.start_urls = [kwargs.get('url')]
        self.item_count = 0
        self.max_item_count = 5
        self.visited_urls = set()  # Set to keep track of visited URLs
        self.queue = deque()  # Queue for BFS

    # Keywords to search for in URLs
    keywords = {
        "programs": ["program", "degree", "course", "major", "school", "faculty", "faculties"],
        "tuition": ["tuition", "cost", "fees", "finaid", "financialaid", "financial"],
        "calendar": ["calendar", "intake", "term", "start"],
        "deadlines": ["apply", "deadline", "application", "admission"],
        "requirements": ["req", "requirements"],
        "english": ["english", "language", "proficiency", "ielts", "toefl"]
    }

    def parse_start_url(self, response):
        self.queue.append((response.url, 0))
        return self.parse_next()

    def parse_next(self):
        while self.queue:
            url, depth = self.queue.popleft()
            if url not in self.visited_urls:
                self.visited_urls.add(url)
                yield scrapy.Request(url, callback=self.parse_item, meta={'depth': depth})

    def parse_item(self, response):
        # Calculate the depth of the URL
        depth = response.meta['depth']

        # Check if any keyword is present in the URL
        for type_, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in response.url:
                    self.item_count += 1

                    if self.item_count > self.max_item_count:
                        raise scrapy.exceptions.CloseSpider("Reached maximum item count")
                    else:
                        link_item = LinkItem()
                        link_item["url"] =      response.url
                        link_item["type"] =     type_
                        link_item["keyword"] =  keyword
                        link_item["depth"] =    depth

                        yield link_item

        # Extract links for the next level of BFS
        links = LinkExtractor().extract_links(response)
        for link in links:
            self.queue.append((link.url, depth + 1))

        yield from self.parse_next()