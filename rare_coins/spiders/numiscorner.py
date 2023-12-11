import scrapy


class NumiscornerSpider(scrapy.Spider):
    name = 'numiscorner'
    start_urls = ['https://www.numiscorner.com/collections/all']

    def parse(self, response):
        products = response.css('div#collectionProduct')

        for product in products:
            title = product.css('a.product-image-container img::attr(alt)').get()
            price = product.css('.price strong span.money::text').get()
            image_url = product.css('a.product-image-container img.lazyload::attr(data-srcset)').get()
            if image_url:
                image_url = image_url.split(' ')[0]
            yield {
                'Title': title,
                'Price': price.strip() if price else None,
                'Image': image_url,
            }
