import scrapy
from scrapy_splash import SplashRequest


class Test3Spider(scrapy.Spider):
    name = 'test3'
    allowed_domains = ['letterboxd.com']
    #start_urls = ['https://letterboxd.com/films/popular/size/small/page/1/']

    script1 = '''
    function main(splash, args)
        splash.private_mode_enabled = false
        url = args.url
        assert(splash:go(url))
        assert(splash:wait(1))
        movies = assert(splash:select_all("a.frame.has-menu"]))
        movies[2]:mouse_click()
        assert(splash:wait(1))
        splash:set_viewport_full()
        return splash:html()
    end
    '''
    def start_requests(self):
        yield SplashRequest(url="https://letterboxd.com/films/popular/size/small/page/1/", callback=self.parse, endpoint="execute", args={
            'lua_source': self.script1
        })

    def parse(self, response):
        # movies  = response.xpath('//a[@class="frame has-menu"]').getall()
        # print (movies)
      
        yield {
            'title' : response.xpath('//section[@id="featured-film-header"]/h1/text()').get(),
            'year' : response.xpath('//small[@class="number"]/a/text()').get(),
            'duration' : response.xpath('(//p[@class="text-link text-footer"]/text())[1]').get(),
            'genre' : response.xpath('//div[@class="text-sluglist capitalize"]/p/a/text()').getall(),
            'rating' : response.xpath('//a[contains(@class, "tooltip display-rating")]/text()').get(),
            'language': response.xpath('((//span[contains(text(), "Language")]/parent::node()/following::node())/p/a/text())[1]').get()  
        }

