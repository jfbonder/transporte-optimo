# -*- coding: utf-8 -*-
"""Código común a los generadores de guías, sugerencias y sitio.

Lee notas/Notas-TO.tex una sola vez y expone:

- las rutas y direcciones del repositorio (RAIZ, TEX, REPO, SITIO, COLAB);
- CUADERNOS, la tabla cuaderno-capítulos, que es la fuente única para las
  guías y el sitio (el README y el Apéndice E de las notas deben coincidir);
- capitulos(), la lista de capítulos y apéndices numerados de las notas;
- PREAMBULO, el preámbulo de las guías (amsart con el encabezado del curso),
  construido a partir del preámbulo de las notas;
- encabezado_fancy(), las líneas de LaTeX del encabezado de portada y de página.
"""
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
TEX = RAIZ / 'notas' / 'Notas-TO.tex'
REPO = 'https://github.com/jfbonder/transporte-optimo'
SITIO = 'https://jfbonder.github.io/transporte-optimo/'
COLAB = 'https://colab.research.google.com/github/jfbonder/transporte-optimo/blob/main/cuadernos/'

# ---------------------------------------------------------------- cuadernos
# (archivo, nombre, capítulos que acompaña, capítulo con sus ejercicios
#  computacionales, descripción para el sitio)
CUADERNOS = [
    ('01-monge-kantorovich.ipynb', 'Monge y Kantorovich', ('1', '2'), '2',
     'Planes discretos con POT, mapas y planes en dimensión uno, asignación y '
     'Birkhoff, costos cóncavos, convergencia débil de planes.'),
    ('02-dualidad.ipynb', 'Dualidad', ('3', '4', '5', '6'), '6',
     'Duales con linprog, potenciales de Kantorovich, holgura complementaria, '
     'mejora de potenciales, costo 0–1.'),
    ('03-ot-dimension-uno.ipynb', 'OT en dimensión uno', ('8',), '8',
     'Pseudoinversas, el mapa monótono, planes con átomos, fórmula del costo '
     'óptimo, plan antimonótono.'),
    ('04-distancias-wasserstein.ipynb', 'Distancias de Wasserstein', ('10',), '10',
     'W<sub>p</sub> entre muestras, comparación entre exponentes, geodésicas e '
     'interpolación, Kantorovich–Rubinstein.'),
    ('05-baricentros-wasserstein.ipynb', 'Baricentros de Wasserstein', ('12',), '12',
     'Baricentros en dimensión uno, de gaussianas y de medidas discretas; '
     'formulación multimarginal.'),
    ('06-transporte-entropico-sinkhorn.ipynb', 'Transporte entrópico y Sinkhorn', ('13',), '13',
     'Planes entrópicos, Sinkhorn en versión escalada y en el dominio '
     'logarítmico, límites en ε, baricentros entrópicos de formas.'),
]


def cuaderno_que_acompania(num):
    """Cuaderno que acompaña al capítulo `num` (cadena), o None."""
    for c in CUADERNOS:
        if num in c[2]:
            return c
    return None


def cuaderno_con_ejercicios(num):
    """Cuaderno cuyos ejercicios computacionales están en el capítulo `num`, o None."""
    for c in CUADERNOS:
        if c[3] == num:
            return c
    return None


# ---------------------------------------------------------------- fuente
src = TEX.read_text(encoding='utf-8')
L = src.split('\n')


def argumento(linea, inicio):
    """Contenido del grupo {...} que abre en linea[inicio] (llaves balanceadas)."""
    assert linea[inicio] == '{'
    prof = 0
    for k in range(inicio, len(linea)):
        if linea[k] == '{':
            prof += 1
        elif linea[k] == '}':
            prof -= 1
            if prof == 0:
                return linea[inicio + 1:k]
    raise ValueError('llaves no balanceadas: ' + linea)


