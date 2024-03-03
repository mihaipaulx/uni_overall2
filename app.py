from flask import Flask, render_template
from flask_socketio import SocketIO
import scrapy.crawler as crawler
from crawl.crawl.spiders.uni_crawler import MySpider
from dotenv import load_dotenv
import os
from forms import YourForm
import json
from scrapy import signals
from scrapy.signalmanager import dispatcher
from multiprocessing import Process, Queue
from twisted.internet import reactor
from functools import partial
import traceback
import logging
from scrapy.utils.project import get_project_settings

  # Configure logging
logging.basicConfig(level=logging.ERROR)


# Load environment variables
load_dotenv()

# Initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize socketio
socketio = SocketIO(app)

spider_settings = {
    'FEEDS': {
        "./output/links.jsonl": {
            "format": "jsonlines",
            "overwrite": True
        }
    }
}

from multiprocessing.context import Process

# -----

def f(q, allowed_domains, start_urls):
    try:
         # Get project settings
        settings = get_project_settings()

        # Customize spider settings
        spider_settings = {
            'FEEDS': {
                "./output/links.jsonl": {
                    "format": "jsonlines",
                    "overwrite": True
                }
            }
        }

        # Update the settings with custom spider settings
        settings.update(spider_settings)

        # Initialize CrawlerRunner with custom settings
        runner = crawler.CrawlerRunner(settings)
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

# ------

# def crawl(domain, url):
#     crawler = CrawlerProcess(spider_settings)
#     crawler.crawl(CrawlSpider, domain=domain, url=url)
#     crawler.start(stop_after_crawl=False)

@socketio.on('submit')
def handle_submit(allowed_domains, start_urls):
    dispatcher.connect(emit_result, signals.spider_closed)
    # crawl_partial = partial(crawl, domain, url)
    # print("DON'T IGNORE ME 1")
    # # Create a Process instance with the partial function
    # process = Process(target=crawl_partial)
    # print("DON'T IGNORE ME 2")
    # process.start()
    # print("DON'T IGNORE ME 3")
    # process.join(15)
    # print("DON'T IGNORE ME 4")
    
    # print("DON'T IGNORE ME 5")
    
    run_spider(allowed_domains, start_urls)

    # process = CrawlerProcess(spider_settings)
    # process.crawl(CrawlSpider, domain=domain, url=url)
    # process.start(stop_after_crawl=False)

    # emit_result()

def emit_result():
  print("Emit result fired")
  # This method is called when the spider is closed
  # Read the JSON file and emit a SocketIO signal with the data
  file_path = os.path.join(os.path.dirname(__file__), 'output', 'links.jsonl')

  if os.path.exists(file_path):
      with open(file_path, 'r') as file:
          data = [json.loads(line) for line in file]
          print(data)
          socketio.emit('spider_closed', data)
          print("SPIDER CLOSED SENT")
  # dispatcher.disconnect(emit_result, signals.spider_closed)

@app.route('/')
def index():
    form = YourForm()
    return render_template('index.html', form=form)

@socketio.on_error() # Handles all errors in the socket communication
def handle_error(e):
    print("An error occurred:", e)
    print(traceback.format_exc())

if __name__ == '__main__':
  socketio.run(app, debug=True, log_output=True)