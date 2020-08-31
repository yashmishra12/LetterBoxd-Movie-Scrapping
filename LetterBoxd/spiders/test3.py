import scrapy
from scrapy_splash import SplashRequest
import re


class Test3Spider(scrapy.Spider):
    name = 'test3'
    allowed_domains = ['letterboxd.com']
    #start_urls = ['https://letterboxd.com/films/popular/size/small/page/1/']

    script = '''
    function main(splash, args)
        splash.private_mode_enabled = false
        assert(splash:go(args.url))
        assert(splash:wait(0.5))
        return splash:html()
    end
    '''

    def start_requests(self):
        yield SplashRequest(url="https://letterboxd.com/csi/film/get-out-2017/rating-histogram/", callback=self.parse, endpoint="execute", args={
            'lua_source': self.script
        })

    def parse(self, response):
        rating = response.xpath('//a[contains(@class,"tooltip display-rating")]/text()').get()
        yield response.follow(url = "https://letterboxd.com/film/get-out-2017/", callback = self.parse_movies, meta = {'rating':rating})
      
    def parse_movies(self, response):
        
        rating = response.request.meta['rating']

        temp = ""
        duration = response.xpath('(//p[@class="text-link text-footer"]/text())[1]').get()
        x = re.findall("\d", duration)
        duration = temp.join(x)

        yield {
            'title' : response.xpath('//section[@id="featured-film-header"]/h1/text()').get(),
            'year' : response.xpath('//small[@class="number"]/a/text()').get(),
            'duration' : duration,
            'genre' : response.xpath('//div[@class="text-sluglist capitalize"]/p/a/text()').getall(),
            'rating': rating,
            'language': response.xpath('((//span[contains(text(), "Language")]/parent::node()/following::node())/p/a/text())[1]').get()  
        }    

