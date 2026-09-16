#!/usr/bin/env python3
"""Genera index.html (el sitio de GitHub Pages, servido desde la raíz del repo) a partir de la tabla de
contenidos de las notas (notas/Notas-TO.toc) y de las descripciones de abajo.

Uso:  python3 herramientas/generar_sitio.py   (después de compilar las notas)
"""
import re, pathlib, html

RAIZ = pathlib.Path(__file__).resolve().parent.parent
TOC = RAIZ / 'notas' / 'Notas-TO.toc'
DEST = RAIZ / 'index.html'
REPO = 'https://github.com/jfbonder/transporte-optimo'
RAW = 'https://raw.githubusercontent.com/jfbonder/transporte-optimo/main/'
COLAB = 'https://colab.research.google.com/github/jfbonder/transporte-optimo/blob/main/cuadernos/'
PDF = 'notas/Notas-TO.pdf'

RESUMEN = {
 '1': 'El problema de Monge y su relajación de Kantorovich: mapas y planes de transporte, el caso discreto (asignación y matrices biestocásticas), el push-forward y la formulación en espacios de medida.',
 '2': 'Convergencia débil de medidas, compacidad de los planes (Prokhorov) y existencia de planes óptimos para costos semicontinuos inferiormente.',
 '3': 'Lo esencial de la dualidad en programación lineal: dual, dualidad débil y fuerte, holgura complementaria.',
 '4': 'El problema dual de Kantorovich, dualidad débil y la demostración de la dualidad fuerte vía Fenchel–Rockafellar.',
 '5': 'Potenciales de Kantorovich en el caso discreto: existencia, relación con el soporte de los planes óptimos y ejemplos con potenciales no únicos.',
 '6': 'La c-transformada, existencia de potenciales de Kantorovich, caracterización del soporte de los planes óptimos y el costo cuadrático vía Legendre.',
 '7': 'Acoplamientos y copulas, matching estable, transporte multimarginal y estabilidad de los planes bajo discretización.',
 '8': 'Función de distribución y pseudoinversa, el mapa monótono, c-monotonicidad cíclica y optimalidad del plan monótono para costos convexos; fórmula del costo óptimo.',
 '9': 'El teorema de Brenier: para el costo cuadrático el plan óptimo es el gradiente de una función convexa; factorización polar.',
 '10': 'Las distancias Wₚ en Pₚ: desigualdad triangular vía pegado, metrización de la convergencia débil, Kantorovich–Rubinstein y geodésicas.',
 '11': 'Una demostración de la desigualdad de Brunn–Minkowski con transporte óptimo.',
 '12': 'Baricentros de Wasserstein: existencia, convexidad y unicidad, criterio de optimalidad, formulación multimarginal y los casos explícitos (dimensión uno, gaussianas).',
 '13': 'Regularización entrópica, dualidad entrópica, el algoritmo de Sinkhorn y su convergencia, límites en ε y baricentros entrópicos.',
 'A': 'Repaso de teoría de la medida, desintegración de medidas y el lema de pegado.',
 'B': 'El teorema de Fenchel–Rockafellar.',
 'C': 'Factorización polar de matrices inversibles.',
 'D': 'Subdiferencial de funciones convexas y teorema de Rademacher.',
 'E': 'Los cuadernos de cómputo: POT, convenciones y tabla capítulo–cuaderno.',
}

CUADERNOS = [
 ('01-monge-kantorovich.ipynb', 'Monge y Kantorovich', 'Capítulos 1–2', 'Planes discretos con POT, mapas y planes en dimensión uno, asignación y Birkhoff, costos cóncavos, convergencia débil de planes.'),
 ('02-dualidad.ipynb', 'Dualidad', 'Capítulos 3–6', 'Duales con linprog, potenciales de Kantorovich, holgura complementaria, mejora de potenciales, costo 0–1.'),
 ('03-ot-dimension-uno.ipynb', 'OT en dimensión uno', 'Capítulo 8', 'Pseudoinversas, el mapa monótono, planes con átomos, fórmula del costo óptimo, plan antimonótono.'),
 ('04-distancias-wasserstein.ipynb', 'Distancias de Wasserstein', 'Capítulo 10', 'Wₚ entre muestras, comparación con otras métricas, geodésicas e interpolación, Kantorovich–Rubinstein.'),
 ('05-baricentros-wasserstein.ipynb', 'Baricentros de Wasserstein', 'Capítulo 12', 'Baricentros en dimensión uno, de gaussianas y de medidas discretas; formulación multimarginal.'),
 ('06-transporte-entropico-sinkhorn.ipynb', 'Transporte entrópico y Sinkhorn', 'Capítulo 13', 'Planes entrópicos, Sinkhorn en versión escalada y en el dominio logarítmico, límites en ε, baricentros entrópicos de formas.'),
]
CUADERNO_DE_CAP = {'2': 0, '6': 1, '8': 2, '10': 3, '12': 4, '13': 5}

