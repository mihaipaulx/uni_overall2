from flask import Flask, render_template
from flask_socketio import SocketIO
from scrapy.crawler import CrawlerProcess
from crawl.crawl.spiders.uni_crawler import CrawlSpider
from dotenv import load_dotenv
import os
from forms import YourForm
import json
from scrapy import signals
from scrapy.signalmanager import dispatcher
from multiprocessing import Process
from functools import partial
from twisted.internet import reactor, defer

# Load environment variables
load_dotenv()

# Initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize socketio
socketio = SocketIO(app)

spider_settings = {
        'FEEDS': { "./output/links.jsonl": { "format": "jsonlines", "overwrite": True } }
    }

def crawl(domain, url):
    crawler = CrawlerProcess(spider_settings)
    crawler.crawl(CrawlSpider, domain=domain, url=url)
    crawler.start(stop_after_crawl=False)

d = defer.Deferred()

@socketio.on('submit')
def handle_submit(domain, url):
    dispatcher.connect(emit_result, signal=signals.spider_closed)
    # Create a Process instance with the partial function


    process = CrawlerProcess(spider_settings)

    d.addCallback(emit_result)

    process.crawl(CrawlSpider, domain=domain, url=url)
    
    reactor.run()


def emit_result():
    # This method is called when the spider is closed
    # Read the JSON file and emit a SocketIO signal with the data

    file_path = os.path.join(os.path.dirname(__file__), 'output', 'links.jsonl')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = [json.loads(line) for line in file]
            socketio.emit('spider_closed', data)
            print("SPIDER CLOSED SENT")
        os.remove(file_path)
        dispatcher.disconnect(emit_result, signal=signals.spider_closed)
        
@app.route('/')
def index():
    form = YourForm()

    return render_template('index.html', form=form)

if __name__ == '__main__':

    socketio.run(app)