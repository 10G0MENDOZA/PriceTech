import schedule
import time
import os

# =========================================================
# BASE SCRAPY
# =========================================================

BASE = "C:\\Users\\USUARIO\\Desktop\\PriceTech\\scrapers\\scrapy_projects"

COMPULAGO = BASE + "\\compulago_scraper"
COMPUTERWORKING = BASE + "\\computerworking_scraper"

# =========================================================
# SELENIUM
# =========================================================

EXITO = "C:\\Users\\USUARIO\\Desktop\\PriceTech\\selenium_scrapers\\exito"

JUMBO = "C:\\Users\\USUARIO\\Desktop\\PriceTech\\selenium_scrapers\\jumbo"

# =========================================================
# EJECUTAR TODOS
# =========================================================

def run_all():

    print("\n================================================")
    print("🚀 EJECUTANDO TODOS LOS SCRAPERS")
    print("================================================\n")

    # =====================================================
    # COMPULAGO
    # =====================================================

    print("🟢 Compulago (Scrapy)...")

    os.system(
        f'cd "{COMPULAGO}" && scrapy crawl compulago'
    )

    print("✅ Compulago finalizado\n")

    # =====================================================
    # COMPUTERWORKING
    # =====================================================

    print("🟢 ComputerWorking (Scrapy)...")

    os.system(
        f'cd "{COMPUTERWORKING}" && scrapy crawl computerworking'
    )

    print("✅ ComputerWorking finalizado\n")

    # =====================================================
    # EXITO
    # =====================================================

    print("🟢 Éxito (Selenium)...")

    os.system(
        f'cd "{EXITO}" && python exito_selenium.py'
    )

    print("✅ Éxito finalizado\n")

    # =====================================================
    # JUMBO
    # =====================================================

    print("🟢 Jumbo (Selenium)...")

    os.system(
        f'cd "{JUMBO}" && python jumbo_selenium.py'
    )

    print("✅ Jumbo finalizado\n")

    # =====================================================
    # FIN
    # =====================================================

    print("================================================")
    print("🎯 TODOS LOS SCRAPERS TERMINARON")
    print("================================================\n")


# =========================================================
# SCHEDULE
# =========================================================

# cada 30 minutos
schedule.every(30).minutes.do(run_all)

print("⏰ Scheduler iniciado...")

# ejecutar inmediatamente
run_all()

# loop infinito
while True:

    schedule.run_pending()

    time.sleep(1)