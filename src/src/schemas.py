from dataclasses import dataclass, asdict
from typing import Optional, Literal, Dict, Any

Categoria = Literal["parque","taller","evento","museo","teatro","deporte","aire_libre","cultural","otro"]
Zona = Literal["eixample","gracia","sarria","gotico","raval","barceloneta","sants","horta","nou_barris","sant_marti","les_corts","sant_andreu","otra"]
Precio = Literal["gratuito","economico","moderado","premium"]

Dia = Literal["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]

@dataclass
class Actividad:
    nombre: str
    descripcion: str = ""
    categoria: Categoria = "otro"
    zona: Zona = "otra"
    edad_minima: Optional[float] = None
    edad_maxima: Optional[float] = None
    precio: Precio = "gratuito"
    direccion: str = ""
    nombre_lugar: str = ""
    horario: str = ""
    fecha_inicio: Optional[str] = None   # YYYY-MM-DD
    fecha_fin: Optional[str] = None      # YYYY-MM-DD
    fecha_formateada: str = ""
    fecha_fin_formateada: str = ""
    dia_semana: Optional[Dia] = None
    es_fin_de_semana: int = 0
    telefono: str = ""
    web: str = ""
    imagen_url: str = ""
    destacado: bool = False
    fuente: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class CarteleraItem:
    titulo: str
    nivel_recomendacion: Literal["seguro_<12","probablemente_familiar"]
    clasificacion: str = "No especificada"
    genero: str = ""
    duracion: str = ""
    sinopsis: str = ""
    director: str = ""
    ano: str = ""
    valoracion: str = ""
    imagen_url: str = ""
    cines: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
