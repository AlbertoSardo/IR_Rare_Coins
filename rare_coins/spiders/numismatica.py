import scrapy
import json


class NumismaticaTrionfaleSpider(scrapy.Spider):
    name = "numismatica"
    start_urls = ["https://www.numismaticatrionfale.com/home.aspx"]

    def parse(self, response):
        for item in response.css("div.vetrinaitem"):
            title = item.css("div.vetrinaitem_corpo h2::text").get()
            price = item.css("div.vetrinaitem_prezzo span::text").get()
            description = item.css("div.vetrinaitem_riassunto::text").get()
            image_url = item.css("div.vetrinaitem_immagine img::attr(src)").get()

            yield {
                "Title": title.strip() if title else None,
                "Price": price.strip() if price else None,
                "Description": description.strip() if description else None,
                "Image": response.urljoin(image_url) if image_url else None,
            }
