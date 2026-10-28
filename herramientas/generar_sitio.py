#!/usr/bin/env python3
"""Genera index.html (el sitio de GitHub Pages, servido desde la raíz del repo) a
partir de la tabla de contenidos de las notas (notas/Notas-TO.toc), de la tabla
de cuadernos de comun.py y de las descripciones de abajo.

Para agregar una nota al material extra: dejar el .tex en material-extra/,
compilarlo (make extra) y agregar una entrada a EXTRA, más abajo. Si queda un
.tex sin entrada, este script avisa y no lo publica; si una entrada apunta a un
PDF que no existe, avisa y la saltea. Con EXTRA vacía la sección no aparece.

Uso:  python3 herramientas/generar_sitio.py   (después de compilar las notas)
"""
import html
import pathlib
import re
import subprocess
import sys
from string import Template

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from comun import COLAB, CUADERNOS, RAIZ, REPO, cuaderno_que_acompania  # noqa: E402

TOC = RAIZ / 'notas' / 'Notas-TO.toc'
PDF_NOTAS = RAIZ / 'notas' / 'Notas-TO.pdf'
DEST = RAIZ / 'index.html'
PDF = 'notas/Notas-TO.pdf'

# Descripciones de cada capítulo y apéndice. Son HTML (no se escapan).
RESUMEN = {
 '1': 'El problema de Monge y su relajación de Kantorovich: mapas y planes de transporte, el caso discreto (asignación y matrices biestocásticas), el push-forward y la formulación en espacios de medida.',
 '2': 'Convergencia débil de medidas, compacidad de los planes (Prokhorov) y existencia de planes óptimos para costos semicontinuos inferiormente.',
 '3': 'Lo esencial de la dualidad en programación lineal: dual, dualidad débil y fuerte, holgura complementaria.',
 '4': 'El problema dual de Kantorovich, dualidad débil y la demostración de la dualidad fuerte vía Fenchel–Rockafellar.',
 '5': 'Potenciales de Kantorovich en el caso discreto: existencia, relación con el soporte de los planes óptimos y ejemplos con potenciales no únicos.',
 '6': 'La <i>c</i>-transformada, existencia de potenciales de Kantorovich, caracterización del soporte de los planes óptimos y el costo cuadrático vía Legendre.',
 '7': 'Acoplamientos y cópulas, emparejamiento estable, transporte multimarginal y estabilidad de los planes bajo discretización.',
 '8': 'Función de distribución y pseudoinversa, el mapa monótono, <i>c</i>-monotonía cíclica y optimalidad del plan monótono para costos convexos; fórmula del costo óptimo.',
 '9': 'El teorema de Brenier: para el costo cuadrático el plan óptimo es el gradiente de una función convexa; factorización polar.',
 '10': 'Las distancias W<sub>p</sub> en 𝒫<sub>p</sub>: desigualdad triangular vía pegado, metrización de la convergencia débil, Kantorovich–Rubinstein y geodésicas.',
 '11': 'Una demostración de la desigualdad de Brunn–Minkowski con transporte óptimo.',
 '12': 'Baricentros de Wasserstein: existencia, convexidad y unicidad, criterio de optimalidad, formulación multimarginal y los casos explícitos (dimensión uno, gaussianas).',
 '13': 'Regularización entrópica, dualidad entrópica, el algoritmo de Sinkhorn y su convergencia, límites en ε y baricentros entrópicos.',
 'A': 'Repaso de teoría de la medida, desintegración de medidas y el lema de pegado.',
 'B': 'La transformada de Legendre–Fenchel en espacios de Banach y una demostración del teorema de Fenchel–Rockafellar en la forma que usa la dualidad de Kantorovich (Capítulo 4).',
 'C': 'La raíz cuadrada de una matriz simétrica definida positiva y la escritura de una matriz inversible como composición de una ortogonal y del gradiente de una función convexa: el modelo finito-dimensional del teorema de Brenier.',
 'D': 'Subdiferencial de funciones convexas y teorema de Rademacher.',
 'E': 'Los cuadernos de cómputo: POT, convenciones y tabla capítulo–cuaderno.',
}

