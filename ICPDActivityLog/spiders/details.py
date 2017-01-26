# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from ICPDActivityLog.items import IcpdScrapedDetail
from datetime import date, timedelta
from ICPDActivityLog.dbconn import AddDetails


class DetailsSpider(scrapy.Spider):
    name = "details"
    start_urls = ['http://www.iowa-city.org/icgov/apps/police/activityLog.asp']
    now = date.today()

    def parse(self, response):


        dispatches = response.css('div#content div.pad table tbody tr td a::attr(href)').extract()

        if len(dispatches) < 1:
            raise CloseSpider("No further dates to scrape")


        # todo Create request for each dispatch url and extract details
        for dispatch in dispatches:
            detail_page = response.urljoin(dispatch)
            yield scrapy.Request(detail_page, callback=self.scrape_details)

        # details all gathered, request next page and start over
        self.now = self.now - timedelta(1)
        next_page = response.urljoin('?date=' + self.now.strftime('%m%d%Y'))
        yield scrapy.Request(next_page, callback=self.parse)

    def scrape_details(self, response):
        details = response.xpath('//div[@id="content"]/div[@class="pad"]/table/tbody/tr/td')
        notes = []
        for det in details:
            note = ''.join(det.xpath('.//text()').extract())
            notes.append(note)

        icpd_detail = IcpdScrapedDetail(dispatch=notes[0], details=notes[-1])

        AddDetails(icpd_detail)

        yield dict(icpd_detail)
