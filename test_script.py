import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor
from crawl.crawl.spiders.uni_crawler import MySpider
# your spider

def f(q, allowed_domains, start_urls):
    try:
        runner = crawler.CrawlerRunner()
        deferred = runner.crawl(MySpider, allowed_domains=allowed_domains, start_urls=start_urls)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)

def run_spider(allowed_domains, start_urls):
    q = Queue()
    p = Process(target=f, args=(q, allowed_domains, start_urls))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

if __name__ == '__main__':
    print('first run:')
    run_spider("oc.edu", 'https://oc.edu/')