# Calendario Medieval 2026–2030

Sitio estático para GitHub Pages. El tablón de noticias (5 al día: 4 en inglés y 1 en español) se renueva solo cada día gracias a un bot de GitHub Actions.

## Archivos del proyecto

| Archivo | Para qué sirve | Dónde va en el repo |
|---|---|---|
| `index.html` | La página | raíz |
| `news.json` | Lo escribe el bot cada día | raíz |
| `README.md` | Estas instrucciones | raíz |
| `noticias.py` | Busca, limpia y elige las 5 noticias | `scripts/noticias.py` |
| `noticias.yml` | Lo ejecuta GitHub a diario | `.github/workflows/noticias.yml` |

Estructura final que debe quedar en el repo:

```
index.html
news.json
README.md
scripts/noticias.py
.github/workflows/noticias.yml
```

---

## Paso 1: Crear el repositorio

1. Entra en github.com e inicia sesión.
2. Pulsa **+ → New repository**.
3. Ponle nombre (por ejemplo `calendario-medieval`), déjalo en **Public** y pulsa **Create repository**.

## Paso 2: Subir los archivos

> Importante: GitHub NO descomprime zips y NO deja subir carpetas que empiezan por punto (`.github`). Por eso los archivos se suben en dos tandas.

**2a. Archivos de la raíz (subida normal)**

1. En el repo, pulsa **Add file → Upload files**.
2. Sube `index.html`, `news.json` y `README.md`.
3. Pulsa **Commit changes**.

**2b. El script (se crea a mano)**

1. Pulsa **Add file → Create new file**.
2. En el nombre escribe exactamente: `scripts/noticias.py`
   (al escribir la `/` se crea la carpeta sola).
3. Abre `noticias.py`, copia todo su contenido y pégalo en el editor.
4. Pulsa **Commit changes**.

**2c. El workflow (se crea a mano)**

1. Pulsa **Add file → Create new file**.
2. En el nombre escribe exactamente: `.github/workflows/noticias.yml`
3. Abre `noticias.yml`, copia todo su contenido y pégalo en el editor.
4. Pulsa **Commit changes**.

**Comprobación:** en la pantalla principal del repo deben verse las carpetas `scripts` y `.github`. Entra en `.github/workflows/` y debe estar `noticias.yml`.

> Si usas un ordenador con Git, puedes subir todo de una vez con `git push` desde la carpeta del zip completo; ahí sí se respeta `.github`.

## Paso 3: Activar GitHub Pages

1. Ve a **Settings → Pages**.
2. En **Source** elige **Deploy from a branch**.
3. Selecciona la rama `main` y la carpeta `/ (root)`. Pulsa **Save**.
4. En uno o dos minutos la página estará en:
   `https://TU-USUARIO.github.io/NOMBRE-DEL-REPO/`

## Paso 4: Dar permisos al bot

1. Ve a **Settings → Actions → General**.
2. Baja hasta **Workflow permissions**.
3. Marca **Read and write permissions** y pulsa **Save**.

Sin esto, el bot no puede guardar el `news.json` y falla al final.

## Paso 5: Probar el bot a mano

1. Ve a la pestaña **Actions**.
2. Si aparece un botón verde "I understand my workflows, go ahead and enable them", púlsalo.
3. En la lista de la izquierda pulsa **Noticias diarias**.
4. Pulsa **Run workflow → Run workflow**.
5. Espera un minuto y entra en la ejecución. En el log verás qué fuentes respondieron (`OK` / `ERR`).
6. Si terminó en verde, `news.json` se habrá actualizado y la página mostrará las noticias nuevas.

A partir de ahí el bot corre solo todos los días a las 11:00 UTC.

## Paso 6 (opcional): Traducir al español las noticias en inglés

1. Ve a **Settings → Secrets and variables → Actions → New repository secret**.
2. Nombre: `ANTHROPIC_API_KEY`
3. Valor: tu clave de API de Anthropic.
4. Pulsa **Add secret**.

Si no lo configuras, todo funciona igual, pero las notas en inglés se quedan en inglés.

---

## Qué limpia el script

- Descarta notas fuera de tema (podcasts, reseñas, recetas, eventos…).
- Quita duplicados: mismo enlace, mismo título o la misma historia en dos medios.
- No repite las noticias del día anterior mientras haya otras.
- Máximo 1 por medio (2 solo si faltan).

## Problemas frecuentes

| Problema | Solución |
|---|---|
| No aparece "Noticias diarias" en Actions | Falta `.github/workflows/noticias.yml`. Repite el paso 2c. |
| El workflow falla en "Generar news.json" | Comprueba que existe `scripts/noticias.py` (paso 2b). |
| Falla en "Guardar cambios" (error 403) | Falta el paso 4: Read and write permissions. |
| La página no carga | Revisa el paso 3 y espera un par de minutos. |
| Las noticias no cambian | Mira el log en Actions; puede que algunas fuentes den `ERR`. |