EXTRA_DIR = RAIZ / 'material-extra'

# Material extra: cosas escritas para alguna clase en particular, sobre temas
# que las notas usan pero no desarrollan o que conviene ver en movimiento. Una
# entrada por archivo: (nombre sin extensión en material-extra/, extensión,
# título, descripción en HTML). La extensión decide cómo se publica: 'pdf' se
# enlaza con su cantidad de páginas y su fuente LaTeX; 'html' es una página que
# se abre en el navegador.
EXTRA = [
    ('geodesicas', 'pdf', 'Introducción a las geodésicas en espacios métricos',
     'Longitud de curvas, espacios de longitud, reparametrización por longitud de arco y el '
     'teorema de Hopf–Rinow, con dos ejemplos sin compacidad local. Es el trasfondo métrico '
     'que supone la última sección del Capítulo 10.'),
    ('baricentros', 'html', 'Baricentros de Wasserstein',
     'Dos aplicaciones. La primera: N corridas de cromatografía del mismo compuesto, cada una '
     'con su deriva del tiempo de retención; promediarlas punto a punto ensancha el pico y '
     'puede partirlo en dos, mientras que el baricentro devuelve el perfil intacto. Un panel '
     'muestra lo mismo en coordenadas de cuantiles, donde el baricentro es literalmente el '
     'promedio (Proposición 12.6.1). La segunda: promediar tres figuras, con los pesos en un '
     'triángulo que se puede arrastrar, resuelto con el Sinkhorn convolucional del Capítulo 13.'),
    ('brunn-minkowski', 'html', 'Brunn–Minkowski en el plano',
     'La suma de Minkowski de dos rectángulos, uno rotado respecto del otro, con la curva '
     '|(1−t)A+tB|<sup>1/2</sup> dibujándose al lado de la cota (1−t)|A|<sup>1/2</sup>+t|B|<sup>1/2</sup>. '
     'Se puede animar o mover <i>t</i> a mano, y cambiar el ángulo: a 0°, o con <i>B</i> homotético '
     'de <i>A</i>, la curva se apoya sobre la recta, que es el caso de igualdad.'),
]


def practica(num):
    return ('practicas/apendice-%s.pdf' % num) if not num.isdigit() else ('practicas/practica-%02d.pdf' % int(num))


def leer_toc():
    """(num, titulo, pagina) de cada capítulo y apéndice numerado, desde el .toc."""
    if not TOC.exists():
        sys.exit('falta %s: compilar antes las notas (make notas)' % TOC.relative_to(RAIZ))
    caps = []
    for l in TOC.read_text(encoding='utf-8').split('\n'):
        if not l.startswith('\\contentsline {chapter}'):
            continue
        m = re.search(r'\}\{(\d+|[A-Z])\}\{(.*)\}\}\{(\d+)\}\{(?:chapter|appendix)', l)
        if m:
            caps.append((m.group(1), m.group(2).replace('---', '—').replace('--', '–'), int(m.group(3))))
    return caps


def paginas_pdf(pdf=PDF_NOTAS):
    try:
        out = subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True, check=True).stdout
        return re.search(r'Pages:\s+(\d+)', out).group(1)
    except (OSError, subprocess.CalledProcessError, AttributeError) as e:
        print('aviso: no se pudo contar las páginas de %s con pdfinfo (poppler-utils): %s'
              % (pdf.name, e), file=sys.stderr)
        return '—'


