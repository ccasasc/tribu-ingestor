import requests
from bs4 import BeautifulSoup
from typing import List
from ..schemas import CarteleraItem

URL = "https://www.ecartelera.com/cines/0,9,23.html"

def fetch() -> List[CarteleraItem]:
    r = requests.get(URL, timeout=30, headers={"User-Agent":"Mozilla/5.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    items: List[CarteleraItem] = []

    # MVP: saca títulos que aparezcan en el listado de películas del cine.
    # El HTML exacto puede variar; esto es heurístico.
    for el in soup.select("a[href*='/pelicula/'], a[href*='/peliculas/']")[:200]:
        titulo = el.get_text(" ", strip=True)
        href = el.get("href","").strip()
        if not titulo or len(titulo) < 2:
            continue

        # Reglas conservadoras (MVP):
        # si parece animación/familiar en el texto cercano -> seguro_<12
        nearby = (el.find_parent().get_text(" ", strip=True) if el.find_parent() else titulo).lower()
        if any(x in nearby for x in ["animación", "animacion", "familiar", "infantil"]):
            nivel = "seguro_<12"
            genero = "Familiar"
        else:
            nivel = "probablemente_familiar"
            genero = ""

        poster = ""
        img = el.find("img")
        if img and img.get("src"):
            poster = img.get("src")

        # Cines: en esta URL es un cine concreto; puedes poner el nombre del cine o "Barcelona"
        items.append(CarteleraItem(
            titulo=titulo,
            nivel_recomendacion=nivel,
            genero=genero,
            imagen_url=poster,
            cines="Barcelona (según eCartelera)"
        ))

    # dedupe por título
    dedup = {}
    for it in items:
        dedup[it.titulo.lower()] = it
    return list(dedup.values())
