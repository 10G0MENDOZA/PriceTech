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

from selenium.common.exceptions import TimeoutException

from webdriver_manager.chrome import ChromeDriverManager

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

from database.mongo_connection import get_db

# =========================
# MONGO
# =========================

db = get_db()
coleccion = db["productos"]

# =========================
# SELENIUM
# =========================

options = Options()

options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 30)

# =========================
# URLS
# =========================

urls = [
    "https://www.falabella.com.co/falabella-co/search?Ntt=MEMORIA+RAM",
    "https://www.falabella.com.co/falabella-co/category/cat1361001/Computadores-Portatiles?isPLP=true&Ntt=portatiles+intel+core+i7"
]

total_guardados = 0

# =========================
# SCRAPING
# =========================

for url in urls:

    print(f"\n🌐 Entrando:\n{url}")

    driver.get(url)

    # =========================
    # ESPERAR PRODUCTOS
    # =========================

    try:

        wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "div[data-pod], div[class*='pod-details']"
                )
            )
        )

        print("✅ Productos cargados")

    except TimeoutException:

        print("❌ No cargaron productos")
        continue

    time.sleep(5)

    # =========================
    # SCROLL
    # =========================

    last_height = driver.execute_script(
        "return document.body.scrollHeight"
    )

    for _ in range(10):

        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

        time.sleep(3)

        new_height = driver.execute_script(
            "return document.body.scrollHeight"
        )

        if new_height == last_height:
            break

        last_height = new_height

    print("✅ Scroll terminado")

    # =========================
    # PRODUCTOS
    # =========================

    productos = driver.find_elements(
    By.CSS_SELECTOR,
    "div[data-pod]"
)

    # fallback
    if not productos:

        productos = driver.find_elements(
        By.CSS_SELECTOR,
        "div[class*='pod-details']"
    )

    print(f"📦 Productos encontrados: {len(productos)}")

    vistos = set()

    for item in productos:

        try:

            # =========================
            # MARCA
            # =========================

            marca = ""

            try:

                marca = item.find_element(
                    By.CSS_SELECTOR,
                    "b.pod-title"
                ).text.strip()

            except:
                pass

            # =========================
            # NOMBRE
            # =========================

            try:

                nombre = item.find_element(
                    By.CSS_SELECTOR,
                    "b.pod-subTitle"
                ).text.strip()

            except:
                continue

            nombre_completo = f"{marca} {nombre}".strip()

            # =========================
            # DUPLICADOS
            # =========================

            if nombre_completo in vistos:
                continue

            vistos.add(nombre_completo)

            # =========================
            # URL
            # =========================

            producto_url = url

            try:

                link = item.find_element(
                    By.XPATH,
                    ".//ancestor::a[1]"
                )

                href = link.get_attribute("href")

                if href:
                    producto_url = href

            except:
                pass

            # =========================
            # PRECIO
            # =========================

            precio = None

            spans = item.find_elements(
                By.TAG_NAME,
                "span"
            )

            precios_encontrados = []

            for span in spans:

                texto = span.text.strip()

                if "$" in texto:

                    numero = re.sub(r"[^\d]", "", texto)

                    if numero:

                        valor = int(numero)

                        # evitar descuentos %
                        if valor > 10000:
                            precios_encontrados.append(valor)

            if precios_encontrados:

                # tomar el menor normalmente es el actual
                precio = min(precios_encontrados)

            # =========================
            # VALIDAR PRECIO
            # =========================

            if not precio:

                print(f"⚠️ Sin precio: {nombre_completo}")
                continue

            # =========================
            # DEBUG
            # =========================

            print("\n====================")
            print(f"✅ {nombre_completo}")
            print(f"💰 ${precio:,}")
            print(f"🔗 {producto_url}")

            # =========================
            # MONGO
            # =========================

            existe = coleccion.find_one({
                "nombre": nombre_completo
            })

            if not existe:

                producto = {
                    "nombre": nombre_completo,
                    "precio": precio,
                    "url": producto_url,
                    "tienda": "falabella"
                }

                coleccion.insert_one(producto)

                total_guardados += 1

                print("💾 Guardado")

            else:

                print("⚠️ Ya existe")

        except Exception as e:

            print(f"❌ Error producto: {e}")

driver.quit()

print("\n🎯 Scraping Falabella completado")
print(f"📦 Total guardados: {total_guardados}")