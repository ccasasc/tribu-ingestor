import json
from typing import List
from .connectors import mammaproof, cosmocaixa, ecartelera
from .schemas import Actividad, CarteleraItem

def dedupe_actividades(items: List[Actividad]) -> List[Actividad]:
    # MVP: dedupe simple por (nombre, fecha_inicio, nombre_lugar)
    seen = set()
    out = []
    for it in items:
        key = (it.nombre.strip().lower(), it.fecha_inicio or "", (it.nombre_lugar or "").strip().lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out

def run():
    actividades: List[Actividad] = []
    cartelera: List[CarteleraItem] = []

    # Conectores MVP
    actividades += mammaproof.fetch()
    actividades += cosmocaixa.fetch()
    cartelera += ecartelera.fetch()

    actividades = dedupe_actividades(actividades)

    with open("docs/actividades.json", "w", encoding="utf-8") as f:
        json.dump([a.to_dict() for a in actividades], f, ensure_ascii=False, indent=2)

    with open("docs/cartelera.json", "w", encoding="utf-8") as f:
        json.dump([c.to_dict() for c in cartelera], f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    run()
