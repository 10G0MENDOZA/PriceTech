# PriceTech

PriceTech es una plataforma web inteligente de comparación de precios tecnológicos desarrollada con Python. El sistema utiliza técnicas avanzadas de Web Scraping para recopilar productos desde múltiples tiendas online y compararlos automáticamente en una sola interfaz moderna e intuitiva.

El proyecto fue construido utilizando Flask, MongoDB, Scrapy, Selenium y Chart.js, permitiendo realizar búsquedas inteligentes, visualizar precios y detectar automáticamente las mejores ofertas disponibles.

---

# Objetivo del Proyecto

El objetivo principal de PriceTech es ayudar a los usuarios a encontrar el mejor precio disponible para productos tecnológicos entre diferentes tiendas online de manera rápida y automatizada.

La plataforma permite:

- Comparar precios en tiempo real
- Detectar automáticamente la mejor oferta
- Visualizar diferencias de precios
- Automatizar extracción de productos
- Centralizar información de múltiples tiendas

---

# Tecnologías Utilizadas

## Backend

- Python
- Flask
- Jinja2
- PyMongo

## Base de Datos

- MongoDB

## Web Scraping

### Scrapy

Utilizado para:

- Compulago
- ComputerWorking

### Selenium

Utilizado para:

- Éxito
- Jumbo
- Falabella

Selenium fue necesario debido a que algunas páginas cargan contenido dinámicamente mediante JavaScript.

---

# Frontend

- HTML5
- CSS3
- JavaScript
- Chart.js

---

# Automatización

- Schedule
- Scheduler automático en Python

---

# Funcionalidades Principales

## Comparador Inteligente

El usuario puede realizar búsquedas como:

- portatil hp
- victus hp
- memoria ram
- ssd 1tb

El sistema analiza la búsqueda y compara automáticamente los productos entre múltiples tiendas.

---

## Mejor Oferta Automática

PriceTech detecta automáticamente:

- El producto más barato
- Diferencia de precios
- Ahorro estimado
- Mejor tienda

---

## Visualización de Datos

Se implementó una gráfica dinámica utilizando Chart.js para mostrar:

- Comparación de precios
- Diferencias entre tiendas
- Análisis visual rápido

---

## Sistema de Scraping Automatizado

El proyecto integra múltiples scrapers especializados:

### Scrapy

Scrapers rápidos y eficientes para:

- Compulago
- ComputerWorking

### Selenium

Scrapers dinámicos para:

- Éxito
- Jumbo
- Falabella

---

## Actualización Automática

Se desarrolló un scheduler automático encargado de ejecutar periódicamente todos los scrapers para mantener la base de datos actualizada constantemente.

---

# Arquitectura del Proyecto

```txt
PriceTech/
│
├── app.py
├── scheduler.py
├── requirements.txt
│
├── database/
│   └── mongo_connection.py
│
├── templates/
│   ├── index.html
│   └── productos.html
│
├── static/
│   ├── index.css
│   ├── productos.css
│   └── video/
│
├── scrapers/
│   └── scrapy_projects/
│       ├── compulago_scraper/
│       └── computerworking_scraper/
│
├── selenium_scrapers/
│   ├── exito/
│   ├── jumbo/
│   └── falabella/
│
└── README.md
```

---

# Flujo General del Sistema

1. Los scrapers extraen productos desde tiendas online.
2. Los productos son almacenados en MongoDB.
3. Flask consulta la base de datos.
4. El usuario realiza una búsqueda.
5. El sistema filtra resultados relevantes.
6. Se muestran:
   - precios
   - mejor oferta
   - ahorro estimado
   - gráfica comparativa

---

# Base de Datos

MongoDB almacena:

- Nombre del producto
- Precio
- Tienda
- URL del producto
- Fecha de actualización

Ejemplo:

```json
{
  "nombre": "Portatil HP Intel Core i5",
  "precio": 2319900,
  "tienda": "exito",
  "url": "https://..."
}
```

---

# Sistema de Búsqueda

El buscador fue desarrollado utilizando:

- Regex dinámicos
- Filtrado inteligente
- Limpieza de texto
- Normalización de búsquedas

El sistema identifica automáticamente categorías como:

- Portátiles
- Memorias RAM
- SSD

Evitando resultados incorrectos entre categorías distintas.

---

# Instalación del Proyecto

## 1. Clonar repositorio

```bash
git clone https://github.com/10G0MENDOZA/PriceTech.git
```

---

## 2. Entrar al proyecto

```bash
cd PriceTech
```

---

## 3. Crear entorno virtual

```bash
python -m venv venv
```

---

## 4. Activar entorno virtual

### Windows

```bash
venv\Scripts\activate
```

---

## 5. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 6. Ejecutar MongoDB

Asegurarse de tener MongoDB ejecutándose en:

```txt
localhost:27017
```

---

## 7. Ejecutar aplicación

```bash
python app.py
```

---

# Ejecución del Scheduler

Para actualizar automáticamente los productos:

```bash
python scheduler.py
```

---

# Tiendas Integradas

Actualmente el sistema trabaja con:

- Éxito
- Jumbo
- Falabella
- Compulago
- ComputerWorking

---

# Características Destacadas

- Comparación automática de precios
- Web scraping avanzado
- Búsqueda inteligente
- Mejor oferta automática
- Dashboard visual
- Gráficas dinámicas
- Automatización de scrapers
- Interfaz moderna
- Arquitectura escalable

---

# Retos Durante el Desarrollo

Durante el desarrollo se enfrentaron desafíos como:

- Páginas dinámicas con JavaScript
- Diferencias de nombres entre tiendas
- Normalización de productos
- Filtrado inteligente
- Optimización de búsquedas
- Integración entre Scrapy y Selenium
- Manejo de datos duplicados
- Automatización periódica

---

# Mejoras Futuras

- Integración de Inteligencia Artificial
- Historial de precios
- Alertas automáticas
- API REST
- Dashboard administrativo
- Más tiendas integradas
- Sistema de usuarios
- Comparación avanzada de especificaciones

---

# Integrantes

- Diego Mendoza
- [Nombre del compañero]

---

# Video Explicativo

El video explicativo del funcionamiento del proyecto se encuentra en el enlace entregado junto al repositorio.

---

# Estado del Proyecto

Proyecto funcional y operativo.
