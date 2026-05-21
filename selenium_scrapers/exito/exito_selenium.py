import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from database.mongo_connection import get_db


# =========================================================
# URLS — PORTÁTILES Y MEMORIAS RAM
# =========================================================

URLS = [

    # --- PORTÁTILES ---
    {
        "url": "https://www.exito.com/tecnologia/computadores/portatiles",
        "categoria": "portatil",
        "keywords_incluir": ["portatil", "portátil", "laptop", "notebook"],
        "keywords_excluir": ["memoria", "ram", "ddr3", "ddr4", "ddr5"]
    },

    # --- MEMORIAS RAM ---
    {
        "url": "https://www.exito.com/s?q=MEMORIA+DDR4&sort=score_desc&page=0",
        "categoria": "memoria",
        "keywords_incluir": ["memoria", "ram", "ddr3", "ddr4", "ddr5", "sodimm", "dimm"],
        "keywords_excluir": ["portatil", "portátil", "laptop", "notebook", "computador"]
    },
    {
        "url": "https://www.exito.com/s?q=MEMORIA+DDR3&sort=score_desc&page=0",
        "categoria": "memoria",
        "keywords_incluir": ["memoria", "ram", "ddr3", "ddr4", "ddr5", "sodimm", "dimm"],
        "keywords_excluir": ["portatil", "portátil", "laptop", "notebook", "computador"]
    },
    {
        "url": "https://www.exito.com/s?q=MEMORIA+RAM&sort=score_desc&page=0",
        "categoria": "memoria",
        "keywords_incluir": ["memoria", "ram", "ddr3", "ddr4", "ddr5", "sodimm", "dimm"],
        "keywords_excluir": ["portatil", "portátil", "laptop", "notebook", "computador"]
    },

]


# =========================================================
# INICIAR DRIVER
# =========================================================

def iniciar_driver():
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )


# =========================================================
# SCROLL INTELIGENTE
# =========================================================

def hacer_scroll(driver):
    print("  Iniciando scroll...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    intentos = 0
    while intentos < 15:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        intentos += 1
    print(f"  Scroll terminado ({intentos} iteraciones)")


# =========================================================
# OBTENER PRECIO
# =========================================================

def obtener_precio(producto, nombre):
    selectores = [
        ".ProductPrice_container__price__XmMWA",
        "[data-testid='store-price']",
        ".price_fs-price__4GZ9F",
        "[data-fs-container-price-otros='true']",
    ]
    for selector in selectores:
        try:
            precio_texto = producto.find_element(By.CSS_SELECTOR, selector).text
            precio_limpio = int(re.sub(r"[^\d]", "", precio_texto))
            if precio_limpio > 0:
                return precio_limpio
        except:
            continue
    print(f"  ⚠ Sin precio: {nombre}")
    return None


# =========================================================
# VALIDAR PRODUCTO
# =========================================================

def es_valido(nombre, keywords_incluir, keywords_excluir):
    nombre_lower = nombre.lower()

    # Debe tener AL MENOS UNA palabra de incluir
    tiene_incluir = any(kw in nombre_lower for kw in keywords_incluir)

    # NO debe tener palabras de excluir (a menos que también tenga incluir)
    # Para portátiles: "Portatil HP RAM 8GB" SÍ es válido (RAM está en el nombre)
    # Para memorias: "Memoria DDR4 Para Portatil" SÍ es válido
    # Lo que excluimos son productos que SON otra categoría
    tiene_excluir = all(kw in nombre_lower for kw in keywords_excluir)

    return tiene_incluir and not tiene_excluir


# =========================================================
# SCRAPER PRINCIPAL
# =========================================================

def main():
    driver = iniciar_driver()
    db = get_db()

    total_guardados = 0
    total_errores = 0
    total_saltados = 0

    for config in URLS:

        url        = config["url"]
        categoria  = config["categoria"]
        kw_incluir = config["keywords_incluir"]
        kw_excluir = config["keywords_excluir"]

        print("\n" + "=" * 60)
        print(f"🌐 [{categoria.upper()}] {url}")
        print("=" * 60)

        driver.get(url)
        time.sleep(5)

        hacer_scroll(driver)

        # =====================================================
        # SELECTOR DE PRODUCTOS
        # =====================================================

        productos = driver.find_elements(
            By.CSS_SELECTOR,
            "div.productCard_contentInfo__CBBA7"
        )

        print(f"📦 Productos encontrados: {len(productos)}")

        if len(productos) == 0:
            productos = driver.find_elements(
                By.CSS_SELECTOR,
                "[data-testid='product-card']"
            )
            print(f"  (selector alternativo): {len(productos)}")

        # =====================================================
        # PROCESAR CADA PRODUCTO
        # =====================================================

        for p in productos:
            try:

                # Nombre
                nombre = p.find_element(
                    By.CSS_SELECTOR,
                    "h3.styles_name__qQJiK"
                ).text.strip()

                if not nombre:
                    continue

                # Validar que sea el producto correcto
                nombre_lower = nombre.lower()

                tiene_incluir = any(kw in nombre_lower for kw in kw_incluir)

                # Para portátiles: excluir solo si el nombre EMPIEZA con memoria/ram
                # (no excluir "Portatil HP RAM 8GB")
                if categoria == "portatil":
                    es_falso = nombre_lower.startswith(tuple([
                        "memoria", "modulo", "sodimm", "dimm", "ram "
                    ]))
                else:
                    # Para memorias: excluir si empieza con equipo completo
                    es_falso = nombre_lower.startswith(tuple([
                        "portatil", "portátil", "laptop", "notebook",
                        "computador", "pc ", "all in one", "torre",
                        "desktop", "equipo", "tablet"
                    ]))

                if not tiene_incluir or es_falso:
                    print(f"  ⏭ Saltado: {nombre[:60]}")
                    total_saltados += 1
                    continue

                # URL
                try:
                    link = p.find_element(
                        By.CSS_SELECTOR,
                        "a[data-testid='product-link']"
                    )
                    url_producto = link.get_attribute("href")
                except:
                    url_producto = url

                # Precio
                precio = obtener_precio(p, nombre)
                if precio is None:
                    total_errores += 1
                    continue

                # =====================================================
                # GUARDAR EN MONGODB
                # =====================================================

                data = {
                    "nombre": nombre,
                    "precio": precio,
                    "url": url_producto,
                    "tienda": "exito"
                }

                db.productos.update_one(
                    {"nombre": nombre, "tienda": "exito"},
                    {"$set": data},
                    upsert=True
                )

                print(f"  ✅ [{categoria}] {nombre[:55]} → ${precio:,}")
                total_guardados += 1

            except Exception as e:
                print(f"  ❌ Error: {e}")
                total_errores += 1

    driver.quit()

    print("\n" + "=" * 60)
    print("✅ SCRAPING COMPLETO — ÉXITO")
    print(f"  ✅ Guardados:  {total_guardados}")
    print(f"  ⏭ Saltados:   {total_saltados}")
    print(f"  ❌ Errores:    {total_errores}")
    print("=" * 60)


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()