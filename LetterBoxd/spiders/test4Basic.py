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
        assert(splash:go(args.url))
        assert(splash:wait(0.5))
        return splash:html()
    end
    '''
 
    def start_requests(self):
        yield SplashRequest(url='https://letterboxd.com/films/popular/size/small/page/1/', callback=self.parse, endpoint="execute", args={
            'lua_source': self.script1
        })
 
    def parse(self, response):
        for movie in response.xpath("//li[@class='listitem poster-container']"):
            print("SHAKTIMAAN---------------------------------", movie)
            movie_url = movie.xpath("(.//a[@class='frame'])[1]/@href").get()
            yield scrapy.Request(
                url=f'https://letterboxd.com{movie_url}',
                callback=self.parse_movie,
            )
 
        next_page = response.xpath("//a[@class='next']/@href").get()
        if next_page:
            yield SplashRequest(
                url=f'https://letterboxd.com{next_page}',
                endpoint='execute',
                args={
                    'lua_source': self.script1
                },
                callback=self.parse
            )
 
    def parse_movie(self, response):
        title = response.xpath(
            '//section[@id="featured-film-header"]/h1/text()').get(),
        year = response.xpath('//small[@class="number"]/a/text()').get(),
        duration = response.xpath(
            '(//p[@class="text-link text-footer"]/text())[1]').get(),
        genre = response.xpath(
            '//div[@class="text-sluglist capitalize"]/p/a/text()').getall(),
        rating = response.xpath(
            '//a[contains(@class, "tooltip display-rating")]/text()').get(),
        language = response.xpath(
            '((//span[contains(text(), "Language")]/parent::node()/following::node())/p/a/text())[1]').get()
 
        yield {
            'title': title,
            'year': year,
            'duration': duration,
            'genre': genre,
            'rating': rating,
            'language': language
        }