# ------------------------------------------------------------ tabla de contenidos
caps = []
for l in TOC.read_text(encoding='utf-8').split('\n'):
    if not l.startswith('\\contentsline {chapter}'):
        continue
    m = re.search(r'\}\{(\d+|[A-Z])\}\{(.*)\}\}\{(\d+)\}\{(?:chapter|appendix)', l)
    if m:
        caps.append((m.group(1), m.group(2).replace('--', '–'), int(m.group(3))))

def practica(num):
    return ('practicas/apendice-%s.pdf' % num) if not num.isdigit() else ('practicas/practica-%02d.pdf' % int(num))

filas = []
for num, tit, pag in caps:
    if num == 'E':
        continue
    es_ap = not num.isdigit()
    enlaces = ['<a href="%s#page=%d">notas</a>' % (PDF, pag), '<a href="%s">guía</a>' % practica(num)]
    if num in CUADERNO_DE_CAP:
        arch, nom, _, _ = CUADERNOS[CUADERNO_DE_CAP[num]]
        enlaces.append('<a href="%s%s">cuaderno</a>' % (COLAB, arch))
    etiqueta = ('Apéndice %s' % num) if es_ap else ('Capítulo %s' % num)
    filas.append('''      <article class="cap">
        <div class="num">%s</div>
        <div>
          <h3>%s</h3>
          <p>%s</p>
          <p class="enlaces">%s</p>
        </div>
      </article>''' % (etiqueta, html.escape(tit), html.escape(RESUMEN.get(num, '')), ' · '.join(enlaces)))

tarjetas = []
for arch, nom, caps_, desc in CUADERNOS:
    tarjetas.append('''      <article class="cuaderno">
        <h3>%s</h3>
        <p class="meta">%s</p>
        <p>%s</p>
        <p class="enlaces"><a class="boton" href="%s%s">Abrir en Colab</a> <a class="nw" href="%scuadernos/%s">descargar&nbsp;.ipynb</a></p>
      </article>''' % (html.escape(nom), caps_, html.escape(desc), COLAB, arch, RAW, arch))

