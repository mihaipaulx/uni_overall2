from flask import Flask, render_template
from flask_socketio import SocketIO
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from crawl.crawl.spiders.uni_crawler import CrawlSpider
from dotenv import load_dotenv
import os
from forms import YourForm
import json
from scrapy import signals
from scrapy.signalmanager import dispatcher

# Load environment variables
load_dotenv()

# Initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize socketio
socketio = SocketIO(app)

@app.route('/')
def index():
    form = YourForm()

    return render_template('index.html', form=form)



@socketio.on('submit')
def handle_submit(domain, url):
    spider_settings = {
        'FEED_FORMAT': 'jsonlines',
        'FEED_URI': './output/links.jsonl',
    }
    output_file_path = os.path.join(os.path.dirname(__file__), 'output', 'links.jsonl')
    if os.path.exists(output_file_path):
        # If it exists, remove the file
        os.remove(output_file_path)
    process = CrawlerProcess(spider_settings)
    process.crawl(CrawlSpider, domain=domain, url=url)
    dispatcher.connect(emit_result, signal=signals.spider_closed)
    process.start(stop_after_crawl=False)

def emit_result():
    # This method is called when the spider is closed
    # Read the JSON file and emit a SocketIO signal with the data

    file_path = os.path.join(os.path.dirname(__file__), 'output', 'links.jsonl')

    with open(file_path, 'r') as file:
        data = [json.loads(line) for line in file]
        socketio.emit('spider_closed', data)
        print("SPIDER CLOSED SENT")


if __name__ == '__main__':
    socketio.run(app, debug=True)