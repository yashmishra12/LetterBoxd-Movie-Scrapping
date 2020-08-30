import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Test4crawlSpider(CrawlSpider):
    name = 'test4Crawl'
    allowed_domains = ['letterboxd.com']
    
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'


    def start_requests(self):
        yield scrapy.Request(url = 'https://letterboxd.com/films/popular/size/small/page/1/', headers = {
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//div/a[@class='frame has-menu']")), callback='parse_item', follow=True, process_request='set_user_agent'),
    )

    def set_user_agent (self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request
    

    def parse_item(self, response):
        yield {
            'title' : response.xpath('//section[@id="featured-film-header"]/h1/text()').get(),
            'year' : response.xpath('//small[@class="number"]/a/text()').get(),
            'duration' : response.xpath('(//p[@class="text-link text-footer"]/text())[1]').get(),
            'genre' : response.xpath('//div[@class="text-sluglist capitalize"]/p/a/text()').getall(),
            'rating' : response.xpath('//a[contains(@class, "tooltip display-rating")]/text()').get(),
            'language': response.xpath('((//span[contains(text(), "Language")]/parent::node()/following::node())/p/a/text())[1]').get()  
        }
