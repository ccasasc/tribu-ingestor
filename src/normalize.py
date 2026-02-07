import re
from datetime import datetime
from dateutil import parser

DAYS_ES = ["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]

def safe_parse_date(text: str) -> str | None:
    if not text:
        return None
    try:
        dt = parser.parse(text, dayfirst=True, fuzzy=True)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return None

def format_ddmmyyyy(ymd: str | None) -> str:
    if not ymd:
        return ""
    try:
        dt = datetime.strptime(ymd, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except Exception:
        return ""

def day_of_week_es(ymd: str | None) -> str | None:
    if not ymd:
        return None
    try:
        dt = datetime.strptime(ymd, "%Y-%m-%d")
        return DAYS_ES[dt.weekday()]
    except Exception:
        return None

def is_weekend(ymd: str | None) -> int:
    if not ymd:
        return 0
    try:
        dt = datetime.strptime(ymd, "%Y-%m-%d")
        return 1 if dt.weekday() >= 5 else 0
    except Exception:
        return 0

def normalize_precio(text: str) -> str:
    t = (text or "").lower()
    if any(x in t for x in ["gratis","gratuït","gratuito","0€","0 €","entrada libre"]):
        return "gratuito"
    # heurística simple de euros
    nums = re.findall(r"(\d+(?:[.,]\d+)?)\s*€", t)
    if nums:
        try:
            v = float(nums[0].replace(",", "."))
            if v < 10: return "economico"
            if v <= 25: return "moderado"
            return "premium"
        except Exception:
            pass
    return "gratuito"

def normalize_categoria_by_source(source: str) -> str:
    s = (source or "").lower()
    if "muse" in s or "cosmocaixa" in s: return "museo"
    if "teatre" in s or "auditori" in s or "palau" in s: return "teatro"
    if "bibli" in s: return "cultural"
    if "cine" in s or "cartelera" in s: return "cultural"
    return "otro"

def normalize_zona_from_text(_text: str) -> str:
    # MVP: muy conservador, dejamos "otra" salvo que detectemos algo claro.
    return "otra"

def extract_age_range(text: str):
    """
    Devuelve (edad_min, edad_max) en años (float) si se detecta.
    MVP: patrones básicos.
    """
    t = (text or "").lower()
    # +3, +7
    m = re.search(r"\+\s*(\d{1,2})", t)
    if m:
        return float(m.group(1)), None
    # 0-6, 3 a 8, de 3 a 8
    m = re.search(r"(\d{1,2})\s*(?:-|a)\s*(\d{1,2})", t)
    if m:
        return float(m.group(1)), float(m.group(2))
    return None, None
