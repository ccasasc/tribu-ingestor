import requests
from bs4 import BeautifulSoup
from typing import List
from ..schemas import Actividad
from ..normalize import safe_parse_date, format_ddmmyyyy, day_of_week_es, is_weekend, normalize_precio, extract_age_range

URL = "https://cosmocaixa.org/es/actividades"

def fetch() -> List[Actividad]:
    r = requests.get(URL, timeout=30, headers={"User-Agent":"Mozilla/5.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    items: List[Actividad] = []

    # MVP: capturar cards típicas con título + link
    cards = soup.select("a[href*='actividades'], a[href*='actividad'], .card a[href]")
    seen = set()

    for a in cards[:400]:
        href = a.get("href","").strip()
        title = a.get_text(" ", strip=True)
        if not href or len(title) < 6:
            continue
        if href.startswith("/"):
            href = "https://cosmocaixa.org" + href
        key = (title.lower(), href)
        if key in seen:
            continue
        seen.add(key)

        # Intento extraer info del card contenedor
        container = a.find_parent()
        text = container.get_text(" ", strip=True) if container else title

        fecha_inicio = safe_parse_date(text)  # heurístico
        edad_min, edad_max = extract_age_range(text)

        act = Actividad(
            nombre=title,
            descripcion=text[:400],
            categoria="museo",
            zona="otra",
            edad_minima=edad_min,
            edad_maxima=edad_max,
            precio=normalize_precio(text),
            nombre_lugar="CosmoCaixa",
            web=href,
            fuente="CosmoCaixa",
        )

        act.fecha_inicio = fecha_inicio
        act.fecha_fin = fecha_inicio
        act.fecha_formateada = format_ddmmyyyy(act.fecha_inicio)
        act.fecha_fin_formateada = format_ddmmyyyy(act.fecha_fin)
        act.dia_semana = day_of_week_es(act.fecha_inicio)
        act.es_fin_de_semana = is_weekend(act.fecha_inicio)

        items.append(act)

    return items
