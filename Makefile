# Teoría de Transporte Óptimo — construcción del material
#
#   make            notas + guías + sitio + sincronización de los cuadernos
#   make notas      compila notas/Notas-TO.pdf
#   make practicas  regenera y compila las guías y sugerencias.pdf (compila antes las notas si hace falta)
#   make sitio      regenera index.html (compila antes las notas si hace falta)
#   make sincronizar  actualiza en los cuadernos los ejercicios computacionales y los números de las citas a las notas
#   make cuadernos  ejecuta los seis cuadernos y guarda sus salidas (requiere jupyter y pot)
#   make limpiar    borra los auxiliares de LaTeX
#
# Los PDF son reproducibles: la fecha que se graba en ellos es la del último
# commit (o la que se fije en SOURCE_DATE_EPOCH), no la de la compilación.

SHELL := /bin/bash
LATEXMK = latexmk -pdf -interaction=nonstopmode -quiet

SOURCE_DATE_EPOCH ?= $(shell git log -1 --format=%ct 2>/dev/null || date +%s)
export SOURCE_DATE_EPOCH
export FORCE_SOURCE_DATE = 1

FIGURAS = $(wildcard notas/*.jpg notas/*.jpeg notas/*.png)

.PHONY: todo notas practicas sitio sincronizar cuadernos limpiar aux

todo: notas practicas sitio sincronizar

notas: notas/Notas-TO.pdf

notas/Notas-TO.pdf: notas/Notas-TO.tex notas/biblio.bib $(FIGURAS)
	cd notas && $(LATEXMK) Notas-TO.tex

# las guías leen notas/Notas-TO.aux y el sitio notas/Notas-TO.toc, que
# 'make limpiar' borra aunque el PDF siga al día: en ese caso se recompila
aux: notas/Notas-TO.pdf
	@test -f notas/Notas-TO.aux -a -f notas/Notas-TO.toc || (cd notas && $(LATEXMK) -g Notas-TO.tex)

practicas: aux
	python3 herramientas/generar_practicas.py
	python3 herramientas/generar_sugerencias.py
	cd practicas && for f in practica-*.tex apendice-*.tex sugerencias.tex; do $(LATEXMK) $$f || exit 1; done

sitio: aux
	python3 herramientas/generar_sitio.py

sincronizar: aux
	python3 herramientas/sincronizar_cuadernos.py

cuadernos:
	for f in cuadernos/*.ipynb; do \
	  jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=1200 "$$f" || exit 1; \
	done

limpiar:
	cd notas && latexmk -c -quiet; rm -f *.bbl *.run.xml
	cd practicas && latexmk -c -quiet; rm -f *.bbl