def tarjetas_extra():
    """Las tarjetas del material extra, y un aviso por cada fuente sin entrada en EXTRA."""
    listados = {n for n, _, _, _ in EXTRA}
    fuentes = []
    if EXTRA_DIR.is_dir():
        fuentes = sorted(EXTRA_DIR.glob('*.tex')) + sorted(EXTRA_DIR.glob('*.html'))
    for f in fuentes:
        if f.stem not in listados:
            print('aviso: material-extra/%s no figura en EXTRA (generar_sitio.py): '
                  'no se publica en el sitio' % f.name, file=sys.stderr)
    tarjetas = []
    for nombre, tipo, titulo, desc in EXTRA:
        arch = EXTRA_DIR / ('%s.%s' % (nombre, tipo))
        if not arch.exists():
            print('aviso: falta material-extra/%s.%s%s: se saltea «%s»'
                  % (nombre, tipo, ' (make extra)' if tipo == 'pdf' else '', titulo),
                  file=sys.stderr)
            continue
        rel = 'material-extra/%s.%s' % (nombre, tipo)
        if tipo == 'pdf':
            meta = 'PDF · %s páginas' % paginas_pdf(arch)
            enlaces = ('<a class="boton" href="%s">Leer</a> '
                       '<a class="nw" href="%s/blob/main/material-extra/%s.tex">fuente LaTeX</a>'
                       % (rel, REPO, nombre))
        else:
            meta = 'Página interactiva'
            enlaces = ('<a class="boton" href="%s">Abrir</a> '
                       '<a class="nw" href="%s/blob/main/%s">ver el código</a>'
                       % (rel, REPO, rel))
        tarjetas.append('''      <article class="cuaderno">
        <h3>%s</h3>
        <p class="meta">%s</p>
        <p>%s</p>
        <p class="enlaces">%s</p>
      </article>''' % (html.escape(titulo), meta, desc, enlaces))
    return tarjetas


def main():
    caps = leer_toc()
    filas = []
    for num, tit, pag in caps:
        if num == 'E':
            continue
        es_ap = not num.isdigit()
        enlaces = ['<a href="%s#page=%d">notas</a>' % (PDF, pag), '<a href="%s">guía</a>' % practica(num)]
        c = None if es_ap else cuaderno_que_acompania(num)
        if c:
            enlaces.append('<a href="%s%s">cuaderno <i>%s</i></a>' % (COLAB, c[0], html.escape(c[1])))
        etiqueta = ('Apéndice %s' % num) if es_ap else ('Capítulo %s' % num)
        filas.append('''      <article class="cap">
        <div class="num">%s</div>
        <div>
          <h3>%s</h3>
          <p>%s</p>
          <p class="enlaces">%s</p>
        </div>
      </article>''' % (etiqueta, html.escape(tit), RESUMEN.get(num, ''), ' · '.join(enlaces)))

    tarjetas = []
    for arch, nom, cps, _, desc in CUADERNOS:
        meta = ('Capítulo %s' % cps[0]) if len(cps) == 1 else ('Capítulos %s–%s' % (cps[0], cps[-1]))
        tarjetas.append('''      <article class="cuaderno">
        <h3>%s</h3>
        <p class="meta">%s</p>
        <p>%s</p>
        <p class="enlaces"><a class="boton" href="%s%s">Abrir en Colab</a> <a class="nw" href="%s/blob/main/cuadernos/%s">ver en GitHub</a></p>
      </article>''' % (html.escape(nom), meta, desc, COLAB, arch, REPO, arch))

    extras = tarjetas_extra()
    seccion_extra = nav_extra = ''
    if extras:
        nav_extra = '<a href="#extra">Material extra</a>'
        seccion_extra = SECCION_EXTRA.substitute(tarjetas='\n'.join(extras))

    pagina = PAGINA.substitute(repo=REPO, pdf=PDF, paginas=paginas_pdf(),
                               filas='\n'.join(filas), tarjetas='\n'.join(tarjetas),
                               nav_extra=nav_extra, seccion_extra=seccion_extra)
    DEST.write_text(pagina, encoding='utf-8')
    print('index.html generado;', len(filas), 'capítulos/apéndices,',
          len(extras), 'de material extra')


