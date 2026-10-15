#!/usr/bin/env python3
"""Genera las guías de ejercicios (practicas/*.tex) y practicas/INDICE.md a
partir de las notas.

Cada capítulo y apéndice de notas/Notas-TO.tex termina con una sección
\\section*{Ejercicios}. Este script extrae esas secciones, les antepone el
preámbulo de las notas (adaptado a amsart) y produce un archivo .tex por
guía, con la misma numeración de ejercicios que las notas. Las referencias
a resultados de las notas se resuelven con el paquete xr-hyper leyendo
notas/Notas-TO.aux, de modo que hay que compilar primero las notas.

Uso:  python3 herramientas/generar_practicas.py
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from comun import (L, PREAMBULO, RAIZ, REPO, capitulos,  # noqa: E402
                   cuaderno_con_ejercicios, encabezado_fancy, titulo_texto)

DEST = RAIZ / 'practicas'
NOTA_ESTRELLA = '($\\bigstar$) ejercicio de mayor dificultad o que excede el programa.'


def resolver_referencias(texto):
    """Antepone N- a las referencias a etiquetas que no están en la guía misma,
    para que xr-hyper las tome de las notas."""
    locales = set(re.findall(r'\\label\{([^}]*)\}', texto))

    def fix(m):
        cmd, lab = m.group(1), m.group(2)
        return m.group(0) if lab in locales else '\\%s{N-%s}' % (cmd, lab)
    return re.sub(r'\\(ref|eqref|pageref)\{([^}]*)\}', fix, texto)


def main():
    DEST.mkdir(exist_ok=True)
    indice = []
    for num, titulo, i0, i1 in capitulos():
        bloque = L[i0:i1]
        j = next((k for k, l in enumerate(bloque) if l.startswith('\\section*{Ejercicios}')), None)
        if j is None:          # el Apéndice E (cuadernos) no tiene ejercicios
            continue
        cuerpo = bloque[j + 1:]
        while cuerpo and cuerpo[-1].strip() == '':
            cuerpo.pop()
        texto = resolver_referencias('\n'.join(cuerpo))
        es_ap = not num.isdigit()
        nombre = ('apendice-%s' % num) if es_ap else ('practica-%02d' % int(num))
        encabezado_num = ('Apéndice %s' % num) if es_ap else ('Práctica %s' % num)
        nota = ('Los ejercicios son los de la sección de ejercicios del %s de las notas del curso, '
                'con la misma numeración; las referencias a teoremas, proposiciones y secciones '
                'remiten a las notas (\\url{%s}).' % (('Apéndice~%s' % num) if es_ap else ('Capítulo~%s' % num), REPO))
        if '\\bigstar' in texto:
            nota += ' ' + NOTA_ESTRELLA
        partes = [PREAMBULO, '', '\\begin{document}',
                  '\\renewcommand{\\thechapter}{%s}' % num]
        partes += encabezado_fancy('%s: %s' % (encabezado_num, titulo), encabezado_num)
        partes += ['\\noindent{\\footnotesize %s}' % nota, '\\medskip', '']
        cuaderno = None if es_ap else cuaderno_con_ejercicios(num)
        if cuaderno:
            partes += ['\\cuadernolink{%s}{%s}' % (cuaderno[1], cuaderno[0]), '']
        partes.append(texto)
        if re.search(r'\\cite[a-z]*[\[{]', texto):
            partes += ['', '\\bibliographystyle{plain}', '\\bibliography{../notas/biblio}']
        partes += ['', '\\end{document}', '']
        (DEST / (nombre + '.tex')).write_text('\n'.join(partes), encoding='utf-8')
        n_ej = len(re.findall(r'\\begin\{ejercicio\}', texto))
        indice.append((nombre, encabezado_num, titulo_texto(titulo), n_ej))
        print(nombre, '->', n_ej, 'ejercicios')

    with open(DEST / 'INDICE.md', 'w', encoding='utf-8') as f:
        f.write('# Guías de ejercicios\n\nGeneradas automáticamente desde `notas/Notas-TO.tex` con '
                '`herramientas/generar_practicas.py`. No editar los `.tex` a mano: los cambios van en las notas. '
                'Los ejercicios marcados con (★) son de mayor dificultad o exceden el programa.\n\n')
        f.write('| Archivo | Guía | Tema | Ejercicios |\n|---|---|---|---|\n')
        for nombre, enc, tit, n in indice:
            f.write('| `%s.pdf` | %s | %s | %d |\n' % (nombre, enc, tit, n))


if __name__ == '__main__':
    main()
