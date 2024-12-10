import scrapy
from bookstoscrape.items import Book

class BooksSpider(scrapy.Spider):
    name = "books_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            book_item = Book()

            book_item['title'] = book.css('h3 a::text').get()
            book_item['price'] = book.css('.product_price .price_color::text').get()
            book_item['rating'] = book.css('.star-rating::attr(class)').get().split()[1]

            yield book_item
