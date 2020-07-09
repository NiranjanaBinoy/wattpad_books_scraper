Wattpad Books Scraper: (on going project)

A Python scraper using Scrapy.\
The scraper is suppose to  login into the wattpad account of the username and password provided and scrap the data from teh book 
 entered by the user.\

Input:
* Username
* Password
* Book name

Working part:
* Spider is logging into wattpad.
* Spider is crawling till the writw >> Mystories >> book >> chapters
* Spider is retrieving the chapter text and title for the book selected.

Remaining:
* Cleaning of the chapter data retrieved to increase readability.
* To develop an interface to enter username and password along with the name of the book to be scraped.
* Exporting book to a readable text format.