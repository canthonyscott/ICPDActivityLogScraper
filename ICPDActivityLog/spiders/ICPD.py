import scrapy
from scrapy.exceptions import CloseSpider
from ICPDActivityLog.items import IcpdactivitylogItem
from datetime import date, timedelta
from ICPDActivityLog.dbconn import AddToDb


class ICPDSpider(scrapy.Spider):
    name = "ICPD"
    now = date.today()

    start_urls =[
        'https://www8.iowa-city.org/icgov/apps/police/activitylog.asp'
    ]

    def parse(self, response):

        ids = response.xpath('//div[@class="pad"]/table/tbody/tr/td/a/text()').extract()
        data = [txt for item in response.css('div.pad table tbody tr td') for txt in item.select('text()').extract() or [u'']]

        if len(data) < 1:
            raise CloseSpider('No further dates to scrape')

        x = 0
        for id in ids:
            row = data[x:x+9]
            log_item = IcpdactivitylogItem(dispatch=id, inc=row[2].strip(), activity=row[3], disposition=row[4], addr=row[5],
                                           apt=row[6], time=row[7].strip(), date=self.now.strftime('%Y%m%d'))
            AddToDb(log_item) # Pass this scrapy item to the database controller
            x = x + 9
            yield dict(log_item)

        self.now = self.now - timedelta(1)
        next_page = response.urljoin('?date=' + self.now.strftime('%m%d%Y'))
        yield scrapy.Request(next_page, callback=self.parse)




