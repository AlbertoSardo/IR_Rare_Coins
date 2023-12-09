import scrapy


class DelcampeSpider(scrapy.Spider):
    name = "delcampe"
    allowed_domains = ["www.delcampe.net"]
    start_urls = ["https://www.delcampe.net/it/collezionismo/monete-banconote/search"]

    def parse(self, response):
        # Seleziona tutti gli elementi che iniziano con 'item-'
        items = response.css('div[id^="item-"]')

        for item in items:
            title = item.css('.item-title::text').get()
            price = item.css('.item-price::text').get()
            image_url = item.css('.image-thumb::attr(data-original)').get()

            yield {
                'Title': title,
                'Price': price,
                'Image_URL': image_url
            }
