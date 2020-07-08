# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest


class WattpadBooksSpider(scrapy.Spider):
    name = 'wattpad_books'
    allowed_domains = ['wattpad.com']
    start_urls = ['https://www.wattpad.com/login']

    def parse(self, response):
        yield FormRequest('https://www.wattpad.com/login?nextUrl=%2Fhome',
                          formdata={
                              'username': 'AnnaBella201',
                              'password': 'MyWolverin'
                          },
                          callback=self.parse_logged_in
                          )

    def parse_logged_in(self, response):
        my_works_url = response.xpath(
            '// *[ @ id = "header"] / nav[2] / ul / li / div[2] / ul / li[2] / a/@href').extract_first()
        absolute_work_url = response.urljoin(my_works_url)
        yield scrapy.Request(absolute_work_url, callback=self.parse_my_stories)

    def parse_my_stories(self, response):
        my_books_list = response.xpath('//*[@class = "row story-list"]/div/div')
        for book_ref in my_books_list:
            book_url = book_ref.xpath('.//a/@href').extract_first()
            absolute_book_url = response.urljoin(book_url)
            yield scrapy.Request(absolute_book_url, callback=self.parse_my_book)
            break

    def parse_my_book(self, response):
        chapter_list = response.xpath('//*[@class="parts-list text-left"]/div')
        print(len(chapter_list.extract()))
        for chapter_ref in chapter_list:
            chapter_url = chapter_ref.xpath('.//*[@class="part-name col-xs-12"]/a/@href').extract_first()
            absolute_chapter_url = response.urljoin(chapter_url)
            yield scrapy.Request(absolute_chapter_url, self.parse_read_chapters)

    def parse_read_chapters(self, response):
        writer_editor = response.xpath('//*[@id="writer-editor"]')
        chapter_url = response.url
        chapter_title = writer_editor.xpath('.//*[@id="story-title"]/text()').extract_first()
        chapter_body = writer_editor.xpath('.//div[1]')
        yield {
            'id': int(chapter_url.split('/')[-1]),
            'title':chapter_title,
            'body':chapter_body
        }
