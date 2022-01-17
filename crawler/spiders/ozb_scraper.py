import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

base_url = "https://www.ozbargain.com.au"

class OzbCrawler(CrawlSpider):
    name = "ozb"
    page = 10
    wish_list = [
        'Nintendo', 
        '3080', 
        'LEGO',
        'Credit Card',
    ]
    
    def start_requests(self):
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

            TAG_SELECTOR = '.tagger.expired ::text'
            NAME_SELECTOR = 'h2 ::text'
            PRICE_SELECTOR = 'em ::text'
            HREF_SELECTOR = 'a ::attr(href)'

            item_tag = item.css(TAG_SELECTOR).get() # Check any expired deal
            item_name = item.css(NAME_SELECTOR).get()
            item_price = item.css(PRICE_SELECTOR).get()
            item_link = item.css(HREF_SELECTOR).get()

            for wish_item in OzbCrawler.wish_list:
                yield self.get_wish(wish_item, item_tag, item_name, item_price, item_link)      

    def get_wish(self, wish_item, item_tag, item_name, item_price, item_link):        
        if(wish_item in item_name and item_tag is None):
            match_entry = {
                'tag': item_tag,
                'name': item_name,
                'price': item_price,
                'link': f'{base_url}{item_link}'
            }

            return match_entry
