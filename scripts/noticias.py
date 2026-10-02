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
        try:
            d = datetime.fromisoformat(s.strip().replace("Z", "+00:00"))
        except Exception:
            return None
    return d if d.tzinfo else d.replace(tzinfo=UTC)

def local(tag):
    return tag.rsplit("}", 1)[-1]

def parse(xml, fuente, idioma):
    out = []
    for node in ET.fromstring(xml).iter():
        if local(node.tag) not in ("item", "entry"):
            continue
        d = {}
        for c in node:
            k = local(c.tag)
            if k == "link":
                if c.get("href") and c.get("rel", "alternate") == "alternate":
                    d.setdefault("link", c.get("href"))
                elif c.text and c.text.strip():
                    d.setdefault("link", c.text.strip())
            elif k in ("pubDate", "published", "updated", "date"):
                d.setdefault("date", c.text)
            elif k in ("title", "description", "summary", "encoded", "content"):
                d.setdefault(k, c.text or "")
        link, title = d.get("link", ""), strip(d.get("title"))
        if not title or not link.startswith("http"):
            continue
        resumen = strip(d.get("description") or d.get("summary") or d.get("encoded") or d.get("content"))
        out.append({"titulo": title, "resumen": cut(resumen), "fuente": fuente, "url": link,
                    "idioma": idioma, "dt": parse_date(d.get("date"))})
    return out

# ---------- limpieza ----------
def norm_url(u):
    u = re.sub(r"[?#].*$", "", u.strip().lower())
    return re.sub(r"^https?://(www\.)?", "", u).rstrip("/")

def words(t):
    return {w for w in re.findall(r"[a-záéíóúñü0-9]{4,}", t.lower()) if w not in STOP}

def same_story(a, b):
    if norm_url(a["url"]) == norm_url(b["url"]):
        return True
    wa, wb = words(a["titulo"]), words(b["titulo"])
    if not wa or not wb:
        return a["titulo"].strip().lower() == b["titulo"].strip().lower()
    return len(wa & wb) / min(len(wa), len(wb)) >= 0.7

def relevante(i, kw):
    if NOISE.search(i["titulo"]):
        return False
    en_titulo = bool(kw.search(i["titulo"]))
    en_resumen = {m.group(0).lower() for m in kw.finditer(i["resumen"])}
    return en_titulo or len(en_resumen) >= 2

def elegir(pool, kw, n, prev_urls, ya, now):
    """Elige hasta n notas: recientes primero, medios distintos, sin duplicados ni repetidas de ayer."""
    base = [i for i in pool if relevante(i, kw)]
    vistos, unicos = [], []
    for i in sorted(base, key=lambda i: i["dt"] or datetime.min.replace(tzinfo=UTC), reverse=True):
        if not any(same_story(i, j) for j in vistos):
            vistos.append(i); unicos.append(i)
    def edad(i):
        return (now - i["dt"]) if i["dt"] else timedelta(days=999)
    orden = ([i for i in unicos if edad(i) <= timedelta(days=4)]
             + [i for i in unicos if timedelta(days=4) < edad(i) <= timedelta(days=10)]
             + [i for i in unicos if edad(i) > timedelta(days=10)])
    pick = []
    for tope, permitir_ayer in ((1, False), (2, False), (99, False), (99, True)):
        for i in orden:
            if len(pick) >= n:
                return pick
            if i in pick or any(same_story(i, j) for j in pick + ya):
                continue
            if not permitir_ayer and norm_url(i["url"]) in prev_urls:
                continue
            if sum(1 for j in pick if j["fuente"] == i["fuente"]) >= tope:
                continue
            pick.append(i)
    return pick

# ---------- traducción (opcional) ----------
def traducir(items):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return
    for it in items:
        if it["idioma"] != "en":
            continue
        try:
            prompt = ("Traduce al español neutral este titular y resumen. Responde SOLO con JSON "
                      '{"titulo":"...","resumen":"..."} sin explicaciones.\n\n'
                      + json.dumps({"titulo": it["titulo"], "resumen": it["resumen"]}, ensure_ascii=False))
            body = json.dumps({"model": "claude-haiku-4-5-20251001", "max_tokens": 500,
                               "messages": [{"role": "user", "content": prompt}]}).encode()
            req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, headers={
                "content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01"})
            txt = json.load(urllib.request.urlopen(req, timeout=60))["content"][0]["text"].strip()
            t = json.loads(re.sub(r"^```(?:json)?|```$", "", txt).strip())
            it["titulo"], it["resumen"], it["traducido"] = t["titulo"], t["resumen"], True
        except Exception as e:
            print("Traducción falló:", e)

def cargar(feeds, idioma):
    pool = []
    for fuente, urls in feeds.items():
        for u in urls:
            try:
                items = parse(get(u), fuente, idioma)
                print(f"OK  {fuente}: {len(items)} entradas ({u})")
                pool += items
                break
            except Exception as e:
                print(f"ERR {fuente}: {u} -> {e}")
    return pool

def anteriores():
    try:
        with open(OUT, encoding="utf-8") as f:
            return {norm_url(x["url"]) for x in json.load(f).get("items", [])}
    except Exception:
        return set()

def main():
    now = datetime.now(UTC)
    prev = anteriores()
    pool_en = cargar(FEEDS_EN, "en")
    pool_es = cargar(FEEDS_ES, "es")
    es = elegir(pool_es, KW_ES, N_ES, prev, [], now)
    # si no hay nota en español, se completa con más notas en inglés para llegar a 5
    en = elegir(pool_en, KW_EN, N_EN + N_ES - len(es), prev, es, now)
    pick = en + es
    if not pick:
        print("Sin noticias nuevas: se conserva news.json anterior.")
        if not os.path.exists(OUT):
            json.dump({"actualizado": None, "items": []}, open(OUT, "w", encoding="utf-8"))
        return
    traducir(pick)
    for i in pick:
        dt = i.pop("dt")
        i["fecha"] = dt.date().isoformat() if dt else ""
    json.dump({"actualizado": now.isoformat(timespec="seconds"), "items": pick},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Listo: {len(pick)} noticias ({sum(i['idioma']=='es' for i in pick)} en español).")

if __name__ == "__main__":
    main()
