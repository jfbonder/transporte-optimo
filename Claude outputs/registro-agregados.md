# Registro de cambios: agregados de «dat» (15/10/2026)

Implementa los ítems marcados «ya» en la recomendación v2 de dat. No hay commit. Al final se corrió `make`: compila sin errores, sin referencias ni citas indefinidas, sin cajas overfull en las notas ni en las guías (la línea de base también tenía 0; apareció una nueva en el Ej. 10.12(d) y se corrigió pasando la desigualdad a display), y BibTeX da 0 advertencias. Las notas pasan de 200 a 204 páginas.

## Numeración

- **Ejercicios teóricos existentes: sin cambios.** Se verificó comparando contra `git show HEAD:notas/Notas-TO.tex` (script en el scratchpad): ningún ejercicio teórico cambió de número.
- **Ejercicios computacionales que se corrieron** (aceptable; los cuadernos se resincronizaron con `make`): cap. 10, `ejc.Wp.escala`…`ejc.Wp.KR` pasan de 10.12–10.16 a 10.13–10.17; cap. 13, `ejc.eps.valores`…`ejc.eps.unicidad` pasan de 13.8–13.12 a 13.10–13.14.
- **Teoremas, proposiciones y observaciones:** todos los entornos nuevos están al final de su sección, así que no se corrió ningún número existente.

## Ejercicios nuevos

| Número | Label | Tipo | Capítulo |
|---|---|---|---|
| 10.12 | `ejer.Wp.empirica.1D` | teórico (al final de los teóricos) | 10 |
| 10.18 | `ejc.Wp.muestras` | computacional (al final de los computacionales) | 10 |
| 13.8 | `ejer.OTeps.derivadas` | teórico (al final de los teóricos) | 13 |
| 13.9 | `ejer.sinkhorn.sesgo` | teórico (al final de los teóricos) | 13 |

Los cuatro tienen su entrada `\sug{...}` en `practicas/sugerencias-fuente.tex`, ubicada después de la del ejercicio anterior en las notas (`ejer.Wp.lineal`, `ejc.Wp.KR` y `ejer.bar.entropico`).

## Cambios por archivo

### `notas/Notas-TO.tex`

**Cap. 7, Sec. 7.3 (emparejamientos y precios)**
- Se agregó la hipótesis de *utilidad transferible* al definir el matching óptimo.
- Al final del párrafo de matching estable: la equivalencia vale en el modelo con utilidad transferible, y en el caso discreto es el juego de asignación de Shapley–Shubik (núcleo = soluciones del dual de la asignación) `\cite{ShapleyShubik1971}`.
- Párrafo nuevo de contraste con Gale–Shapley `\cite{GaleShapley1962}`: sin pagos, con preferencias ordinales, existencia de un matching estable por un algoritmo de propuestas, y un problema de naturaleza combinatoria.
- En el párrafo de precios de equilibrio: la correspondencia en el caso discreto también está en `\cite{ShapleyShubik1971}`.
- No se citó a Galichon 2016: no se pudo verificar el capítulo (ver abajo).

**Cap. 7, Sec. 7.5**
- Se agregó `\label{sec.discretizacion}` (no cambia la numeración).
- Remisión entre paréntesis al Corolario `cor.Wp.empirica`.

**Cap. 9, Obs. `obs.gaussianas.generales`**
- Remisión a `\eqref{eq:W2.gauss}` (fórmula con medias).
- Oración sobre la FID: es exactamente W₂² entre las gaussianas ajustadas a las representaciones de una red, `\cite{Heusel2017}`.

