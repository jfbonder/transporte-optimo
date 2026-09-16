# Teoría de Transporte Óptimo

Material del curso *Teoría de Transporte Óptimo* (FCEN–UBA, 2do cuatrimestre 2026), de Julián Fernández Bonder: notas de clase, guías de ejercicios y cuadernos de cómputo.

**Sitio del curso:** <https://jfbonder.github.io/transporte-optimo/>

## Contenido

| Carpeta | Qué hay |
|---|---|
| [`notas/`](notas/) | Las notas completas: [`Notas-TO.pdf`](notas/Notas-TO.pdf) y su fuente LaTeX (`Notas-TO.tex`, `biblio.bib`). |
| [`practicas/`](practicas/) | Una guía de ejercicios por capítulo (`practica-NN.pdf`) y por apéndice (`apendice-X.pdf`). Se generan automáticamente a partir de las secciones de ejercicios de las notas, con la misma numeración. Ver [`practicas/INDICE.md`](practicas/INDICE.md). |
| [`cuadernos/`](cuadernos/) | Seis cuadernos de Python (Jupyter) que acompañan las notas, con la biblioteca [POT](https://pythonot.github.io/). Cada uno termina con los ejercicios computacionales del capítulo correspondiente. |
| [`herramientas/`](herramientas/) | Los scripts que generan las guías y el sitio. |

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

Para ejecutarlos localmente: `pip install pot numpy scipy matplotlib jupyter`.

## Cómo se construye el material

La fuente única es `notas/Notas-TO.tex`. Las guías y el sitio se derivan de ella:

```
make notas       # compila las notas (latexmk)
make practicas   # regenera practicas/*.tex desde las notas y las compila
make sitio       # regenera index.html a partir del índice de las notas
make             # todo lo anterior
```

Requisitos: una distribución TeX Live completa (con `babel-spanish`, `amsart`, `xr-hyper`, `enumitem`, `mathtools`, `tikz`) y Python 3. Las guías toman la numeración de teoremas y ejercicios del archivo `notas/Notas-TO.aux`, de modo que hay que compilar las notas antes que las guías (el `Makefile` lo hace en el orden correcto).

Los archivos `practicas/*.tex` **no se editan a mano**: cualquier cambio en un ejercicio va en las notas y se regenera.

## Correcciones y sugerencias

Abrir un *issue* o un *pull request*, o escribir a <jfbonder@dm.uba.ar>.

## Licencia

[CC BY-NC-SA 4.0](LICENSE.md). Se puede copiar, redistribuir y adaptar el material con atribución, sin fines comerciales y bajo la misma licencia.