def capitulos():
    """Capítulos y apéndices numerados de las notas, en orden.

    Devuelve una lista de tuplas (num, titulo, inicio, fin): num es '1', '2', ...
    para los capítulos y 'A', 'B', ... para los apéndices; titulo es el argumento
    de \\chapter{...} (sin los \\label que siguen); [inicio, fin) es el rango de
    líneas de L que ocupa, cortado en \\appendix para el último capítulo y en
    \\bibliographystyle para el último apéndice. Los \\chapter* (prefacio) no
    se numeran y se omiten.
    """
    i_app = next(i for i, l in enumerate(L) if l.startswith('\\appendix'))
    i_bib = next(i for i, l in enumerate(L) if l.startswith('\\bibliographystyle'))
    idx = [i for i, l in enumerate(L) if l.startswith('\\chapter{')]
    res = []
    n_cap = n_app = 0
    for k, i in enumerate(idx):
        if i < i_app:
            n_cap += 1
            num = str(n_cap)
        else:
            num = chr(ord('A') + n_app)
            n_app += 1
        fin = idx[k + 1] if k + 1 < len(idx) else i_bib
        if i < i_app:
            fin = min(fin, i_app)
        titulo = argumento(L[i], len('\\chapter'))
        res.append((num, titulo, i, fin))
    return res


def titulo_texto(titulo):
    """Título de capítulo en texto plano (para Markdown y HTML)."""
    return (titulo.replace('\\texorpdfstring{$c$}{c}', 'c')
                  .replace('---', '—').replace('--', '–'))


# ---------------------------------------------------------------- preámbulo
i_doc = next(i for i, l in enumerate(L) if l.startswith('\\begin{document}'))
pre_out = []
for l in L[:i_doc]:
    if l.startswith('\\documentclass'):
        pre_out += ['\\documentclass[11pt,a4paper]{amsart}',
                    '\\usepackage{xr-hyper}',
                    '\\newcounter{chapter}',
                    '\\usepackage{fancyhdr}',
                    '\\usepackage{geometry} \\geometry{top=2cm,bottom=2.5cm,left=2.5cm,right=2.5cm}']
        continue
    if l.startswith('\\numberwithin{section}{chapter}') or l.startswith('\\numberwithin{figure}{chapter}'):
        continue
    if l.startswith('\\setlength{') or l.startswith('\\hfuzz'):
        continue
    pre_out.append(l)
pre_out += ['\\vfuzz7pt \\hfuzz7pt',
            '\\externaldocument[N-]{../notas/Notas-TO}',
            # encabezado con logos, en el formato de las guías del curso
            '\\newcommand{\\encabezado}[1]{%',
            '\\noindent \\includegraphics[scale=2.1]{logo-dm-wide.png} \\hskip 9.5cm',
            '\\includegraphics[scale=0.08]{logo-exactas-uba.jpg}',
            '\\smallskip',
            '\\usefont{T1}{phv}{m}{n}',
            '\\begin{center}{\\Large\\sc Teoría de Transporte Óptimo}\\end{center}',
            '\\bigskip',
            '\\noindent{\\sc #1}\\\\[-0.4cm]',
            '\\hrule',
            '\\normalfont}',
            '\\newcommand{\\cuadernolink}[2]{\\noindent\\textbf{Cuaderno:} \\emph{#1} '
            '(\\href{' + COLAB + '#2}{abrir en Colab}).\\par\\medskip}']
PREAMBULO = '\n'.join(pre_out)


def encabezado_fancy(titulo, corto):
    """Líneas de LaTeX para el encabezado de portada y los de página."""
    return ['\\encabezado{%s}' % titulo,
            '\\bigskip',
            '\\pagestyle{fancy}',
            '\\fancyhead[L]{{\\footnotesize{\\usefont{T1}{phv}{m}{n}{\\sc Teoría de Transporte Óptimo}}}}',
            '\\fancyhead[R]{\\footnotesize \\usefont{T1}{phv}{m}{n}{\\sc %s}}' % corto,
            '\\thispagestyle{plain}']
