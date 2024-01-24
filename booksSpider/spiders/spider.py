import scrapy
from urllib.parse import urljoin
from booksSpider.items import BookItem

class BooksSpider(scrapy.Spider):
    """
    Simple spider to scrape books's data from https://books.toscrape.com/
    """
    name = "bookss"
    start_urls = ["https://books.toscrape.com/index.html"]

    def parse(self, response):
        """
        Parse index.html to get all category's urls and follow them to scrape each one.
        """
        category_links = response.xpath("//ul[@class='nav nav-list']/li/ul/li[*]/a/@href").getall()

        for category_link in category_links:
            yield response.follow(category_link, callback=self.parse_category)

    def parse_category(self, response):
        """
        Parse category page and extract books's.
        Datas are stored in scrapy items.
        If there is a next page, it will go to and scrape it until no more.
        """
        for book in response.xpath("//article[@class='product_pod']"):
            rankDict = {
                "One": 1,
                "Two": 2,
                "Three": 3,
                "Four": 4,
                "Five": 5
            }
            item = BookItem()
            item["title"] = book.xpath("h3/a/@title").get()
            item["price"] = book.xpath("div[@class='product_price']/p[@class='price_color']/text()").get()
            item["rank"] = rankDict[book.xpath("p/@class").get().split(" ")[1]]
            item["availability"] = bool(book.xpath("div[@class='product_price']/p[@class='instock availability']/i[@class='icon-ok']"))
            item["category"] = response.xpath("//div[@class='page-header action']/h1/text()").get()
            item["url"] = urljoin(response.url, book.xpath("h3/a/@href").get())
            yield item

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_category)