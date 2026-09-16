#!/usr/bin/env python3
"""Genera practicas/sugerencias.tex: un único documento con las sugerencias de
los ejercicios, ordenadas por capítulo y con la numeración de las notas.

Las sugerencias se escriben en practicas/sugerencias-fuente.tex, una entrada
\\sug{etiqueta}{texto} por ejercicio (la etiqueta es la del \\label del ejercicio en
las notas). La numeración y el orden se toman de notas/Notas-TO.tex.

Uso:  python3 herramientas/generar_sugerencias.py   (después de compilar las notas)
"""
import re, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from comun import src, L, PREAMBULO, RAIZ, REPO, encabezado_fancy  # noqa: E402

DEST = RAIZ / 'practicas' / 'sugerencias.tex'
FUENTE = RAIZ / 'practicas' / 'sugerencias-fuente.tex'

i_app = next(i for i, l in enumerate(L) if l.startswith('\\appendix'))
caps = []  # (num, titulo, linea)
n_cap = 0; n_app = 0
for i, l in enumerate(L):
    if l.startswith('\\chapter'):
        if i < i_app:
            n_cap += 1; num = str(n_cap)
        else:
            num = chr(ord('A') + n_app); n_app += 1
        m = re.match(r'\\chapter\{(.*?)\}(\\label|$)', l)
        caps.append((num, m.group(1), i))

def cap_de(linea):
    c = None
    for num, tit, i in caps:
        if i <= linea:
            c = (num, tit)
    return c

# leer la fuente: \sug{etiqueta}{texto} con llaves balanceadas
fuente = FUENTE.read_text(encoding='utf-8')
fuente = re.sub(r'(?m)^%.*$', '', fuente)          # comentarios de línea completa
S = {}
pos = 0
while True:
    k = fuente.find('\\sug{', pos)
    if k < 0:
        break
    j = k + 5
    lab = fuente[j:fuente.index('}', j)]
    j = fuente.index('}', j) + 1
    assert fuente[j] == '{', 'falta el segundo argumento en ' + lab
    prof = 1; j += 1; ini = j
    while prof:
        if fuente[j] == '{': prof += 1
        elif fuente[j] == '}': prof -= 1
        j += 1
    if lab in S:
        sys.exit('etiqueta repetida en la fuente: ' + lab)
    S[lab] = fuente[ini:j - 1].strip()
    pos = j

# ejercicios de las notas, en orden
pat = re.compile(r'\\begin\{ejercicio\}(?:\[(.*?)\])?\\label\{([^}]*)\}', re.S)
por_cap = {}
cnt = {}
total = 0
vistos = set()
for m in pat.finditer(src):
    linea = src[:m.start()].count('\n')
    num, tit = cap_de(linea)
    cnt[num] = cnt.get(num, 0) + 1
    lab = m.group(2)
    vistos.add(lab)
    if lab not in S:
        continue
    titulo_ej = (m.group(1) or '').replace('$\\bigstar$ ', '').replace('$\\bigstar$', '')
    titulo_ej = re.sub(r'\\(ref|eqref|pageref)\{([^}]*)\}', r'\\\1{N-\2}', titulo_ej)
    sug = re.sub(r'\\(ref|eqref|pageref)\{([^}]*)\}', r'\\\1{N-\2}', S[lab])
    por_cap.setdefault(num, (tit, []))[1].append((cnt[num], titulo_ej, sug))
    total += 1
huerfanas = [k for k in S if k not in vistos]
if huerfanas:
    sys.exit('sugerencias sin ejercicio en las notas: ' + ', '.join(huerfanas))

partes = [PREAMBULO, '',
          '\\newcommand{\\ejlabel}[2]{\\par\\medskip\\noindent\\textbf{Ejercicio #1}\\ifx\\relax#2\\relax\\else\\ (#2)\\fi\\textbf{.}\\ }',
          '\\begin{document}']
partes += encabezado_fancy('Sugerencias para los ejercicios', 'Sugerencias')
partes += ['\\noindent{\\footnotesize La numeración es la de las notas y de las guías (Ejercicio $n.k$ = ejercicio $k$ del Capítulo $n$); las referencias remiten a las notas (\\url{%s}). Las sugerencias indican una idea o el resultado que conviene usar, no una solución completa. Sólo figuran los ejercicios que tienen sugerencia.}' % REPO,
          '\\bigskip']
for num, tit, _ in caps:
    if num not in por_cap:
        continue
    tit_limpio = tit.replace('\\texorpdfstring{$c$}{c}', '$c$')
    etiqueta = ('Apéndice %s' % num) if not num.isdigit() else ('Capítulo %s' % num)
    partes.append('\\section*{%s. %s}' % (etiqueta, tit_limpio))
    for k, titulo_ej, sug in por_cap[num][1]:
        partes.append('\\ejlabel{%s.%d}{%s}%s' % (num, k, titulo_ej, sug))
        partes.append('')
if '\\cite' in '\n'.join(partes):
    partes += ['\\bibliographystyle{plain}', '\\bibliography{../notas/biblio}']
partes += ['\\end{document}', '']
DEST.write_text('\n'.join(partes), encoding='utf-8')
print('sugerencias.tex: %d sugerencias en %d capítulos; ejercicios sin sugerencia: %d' % (total, len(por_cap), len(vistos) - total))
