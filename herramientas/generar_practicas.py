#!/usr/bin/env python3
"""Genera las guías de ejercicios (practicas/*.tex) a partir de las notas.

Cada capítulo y apéndice de notas/Notas-TO.tex termina con una sección
\\section*{Ejercicios}. Este script extrae esas secciones, les antepone el
preámbulo de las notas (adaptado a amsart) y produce un archivo .tex por
guía, con la misma numeración de ejercicios que las notas. Las referencias
a resultados de las notas se resuelven con el paquete xr-hyper leyendo
notas/Notas-TO.aux, de modo que hay que compilar primero las notas.

Uso:  python3 herramientas/generar_practicas.py
"""
import re, pathlib, unicodedata, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

RAIZ = pathlib.Path(__file__).resolve().parent.parent
TEX = RAIZ / 'notas' / 'Notas-TO.tex'
DEST = RAIZ / 'practicas'
REPO = 'https://github.com/jfbonder/transporte-optimo'
COLAB = 'https://colab.research.google.com/github/jfbonder/transporte-optimo/blob/main/cuadernos/'

# cuaderno asociado a cada capítulo (sólo los que tienen ejercicios computacionales)
CUADERNOS = {
    2: ('Monge y Kantorovich', '01-monge-kantorovich.ipynb'),
    6: ('Dualidad', '02-dualidad.ipynb'),
    8: ('OT en dimensión uno', '03-ot-dimension-uno.ipynb'),
    10: ('Distancias de Wasserstein', '04-distancias-wasserstein.ipynb'),
    12: ('Baricentros de Wasserstein', '05-baricentros-wasserstein.ipynb'),
    13: ('Transporte entrópico y Sinkhorn', '06-transporte-entropico-sinkhorn.ipynb'),
}

from comun import src, L, PREAMBULO  # noqa: E402

# ---------------------------------------------------------------- capítulos
caps = []   # (numero o letra, titulo, inicio, fin)
i_app = next(i for i, l in enumerate(L) if l.startswith('\\appendix'))
i_bib = next(i for i, l in enumerate(L) if l.startswith('\\bibliographystyle'))
idx = [i for i, l in enumerate(L) if l.startswith('\\chapter')]
n_cap = 0; n_app = 0
for k, i in enumerate(idx):
    fin = idx[k + 1] if k + 1 < len(idx) else i_bib
    if i < i_app:
        n_cap += 1; num = str(n_cap)
    else:
        num = chr(ord('A') + n_app); n_app += 1
    m = re.match(r'\\chapter\{(.*)\}\\label', L[i]) or re.match(r'\\chapter\{(.*)\}', L[i])
    titulo = m.group(1)
    caps.append((num, titulo, i, min(fin, i_app if i < i_app else fin)))

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

DEST.mkdir(exist_ok=True)
indice = []
for num, titulo, i0, i1 in caps:
    bloque = L[i0:i1]
    try:
        j = next(k for k, l in enumerate(bloque) if l.startswith('\\section*{Ejercicios}'))
    except StopIteration:
        continue
    cuerpo = bloque[j + 1:]
    while cuerpo and cuerpo[-1].strip() == '':
        cuerpo.pop()
    texto = '\n'.join(cuerpo)
    # el Apéndice E (cuadernos) no tiene ejercicios; los demás sí
    locales = set(re.findall(r'\\label\{([^}]*)\}', texto))
    def fix(m):
        cmd, lab = m.group(1), m.group(2)
        return m.group(0) if lab in locales else '\\%s{N-%s}' % (cmd, lab)
    texto = re.sub(r'\\(ref|eqref|pageref)\{([^}]*)\}', fix, texto)
    # dentro de una guía "Ejercicio~\ref{...}" local ya da el número correcto
    es_ap = not num.isdigit()
    nombre = ('apendice-%s' % num) if es_ap else ('practica-%02d' % int(num))
    encabezado_num = ('Apéndice %s' % num) if es_ap else ('Práctica %s' % num)
    partes = [PREAMBULO, '', '\\begin{document}',
              '\\renewcommand{\\thechapter}{%s}' % num,
              '\\encabezado{%s: %s}' % (encabezado_num, titulo),
              '\\bigskip',
              '\\pagestyle{fancy}',
              '\\fancyhead[L]{{\\footnotesize{\\usefont{T1}{phv}{m}{n}{\\sc Teoría de Transporte Óptimo}}}}',
              '\\fancyhead[R]{\\footnotesize \\usefont{T1}{phv}{m}{n}{\\sc %s}}' % encabezado_num,
              '\\thispagestyle{plain}',
              '\\noindent{\\footnotesize Los ejercicios son los de la sección de ejercicios del %s de las notas del curso, con la misma numeración; las referencias a teoremas, proposiciones y secciones remiten a las notas (\\url{%s}).}' % (
                  ('Apéndice~%s' % num) if es_ap else ('Capítulo~%s' % num), REPO),
              '\\medskip', '']
    if not es_ap and int(num) in CUADERNOS:
        nom, arch = CUADERNOS[int(num)]
        partes.append('\\cuadernolink{%s}{%s}' % (nom, arch))
        partes.append('')
    partes.append(texto)
    if re.search(r'\\cite[\[{]', texto):
        partes += ['', '\\bibliographystyle{plain}', '\\bibliography{../notas/biblio}']
    partes += ['', '\\end{document}', '']
    (DEST / (nombre + '.tex')).write_text('\n'.join(partes), encoding='utf-8')
    indice.append((nombre, encabezado_num, titulo, len(re.findall(r'\\begin\{ejercicio\}', texto))))
    print(nombre, '->', indice[-1][3], 'ejercicios')

# ---------------------------------------------------------------- índice
with open(DEST / 'INDICE.md', 'w', encoding='utf-8') as f:
    f.write('# Guías de ejercicios\n\nGeneradas automáticamente desde `notas/Notas-TO.tex` con `herramientas/generar_practicas.py`. No editar los `.tex` a mano: los cambios van en las notas.\n\n')
    f.write('| Archivo | Guía | Tema | Ejercicios |\n|---|---|---|---|\n')
    for nombre, enc, tit, n in indice:
        f.write('| `%s.pdf` | %s | %s | %d |\n' % (nombre, enc, tit.replace('\\texorpdfstring{$c$}{c}', 'c'), n))