pagina = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Teoría de Transporte Óptimo</title>
<meta name="description" content="Teoría de Transporte Óptimo: curso optativo de la FCEN-UBA. Notas de clase, guías de ejercicios y cuadernos de cómputo.">
<style>
  :root { --tinta:#1d1d1f; --gris:#5b5b60; --linea:#e3e3e6; --acento:#8b1e1e; --fondo:#fbfbf9; --tarjeta:#fff; }
  @media (prefers-color-scheme: dark) {
    :root { --tinta:#ececec; --gris:#a5a5ab; --linea:#333338; --acento:#e0706b; --fondo:#141416; --tarjeta:#1d1d20; }
  }
  * { box-sizing:border-box; }
  body { margin:0; font:17px/1.55 Georgia, "Times New Roman", serif; color:var(--tinta); background:var(--fondo); }
  header, main, footer { max-width:880px; margin:0 auto; padding:0 16px; }
  header { padding-top:56px; padding-bottom:24px; border-bottom:1px solid var(--linea); }
  h1 { font-size:2.2rem; margin:0 0 6px; font-weight:normal; letter-spacing:.01em; }
  .sub { color:var(--gris); margin:0 0 6px; }
  .autor { font-family:system-ui, sans-serif; font-size:.9rem; }
  nav { margin-top:22px; font-family:system-ui, sans-serif; font-size:.95rem; }
  nav a { margin-right:18px; color:var(--acento); text-decoration:none; }
  h2 { font-weight:normal; font-size:1.5rem; margin:44px 0 14px; }
  p { margin:0 0 12px; }
  a { color:var(--acento); }
  .descarga { display:flex; flex-wrap:wrap; gap:10px; margin:14px 0 6px; font-family:system-ui, sans-serif; font-size:.95rem; }
  .boton { display:inline-block; padding:8px 14px; border:1px solid var(--acento); border-radius:6px; text-decoration:none; color:var(--acento); }
  .boton.lleno { background:var(--acento); color:#fff; }
  .cap { display:grid; grid-template-columns:110px 1fr; gap:14px; padding:16px 0; border-bottom:1px solid var(--linea); }
  .cap .num { color:var(--gris); font-family:system-ui, sans-serif; font-size:.85rem; text-transform:uppercase; letter-spacing:.06em; padding-top:6px; }
  .cap h3, .cuaderno h3 { margin:0 0 4px; font-size:1.1rem; font-weight:normal; }
  .cap p, .cuaderno p { color:var(--gris); font-size:.97rem; margin:0 0 6px; }
  .enlaces { font-family:system-ui, sans-serif; font-size:.9rem; }
  .cuadernos { display:grid; grid-template-columns:repeat(auto-fill, minmax(260px, 1fr)); gap:14px; }
  .cuaderno { background:var(--tarjeta); border:1px solid var(--linea); border-radius:10px; padding:16px; }
  .cuaderno .meta { font-family:system-ui, sans-serif; font-size:.8rem; text-transform:uppercase; letter-spacing:.06em; }
  .cuaderno .boton { padding:6px 10px; font-size:.85rem; margin-right:8px; }
  .nw { white-space:nowrap; }
  code { font-size:.9em; background:var(--linea); padding:1px 5px; border-radius:4px; }
  footer { margin-top:56px; padding:24px 16px 48px; border-top:1px solid var(--linea); color:var(--gris); font-size:.9rem; }
  @media (max-width:560px) { .cap { grid-template-columns:1fr; gap:4px; } header { padding-top:36px; } h1 { font-size:1.7rem; } }
</style>
</head>
<body>
<header>
  <h1>Teoría de Transporte Óptimo</h1>
  <p class="sub">Curso optativo para las licenciaturas en Matemática y en Ciencia de Datos y para el Doctorado en Matemática.<br>Departamento de Matemática, Facultad de Ciencias Exactas y Naturales, Universidad de Buenos Aires.</p>
  <p class="sub autor">Julián Fernández Bonder · 2do cuatrimestre 2026 · Notas de clase, guías de ejercicios y cuadernos de cómputo</p>
  <nav><a href="#notas">Notas</a><a href="#capitulos">Capítulos</a><a href="#cuadernos">Cuadernos</a><a href="#uso">Cómo usar el material</a><a href="%(repo)s">Repositorio</a></nav>
</header>
<main>
  <section id="notas">
    <h2>Las notas</h2>
    <p>Un curso de un cuatrimestre sobre transporte óptimo, desde el problema de Monge y la relajación de Kantorovich hasta el teorema de Brenier, las distancias de Wasserstein, los baricentros y el transporte entrópico. Están pensadas para estudiantes avanzados de licenciatura y de doctorado en matemática; se asume análisis real y algo de teoría de la medida (repasada en el Apéndice A). Cada capítulo termina con una sección de ejercicios; seis de ellos incluyen además ejercicios computacionales que se resuelven con los cuadernos de más abajo.</p>
    <div class="descarga">
      <a class="boton lleno" href="%(pdf)s">Notas completas (PDF, %(paginas)s páginas)</a>
      <a class="boton" href="%(repo)s/tree/main/practicas">Todas las guías</a>
      <a class="boton" href="%(repo)s/tree/main/notas">Fuentes LaTeX</a>
    </div>
  </section>

  <section id="capitulos">
    <h2>Capítulos</h2>
%(filas)s
  </section>

  <section id="cuadernos">
    <h2>Cuadernos de cómputo</h2>
    <p>Seis cuadernos de Python que acompañan las notas, con la biblioteca <a href="https://pythonot.github.io/">POT</a>. No requieren instalar nada: el botón abre una copia en Google Colab (hace falta una cuenta de Google para ejecutarla). Cada cuaderno termina con los ejercicios computacionales del capítulo correspondiente.</p>
    <div class="cuadernos">
%(tarjetas)s
    </div>
  </section>

  <section id="uso">
    <h2>Cómo usar el material</h2>
    <p>Para estudiar por cuenta propia, el orden natural es el de los capítulos: leer el capítulo, hacer la guía, y en los capítulos que lo tienen, trabajar el cuaderno. Las guías son exactamente las secciones de ejercicios de las notas, con la misma numeración, generadas desde el mismo archivo fuente; las referencias a teoremas y proposiciones remiten a las notas.</p>
    <p>Correcciones y sugerencias: abrir un <em>issue</em> o un <em>pull request</em> en el <a href="%(repo)s">repositorio</a>, o escribir a <code>jfbonder@dm.uba.ar</code>.</p>
  </section>
</main>
<footer>
  <p>© 2026 Julián Fernández Bonder. Este material se distribuye bajo licencia <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es">CC BY-NC-SA 4.0</a>: se puede copiar, redistribuir y adaptar con atribución, sin fines comerciales y compartiendo bajo la misma licencia.</p>
  <p>Instituto de Cálculo (FCEN–CONICET) y Departamento de Matemática (FCEN–UBA).</p>
</footer>
</body>
</html>
'''
# páginas del PDF
import subprocess
try:
    out = subprocess.run(['pdfinfo', str(RAIZ / 'notas' / 'Notas-TO.pdf')], capture_output=True, text=True).stdout
    paginas = re.search(r'Pages:\s+(\d+)', out).group(1)
except Exception:
    paginas = '—'
DEST.write_text(pagina % dict(repo=REPO, pdf=PDF, paginas=paginas, filas='\n'.join(filas), tarjetas='\n'.join(tarjetas)), encoding='utf-8')
print('index.html generado;', len(filas), 'capítulos/apéndices')
