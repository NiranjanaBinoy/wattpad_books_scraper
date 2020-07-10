Wattpad Books Scraper:

A Python scraper using Scrapy.\
The scraper is suppose to  login into the wattpad account of the username and password provided and scrap the data from teh book 
 entered by the user.\

Input:
* Username
* Password
* Book name

Working part:
* Spider is logging into wattpad.
* Spider is crawling till the write >> Mystories >> book >> chapters
* Spider is retrieving the chapter text and title for the book selected.
* Chapter body is cleaned of the html tags
* The dictionary with chapter id, title and body is yielded. 