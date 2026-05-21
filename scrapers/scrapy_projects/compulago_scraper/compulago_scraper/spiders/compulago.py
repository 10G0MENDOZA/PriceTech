import scrapy
import re

class CompulagoSpider(scrapy.Spider):
    name = "compulago"
    allowed_domains = ["compulago.com"]
    
    start_urls = [
        "https://compulago.com/categoria/portatil-partes/memoria-ram/",
        "https://compulago.com/categoria/portatiles/"
    ]

    def parse(self, response):

        productos = response.css("a::attr(href)").getall()
        seen = set()

        for url in productos:

            if not url:
                continue

            if "/producto/" not in url:
                continue

            if url in seen:
                continue
            seen.add(url)

            yield response.follow(url, callback=self.parse_producto)

        # paginación
        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_producto(self, response):

        nombre = response.css("h1::text").get()
        precio = response.css(".woocommerce-Price-amount::text").get()

        # atributos (RAM, procesador, etc)
        atributos = response.css(".product-attributes li::text").getall()
        atributos = [a.strip() for a in atributos if a.strip()]

        if nombre and precio:
            yield {
                "nombre": nombre.strip(),
                "precio": self.limpiar_precio(precio),
                "url": response.url,
                "tienda": "compulago",
                "atributos": atributos
            }

    def limpiar_precio(self, precio):
        numeros = re.sub(r"[^\d]", "", precio)
        return int(numeros) if numeros else 0