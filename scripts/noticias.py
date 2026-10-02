#!/usr/bin/env python3
"""Genera news.json con 5 noticias geopolíticas al día (4 en inglés + 1 en español)
de medios de la tradición liberal clásica / escuela austriaca.
Corre a diario en GitHub Actions (ver .github/workflows/noticias.yml).

Limpieza que hace:
  - descarta notas fuera de tema (recetas, podcasts, reseñas, etc.)
  - quita duplicados (mismo enlace, mismo título o la misma historia en dos medios)
  - no repite las noticias de ayer mientras haya otras disponibles
  - máximo 1 por medio (2 solo si faltan)
"""
import json, os, re, html, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

N_EN, N_ES = 4, 1                      # 4 en inglés + 1 en español = 5
UTC = timezone.utc
UA = {"User-Agent": "Mozilla/5.0 (compatible; CalendarioMedievalBot/1.0)"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "news.json")

# Cada medio tiene enlaces alternos: se usa el primero que funcione.
FEEDS_EN = {
    "Mises Institute": ["https://mises.org/feed/blog.rss", "https://mises.org/rss.xml", "https://mises.org/feed"],
    "Antiwar.com": ["https://original.antiwar.com/feed/", "https://www.antiwar.com/blog/feed/"],
    "Libertarian Institute": ["https://libertarianinstitute.org/feed/"],
    "Cato Institute": ["https://www.cato.org/rss/recent-opeds", "https://www.cato.org/rss/commentary"],
    "AIER": ["https://www.aier.org/feed/"],
    "FEE": ["https://fee.org/feed/"],
    "Reason": ["https://reason.com/feed/"],
    "Ron Paul Institute": ["https://ronpaulinstitute.org/feed/"],
}
FEEDS_ES = {
    "Instituto Juan de Mariana": ["https://juandemariana.org/feed", "https://www.juandemariana.org/feed"],
    "El Cato": ["https://www.elcato.org/rss.xml", "https://www.elcato.org/feed"],
    "Libertad y Progreso": ["https://libertadyprogresonline.org/feed/"],
    "Libertad Digital": ["https://feeds2.feedburner.com/libertaddigital/internacional"],
    "Instituto Mises": ["https://mises.org.es/feed/"],
}

KW_EN = re.compile(r"\b(war|wars|ukraine|russia\w*|china|chinese|taiwan|iran\w*|israel\w*|gaza|nato|sanctions?|"
                   r"tariffs?|empire|foreign policy|military|middle east|venezuela\w*|pentagon|geopolit\w*|brics|"
                   r"treaty|sovereignty|syria\w*|north korea\w*|cuba\w*|argentin\w*|milei|european union|trade war|"
                   r"ceasefire|invasion|nuclear|diplomacy|embargo|ethiopia|sudan|yemen|lebanon|hamas|hezbollah)\b", re.I)
KW_ES = re.compile(r"\b(guerra|guerras|ucrania|rusia|rusos?|china|chinos?|taiw[aá]n|ir[aá]n|iran[ií]es?|israel\w*|gaza|"
                   r"otan|sanciones|aranceles?|imperio|pol[ií]tica exterior|militar\w*|medio oriente|venezuel\w*|"
                   r"pent[aá]gono|geopol[ií]tic\w*|brics|tratado|soberan[ií]a|siria|corea del norte|cuba\w*|"
                   r"argentin\w*|milei|uni[oó]n europea|alto el fuego|invasi[oó]n|nuclear\w*|diplomacia|embargo|"
                   r"estados unidos|ee\. ?uu\.?|trump)\b", re.I)
# Notas que no sirven aunque mencionen un tema geopolítico.
NOISE = re.compile(r"\b(podcast|episode|episodio|webinar|livestream|newsletter|digest|giveaway|donat\w*|"
                   r"book review|film review|recipe|receta|sandwich|BLT|quiz|job opening|hiring|"
                   r"event|register now|join us|sale|discount)\b", re.I)
STOP = set("the and for with from that this into over about after before their have been will would "
           "could should what when where which while than then them they your more most just like "
           "los las del por con para una uno como pero sobre entre sus este esta esto desde hasta".split())


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
        return r.read()

def strip(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t or ""))).strip()

def cut(t, n=220):
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0].rstrip(".,;:") + "…"

def parse_date(s):
    if not s:
        return None
    try:
        d = parsedate_to_datetime(s)
    except Exception:
