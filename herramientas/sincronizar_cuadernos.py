#!/usr/bin/env python3
"""Sincroniza los cuadernos con las notas.

1. Ejercicios computacionales. La última sección de cada cuaderno
   («## Ejercicios computacionales») se regenera a partir de la subsección
   \\subsection*{Ejercicios computacionales} del capítulo correspondiente de
   notas/Notas-TO.tex (la tabla de comun.CUADERNOS dice cuál), con la
   numeración de las notas. Así los enunciados del cuaderno y de las notas
   (y de las guías) no pueden divergir: el .tex manda.

2. Referencias numeradas. En las celdas de texto, una cita a las notas se
   escribe seguida de un comentario HTML con la etiqueta LaTeX, por ejemplo
   «Teorema 8.4.1<!--ref:teo:optimalidad-->». El comentario no se ve al
   renderizar el cuaderno; el script reemplaza el número que lo precede por
   el que figura hoy en notas/Notas-TO.aux.

Solo cambia celdas de texto: las salidas de las celdas de código no se tocan.
Hay que compilar antes las notas (necesita notas/Notas-TO.aux).

Uso:  python3 herramientas/sincronizar_cuadernos.py [--verificar]
      (--verificar no escribe nada y termina con error si algo está desactualizado)
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from comun import CUADERNOS, L, RAIZ, capitulos  # noqa: E402

AUX = RAIZ / 'notas' / 'Notas-TO.aux'
ENCABEZADO = '## Ejercicios computacionales'
MARCA = re.compile(r'(\d+(?:\.\d+)*|[A-Z](?:\.\d+)*)<!--ref:([^>]*?)-->')


def leer_aux():
    if not AUX.exists():
        sys.exit('falta %s: compilar antes las notas (make notas)' % AUX.relative_to(RAIZ))
    etiquetas = {}
    for m in re.finditer(r'\\newlabel\{([^}]*)\}\{\{([^}]*)\}', AUX.read_text(encoding='utf-8')):
        etiquetas[m.group(1)] = m.group(2)
    return etiquetas


# ------------------------------------------------------------ LaTeX -> Markdown
MACROS_MATEMATICAS = [(r'\ve', r'\varepsilon'), (r'\R', r'{\mathbb R}'), (r'\LL', r'\mathcal L'),
                      (r'\id', r'\mathrm{id}')]

# Comandos que MathJax entiende y que efectivamente aparecen hoy en los enunciados
# computacionales. Sirve de red: si alguien usa en las notas una macro propia nueva,
# el script avisa en vez de dejarla pasar y que el cuaderno la muestre en crudo.
MATHJAX_CONOCIDAS = {
    r'\mathbb', r'\mathcal', r'\mathrm', r'\varepsilon', r'\mu', r'\nu', r'\pi',
    r'\lambda', r'\sigma', r'\Sigma', r'\varphi', r'\psi', r'\delta', r'\gamma',
    r'\alpha', r'\beta', r'\theta', r'\tau', r'\Pi', r'\int', r'\sum', r'\min',
    r'\max', r'\inf', r'\sup', r'\log', r'\exp', r'\sqrt', r'\frac', r'\tfrac',
    r'\dfrac', r'\le', r'\leq', r'\ge', r'\geq', r'\ne', r'\neq', r'\to',
    r'\mapsto', r'\times', r'\cdot', r'\pm', r'\cup', r'\cap', r'\subset',
    r'\in', r'\notin', r'\bigl', r'\bigr', r'\Bigl', r'\Bigr', r'\left',
    r'\right', r'\bigstar', r'\dots', r'\ldots', r'\cdots', r'\quad', r'\qquad',
    r'\text', r'\textrm', r'\emph', r'\bar', r'\tilde', r'\widetilde', r'\hat',
    r'\partial', r'\nabla', r'\infty', r'\ll', r'\approx', r'\sim', r'\circ',
    r'\langle', r'\rangle', r'\lfloor', r'\rfloor', r'\lceil', r'\rceil',
    r'\begin', r'\end', r'\\', r'\mathbf', r'\phi', r'\bmod', r'\varphi', r'\rho',
    r'\omega', r'\Omega', r'\zeta', r'\chi', r'\xi', r'\eta', r'\det', r'\lim',
    r'\liminf', r'\limsup', r'\operatorname', r'\colon', r'\ldots',
}


def a_markdown(tex, ref):
    """Convierte el texto de un enunciado (LaTeX de las notas) a Markdown de Jupyter."""
    s = re.sub(r'\\label\{[^}]*\}', '', tex)
    s = re.sub(r'(?m)%.*$', '', s)
    s = re.sub(r'\\(?:ref|eqref)\{([^}]*)\}', lambda m: ref(m.group(1)), s)
    # Nota: estas dos sustituciones no admiten llaves anidadas (\emph{\texttt{x}} se
    # rompería). Hoy no aparece en ninguna subsección computacional; si llegara a
    # aparecer, hay que pasar a un parseo con llaves balanceadas.
    s = re.sub(r'\\emph\{([^{}]*)\}', r'*\1*', s)
    s = re.sub(r'\\texttt\{([^{}]*)\}', r'`\1`', s)
    s = re.sub(r'\s*\n\s*', ' ', s)                       # un solo párrafo
    s = s.replace('\\ ', ' ')                                 # cf.\ , etc.
    s = re.sub(r'\\\[(.*?)\\\]', lambda m: '$$' + m.group(1).strip() + '$$', s)

    def mat(t):                                               # macros propias de las notas
        for macro, reemplazo in MACROS_MATEMATICAS:
            t = re.sub(re.escape(macro) + r'(?![A-Za-z])', lambda _, r=reemplazo: r, t)
        desconocidas = set(re.findall(r'\\[A-Za-z]+', t)) - MATHJAX_CONOCIDAS
        if desconocidas:
            print('aviso: macros que MathJax podría no conocer en un enunciado: %s'
                  % ', '.join(sorted(desconocidas)), file=sys.stderr)
        return t
    partes = re.split(r'(\$\$.*?\$\$|\$[^$]*\$)', s)
    for k in range(len(partes)):
        if k % 2:
            partes[k] = mat(partes[k])
        else:                                                 # texto: ~ y -- tipográficos
            partes[k] = partes[k].replace('~', ' ').replace('---', '—').replace('--', '–')
    s = ''.join(partes)
    return re.sub(r'  +', ' ', s).strip()


def ejercicios_computacionales(cap, ref):
    """Celda Markdown con los ejercicios computacionales del capítulo `cap`."""
    num, titulo, i0, i1 = next(c for c in capitulos() if c[0] == cap)
    bloque = '\n'.join(L[i0:i1])
    k = bloque.find('\\subsection*{Ejercicios computacionales}')
    if k < 0:
        sys.exit('el Capítulo %s no tiene ejercicios computacionales' % cap)
    bloque = bloque[k:]
    items = []
    for m in re.finditer(r'\\begin\{ejercicio\}(?:\[(.*?)\])?\\label\{([^}]*)\}(.*?)\\end\{ejercicio\}',
                         bloque, flags=re.S):
        tit = a_markdown(m.group(1) or '', ref)
        items.append('**Ejercicio %s (%s).** %s' % (ref(m.group(2)), tit, a_markdown(m.group(3), ref)))
    if not items:
        sys.exit('no encontré ejercicios computacionales en el Capítulo %s' % cap)
    tit = titulo.replace('\\texorpdfstring{$c$}{c}', '$c$').replace('--', '–')
    intro = ('Los enunciados siguientes son los de la subsección «Ejercicios computacionales» del '
             'Capítulo %s de las notas (*%s*), con la misma numeración; las referencias a secciones '
             'son a las de este cuaderno.' % (num, tit))
    return '\n\n'.join([ENCABEZADO, intro] + items) + '\n'


def lineas(texto):
    """Texto -> lista de líneas en el formato de nbformat."""
    ls = texto.split('\n')
    return [l + '\n' for l in ls[:-1]] + ([ls[-1]] if ls[-1] else [])


def main():
    verificar = '--verificar' in sys.argv
    etq = leer_aux()

    def ref(lab):
        if lab not in etq:
            sys.exit('etiqueta inexistente en las notas: ' + lab)
        return etq[lab]

    pendientes = []
    for arch, _, _, cap, _ in CUADERNOS:
        ruta = RAIZ / 'cuadernos' / arch
        nb = json.loads(ruta.read_text(encoding='utf-8'))
        original = json.dumps(nb, ensure_ascii=False)
        celdas_ej = [c for c in nb['cells']
                     if c['cell_type'] == 'markdown' and ''.join(c['source']).lstrip().startswith(ENCABEZADO)]
        if len(celdas_ej) != 1:
            sys.exit('%s: debe haber exactamente una celda que empiece con «%s»' % (arch, ENCABEZADO))
        celdas_ej[0]['source'] = lineas(ejercicios_computacionales(cap, ref))
        for c in nb['cells']:
            if c['cell_type'] != 'markdown':
                continue
            texto = ''.join(c['source'])
            nuevo = MARCA.sub(lambda m: ref(m.group(2)) + '<!--ref:%s-->' % m.group(2), texto)
            if nuevo != texto:
                c['source'] = lineas(nuevo)
        # Reescribimos el JSON a mano, con indent=1, que es el formato de nbformat. No
        # usamos nbformat.read/write para no agregar una dependencia; la contrapartida es
        # que no se preservaría el campo `id` de nbformat 4.5 si Jupyter llegara a
        # agregarlo (hoy no está en ninguno de los seis cuadernos).
        if json.dumps(nb, ensure_ascii=False) != original:
            pendientes.append(arch)
            if not verificar:
                ruta.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    if verificar and pendientes:
        sys.exit('cuadernos desactualizados respecto de las notas: ' + ', '.join(pendientes))
    print('cuadernos sincronizados con las notas;', ('actualizados: ' + ', '.join(pendientes)) if pendientes else 'sin cambios')


if __name__ == '__main__':
    main()