**Cap. 10, Sec. 10.3**
- Se corrigió la cita `\cite[Theorem~6.9]{Villani2003}` a `\cite[Theorem~6.9]{Villani2009}`. El Teo. 6.9 es de *Optimal Transport: Old and New*, no de *Topics*. No se usó el «Teo. 7.12 de *Topics*» que había sugerido en la v2, porque no pude verificarlo.
- Al final de la sección se agregó la subsección sin número «Medidas empíricas», con:
  - **Corolario 10.3.5 `cor.Wp.empirica`** (consistencia de la medida empírica, soporte compacto). Prueba: separabilidad de C(K) por Stone–Weierstrass, ley fuerte de los grandes números para una sucesión densa, y la recíproca en compactos del Teo. `teo.Wp.convergencia`. Incluye la consistencia de W_p(μ_n, ν_m).
  - **Observación 10.3.6** («El caso general»): teorema de Varadarajan `\cite[Theorem~11.4.1]{Dudley2002}`, más la ley fuerte para los momentos y la versión general del Teo. `teo.Wp.convergencia`.
  - **Observación 10.3.7 `obs.Wp.tasas`** (velocidad y maldición de la dimensión):
    - d = 1 (Ej. 10.12);
    - Fournier–Guillin, Teo. 1, en los tres regímenes `\cite[Theorem~1]{FournierGuillin2015}`;
    - Dudley, cota n^{-1/d} y cota inferior para medidas absolutamente continuas `\cite{Dudley1969}`, `\cite{WeedBach2019}`;
    - el caso crítico d = 2 de Ajtai–Komlós–Tusnády `\cite{AKT1984}`;
    - el factor 2^{10} en d = 10;
    - la dimensión intrínseca según Weed–Bach;
    - remisión a `ejc.Wp.muestras`.

**Cap. 10, Sec. 10.6, Obs. «W₁ como distancia entre medidas con signo»**
- Se reescribió la parte de WGAN:
  - GAN de Wasserstein `\cite{Arjovsky2017}`;
  - el supremo restringido es solo una cota inferior;
  - el recorte de pesos da funciones K-Lipschitz con K no controlado (se estima a lo sumo K·W₁);
  - la penalización del gradiente `\cite{Gulrajani2017}` impone la restricción solo de manera aproximada.

**Cap. 10, ejercicios**
- Ej. 10.12 `ejer.Wp.empirica.1D`: binomial; E W₁ ≤ n^{-1/2}∫√(F(1−F)) ≤ R n^{-1/2}; uniforme (π/8); y p > 1.
- Ej. 10.18 `ejc.Wp.muestras`: experimento d ∈ {1, 2, 5, 10}, n ∈ {50, …, 800}, 10 réplicas, log-log con barras.

**Cap. 13, Sec. 13.2, al final: subsección sin número «Derivadas del costo entrópico»**
- **Proposición 13.2.5 `prop.OTeps.derivada`**: F(C) = OT_ε es cóncava y diferenciable con ∂F/∂c_ij = π^ε_ij; gradiente respecto de las posiciones; caso cuadrático con la proyección baricéntrica.
  - Prueba completa en tres pasos: dos desigualdades, continuidad del plan por compacidad más unicidad, y conclusión.
- Párrafo sobre el teorema de la envolvente («de Danskin», solo nombrado, sin cita): en el caso no regularizado, la función puede no ser diferenciable; la derivada respecto de los pesos es el potencial (Ej. 13.8).
- **Observación 13.2.6 `obs.soporte.libre`**: la actualización z_i ← Σλ_k T̂_k(z_i) es un paso del método de descenso por gradiente con paso 1/(2b_i); sus puntos fijos son puntos críticos (versión discreta de `prop.bar.criterio`), y G no es convexa. Se presenta como optimización; no se mencionan flujos gradiente.

**Cap. 13, Obs. `obs.sinkhorn.tasa`**
- Frase de complejidad, sin fórmula: Sinkhorn más el redondeo a Π(a, b) aproxima OT(a, b), para cada error fijo, en tiempo casi lineal en el tamaño de la matriz de costos `\cite{AltschulerWeedRigollet2017}`.

**Cap. 13, Sec. 13.4, después de la demostración de `teo.eps.cero`**
- Párrafo sin número: OT_ε − OT = ε KL(π^ε) + (⟨C, π^ε⟩ − OT); el primer término es ε KL(π⁰) + o(ε) y el segundo es exponencialmente chico `\cite{Cominetti1994}` (ya estaba en la bibliografía), con constantes explícitas en `\cite{Weed2018}`.

**Cap. 13, Sec. 13.4, al final**
- **Observación 13.4.5 `obs.divergencia.sinkhorn`**:
  - el sesgo de OT_ε;
  - la definición de S_ε `\cite{GenevayPeyreCuturi2018,Feydy2019}`;
  - las propiedades de `\cite[Theorem~1]{Feydy2019}` (no negatividad, definida, convexidad y metrización de la convergencia débil), para soporte compacto y c = |x − y| o |x − y|²;
  - los límites ε → 0 y ε → ∞ (MMD).

**Cap. 13, ejercicios**
- Ej. 13.8 `ejer.OTeps.derivadas`: (a) caso sin regularizar, con el ejemplo 2×2 no diferenciable; (b) derivada respecto de los pesos = φ^ε.
- Ej. 13.9 `ejer.sinkhorn.sesgo`:
  - (a) 0 < OT_ε(α, α) ≤ ε H(a);
  - (b) ejemplo con α = ½(δ₋₁ + δ₁) y β_t = ½(δ₋ₜ + δₜ), donde la derivada en t = 1 vale 4(1 − 2p) > 0;
  - (c) S_ε no depende de la convención de regularización;
  - (d) límites de S_ε.

**Ap. E**
- La tabla de cuadernos pasa a decir `ejc.Wp.escala`–`ejc.Wp.muestras`.

### `notas/biblio.bib`

Entradas nuevas (sección siguiente).

### `practicas/sugerencias-fuente.tex`

Cuatro entradas `\sug` nuevas, en orden.

### Archivos regenerados por `make`

- `Notas-TO.pdf`;
- `practicas/practica-10.tex`, `practica-13.tex`, todos los PDF de las guías, `sugerencias.tex` y su PDF, e `INDICE.md`;
- `index.html` (204 páginas, enlaces de página);
- los cuadernos 04 y 06 (celda de ejercicios computacionales: 04 recibe el Ej. 10.18; en ambos se renumeraron los computacionales).

## Bibliografía: verificación de cada entrada

