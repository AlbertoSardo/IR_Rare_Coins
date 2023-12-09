import scrapy


class CavalierenumismaticaSpider(scrapy.Spider):
    name = "cavalierenumismatica"
    allowed_domains = ["cavalierenumismatica.com"]
    start_urls = ["https://cavalierenumismatica.com"]

    def parse(self, response):
        coin_divs = response.css('div.col-md-4.col-sm-6')

        for div in coin_divs:
            title = div.css('div.productname a::text').get()
            price = div.css('p.center-text strong::text').get()
            image = div.css('div.products-imgCont img::attr(src)').get()

            yield {
                'Title': title,
                'Price': price,
                'Image': image,
            }
