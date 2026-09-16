# Teoría de Transporte Óptimo — construcción del material
#
#   make            notas + guías + sitio
#   make notas      compila notas/Notas-TO.pdf
#   make practicas  regenera y compila las guías (requiere las notas compiladas)
#   make sitio      regenera index.html
#   make cuadernos  ejecuta los seis cuadernos (requiere jupyter y pot)
#   make limpiar    borra los auxiliares de LaTeX

LATEXMK = latexmk -pdf -interaction=nonstopmode -quiet
PRACTICAS = $(patsubst %.tex,%.pdf,$(wildcard practicas/*.tex))

.PHONY: todo notas practicas sitio cuadernos limpiar

todo: notas practicas sitio

notas: notas/Notas-TO.pdf

notas/Notas-TO.pdf: notas/Notas-TO.tex notas/biblio.bib
	cd notas && $(LATEXMK) Notas-TO.tex

practicas: notas/Notas-TO.pdf
	@test -f notas/Notas-TO.aux || (cd notas && $(LATEXMK) Notas-TO.tex)
	python3 herramientas/generar_practicas.py
	cd practicas && for f in *.tex; do $(LATEXMK) $$f; done

sitio: notas/Notas-TO.pdf
	python3 herramientas/generar_sitio.py

cuadernos:
	for f in cuadernos/*.ipynb; do jupyter nbconvert --to notebook --execute --inplace "$$f"; done

limpiar:
	cd notas && latexmk -c -quiet; rm -f *.bbl *.run.xml
	cd practicas && latexmk -c -quiet; rm -f *.bbl
