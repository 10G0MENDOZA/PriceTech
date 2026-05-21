# app.py

from flask import Flask, render_template, request
from database.mongo_connection import get_db
from datetime import datetime
import re

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="../static"
)

# =========================================================
# FILTRO FORMATO COP
# =========================================================

@app.template_filter('cop')
def formato_cop(valor):

    try:
        return "$ {:,.0f}".format(valor).replace(",", ".")
    except:
        return valor


# =========================================================
# TIENDAS
# =========================================================

TIENDAS = [
    "exito",
    "compulago",
    "computerworking",
    "jumbo",
    "falabella"
]


# =========================================================
# LIMPIAR TEXTO
# =========================================================

def limpiar_texto(texto):

    texto = texto.lower()

    texto = re.sub(r"[^\w\s]", " ", texto)

    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


# =========================================================
# HOME
# =========================================================

@app.route("/")
def index():

    return render_template("index.html")


# =========================================================
# BUSCADOR
# =========================================================

@app.route("/buscar", methods=["POST"])
def buscar():

    db = get_db()

    query = request.form.get(
        "query",
        ""
    ).strip()

    orden = request.form.get(
        "orden",
        "menor"
    )

    query_limpia = limpiar_texto(query)

    palabras = query_limpia.split()

    print("\n" + "=" * 60)
    print("🚀 NUEVA BUSQUEDA")
    print("=" * 60)

    print(f"🔎 QUERY: {query}")

    # =====================================================
    # VALIDAR
    # =====================================================

    if not palabras:

        return render_template(
            "productos.html",
            resultados=[],
            query=query
        )

    # =====================================================
    # FILTROS
    # =====================================================

    filtros = []

    for palabra in palabras:

        filtros.append({
            "nombre": {
                "$regex": palabra,
                "$options": "i"
            }
        })

    texto = " ".join(palabras)

    # =====================================================
    # DETECTAR PORTATILES
    # =====================================================

    if any(p in texto for p in [
        "portatil",
        "laptop",
        "notebook",
        "victus",
        "vivobook"
    ]):

        filtros.append({
            "nombre": {
                "$not": re.compile(
                    r"memoria|ram|ddr3|ddr4|ddr5",
                    re.IGNORECASE
                )
            }
        })

        print("📦 FILTRO PORTATIL ACTIVADO")

    # =====================================================
    # DETECTAR MEMORIAS RAM
    # =====================================================

    elif any(p in texto for p in [
        "ram",
        "memoria",
        "ddr3",
        "ddr4",
        "ddr5"
    ]):

        filtros.append({
            "nombre": {
                "$not": re.compile(
                    r"portatil|laptop|notebook",
                    re.IGNORECASE
                )
            }
        })

        print("📦 FILTRO RAM ACTIVADO")

    # =====================================================
    # ORDEN
    # =====================================================

    orden_precio = 1

    if orden == "mayor":

        orden_precio = -1

    print(f"💰 ORDEN: {orden}")

    # =====================================================
    # PIPELINE
    # =====================================================

    pipeline = [

        {
            "$match": {
                "$and": filtros
            }
        },

        {
            "$sort": {
                "precio": orden_precio
            }
        },

        {
            "$group": {
                "_id": "$tienda",
                "producto": {
                    "$first": "$$ROOT"
                }
            }
        }

    ]

    # =====================================================
    # EJECUTAR
    # =====================================================

    data = list(
        db.productos.aggregate(pipeline)
    )

    print(f"\n📦 RESULTADOS: {len(data)}")

    for d in data:

        print("-" * 50)

        print(d["producto"]["nombre"])

        print(d["producto"]["precio"])

    # =====================================================
    # ORGANIZAR RESULTADOS
    # =====================================================

    resultados = []

    productos_validos = []

    for tienda in TIENDAS:

        encontrado = next(
            (
                d for d in data
                if d["_id"] == tienda
            ),
            None
        )

        if encontrado:

            producto = encontrado["producto"]

            productos_validos.append(producto)

            resultados.append({

                "tienda": tienda,

                "producto": producto,

                "disponible": True,

                "es_mejor": False

            })

        else:

            resultados.append({

                "tienda": tienda,

                "producto": None,

                "disponible": False,

                "es_mejor": False

            })

    # =====================================================
    # MEJOR PRODUCTO
    # =====================================================

    mejor_producto = None

    mejor_precio = 0

    ahorro = 0

    if productos_validos:

        mejor_producto = min(
            productos_validos,
            key=lambda x: x["precio"]
        )

        mejor_precio = mejor_producto["precio"]

        mayor_precio = max(
            productos_validos,
            key=lambda x: x["precio"]
        )["precio"]

        ahorro = mayor_precio - mejor_precio

        for r in resultados:

            if (
                r["disponible"] and
                r["producto"]["precio"] == mejor_precio
            ):

                r["es_mejor"] = True

    # =====================================================
    # DATOS GRAFICA
    # =====================================================

    labels = []

    precios = []

    for r in resultados:

        if r["disponible"]:

            labels.append(r["tienda"])

            precios.append(r["producto"]["precio"])

    # =====================================================
    # RETORNAR
    # =====================================================

    return render_template(

        "productos.html",

        resultados=resultados,

        query=query,

        total_resultados=len(productos_validos),

        mejor_producto=mejor_producto,

        mejor_precio=mejor_precio,

        ahorro=ahorro,

        ultima_actualizacion=datetime.now().strftime(
            "%d/%m/%Y %I:%M %p"
        ),

        labels=labels,

        precios=precios
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )