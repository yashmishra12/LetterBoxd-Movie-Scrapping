import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from LetterBoxd.spiders.test4Basic import Test4basicSpider
import sys



process = CrawlerProcess(settings=get_project_settings())
process.crawl(Test4basicSpider)
process.start