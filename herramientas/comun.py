# -*- coding: utf-8 -*-
"""Código común a los generadores: rutas y preámbulo de las guías (amsart con el
encabezado del curso), construido a partir del preámbulo de las notas."""
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
TEX = RAIZ / 'notas' / 'Notas-TO.tex'
REPO = 'https://github.com/jfbonder/transporte-optimo'
SITIO = 'https://jfbonder.github.io/transporte-optimo/'
COLAB = 'https://colab.research.google.com/github/jfbonder/transporte-optimo/blob/main/cuadernos/'

src = TEX.read_text(encoding='utf-8')
L = src.split('\n')

# ---------------------------------------------------------------- preámbulo
i_doc = next(i for i, l in enumerate(L) if l.startswith('\\begin{document}'))
pre = L[:i_doc]
pre_out = []
for l in pre:
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
            # encabezado con logos, en el formato de las guias del curso
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