SECCION_EXTRA = Template('''
  <section id="extra">
    <h2>Material extra</h2>
    <p>Notas autocontenidas escritas para alguna clase en particular, sobre temas que las notas usan pero no desarrollan. No forman parte del programa ni tienen guía propia; se leen sueltas, cuando hacen falta.</p>
    <div class="cuadernos">
${tarjetas}
    </div>
  </section>
''')


PAGINA = Template('''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Ccircle cx='8' cy='8' r='7' fill='%238b1e1e'/%3E%3C/svg%3E">
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
  <p class="sub autor">Julián Fernández Bonder · segundo cuatrimestre 2026 · Notas de clase, guías de ejercicios y cuadernos de cómputo</p>
  <nav><a href="#notas">Notas</a><a href="#capitulos">Capítulos</a><a href="#cuadernos">Cuadernos</a>${nav_extra}<a href="#uso">Cómo usar el material</a><a href="${repo}">Repositorio</a></nav>
</header>
<main>
  <section id="notas">
    <h2>Las notas</h2>
    <p>Un curso de un cuatrimestre sobre transporte óptimo, desde el problema de Monge y la relajación de Kantorovich hasta el teorema de Brenier, las distancias de Wasserstein, los baricentros y el transporte entrópico. Están pensadas para estudiantes avanzados de licenciatura y de doctorado en matemática; se asume análisis real y algo de teoría de la medida (repasada en el Apéndice A). Cada capítulo termina con una sección de ejercicios; seis capítulos (2, 6, 8, 10, 12 y 13) incluyen además ejercicios computacionales, que se resuelven con los cuadernos de más abajo.</p>
    <div class="descarga">
      <a class="boton lleno" href="${pdf}">Notas completas (PDF, ${paginas} páginas)</a>
      <a class="boton" href="${repo}/tree/main/practicas">Todas las guías</a>
      <a class="boton" href="practicas/sugerencias.pdf">Sugerencias para los ejercicios</a>
      <a class="boton" href="${repo}/tree/main/notas">Fuentes LaTeX</a>
    </div>
  </section>

  <section id="capitulos">
    <h2>Capítulos</h2>
${filas}
  </section>

  <section id="cuadernos">
    <h2>Cuadernos de cómputo</h2>
    <p>Seis cuadernos de Python que acompañan las notas, con la biblioteca <a href="https://pythonot.github.io/">POT</a>. No requieren instalar nada: el botón abre una copia en Google Colab (hace falta una cuenta de Google para ejecutarla). Cada cuaderno termina con los ejercicios computacionales del capítulo correspondiente.</p>
    <div class="cuadernos">
${tarjetas}
    </div>
  </section>
${seccion_extra}
  <section id="uso">
    <h2>Cómo usar el material</h2>
    <p>Para estudiar por cuenta propia, el orden natural es el de los capítulos: leer el capítulo, hacer la guía, y en los capítulos que lo tienen, trabajar el cuaderno. Las guías son exactamente las secciones de ejercicios de las notas, con la misma numeración, generadas desde el mismo archivo fuente; las referencias a teoremas y proposiciones remiten a las notas. El archivo de <a href="practicas/sugerencias.pdf">sugerencias</a> reúne, para los ejercicios de todos los capítulos, una idea o el resultado que conviene usar, sin resolverlos.</p>
    <p>Correcciones y sugerencias: abrir un <em>issue</em> o un <em>pull request</em> en el <a href="${repo}">repositorio</a>, o escribir a <code>jfbonder@dm.uba.ar</code>.</p>
  </section>
</main>
<footer>
  <p>© 2026 Julián Fernández Bonder. El texto y las figuras se distribuyen bajo licencia <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es">CC BY-NC-SA 4.0</a>: se pueden copiar, redistribuir y adaptar con atribución, sin fines comerciales y compartiendo bajo la misma licencia. El código (cuadernos y herramientas) tiene licencia MIT. Las imágenes de terceros no están cubiertas por estas licencias.</p>
  <p>Instituto de Cálculo (IC–CONICET) y Departamento de Matemática (FCEN–UBA).</p>
</footer>
</body>
</html>
''')

if __name__ == '__main__':
    main()
