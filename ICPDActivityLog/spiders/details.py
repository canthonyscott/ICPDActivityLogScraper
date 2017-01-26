# -*- coding: utf-8 -*-
import scrapy


class DetailsSpider(scrapy.Spider):
    name = "details"
    start_urls = ['http://www.iowa-city.org/icgov/apps/police/activityLog.asp']

    def parse(self, response):

        dispatches = response.css('div#content div.pad table tbody tr td a::attr(href)').extract()

        # todo Create request for each dispatch url and extract details

        yield None
