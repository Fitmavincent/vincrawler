import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CarCrawler(CrawlSpider): 
    name = "car"

    # Rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="page-link next"]',)), callback="parse", follow= True),)

    def start_requests(self):
        urls = [
            'https://www.carsales.com.au/cars/?q=(And.Service.carsales._.(C.Make.Toyota._.Model.Corolla.)_.(C.State.Queensland._.Region.Brisbane.)_.BodyStyle.Hatch._.Year.range(2020..).)',
            'https://www.carsales.com.au/cars/toyota/corolla/queensland-state/brisbane-region/hatch-bodystyle/'
        ]

        headers = {
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        }

        

        for url in urls:
            request = scrapy.Request(url = url, headers = headers, callback=self.parse, cb_kwargs=dict(req_url=url))
            
            # request.cb_kwargs['foo'] = 'bar' # Additional arguments for callback

            yield request

    def parse(self, response, req_url):         

        ITEM_CLASS = 'div.listing-item.card'
        for item in response.css(ITEM_CLASS):

            TITLE_SELECTOR = 'div.card-body div.row div.col h3 a.js-encode-search ::text'
            PRICE_SELECTOR = 'div.item-price div.price a ::text'
            ODO_SELECTOR = 'div.card-body div.row div.col ul.key-details li ::text'
            SELLER_TYPE = 'div.card-footer div.row div.flex-column div.seller-type ::text'
            

            yield {
                'title': item.css(TITLE_SELECTOR).get(),
                'price': item.css(PRICE_SELECTOR).get(),
                'details': item.css(ODO_SELECTOR).getall(),
                'seller_type': item.css(SELLER_TYPE).get().replace('\n', '')                
            }