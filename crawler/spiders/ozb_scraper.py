from datetime import datetime
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawler.items import OzbItem

base_url = "https://www.ozbargain.com.au"

class OzbCrawler(CrawlSpider):
    name = "ozb"
    page = 10
    wish_list = []
    # wish_list = [
    #     'Nintendo',
    #     'LEGO',
    #     'Xiaomi'
    # ]
    
    def start_requests(self, *args):
        
        # OzbCrawler.wish_list = self.wishes
        if hasattr(self, 'wishes'):
            print(self.wishes)
            OzbCrawler.wish_list = [e.strip() for e in self.wishes.split(',')] # strip and split at the same time
            print(OzbCrawler.wish_list)
        
        urls = [
            base_url
        ]

        headers = {
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        }        
        
        for i in range(1, OzbCrawler.page + 1):
            urls.append(f'{base_url}/?page={i}')
        
        for url in urls:
            yield scrapy.Request(url = url, headers=headers, callback=self.parse)

    def parse(self, response):
        suggest_item = []

        ITEM_CLASS = '.node-ozbdeal'
        for item in response.css(ITEM_CLASS):
            # for wish_item in OzbCrawler.wish_list:
            yield self.get_wish(item)

    def get_wish(self, item):
        EXPIRE_TAG_SELECTOR = '.tagger.expired ::text'
        UPCOMING_TAG_SELECTOR = '.tagger.upcoming ::text'
        NAME_SELECTOR = 'h2 ::attr(data-title)'
        PRICE_SELECTOR = 'em ::text'
        HREF_SELECTOR = 'a ::attr(href)'
        
        IMAGE_SELECTOR = '.foxshot-container a img::attr(src)'
        TIME_SELECTOR = '//div[@class="submitted"]/text()'

        expired_tag = item.css(EXPIRE_TAG_SELECTOR).get() # Check is expired deal
        upcoming_tag = item.css(UPCOMING_TAG_SELECTOR).get() # Check is upcoming deal
        item_name = item.css(NAME_SELECTOR).get()
        item_price = item.css(PRICE_SELECTOR).get()
        item_link = item.css(HREF_SELECTOR).get()
        
        item_image = item.css(IMAGE_SELECTOR).get()
        item_time = item.xpath(TIME_SELECTOR).get()
        
        for wish_item in OzbCrawler.wish_list:
            if(wish_item.lower() in item_name.lower() and expired_tag is None):
                match_entry = OzbItem (tag = self.process_tag(expired_tag, upcoming_tag), name = item_name, price = item_price, link = f'{base_url}{item_link}', image = item_image, time = self.format_time(item_time))
                return match_entry

    def format_time(self, timeStr):
        stripStr = timeStr.replace(" on ", "").strip()
        datetime_object = datetime.strptime(stripStr, '%d/%m/%Y - %H:%M')
        return datetime_object

    def process_tag(self, *tags):
        for tag in tags:
            if(tag is not None):
                return tag
