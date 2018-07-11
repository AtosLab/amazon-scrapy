# -*- coding: utf-8 -*-
import scrapy


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    start_urls = (
        'http://www.amazon.com/',
    )

    def parse(self, response):
        pass
