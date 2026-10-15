# Teoría de Transporte Óptimo

Material del curso *Teoría de Transporte Óptimo* (FCEN–UBA, segundo cuatrimestre 2026), de Julián Fernández Bonder: notas de clase, guías de ejercicios y cuadernos de cómputo.

**Sitio del curso:** <https://jfbonder.github.io/transporte-optimo/>

## Contenido

| Carpeta | Qué hay |
|---|---|
| [`notas/`](notas/) | Las notas completas: [`Notas-TO.pdf`](notas/Notas-TO.pdf) y su fuente LaTeX (`Notas-TO.tex`, `biblio.bib`). |
| [`practicas/`](practicas/) | Una guía de ejercicios por capítulo (`practica-NN.pdf`) y por apéndice (`apendice-X.pdf`). Se generan automáticamente a partir de las secciones de ejercicios de las notas, con la misma numeración. Ver [`practicas/INDICE.md`](practicas/INDICE.md). Además, [`sugerencias.pdf`](practicas/sugerencias.pdf) reúne sugerencias para los ejercicios de todos los capítulos. |
| [`cuadernos/`](cuadernos/) | Seis cuadernos de Python (Jupyter) que acompañan las notas, con la biblioteca [POT](https://pythonot.github.io/). Cada uno termina con los ejercicios computacionales del capítulo correspondiente. |
| [`herramientas/`](herramientas/) | Los scripts que generan las guías, las sugerencias y el sitio (`comun.py` contiene el código compartido y la tabla capítulo–cuaderno). |

## Cuadernos

Cada cuaderno se abre directamente en Google Colab (no requiere instalar nada; hace falta una cuenta de Google para ejecutarlo).

| Cuaderno | Capítulos | Colab |
|---|---|---|
| Monge y Kantorovich | 1–2 | [abrir](https://colab.research.google.com/github/jfbonder/transporte-optimo/blob/main/cuadernos/01-monge-kantorovich.ipynb) |
| Dualidad | 3–6 | [abrir](https://colab.research.google.com/github/jfbonder/transporte-optimo/blob/main/cuadernos/02-dualidad.ipynb) |
| OT en dimensión uno | 8 | [abrir](https://colab.research.google.com/github/jfbonder/transporte-optimo/blob/main/cuadernos/03-ot-dimension-uno.ipynb) |
| Distancias de Wasserstein | 10 | [abrir](https://colab.research.google.com/github/jfbonder/transporte-optimo/blob/main/cuadernos/04-distancias-wasserstein.ipynb) |
| Baricentros de Wasserstein | 12 | [abrir](https://colab.research.google.com/github/jfbonder/transporte-optimo/blob/main/cuadernos/05-baricentros-wasserstein.ipynb) |
| Transporte entrópico y Sinkhorn | 13 | [abrir](https://colab.research.google.com/github/jfbonder/transporte-optimo/blob/main/cuadernos/06-transporte-entropico-sinkhorn.ipynb) |

Para ejecutarlos localmente: `pip install pot numpy scipy matplotlib jupyter` (la primera celda de código de cada cuaderno instala POT con `%pip`). Requieren NumPy 2.0 o posterior (usan `np.trapezoid`); se probaron con Python 3.13, NumPy 2.5, SciPy 1.18, Matplotlib 3.11 y POT 0.9.7.

Los cuadernos se versionan **con sus salidas**, ejecutados de principio a fin; `make cuadernos` los vuelve a ejecutar y guarda las salidas nuevas. Todo es determinista (semillas fijas). Tiempos aproximados en una CPU de dos núcleos, incluida la instalación de POT: entre 10 y 25 s cada uno, salvo *Transporte entrópico y Sinkhorn*, que tarda alrededor de un minuto.

## Cómo se construye el material

La fuente única es `notas/Notas-TO.tex`. Las guías, el sitio y la sección final de ejercicios computacionales de cada cuaderno se derivan de ella:

```
make notas       # compila las notas (latexmk)
make practicas   # regenera practicas/*.tex y sugerencias.tex desde las notas y los compila
make sitio       # regenera index.html a partir del índice de las notas
make sincronizar # actualiza en los cuadernos los ejercicios computacionales y los números de las citas
make             # todo lo anterior
make cuadernos   # ejecuta los seis cuadernos y guarda sus salidas
make limpiar     # borra los auxiliares de LaTeX
```

Requisitos:

- Una distribución TeX Live con `latexmk`, `bibtex` y los paquetes `amsbook`/`amsart`, `babel-spanish`, `hyperref` y `xr-hyper`, `enumitem`, `mathtools`, `listings`, `tikz`, `fancyhdr` y `geometry`, y las fuentes Type 1 `cm-super` (sin ellas `[T1]{fontenc}` produce fuentes de mapa de bits). En Debian/Ubuntu: `texlive-latex-extra texlive-lang-spanish texlive-pictures cm-super latexmk`.
- Python 3 (los generadores usan solo la biblioteca estándar) y `pdfinfo` (paquete `poppler-utils`), con el que el sitio cuenta las páginas de las notas.

Las guías toman la numeración de teoremas y ejercicios del archivo `notas/Notas-TO.aux`, de modo que hay que compilar las notas antes que las guías (el `Makefile` lo hace en el orden correcto, y recompila las notas si faltan los auxiliares). Los PDF son reproducibles: el `Makefile` fija `SOURCE_DATE_EPOCH` en la fecha del último commit, de modo que dos compilaciones de la misma fuente dan archivos idénticos.

En los cuadernos, las citas a las notas se escriben seguidas de un comentario invisible con la etiqueta, por ejemplo `Teorema 8.4.1<!--ref:teo:optimalidad-->`, y `make sincronizar` actualiza el número si la numeración de las notas cambia; la celda «Ejercicios computacionales» se regenera entera desde las notas y no debe editarse a mano.

Los archivos `practicas/*.tex` **no se editan a mano**: cualquier cambio en un ejercicio va en las notas y se regenera. La excepción es `practicas/sugerencias-fuente.tex`, que sí se edita: contiene una entrada `\sug{etiqueta}{texto}` por ejercicio (la etiqueta es la del `\label` del ejercicio en las notas) y es la fuente de `sugerencias.pdf`.

## Correcciones y sugerencias

Abrir un *issue* o un *pull request*, o escribir a <jfbonder@dm.uba.ar>.

## Licencia

[CC BY-NC-SA 4.0](LICENSE.md). Se puede copiar, redistribuir y adaptar el material con atribución, sin fines comerciales y bajo la misma licencia.
