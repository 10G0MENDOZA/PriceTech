import scrapy
import re


class ComputerworkingSpider(scrapy.Spider):
    name = "computerworking"
    allowed_domains = ["computerworking.com.co"]

    start_urls = [
        # PORTÁTILES
        "https://www.computerworking.com.co/categorias/231/false",

        # MEMORIAS RAM
        "https://www.computerworking.com.co/search/memoria/1"
    ]

    def parse(self, response):

        productos = response.css("div.productBox")

        for p in productos:

            nombre = p.css("div.productCaption h5::text").get()
            precio = p.css("div.productCaption h3::text").get()
            url = p.css("div.productCaption a::attr(href)").get()

            if nombre and precio:

                yield {
                    "nombre": nombre.strip(),
                    "precio": self.limpiar_precio(precio),
                    "url": response.urljoin(url) if url else "",
                    "tienda": "computerworking"
                }

        # PAGINACIÓN 
        next_page = response.css("a[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def limpiar_precio(self, precio):
        numeros = re.sub(r"[^\d]", "", precio)
        return int(numeros) if numeros else 0