# -*- coding: utf-8 -*-
import scrapy


class ThuquanSpider(scrapy.Spider):
    name = 'thuquan'
    domain = 'https://vnthuquan.net/truyen/mautu.aspx?tua='
    allowed_domains = ['vnthuquan.net']
    start_urls = ['http://vnthuquan.net/truyen/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_title)

    def parse_title(self, response):
        list_title = ['#', 'A', 'B', 'C', 'D', 'Đ', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                      'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        for item in list_title:
            new_url = self.domain + item
            request = scrapy.Request(url=new_url, callback=self.parse_page)
            request.meta['url'] = new_url
            yield request

    def parse_page(self, response):
        total_page = response.css("div#khungchinh span.tinhtong::text").get().split(" ")[-1]
        for i in range(int(total_page)):
            x = int(i)+1
            new_url = response.meta['url'] + '&tranghientai=' + str(x)
            yield scrapy.Request(url=new_url, callback=self.parse_list_item)

    def parse_list_item(self, response):
        list_book = response.css("div#khungchinh div ul li a::attr(href)").getall()
        for item in list_book:
            new_url = self.start_urls[0] + item
            request = scrapy.Request(url=new_url, callback=self.parse_content)
            request.meta['url'] = new_url
            yield request

    def parse_content(self, response):
         pass

