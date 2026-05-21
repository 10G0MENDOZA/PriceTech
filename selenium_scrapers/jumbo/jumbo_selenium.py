import time
import re
import sys
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

# =========================================
# IMPORTAR MONGO
# =========================================

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

from database.mongo_connection import get_db

# =========================================
# MONGO
# =========================================

db = get_db()
coleccion = db["productos"]

# =========================================
# SELENIUM
# =========================================

options = Options()

options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

# evitar detección
options.add_experimental_option(
    "excludeSwitches",
    ["enable-automation"]
)

options.add_experimental_option(
    "useAutomationExtension",
    False
)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.execute_script("""
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
})
""")

wait = WebDriverWait(driver, 20)

# =========================================
# URLS
# =========================================

urls = [
    "https://www.jumbocolombia.com/memoria%20ram?_q=memoria%20ram&map=ft",
    "https://www.jumbocolombia.com/tecnologia/informatica/computadores-portatiles"
]

total_guardados = 0

# =========================================
# FUNCION EXTRAER PRECIO
# =========================================

def extraer_precio(texto):

    try:

        numero = re.sub(r"[^\d]", "", texto)

        if numero:
            return int(numero)

    except:
        pass

    return None

# =========================================
# SCRAPING
# =========================================

for url in urls:

    print("\n" + "=" * 60)
    print(f"🌐 Entrando:\n{url}")
    print("=" * 60)

    driver.get(url)

    time.sleep(8)

    # =========================================
    # ESPERAR PRODUCTOS
    # =========================================

    try:

        wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "section.vtex-product-summary-2-x-container"
                )
            )
        )

        print("✅ Productos cargados")

    except Exception as e:

        print("❌ Error cargando productos")
        print(e)

        continue

    # =========================================
    # SCROLL
    # =========================================

    last_height = driver.execute_script(
        "return document.body.scrollHeight"
    )

    for i in range(10):

        print(f"🔽 Scroll #{i+1}")

        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

        time.sleep(3)

        new_height = driver.execute_script(
            "return document.body.scrollHeight"
        )

        if new_height == last_height:

            print("✅ Fin scroll")
            break

        last_height = new_height

    # =========================================
    # PRODUCTOS
    # =========================================

    productos = driver.find_elements(
        By.CSS_SELECTOR,
        "section.vtex-product-summary-2-x-container"
    )

    print(f"\n📦 Productos encontrados: {len(productos)}")

    vistos = set()

    # =========================================
    # RECORRER PRODUCTOS
    # =========================================

    for index, item in enumerate(productos, start=1):

        try:

            print("\n" + "-" * 60)
            print(f"🔎 PRODUCTO #{index}")
            print("-" * 60)

            # =========================================
            # NOMBRE
            # =========================================

            nombre = ""

            try:

                nombre = item.find_element(
                    By.CSS_SELECTOR,
                    "span.vtex-product-summary-2-x-productBrand"
                ).text.strip()

            except Exception as e:

                print("❌ Error nombre")
                print(e)

            if not nombre:

                print("⚠️ Sin nombre")
                continue

            print(f"📝 Nombre: {nombre}")

            # =========================================
            # MARCA
            # =========================================

            marca = ""

            try:

                marca = item.find_element(
                    By.CSS_SELECTOR,
                    "span.vtex-product-summary-2-x-productBrandName"
                ).text.strip()

            except:
                pass

            print(f"🏷️ Marca: {marca}")

            nombre_completo = f"{marca} {nombre}".strip()

            # =========================================
            # DUPLICADOS
            # =========================================

            if nombre_completo in vistos:

                print("⚠️ Duplicado")
                continue

            vistos.add(nombre_completo)

            # =========================================
            # PRECIO
            # =========================================

            precio = None

            try:

                precios = item.find_elements(
                    By.CSS_SELECTOR,
                    "div.tiendasjumboqaio-jumbo-minicart-2-x-price"
                )

                print(f"💲 Precios encontrados: {len(precios)}")

                for p in precios:

                    texto_precio = p.text.strip()

                    print(f"💰 Texto detectado: {texto_precio}")

                    valor = extraer_precio(texto_precio)

                    if valor and valor > 10000:

                        precio = valor
                        break

            except Exception as e:

                print("❌ Error precio")
                print(e)

            # =========================================
            # URL PRODUCTO
            # =========================================

            producto_url = url

            try:

                link = item.find_element(
                    By.XPATH,
                    ".//ancestor::a[1]"
                )

                href = link.get_attribute("href")

                if href:
                    producto_url = href

            except Exception as e:

                print("⚠️ Error URL")
                print(e)

            # =========================================
            # VALIDAR PRECIO
            # =========================================

            if not precio:

                print("❌ NO SE ENCONTRO PRECIO")

                html_debug = item.get_attribute("innerHTML")

                print("\n📄 HTML DEBUG:")
                print(html_debug[:2500])

                continue

            # =========================================
            # DEBUG FINAL
            # =========================================

            print("\n✅ PRODUCTO EXTRAIDO")
            print(f"📝 Nombre: {nombre_completo}")
            print(f"💰 Precio: ${precio}")
            print(f"🔗 URL: {producto_url}")

            # =========================================
            # GUARDAR EN MONGO
            # =========================================

            existe = coleccion.find_one({
                "nombre": nombre_completo
            })

            if not existe:

                producto = {
                    "nombre": nombre_completo,
                    "precio": precio,
                    "url": producto_url,
                    "tienda": "jumbo"
                }

                coleccion.insert_one(producto)

                total_guardados += 1

                print("💾 Guardado en Mongo")

            else:

                print("⚠️ Ya existe en Mongo")

        except Exception as e:

            print(f"❌ Error producto #{index}")
            print(e)

# =========================================
# FINAL
# =========================================

driver.quit()

print("\n" + "=" * 60)
print("🎯 SCRAPING JUMBO FINALIZADO")
print(f"📦 TOTAL GUARDADOS: {total_guardados}")
print("=" * 60)