"""
test1 spider crawls from Ajax URL which does not need JavaScript
"""
import scrapy
from scrapy_splash import SplashRequest
import re



class Test1Spider(scrapy.Spider):
    name = 'test1'
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
    pagination = 1

    def start_requests(self):
        yield scrapy.Request(url=f"https://letterboxd.com/films/ajax/popular/size/small/page/1/", callback=self.parse)
        

    def parse(self, response):
        # url = response.url
        for movie in response.xpath('//a[@class="frame"]/@href'):
            
            movieName = movie.get().split("/")
            movieName = movieName[2]
 
            yield response.follow(
                url=f'https://letterboxd.com/csi/film/{movieName}/rating-histogram/',
                callback=self.parse_movie_rating,
                meta = {'movieName': movieName}
            )


        if (self.pagination < 8137):
            self.pagination += 1
            yield scrapy.Request(
                url=f"https://letterboxd.com/films/ajax/popular/size/small/page/{self.pagination}/",    
                callback=self.parse
            )

    
    def parse_movie_rating(self, response):
        movieName = response.request.meta['movieName']
        rating = response.xpath('//a[contains(@class,"tooltip display-rating")]/text()').get()
        # use extract() instead of get() to get the complete element with its attributes as STRING. Because custom attributes can have different
        # name seen by scrapy and seen by inspect element by us. 
        
        # viewers = response.css("a.tooltip.display-rating ::attr(title)").get()  #THIS IS JUST THE CSS VERSION OF BELOW

        viewers = response.xpath('//a[contains(@class,"tooltip display-rating")]/@title').get()

        yield response.follow(url = f"https://letterboxd.com/film/{movieName}/", callback = self.parse_movies, meta = {'rating':rating, 'viewers': viewers})
      
      
    def parse_movies(self, response):
        
        rating = response.request.meta['rating']
        viewers = response.request.meta['viewers']

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
            'language': response.xpath('((//span[contains(text(), "Language")]/parent::node()/following::node())/p/a/text())[1]').get(),
            'viewers': viewers    
        }    

