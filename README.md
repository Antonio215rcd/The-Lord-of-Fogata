# Calendario Medieval

Sitio estático para GitHub Pages. Incluye un calendario por años y un tablón con 5 noticias al día (4 en inglés y 1 en español) que se renueva solo gracias a un bot de GitHub Actions.

Por defecto el calendario cubre **2026–2030**. Más abajo se explica cómo ampliarlo.

---

## Índice

1. [Archivos del proyecto](#1-archivos-del-proyecto)
2. [Antes de empezar: 4 reglas para no atascarte](#2-antes-de-empezar-4-reglas-para-no-atascarte)
3. [Crear el repositorio](#3-crear-el-repositorio)
4. [Subir los archivos](#4-subir-los-archivos)
5. [Activar GitHub Pages](#5-activar-github-pages)
6. [Permisos del bot](#6-permisos-del-bot)
7. [Probar el bot a mano](#7-probar-el-bot-a-mano)
8. [Traducir las noticias (opcional)](#8-traducir-las-noticias-opcional)
9. [Añadir o quitar años del calendario](#9-añadir-o-quitar-años-del-calendario)
10. [Qué limpia el script](#10-qué-limpia-el-script)
11. [Cambiar la hora del bot (y por qué a veces se retrasa)](#11-cambiar-la-hora-del-bot-y-por-qué-a-veces-se-retrasa)
12. [Problemas frecuentes](#12-problemas-frecuentes)

---

## 1. Archivos del proyecto

| Archivo | Para qué sirve | Dónde va en el repo |
|---|---|---|
| index.html | La página (calendario y tablón) | raíz |
| news.json | Lo escribe el bot cada día | raíz |
| README.md | Estas instrucciones | raíz |
| noticias.py | Busca, limpia y elige las 5 noticias | carpeta scripts |
| noticias.yml | Lo ejecuta GitHub a diario | carpeta .github/workflows |

Estructura final que debe quedar en el repo:

```
index.html
news.json
README.md
scripts/noticias.py
.github/workflows/noticias.yml
```

---

## 2. Antes de empezar: 4 reglas para no atascarte

Estos son los fallos más comunes. Léelos antes de subir nada.

**Regla 1. Escribe las rutas a mano. No las copies de ningún sitio.**
Si copias un nombre desde un texto con formato de código, puede llevarse una comilla invertida pegada. El resultado son carpetas y archivos llamados `` `scripts `` o `` noticias.yml` ``, que GitHub no reconoce. Escribe siempre el nombre con el teclado.

**Regla 2. Comprueba que el archivo pegado esté completo.**
Al copiar y pegar un archivo largo, a veces se corta. Después de guardar, abre el archivo y mira el contador de líneas que aparece arriba:

| Archivo | Líneas que debe tener |
|---|---|
| scripts/noticias.py | **223** |
| .github/workflows/noticias.yml | **29** |

Si `noticias.py` muestra unas 74 líneas, está cortado y el bot fallará a los 3 segundos con "exit code 1". Pégalo de nuevo, entero.

**Regla 3. La carpeta .github no se puede subir con "Upload files".**
GitHub ignora las carpetas que empiezan por punto al subir archivos. Hay que crear ese archivo a mano (paso 4c).

**Regla 4. GitHub no descomprime zips.**
Sube los archivos sueltos, no el zip.

---

## 3. Crear el repositorio

1. Entra en github.com e inicia sesión.
2. Pulsa **+ → New repository**.
3. Ponle un nombre (por ejemplo `calendario-medieval`), déjalo en **Public** y pulsa **Create repository**.

---

## 4. Subir los archivos

### 4a. Archivos de la raíz (subida normal)

1. En el repo, pulsa **Add file → Upload files**.
2. Sube `index.html`, `news.json` y `README.md`.
3. Pulsa **Commit changes**.

### 4b. El script (se crea a mano)

1. Pulsa **Add file → Create new file**.
2. En el nombre escribe **con el teclado**: `scripts/noticias.py`
   (al escribir la `/` se crea la carpeta sola).
3. Abre el archivo `noticias.py`, selecciona todo su contenido, cópialo y pégalo en el editor.
4. Pulsa **Commit changes**.
5. Abre el archivo y comprueba que ponga **223 lines** (regla 2).

### 4c. El workflow (se crea a mano)

1. Pulsa **Add file → Create new file**.
2. En el nombre escribe **con el teclado**: `.github/workflows/noticias.yml`
3. Abre el archivo `noticias.yml`, copia todo su contenido y pégalo en el editor.
4. Pulsa **Commit changes**.

### Comprobación

En la pantalla principal del repo deben verse las carpetas `.github` y `scripts`, sin ningún símbolo extra delante. Si ves `` `scripts `` o `` `.github ``, tienen la comilla: ver el paso de abajo.

### Cómo arreglar un nombre con comilla

1. Abre el archivo con el nombre mal escrito y pulsa el lápiz (**Edit**).
2. En la ruta de arriba, borra todo el nombre y escríbelo a mano bien.
3. Pulsa **Commit changes**. GitHub mueve el archivo solo y la carpeta mala desaparece.

> Si usas un ordenador con Git, puedes subir todo de una vez con `git push` desde la carpeta del proyecto. Ahí sí se respeta `.github`.

---

## 5. Activar GitHub Pages

1. Ve a **Settings → Pages**.
2. En **Source** elige **Deploy from a branch**.
3. Selecciona la rama `main` y la carpeta `/ (root)`. Pulsa **Save**.
4. En uno o dos minutos la página estará en:
   `https://TU-USUARIO.github.io/NOMBRE-DEL-REPO/`

Cada vez que cambies un archivo, GitHub vuelve a publicar la página solo. Lo verás en **Actions** como "pages build and deployment".

---

## 6. Permisos del bot

1. Ve a **Settings → Actions → General**.
2. En **Actions permissions**, comprueba que esté marcado **Allow all actions and reusable workflows**.
3. Baja hasta **Workflow permissions** y marca **Read and write permissions**.
4. Pulsa **Save**.

Sin el permiso de escritura, el bot genera las noticias pero falla al guardarlas (error 403 en "Guardar cambios").

---

## 7. Probar el bot a mano

1. Ve a la pestaña **Actions**.
2. Si aparece un botón verde "I understand my workflows, go ahead and enable them", púlsalo.
3. En el menú de la izquierda, debajo de **All workflows**, debe aparecer **Noticias diarias**. Púlsalo.
4. Pulsa **Run workflow → Run workflow**.
5. Recarga a los 10 o 15 segundos. Verás una ejecución con círculo amarillo (en marcha).
6. Cuando termine:
   - **Verde**: todo bien. Abre `news.json` y verás un commit nuevo de `noticias-bot` con el mensaje "Noticias del día".
   - **Rojo**: entra en la ejecución, pulsa **actualizar** y mira qué paso tiene la ✗ roja.

Una ejecución correcta dura alrededor de 50 segundos. Si falla a los 3 segundos, casi seguro `noticias.py` está cortado (regla 2).

El aviso amarillo "Node.js 20 is deprecated" es solo una advertencia de GitHub. Se puede ignorar.

A partir de ahí el bot corre solo, a las horas que indique el `cron` (por defecto, 9:11 y 21:11 UTC). Puede retrasarse o saltarse alguna ejecución; ver la sección 11 para la estrategia recomendada y el botón de respaldo.

---

## 8. Traducir las noticias (opcional)

Por defecto, las notas en inglés se quedan en inglés. Para que se traduzcan al español:

1. Ve a **Settings → Secrets and variables → Actions → New repository secret**.
2. Nombre: `ANTHROPIC_API_KEY`
3. Valor: tu clave de API de Anthropic.
4. Pulsa **Add secret**.

Si no lo configuras, todo funciona igual.

---

## 9. Añadir o quitar años del calendario

Los años están definidos en `index.html`, en dos líneas seguidas. El calendario calcula los meses y los días con el año elegido, así que no hay que tocar nada más.

Las dos líneas (están hacia la línea 245; en el editor usa la lupa o Ctrl+F y busca `const YEARS`):

```js
const YEARS=[2026,2027,2028,2029,2030];
let year=YEARS.includes(new Date().getFullYear())?new Date().getFullYear():2026,sel=null,store={};
```

### 9a. Arreglo recomendado (hazlo una sola vez)

La segunda línea tiene un `2026` fijo: es el año que se abre cuando el año actual no está en la lista. Si algún día quitas el 2026 de la lista sin cambiar eso, la página se abre en un año que ya no tiene botón y **ningún botón queda marcado**.

Para que no vuelva a pasar, cambia ese `2026` final por `YEARS[0]` (el primer año de la lista):

```js
let year=YEARS.includes(new Date().getFullYear())?new Date().getFullYear():YEARS[0],sel=null,store={};
```

Con este cambio, la página siempre abre en el año actual si está en la lista, y si no, en el primero de la lista. Ya no tendrás que tocar esa línea nunca más.

Pasos: abre `index.html` → lápiz (**Edit**) → busca la línea → cambia `2026` por `YEARS[0]` → **Commit changes**.

### 9b. Añadir años

1. Abre `index.html` y pulsa el lápiz (**Edit**).
2. En la línea `const YEARS=` añade los años que quieras, separados por comas. Por ejemplo, hasta 2040:

```js
const YEARS=[2026,2027,2028,2029,2030,2031,2032,2033,2034,2035,2036,2037,2038,2039,2040];
```

3. Opcional: cambia el título de la pestaña en la línea 7:

```html
<title>Calendario Medieval 2026 · 2040</title>
```

4. Pulsa **Commit changes**.
5. En uno o dos minutos la página mostrará los botones nuevos (recarga con Ctrl+F5 si no los ves).

### 9c. Quitar años (por ejemplo, ya pasó el 2026)

1. Haz primero el arreglo de la sección 9a. Es imprescindible.
2. Abre `index.html` y pulsa el lápiz (**Edit**).
3. En `const YEARS=` borra el año que ya no quieras. Por ejemplo, para quitar el 2026:

```js
const YEARS=[2027,2028,2029,2030];
```

4. Opcional: actualiza el título de la línea 7.
5. Pulsa **Commit changes**.

La lista debe estar siempre **ordenada de menor a mayor**, porque el primero es el que se abre por defecto.

### Qué pasa con los eventos que ya guardaste

- Tus eventos se guardan en el navegador de cada dispositivo (no en GitHub), por fecha y año.
- Si quitas un año, sus eventos **no se borran**, pero no podrás verlos mientras ese año no esté en la lista. Si vuelves a añadir el año, reaparecen.
- Antes de quitar un año con eventos importantes, pulsa **Respaldo** en la página para guardar una copia.

### Cómo se ve con muchos años

Probado en una copia de la página con los años hasta 2040 (15 botones):

- **PC (1440 px):** los botones se reparten en dos filas, centrados.
- **Teléfono (390 px):** tres filas de cinco botones, sin desplazamiento lateral.

Los botones saltan de línea solos, así que puedes añadir los años que quieras sin tocar el diseño. Cada fila extra empuja un poco el calendario hacia abajo.

### Comportamiento probado al quitar el 2026 (con el arreglo 9a)

| Fecha de hoy | Año con el que abre |
|---|---|
| Año que está en la lista (por ejemplo 2029) | Ese año, marcado en rojo |
| Año que ya quitaste (2026) | El primero de la lista (2027) |
| Año fuera del rango (por ejemplo 2035) | El primero de la lista (2027) |

> Escribe la lista a mano o copia solo el contenido del bloque, sin las comillas de código (regla 1).

---

## 10. Qué limpia el script

- Descarta notas fuera de tema (podcasts, reseñas, recetas, eventos, etc.).
- Quita duplicados: mismo enlace, mismo título o la misma historia en dos medios.
- No repite las noticias del día anterior mientras haya otras disponibles.
- Máximo 1 noticia por medio (2 solo si faltan).
- Si no hay noticias nuevas, conserva el `news.json` anterior.

---

## 11. Cambiar la hora del bot (y por qué a veces se retrasa)

En `.github/workflows/noticias.yml` está esta línea:

```yaml
- cron: "11 9,21 * * *"  # 9:11 y 21:11 UTC
```

Los números son **minuto hora día-del-mes mes día-de-la-semana**, y la hora es siempre **UTC**. Lo que escribas después del `#` es solo un comentario: GitHub lo ignora (ponle un espacio antes del `#` y no lo metas dentro de las comillas).

Ejemplos:

| Quieres | Escribe |
|---|---|
| Una vez al día, 9:11 UTC | `11 9 * * *` |
| Dos veces al día (9:11 y 21:11 UTC) | `11 9,21 * * *` |
| Cada 6 horas (4 veces al día) | `11 */6 * * *` |
| Cada 3 horas (8 veces al día) | `11 */3 * * *` |
| Cada 2 horas (12 veces al día) | `11 */2 * * *` |

### Pasar de UTC a tu hora

Resta o suma la diferencia de tu zona. Ejemplo para Argentina y Uruguay (UTC-3, sin cambio de verano):

| UTC | Tu hora |
|---|---|
| 9:11 | 6:11 a.m. |
| 21:11 | 6:11 p.m. |

En España, la diferencia es +1 en invierno y +2 en verano.

### Problema: el bot se ejecuta tarde, o directamente no se ejecuta

Pasó en este proyecto, dos veces:

1. Con el cron `0 11 * * *` (11:00 UTC, las 8:00 a.m. en Argentina), la ejecución programada corrió a las 13:34 hora local: unas 5 horas y media tarde.
2. Con el cron `11 9,21 * * *` (6:11 a.m. y 6:11 p.m.), a las 9:30 a.m. del día siguiente **no había ninguna ejecución programada**. Hubo que lanzar el bot a mano con **Run workflow**.

Esto **no es un error de tu configuración**. El archivo estaba bien escrito.

**Por qué pasa:**
- GitHub avisa en su documentación de que las tareas programadas (`schedule`) pueden retrasarse cuando hay mucha carga en sus servidores, y que no garantiza la hora exacta.
- Las horas en punto (`0 9`, `0 11`, `0 21`) son las más saturadas, porque mucha gente programa sus tareas justo a esa hora.
- En repositorios nuevos o con poca actividad, el retraso suele ser mayor, y a veces una ejecución se salta del todo.
- No hay forma de arreglarlo desde el archivo: la puntualidad depende de GitHub.

### Estrategia recomendada: ejecuciones frecuentes + botón manual de respaldo

Como no se puede garantizar una hora exacta, la forma más fiable es no depender de una sola ejecución:

1. **Ejecuciones más seguidas.** Si una se retrasa o se salta, otra llega poco después. Por ejemplo, cada 3 horas:

```yaml
- cron: "11 */3 * * *"  # 8 veces al día, minuto 11
```

   Es gratis: en un repositorio público, GitHub Actions no tiene coste. Cada ejecución dura menos de un minuto.

2. **Minuto distinto de 0.** Usa `11`, `17` o `43` en vez de `0`, para esquivar la hora en punto.

3. **Botón manual de respaldo.** Si ves que las noticias están viejas y necesitas algo fresco ya, ve a **Actions → Noticias diarias → Run workflow → Run workflow**. Es lo más rápido y siempre funciona, aunque todo lo demás falle.

4. **Si todo falla,** revisa que la última ejecución en Actions no salga en rojo, y que **Settings → Actions → General** siga con **Allow all actions** y **Read and write permissions** (secciones 6 y 7).

### Qué cambia al ejecutar más seguido

El script no repite las noticias que ya están en `news.json` mientras haya otras disponibles. Eso significa que **cada ejecución renueva el tablón**:

| Frecuencia | Cuántas veces cambia el tablón al día |
|---|---|
| `11 9,21 * * *` | 2 |
| `11 */6 * * *` | 4 |
| `11 */3 * * *` | 8 |
| `11 */2 * * *` | 12 |

- Si prefieres que el tablón cambie pocas veces al día, elige menos ejecuciones (y acepta que una pueda retrasarse).
- Si prefieres que siempre haya noticias recientes, elige más ejecuciones.
- Cuando una ejecución no encuentra noticias nuevas, el script conserva el `news.json` anterior y no cambia nada.

### Alternativa avanzada: un disparador externo

Servicios como cron-job.org pueden pedirle a GitHub que lance el workflow a una hora exacta, y suelen ser más puntuales que `schedule`. Requiere crear un token de GitHub y configurar el servicio, así que solo vale la pena si necesitas puntualidad estricta. Para uso normal, la estrategia de arriba es suficiente.

### Cómo saber si una actualización fue manual o programada

1. Ve a **Actions → Noticias diarias**.
2. Cada ejecución indica "Manually run by..." (manual) o "Scheduled" (programada), y la hora.
3. En la página, la línea "Actualizado" muestra la hora de la última ejecución que encontró noticias nuevas, convertida a la hora de tu dispositivo. Si una ejecución no encuentra noticias nuevas, el script conserva el `news.json` anterior y esa hora no cambia.

### Cuándo empieza a valer un cambio de horario

Un cambio en el `cron` vale desde el siguiente horario programado. No dispara una ejecución en el momento.

---

## 12. Problemas frecuentes

| Problema | Causa probable | Solución |
|---|---|---|
| No aparece "Noticias diarias" en Actions | Falta `.github/workflows/noticias.yml`, o está en una carpeta con comilla | Repite el paso 4c y la sección "Cómo arreglar un nombre con comilla" |
| Carpetas o archivos con una comilla (`` `scripts ``) | Copiaste el nombre en vez de escribirlo | Renómbralos escribiendo la ruta a mano |
| El workflow falla a los 3 segundos ("exit code 1") | `noticias.py` está cortado (unas 74 líneas) | Pégalo entero; debe tener 223 líneas |
| Falla en "Guardar cambios" (error 403) | Falta el permiso de escritura | Paso 6: Read and write permissions |
| Al guardar sale "has committed since you started editing" | Abriste el editor y el archivo cambió después | Copia tu texto, recarga la página, abre el editor otra vez, pega y guarda |
| Sale el aviso "You have unsaved changes" | Intentaste salir sin guardar | Pulsa **Cancelar** y guarda con **Commit changes** |
| La página no carga | Pages no está activado o aún publica | Revisa el paso 5 y espera un par de minutos |
| Las noticias no cambian | Alguna fuente falló o no hay noticias nuevas | Mira el log en Actions: cada fuente indica `OK` o `ERR` |
| Los años nuevos no aparecen | Cambio sin guardar o Pages aún publica | Comprueba el commit en `index.html`, espera un par de minutos y recarga con Ctrl+F5 |
| El bot se ejecutó horas más tarde de lo programado, o no se ejecutó | GitHub retrasa o se salta tareas programadas, sobre todo en horas en punto y en repos con poca actividad | Usa ejecuciones más frecuentes (`11 */3 * * *`), un minuto distinto de 0, y el botón **Run workflow** como respaldo (sección 11) |
| La hora de "Actualizado" no cambió aunque el bot corrió | No había noticias nuevas y el script conserva el `news.json` anterior | Es normal. Mira en Actions si la ejecución salió en verde |
| No sé si una actualización fue manual o programada | La página solo muestra la hora | En Actions, cada ejecución dice "Manually run" o "Scheduled" |
| Quité un año de la lista y ningún botón queda marcado, o se ve un año sin botón | La línea de abajo (`let year=...`) todavía tiene el `2026` fijo | Cambia ese `2026` final por `YEARS[0]` (sección 9a) |
| Quité un año y mis eventos desaparecieron | No se borraron: solo están ocultos mientras ese año no esté en la lista | Vuelve a añadir el año a `YEARS` y reaparecen. Antes de quitar años, usa **Respaldo** |
| La lista de años quedó desordenada y abre en un año raro | El primer año de la lista es el que se abre por defecto | Ordena `YEARS` de menor a mayor |

---

## Resumen rápido (checklist)

- [ ] Repo público creado
- [ ] `index.html`, `news.json` y `README.md` subidos a la raíz
- [ ] `scripts/noticias.py` creado a mano (223 líneas)
- [ ] `.github/workflows/noticias.yml` creado a mano
- [ ] Sin comillas raras en ningún nombre
- [ ] Pages activado en la rama `main`, carpeta raíz
- [ ] Read and write permissions activado
- [ ] Probado con **Run workflow** y salió en verde
- [ ] (Recomendado) Cron con minuto distinto de 0 y ejecuciones frecuentes, por ejemplo `11 */3 * * *`
- [ ] Saber usar **Run workflow** como respaldo manual si una ejecución programada no llega
- [ ] (Recomendado) Línea 246 de `index.html` con `YEARS[0]` en vez de `2026` (sección 9a)
