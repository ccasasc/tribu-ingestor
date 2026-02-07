import requests
from bs4 import BeautifulSoup
from typing import List
from ..schemas import Actividad
from ..normalize import safe_parse_date, format_ddmmyyyy, day_of_week_es, is_weekend, normalize_precio, normalize_categoria_by_source, normalize_zona_from_text, extract_age_range

URL = "https://www.mammaproof.org/barcelona/agenda-amarilla/"

def fetch() -> List[Actividad]:
    r = requests.get(URL, timeout=30, headers={"User-Agent":"Mozilla/5.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    items: List[Actividad] = []

    # Nota: Mammaproof cambia su HTML a veces; esto es un MVP.
    # Buscamos tarjetas con enlaces dentro del listado.
    cards = soup.select("article, .post, .type-post")
    for c in cards[:200]:
        a = c.select_one("a[href]")
        title_el = c.select_one("h2, h3, .entry-title")
        if not a or not title_el:
            continue

        nombre = title_el.get_text(" ", strip=True)
        web = a.get("href","").strip()
        desc = ""
        p = c.select_one("p")
        if p:
            desc = p.get_text(" ", strip=True)

        # Intento muy básico de fecha si aparece en el card
        date_text = ""
        time_el = c.select_one("time")
        if time_el:
            date_text = time_el.get("datetime","") or time_el.get_text(" ", strip=True)
        fecha_inicio = safe_parse_date(date_text)

        edad_min, edad_max = extract_age_range(nombre + " " + desc)

        act = Actividad(
            nombre=nombre,
            descripcion=desc,
            categoria=normalize_categoria_by_source("Mammaproof"),
            zona=normalize_zona_from_text(nombre + " " + desc),
            edad_minima=edad_min,
            edad_maxima=edad_max,
            precio=normalize_precio(desc),
            web=web,
            fuente="Mammaproof",
        )
        act.fecha_inicio = fecha_inicio
        act.fecha_fin = fecha_inicio
        act.fecha_formateada = format_ddmmyyyy(act.fecha_inicio)
        act.fecha_fin_formateada = format_ddmmyyyy(act.fecha_fin)
        act.dia_semana = day_of_week_es(act.fecha_inicio)
        act.es_fin_de_semana = is_weekend(act.fecha_inicio)

        items.append(act)

    return items
