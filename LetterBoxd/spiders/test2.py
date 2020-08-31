import scrapy


class Test2Spider(scrapy.Spider):
    name = 'test2'
    allowed_domains = ['letterboxd.com']
    start_urls = ['http://letterboxd.com/']

    def parse(self, response):
        pass
