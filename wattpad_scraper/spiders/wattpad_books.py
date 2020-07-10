# -*- coding: utf-8 -*-
from abc import ABC

import scrapy
import json
import re
from _collections import OrderedDict
from scrapy.http import FormRequest


class WattpadBooksSpider(scrapy.Spider):
    name = 'wattpad_books'
    allowed_domains = ['wattpad.com']
    start_urls = ['https://www.wattpad.com/login']
    CHAPTER_URL = 'https://www.wattpad.com/apiv2/storytext?id={}&output=json'  # api url to retrieve chapter body
    book = 'fates intertwined' # name of the book to be scraped

    # method to login into the wattpad account
    def parse(self, response):
        yield FormRequest('https://www.wattpad.com/login?nextUrl=%2Fhome',
                          formdata={
                              'username': 'AnnaBella201',
                              'password': 'MyWolverin'
                          },
                          callback=self.parse_logged_in
                          )

    # navigate to the mystories section of the account
    def parse_logged_in(self, response):
        my_works_url = response.xpath(
            '// *[ @ id = "header"] / nav[2] / ul / li / div[2] / ul / li[2] / a/@href').extract_first()
        absolute_work_url = response.urljoin(my_works_url)
        yield scrapy.Request(absolute_work_url, callback=self.parse_my_stories)

    # retrieve the list of published books in the list and match it to the book to be scraped
    def parse_my_stories(self, response):
        my_books_list = response.xpath('//*[@class = "row story-list"]/div/div')
        for book_ref in my_books_list:
            book_url = book_ref.xpath('.//a/@href').extract_first()
            absolute_book_url = response.urljoin(book_url)
            # comparing the book names
            if self.book == ' '.join(book_url.split('/')[-1].split('-')[1::]):
                yield scrapy.Request(absolute_book_url, callback=self.parse_my_book)
                break

    # retrieving urls for each chapters and navigate to the chapters
    def parse_my_book(self, response):
        chapter_list = response.xpath('//*[@class="parts-list text-left"]/div')
        for chapter_ref in chapter_list:
            chapter_url = chapter_ref.xpath('.//*[@class="part-name col-xs-12"]/a/@href').extract_first()
            absolute_chapter_url = response.urljoin(chapter_url)
            yield scrapy.Request(absolute_chapter_url, self.parse_read_chapters)

    # navigating to each chapters and scraping the chapter title and id, trigger teh api for chapter body data
    def parse_read_chapters(self, response):
        writer_editor = response.xpath('//*[@id="writer-editor"]')
        chapter_url = response.url
        chapter_title = writer_editor.xpath('.//*[@id="story-title"]/text()').extract_first()
        chapter_body_url = self.CHAPTER_URL.format(chapter_url.split('/')[-1])
        yield scrapy.Request(chapter_body_url, callback=self.parse_chapter_body,
                             meta={'chapter_data': {'id': int(chapter_url.split('/')[-1]), 'title': chapter_title}})

    # cleaning te chapter body and yileding each chapter information.
    def parse_chapter_body(self, response):
        cleanup_re = re.compile(r'<[^>]+>')
        chapter_text = json.loads(response.body)['text']
        chapter_data = response.meta['chapter_data']
        chapter_data['chapter_body'] = cleanup_re.sub('', chapter_text)
        yield chapter_data
