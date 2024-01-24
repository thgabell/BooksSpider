import scrapy

class BookItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    rank = scrapy.Field()
    availability = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
