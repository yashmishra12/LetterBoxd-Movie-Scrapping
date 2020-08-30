import scrapy
from scrapy_splash import SplashRequest

class Test4basicSpider(scrapy.Spider):
    name = 'test4Basic'
    allowed_domains = ['letterboxd.com']
    start_urls = ['https://letterboxd.com/films/popular/size/small/page/1/']
    # start_urls = ['https://letterboxd.com/film/tales-from-the-darkside-the-movie/']

    script1 = '''
    function main(splash, args)
        splash.private_mode_enabled = false
        url = args.url
        assert(splash:go(args.url))
        assert(splash:wait(0.5))
        --movie_list = assert(splash:select_all("a.frame.has-menu"))
        return 
    end
    '''
# https://letterboxd.com/films/popular/size/small/page/1/

# {
#             html = splash:html()
#         }

    def start_requests(self):
        yield SplashRequest(url='https://letterboxd.com/film/tales-from-the-darkside-the-movie/', callback=self.parse, endpoint="execute", args={
            'lua_source': self.script1
        })

    def parse(self, response):
        yield {
            'title' : response.xpath('//section[@id="featured-film-header"]/h1/text()').get(),
            'year' : response.xpath('//small[@class="number"]/a/text()').get(),
            'duration' : response.xpath('(//p[@class="text-link text-footer"]/text())[1]').get(),
            'genre' : response.xpath('//div[@class="text-sluglist capitalize"]/p/a/text()').getall(),
            'rating' : response.xpath('//a[contains(@class, "tooltip display-rating")]/text()').get(),
            'language': response.xpath('((//span[contains(text(), "Language")]/parent::node()/following::node())/p/a/text())[1]').get()  
        }