| Clave | Datos | Fuente con que se verificó |
|---|---|---|
| `Villani2009` | Villani, *Optimal Transport: Old and New*, Grundlehren 338, Springer, Berlin, 2009 | Lista de referencias de arXiv:1407.7245 («Grundlehren der Mathematischen Wissenschaften 338, Springer, Berlin (2009)»). **Teo. 6.9** = «W_p metrizes weak convergence»: citado así en arXiv:1209.1077 («Learning Probability Measures with respect to Optimal Transport Metrics», NIPS 2012), cuya clave [34] es *Old and New*. No se consultó el libro. |
| `Dudley2002` | Dudley, *Real Analysis and Probability*, 2.ª ed., Cambridge Studies in Adv. Math. 74, CUP, 2002, DOI 10.1017/CBO9780511755347 | Catálogo de la TUM (search.ub.tum.de). **Teo. 11.4.1 = teorema de Varadarajan** (convergencia débil c.s. de la empírica): según la cita en arXiv:2601.13946 («By Varadarajan's theorem (Dudley, 2002, Theorem 11.4.1)»). No se consultó el libro. |
| `Dudley1969` | Ann. Math. Statist. 40, 40–50, 1969, DOI 10.1214/aoms/1177697802 | Bibliografía de Weed–Bach (arXiv:1707.00087): «Ann. Math. Statist, 40:40–50». Allí figura el año **1968**; el vol. 40 de *Ann. Math. Statist.* es de 1969 y las búsquedas lo dan como 1969; se usó 1969. El DOI sale del identificador del registro en dml.mathdoc.fr (1177697802). No se pudo abrir Project Euclid (bloqueo anti-bot). Se omitió el número de fascículo. |
| `FournierGuillin2015` | PTRF 162(3), 707–738, 2015, DOI 10.1007/s00440-014-0583-7 | Página de Springer (link.springer.com/doi/10.1007/s00440-014-0583-7). El enunciado del Teo. 1 se verificó en ar5iv (arXiv:1312.2128). |
| `WeedBach2019` | Bernoulli 25(4A), 2620–2648, 2019, DOI 10.3150/18-BEJ1065 | Página DOI (www.doi.org/10.3150/18-BEJ1065). Contenido (dimensión intrínseca, cota inferior de Dudley): arXiv:1707.00087. |
| `AKT1984` | Combinatorica 4(4), 259–264, 1984, DOI 10.1007/BF02579135 | Página de Springer (link.springer.com/article/10.1007/BF02579135); el enunciado √(n log n), en Wikipedia («Ajtai–Komlós–Tusnády theorem»). |
| `Arjovsky2017` | ICML 2017, PMLR 70, 214–223 | proceedings.mlr.press/v70/arjovsky17a.html. El pasaje sobre recorte de pesos y K-Lipschitz, en el PDF de leon.bottou.org (Sec. 3). |
| `Gulrajani2017` | NIPS 2017 (Advances 30), cinco autores | papers.neurips.cc/paper/7159. **Páginas no listadas: omitidas.** |
| `Heusel2017` | NIPS 2017 (Advances 30), cinco autores | proceedings.neurips.cc (hash 8a1d6947…); el resumen introduce la FID. **Páginas omitidas.** |
| `GenevayPeyreCuturi2018` | AISTATS 2018, PMLR 84, 1608–1617 | proceedings.mlr.press/v84/genevay18a.html |
| `Feydy2019` | AISTATS 2019, PMLR 89, 2681–2690, seis autores | proceedings.mlr.press/v89/feydy19a.html. **Teo. 1** (hipótesis, conclusiones, ejemplos \|x−y\| y \|x−y\|², convención KL(·\|α⊗β), límites): ar5iv de arXiv:1810.08278. |
| `AltschulerWeedRigollet2017` | NIPS 2017 (Advances 30) | proceedings.neurips.cc (hash 491442df…). El redondeo y el tiempo Õ(n²L³ log n ε⁻³), en el PDF de NeurIPS (Teo. 1, Alg. 2). La página actual lista «Jonathan Niles-Weed»; se usó «Weed, Jonathan», como en la publicación original (arXiv:1705.09634). **Páginas omitidas.** |
| `Weed2018` | COLT 2018, PMLR 75, 1841–1855 | proceedings.mlr.press/v75/weed18a.html. Su resumen confirma que Cominetti–San Martín probaron la convergencia exponencialmente rápida. |
| `ShapleyShubik1971` | IJGT 1, 111–130, 1971, DOI 10.1007/BF01753437 | link.springer.com/doi/10.1007/BF01753437. El resumen confirma núcleo = soluciones del dual, y precios. |
| `GaleShapley1962` | Amer. Math. Monthly 69, 9–15, 1962 | prismmodelchecker.org (bibitem GS62) y nota de la MAA (número de enero de 1962). Se omitió el número de fascículo. |
| `Cominetti1994` | (ya estaba) | Su uso nuevo («convergencia exponencialmente rápida») se respalda con el resumen de Weed 2018. |

## No incorporado o decidido no hacer

- **Galichon 2016:** no se pudo verificar el capítulo (la página de Princeton UP no tiene índice); no se cita.
- **Danskin 1966:** no se pudo verificar el volumen y las páginas (SIAM bloquea robots); se nombra el teorema de la envolvente «de Danskin» sin cita. La demostración que se da es completa, así que el criterio de las notas se cumple.
- **Villani *Topics*, Teo. 7.12:** no verificado; no se usa.
- **Feydy et al. con costos generales:** las hipótesis generales (núcleo positivo universal) se mencionan solo como «bajo hipótesis sobre el núcleo», sin detallarlas.
- Por indicación del coordinador no se incorporaron *flow matching*, la recíproca ★ ni el cuaderno 07. Tampoco una sección resuelta en el cuaderno 04: solo llega el enunciado por sincronización. El prototipo del experimento, que corre en unos 4 s, está en el scratchpad (`rate.py`).
- **Incidente de red:** `www.doi.org` respondió 429 (rate limit) al intentar abrir 10.1007/BF02579135; los datos se tomaron de la página de Springer. La API de Crossref no está permitida por el proxy.
