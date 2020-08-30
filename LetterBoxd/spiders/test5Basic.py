import scrapy
from scrapy_splash.request import SplashRequest


class Test5basicSpider(scrapy.Spider):
    name = 'test5Basic'
    allowed_domains = ['letterboxd.com']
    # start_urls = ['https://letterboxd.com/films/popular/size/small/page/1/']

    script = '''
    function main(splash, args)
        splash.private_mode_enabled = false
        url = args.url
        assert(splash:go(url))
        assert(splash:wait(4))
        return splash:html()
    end
    '''

    def start_requests(self):
        yield SplashRequest(url="https://letterboxd.com/films/popular/size/small/page/1/", callback=self.parse, endpoint="execute", args={
            'lua_source': self.script
        })

    def parse(self, response):
        links = response.xpath('//a[@class="frame has-menu"]')
        for link in links:
            movie_link = link.xpath('.//@href').get()
            absLink = f"https://letterboxd.com{movie_link}"
            yield response.follow(url = absLink, callback = self.parse_movies)

    def parse_movies(self, response):
        yield {
            'title' : response.xpath('//section[@id="featured-film-header"]/h1/text()').get(),
            'year' : response.xpath('//small[@class="number"]/a/text()').get(),
            'duration' : response.xpath('(//p[@class="text-link text-footer"]/text())[1]').get(),
            'genre' : response.xpath('//div[@class="text-sluglist capitalize"]/p/a/text()').getall(),
            'rating' : response.xpath('//a[contains(@class, "tooltip display-rating")]/text()').get(),
            'language': response.xpath('((//span[contains(text(), "Language")]/parent::node()/following::node())/p/a/text())[1]').get()  
        }