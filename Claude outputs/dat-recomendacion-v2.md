# Segundo informe de evaluación externa: *Teoría de Transporte Óptimo* (FCEN-UBA, 2026)

**Evaluador:** dat (ciencia de datos y aprendizaje automático).
**Fecha:** 15/10/2026.
**Punto de partida:** mi informe anterior (`dat.md`), releído contra el material corregido del repositorio (`notas/Notas-TO.tex`, 200 páginas, cuadernos ejecutados) y el marco que me hizo llegar el autor.

---

## 0. Qué cambia con este marco (y qué retiro)

Mi primer informe evaluó el curso como si fuera la formación en OT de un científico de datos. No lo es: es un curso compartido por la Licenciatura y el Doctorado en Matemática y la Licenciatura en Ciencia de Datos, y la evaluación principal es una exposición de una hora sobre una aplicación elegida por cada estudiante. Con esto en cuenta, varias cosas que dije no se sostienen.

**Lo que retiro:**

- **"Hay margen para hacer lugar aligerando demostraciones (unas 4 clases)"** (punto 10). El balance teoría/aplicaciones está decidido y la regla "caso fácil con demostración, enunciado general y cita" ya es el aligeramiento. Retiro la propuesta, y con ella el presupuesto de "4 clases recuperadas" en el que se apoyaba casi todo mi plan de prioridad 1.
- **"Brunn–Minkowski: pasar a lectura opcional".** Lo retiro. Además, con exposiciones como evaluación, el cap. 11 es justamente la puerta de entrada a varios de los mejores temas teóricos de la lista (§3).
- **"La recíproca de la convergencia en W_p solo está en compactos, y es la que necesita un estadístico"** (punto 6). Era un argumento equivocado. Si μ tiene soporte compacto K, sus medidas empíricas también viven en K, así que **la recíproca en compactos que ya está demostrada alcanza exactamente para la consistencia**. El tratamiento actual (enunciado general, prueba en compactos, cita a Villani 6.9 y Santambrogio 5.11) cumple el criterio de las notas. No hay defecto que corregir.
- **"Repertorio mínimo de variantes en las notas"** (OT desbalanceado, sliced, Gromov–Wasserstein). Choca con la decisión de no incluir "variantes de Peyré". Esos temas pasan a ser **temas de exposición**, que es donde mejor rinden.
- **Un error de mi informe anterior:** escribí "Shapley–Shubert". Es **Shapley–Shubik** (1971, *The assignment game I: The core*).

**Lo que ya está resuelto en el material corregido:**

- La tasa de Sinkhorn (Obs. `obs.sinkhorn.tasa`) ahora distingue medio paso (κ) de iteración completa (κ²). Correcto.
- El matiz del límite ε → 0 que pedía (OT_ε − OT ≈ ε·KL(π⁰ | a⊗b), lineal, con constante menor que log(1/min aᵢ)) está en la sugerencia de `ejc.eps.valores`.
- La celda de instalación usa `%pip`, los cuadernos se versionan con salidas y el README documenta tiempos y versiones.

**Lo que sigue en pie, con otro destino:**

- La consistencia estadística y la tasa n^{-1/d}: el corolario de consistencia va a las notas, y lo demás a ejercicio y exposición.
- La diferenciación y la divergencia de Sinkhorn: van como observaciones cortas en el cap. 13, que todavía no se dio.
- Las precisiones de texto sobre WGAN, utilidad transferible y FID siguen siendo válidas y cuestan casi nada.

---

## 1. El presupuesto real de tiempo

Desde el 19/10 hasta el 2/12 quedan **14 clases** de lunes y miércoles (16 si se llega al 9/12). Hay que verificar los feriados en el calendario académico.

| Bloque | Clases estimadas |
|---|---|
| Cierre del cap. 10 | 0.5 |
| Cap. 11 (Brunn–Minkowski, corto) | 1–1.5 |
| Cap. 12 (baricentros) | 2–3 |
| Cap. 13 (Sinkhorn) | 3 |
| **Subtotal teoría** | **~7** |
| Exposiciones (2 por clase de 2 h) | N/2 (N = cantidad de estudiantes) |

Con N ≈ 10 quedan 1–2 clases de margen; con N ≈ 14, ninguna. **Conclusión: este cuatrimestre no se puede agregar más de unos 30–45 minutos de clase en total.** Todo lo que recomiendo para "ya" está pensado para costar cero o pocos minutos de clase: texto en las notas, ejercicios para las entregas que quedan y temas de exposición.

---

## 2. Revisión punto por punto

### Tabla resumen

| # | Punto del informe anterior | Destino nuevo | Clase este año | Cuándo |
|---|---|---|---|---|
| 1 | Estadística de OT | Corolario de consistencia y observación de tasas en el cap. 10, más 1 ejercicio teórico y 1 computacional, más 2–3 temas de exposición | 0–20 min | **Ya** |
| 2 | Diferenciación | Observación con prueba corta en el cap. 13, más 1 ejercicio | ~20 min dentro del cap. 13 | **Ya** (antes de dar el cap. 13) |
| 3 | Divergencia de Sinkhorn | Observación de media página en el cap. 13, más 1 ejercicio; el desarrollo, a exposición | ~10 min | **Ya** (si el autor no la considera "variante") |
| 4 | Caso con datos reales | Tema de exposición; cuaderno 07 en la versión siguiente | 0 | Exposición ya; cuaderno después |
| 5 | Retoques de una línea | WGAN: ya (cap. 10). TU con cita: ya. FID: ya. *Flow matching*: a exposición, no a las notas | 0 | Ya (costo nulo) |
| 6 | Recíproca en W_p | **Descartar** (no hay defecto); a lo sumo un ejercicio ★ | 0 | Versión siguiente, opcional |
| 7 | Más profundidad en Sinkhorn | κ² ya corregido. La tasa lineal (Birkhoff–Hopf) va a exposición. Una frase sobre complejidad | 0 | Frase ya; resto a exposición |
| 8 | Réplicas y barras de error | Solo donde hay azar: un experimento de tasas en el cuaderno 04 (lo mismo que el punto 1) | 0 | Ejercicio ya; sección del cuaderno después |
| 9 | Cap. 7 breve | **No ampliar.** Solo citas y precisión (TU, Shapley–Shubik, Gale–Shapley); el matching, a exposición | 0 | Ya (3 líneas) |
| 10 | Aligerar demostraciones | **Retirado** | — | — |
| 11 | Temas de segunda línea | Temas de exposición (§3) y lista de reserva | 0 | Ya (lista) |

### (1) Estadística de OT

**(a) Destino.** Tres piezas:

1. Notas, cap. 10: un corolario con demostración al final de la Sec. 10.3, más una observación con las tasas enunciadas y citadas.
2. Un ejercicio teórico (tasa en 1D) y un ejercicio computacional (`ejc.Wp.muestras`).
3. Temas de exposición 9, 10 y 11 de §3.

**(b) Por qué, para ambos públicos.**
- La Sec. 7.5 ("Transporte óptimo y discretización") promete que "sin la teoría continua [...] la discretización es un procedimiento ad hoc sin garantías de consistencia", y esa promesa nunca se cumple en las notas. Es una deuda interna del texto, no un pedido de Ciencia de Datos.
- El corolario se demuestra con herramientas que el curso ya tiene: la ley fuerte de los grandes números, la separabilidad de C(K) y el teorema de convergencia en compactos. Es una aplicación limpia de un teorema que un matemático acaba de ver.
- Para Datos, es *el* resultado que justifica usar W_p con muestras.
- Las tasas (con el caso d = 2 de Ajtai–Komlós–Tusnády) son probabilidad clásica y atraen también a Matemática.

**(c) Alcance y costo.** Unas 1.5–2 páginas en total.

- **Corolario (consistencia).** Sea μ con soporte en un compacto K ⊂ ℝ^d, sean X₁, X₂, … i.i.d. con ley μ y μₙ = (1/n) Σ δ_{Xᵢ}. Entonces, casi seguramente, μₙ ⇀ μ y W_p(μₙ, μ) → 0. En consecuencia, |W_p(μₙ, νₘ) − W_p(μ, ν)| ≤ W_p(μₙ, μ) + W_p(νₘ, ν) → 0.
  - *Prueba del caso fácil, unas 10 líneas:* tomar {f_k} densa y numerable en C(K); aplicar la ley fuerte a cada f_k (numerables eventos de probabilidad 1); pasar a toda f ∈ C(K) por densidad; como μₙ está concentrada en K, cerrar con la recíproca en compactos (Teo. `teo.Wp.convergencia`). El caso general es el teorema de Varadarajan, que se cita (por ejemplo, Dudley, *Real Analysis and Probability*, cap. 11; no recuerdo el número exacto del teorema, hay que verificarlo).
- **Observación (tasas), enunciada y citada.**
  - Para μ en un compacto de ℝ^d y d > 2p, E W_p(μₙ, μ) ≲ n^{-1/d} (Fournier–Guillin 2015; Weed–Bach 2019).
  - Para μ absolutamente continua no se puede mejorar (Dudley 1969 para p = 1).
  - En d = 1 la tasa es n^{-1/2}, y en d = 2, con μ uniforme y p = 1, es √(log n / n) (Ajtai–Komlós–Tusnády 1984).
  - Una frase sobre la "maldición de la dimensión" y sobre por qué Sinkhorn y sliced la mitigan, con remisión a las exposiciones 13 y 14.
- **Ejercicio teórico (tasa en 1D).** Con la fórmula del área del cap. 8, W₁(μₙ, μ) = ∫|Fₙ − F|. Probar que E W₁(μₙ, μ) ≤ n^{-1/2} ∫ √(F(1−F)) dx, usando E|Fₙ(x) − F(x)| ≤ (Var Fₙ(x))^{1/2}. Es corto, elemental, ambos públicos lo pueden hacer, y sirve para una entrega.
- **Ejercicio computacional `ejc.Wp.muestras`.** Dos muestras independientes de la uniforme en [0,1]^d, W₁ con `ot.emd2`, n ∈ {50, …, 800}, d ∈ {1, 2, 5, 10}, 10 réplicas, gráfico log-log con media ± desvío y pendientes. **Lo prototipé:** corre en 3.6 s y da pendientes −0.51, −0.46, −0.24 y −0.13 para d = 1, 2, 5 y 10, consistentes con −1/2, −1/2 (con factor logarítmico), −1/5 y −1/10. El prototipo está en `/tmp/claude-0/-home-claude/024f618a-b408-5799-8866-8b1507175f55/scratchpad/rate.py`. Como `make sincronizar` regenera la celda de ejercicios desde las notas, basta con agregar el enunciado al tex; la sección resuelta del cuaderno puede esperar.
- **Clase:** 0 si se deja como lectura más ejercicio de entrega; 15–20 min si se presenta. Redacción: 4–6 h.

**(d) Cuándo.** **Ya.** El cap. 10 se está terminando y el corolario cierra naturalmente su Sec. 10.3. Si la clase del cap. 10 ya se cerró, sirve como lectura y ejercicio para la entrega correspondiente. La remisión hacia adelante desde la Sec. 7.5 ("véase el Corolario 10.x") es un cambio de una línea en un capítulo ya dado, y no lo reestructura.

### (2) Diferenciación

**(a) Destino.** Notas, cap. 13: una sección u observación corta, "Derivadas del costo entrópico", después de la Sec. 13.4. Más un ejercicio, y la parte de autodiferenciación y aprendizaje en el tema de exposición 18.

**(b) Por qué.** Cumple exactamente el criterio "demostración del caso fácil": en el caso entrópico el minimizador es único y el resultado sale del teorema de la envolvente (Danskin) en diez líneas.
- Para Matemática es un buen ejemplo de análisis convexo: la relación entre potenciales y subgradientes, que conecta con la sensibilidad en PL del cap. 3.
- Para Datos es lo que permite *usar* OT_ε como función de pérdida.
- Además unifica material que ya está: el algoritmo de soporte libre del cap. 12 (x ← Σ λ_k T̂_k(x)) es *exactamente* un paso de gradiente de Σ λ_k W₂² respecto de las posiciones, con paso 1/2. Hoy las notas lo usan sin decirlo.

**(c) Alcance y costo.** 1 página más 1 ejercicio.
- **Proposición.** Para c de clase C¹:
  - ∂OT_ε/∂xᵢ = Σⱼ π^ε_ij ∇ₓc(xᵢ, yⱼ). Con c = |x − y|², esto es 2aᵢ(xᵢ − T̂(xᵢ)), donde T̂ es la proyección baricéntrica.
  - ∇ₐ OT_ε = φ^ε, salvo constante (como función en el símplex). La cuenta con el dual del Teo. `teo.dual.entropico` es directa: el término ε Σ aᵢbⱼ(e^{…} − 1) tiene derivada nula en el óptimo.
  - *Prueba:* Danskin sobre Π(a, b), que es compacto, con minimizador único.
- **Ejercicio.** En el caso no regularizado, OT(a, b) es convexa en (a, b) y los potenciales de Kantorovich son subgradientes. Es sensibilidad en PL, con referencia al cap. 5. Pedir además verificar con diferencias finitas en el cuaderno 06 (2–3 celdas, solo NumPy y POT, sin sumar `torch`/`jax` como dependencia).
- **Clase:** unos 20 min dentro del cap. 13. Redacción: 4–5 h.
- *Advertencia de encuadre:* presentar el descenso por gradiente sobre posiciones como optimización, no como "flujo gradiente", para no rozar la decisión de excluir flujos gradiente.

**(d) Cuándo.** **Ya**, antes de dar el cap. 13. Es barato y el capítulo todavía no se dictó.

### (3) Divergencia de Sinkhorn

**(a) Destino.** Una observación de media página en el cap. 13, más un ejercicio. El desarrollo (MMD, complejidad muestral, propiedades métricas) va al tema de exposición 14.

**(b) Por qué.** No es un problema nuevo sino una propiedad del mismo OT_ε que el capítulo ya estudia: OT_ε(a, a) > 0, y b ↦ OT_ε(a, b) no se minimiza en b = a.
- Cualquiera que use `ot.sinkhorn2` como distancia cae en este sesgo, así que para Datos es indispensable.
- Para Matemática es un ejemplo instructivo de cómo la regularización rompe la estructura métrica.
- **Si el autor considera que esto ya es una "variante de Peyré", que vaya solo a exposición:** es el punto más discutible de esta lista.

**(c) Alcance y costo.**
- **Observación.** Definir S_ε(a, b) = OT_ε(a, b) − ½OT_ε(a, a) − ½OT_ε(b, b) y enunciar con cita que, bajo hipótesis sobre el costo (por ejemplo, c = |x − y|²), S_ε ≥ 0, se anula solo si a = b e interpola entre OT (ε → 0) y una MMD (ε → ∞) (Feydy et al. 2019; Genevay–Peyré–Cuturi 2018).
- **Ejercicio:** (i) con la convención KL(·|a⊗b) de las notas, probar 0 < OT_ε(a, a) ≤ ε H(a) cuando cᵢᵢ = 0; (ii) en el cuaderno, minimizar b ↦ OT_ε(a, b) en una grilla 1D y observar el "encogimiento"; repetir con S_ε.
- **Clase:** unos 10 min. Redacción: 2–3 h.

**(d) Cuándo.** Ya, junto con el punto 2.

### (4) Un caso con datos reales

**(a) Destino.** Este año, **tema de exposición** (17: transferencia de color y adaptación de dominio). En la versión siguiente, un cuaderno 07, "Aplicaciones", que puede armarse a partir de la mejor exposición computacional del año.

**(b) Por qué.** Con exposiciones como evaluación principal, el "caso de punta a punta" que faltaba lo van a producir los estudiantes de Datos, y es mejor que lo hagan ellos a que lo reciban hecho. Mi crítica ("ningún ejercicio *usa* la teoría") pierde peso: los ejercicios verifican la teoría, y las exposiciones la usan. Es una división del trabajo razonable para un curso mixto.

**(c) Alcance y costo.** Este año, 0 clases y 0 páginas: solo el tema en la lista. Versión siguiente: un cuaderno de 15–20 celdas (transferencia de color con proyección baricéntrica, exacta y entrópica, más una variante con sliced), 8–10 h de trabajo.

**(d) Cuándo.** El tema ya; el cuaderno, en la versión siguiente.

### (5) Retoques de una línea

Los cuatro tienen costo de clase nulo. Los evalúo por separado, porque con el marco nuevo no todos se sostienen igual.

- **WGAN (cap. 10, Obs. "W₁ como distancia entre medidas con signo").** **Hacerlo ya**; es el capítulo en curso. El texto actual dice que el supremo "se aproxima restringiéndolo a una familia paramétrica". Falta decir que esa restricción da una **cota inferior** de W₁, y que imponer la condición 1-Lipschitz (recorte de pesos, penalización del gradiente) es el punto delicado, sin garantías. Son dos oraciones con cita (Arjovsky–Chintala–Bottou 2017; Gulrajani et al. 2017). Más que un retoque, evita una lectura equivocada del texto.
- **Utilidad transferible (cap. 7, Sec. 7.3).** **Hacerlo ya.** El texto afirma "la equivalencia entre matching estable y transporte óptimo" sin cita, y por el criterio de las notas necesita referencia. Propuesta: "en el modelo con *utilidad transferible* (Shapley–Shubik 1971; véase Galichon 2016, cap. ...)". Hay que verificar el capítulo en el libro de Galichon. Agregar además una frase de contraste: en el matching de Gale–Shapley (1962) la utilidad no es transferible y no hay formulación como problema de transporte. Son 3 líneas más 2–3 entradas de bibliografía. No reestructura nada.
- **FID (cap. 9, Obs. de gaussianas generales).** **Hacerlo ya o en la próxima pasada.** La última oración ya menciona Bures–Wasserstein; agregar que la *Fréchet Inception Distance* (Heusel et al. 2017) es exactamente W₂² entre las gaussianas ajustadas a los *features* de una red, con una cita. Para Datos es la aplicación más conocida de una fórmula que acaban de demostrar.
- ***Flow matching* (gancho en la Sec. 9.3).** **Lo retiro de las notas.** Sin la formulación dinámica, que el curso no desarrolla, una línea sobre *flow matching* no agrega nada para el público de Matemática y exige una cita que no se puede explicar en el texto. Va al tema de exposición 18, donde se puede presentar lo mínimo de Benamou–Brenier que haga falta.

**Costo total:** unas 6–8 líneas y 5–6 entradas de bibliografía; alrededor de 1 h de redacción.

### (6) Recíproca de la convergencia en W_p

**(a) Destino.** **Descartar** como cambio de las notas. Opcional, en la versión siguiente: un ejercicio ★ ("completar la recíproca para medidas en ℝ^d por truncamiento, siguiendo Santambrogio, Teo. 5.11, o Villani 2003") para estudiantes de doctorado.
**(b) Por qué.** Como expliqué en §0, mi argumento era incorrecto: la versión compacta alcanza para la consistencia con μ de soporte compacto, que es el marco de todo el curso. El tratamiento actual es el que prescribe el criterio de las notas.
**(c) Costo.** Ejercicio ★: un cuarto de página. Clase: 0. **Posible errata de cita, de costo nulo:** la línea 8661 de las notas cita `\cite[Theorem~6.9]{Villani2003}`, y en `biblio.bib` la clave `Villani2003` es *Topics in Optimal Transportation*. Hasta donde recuerdo, el Teo. 6.9 es la numeración de *Optimal Transport: Old and New* (2009); en *Topics* el resultado es el Teo. 7.12. Hay que verificarlo con el libro en la mano antes de cambiarlo.
**(d) Cuándo.** Versión siguiente, si se quiere.

### (7) Más profundidad en Sinkhorn

**(a) Destino.**
- La tasa (κ²) ya está bien.
- La **demostración** de la convergencia lineal (métrica de Hilbert, Birkhoff–Hopf) va a exposición (tema 8): es un tema teórico excelente para Matemática.
- En las notas, **una frase** al final de `obs.sinkhorn.tasa` sobre complejidad: alcanzar precisión δ en las marginales requiere O(nm · log n · δ⁻²) operaciones, o una cota de ese tipo, según Altschuler–Weed–Rigollet 2017. Hay que verificar la forma exacta antes de escribirla; recuerdo el orden ~n²/δ³ en su versión original, mejorado en trabajos posteriores, así que conviene citarla sin fórmula si hay duda.
- Opcional: media oración sobre la convergencia exponencial de ⟨C, π^ε⟩ − OT (Cominetti–San Martín, ya en la bibliografía), complementando lo que la sugerencia de `ejc.eps.valores` ya dice sobre OT_ε − OT.

**(b) Por qué.** Lo que faltaba de fondo (κ frente a κ² y el orden en ε) ya está corregido. Lo que queda es profundidad que es mejor dar como exposición que como clase.
**(c) Costo.** 2–3 líneas. Clase: 0.
**(d) Cuándo.** Ya, al pasar por el cap. 13.

### (8) Réplicas y barras de error en los cuadernos

**(a) Destino.** Restringirlo al único lugar donde hay azar que cuantificar: el experimento de tasas del punto 1 (`ejc.Wp.muestras` y, en la versión siguiente, una sección "7. Medidas empíricas" en el cuaderno 04, de 6–8 celdas).
**(b) Por qué.** Mi pedido general estaba sobredimensionado. Los cuadernos verifican teoremas deterministas (fórmulas cerradas, dualidad, convergencia de Sinkhorn), donde una sola semilla fija es lo correcto y además el README promete reproducibilidad. Las réplicas solo tienen sentido cuando el objeto es estadístico.
**(c) Costo.** Ejercicio: 0 clases, un párrafo en el tex. Sección resuelta: 6–8 celdas, menos de 5 s de ejecución (medido).
**(d) Cuándo.** El ejercicio ya; la sección resuelta, en la versión siguiente.

### (9) Cap. 7 breve

**(a) Destino.** **No ampliar.** Precisión y citas (ver punto 5, utilidad transferible) y la remisión hacia adelante desde la Sec. 7.5 al corolario de consistencia (punto 1). El matching económico va al tema de exposición 12.
**(b) Por qué.** En un curso mixto, el cap. 7 funciona como interludio de interpretaciones. El multimarginal se desarrolla en el cap. 12 y la discretización se resuelve en el cap. 10 (punto 1). Ampliarlo duplicaría material o lo sacaría de su función.
**(c) Costo.** 4–5 líneas en total. Clase: 0.
**(d) Cuándo.** Ya (es corrección de texto, no reestructuración).

### (10) Aligerar demostraciones

**Retirado** (ver §0). Si en la versión siguiente se quiere ayudar a los estudiantes de Datos sin tocar el contenido, alcanza con un párrafo de "Guía de lectura" en el Prefacio, que indique qué demostraciones son instrumentales y cuáles pueden leerse como enunciado en una primera lectura. Es opcional y no lo considero necesario.

### (11) Temas de segunda línea

**(a) Destino.** Temas de exposición (§3): semidiscreto, sliced, desbalanceado, Gromov–Wasserstein, generativos y cuantiles multivariados. Lo que no entra en la lista principal queda en la lista de reserva (§3.4).
**(b) Por qué.** Era el destino natural y yo no lo sabía. Las exposiciones permiten cubrir en amplitud lo que las notas no deben cubrir por decisión de diseño.
**(c) Costo.** 0 clases adicionales; las exposiciones ya están en el plan.
**(d) Cuándo.** La lista, ya (ver §4 sobre plazos).

---

## 3. Temas de exposición (18)

**Criterios.**
- Cada tema cabe en 1 hora y presupone a lo sumo los caps. 1–13.
- Tiene un núcleo demostrable o calculable en la charla.
- Ninguno requiere flujos gradiente, regularidad de Caffarelli ni Monge–Ampère; los excluí a propósito, por la decisión del autor.
- Cinco temas son de análisis geométrico o probabilidad.
- **Referencias:** las doy de memoria, con autores, año, título y medio. No consulté las fuentes en esta sesión; donde tengo dudas sobre algún dato, lo indico.

**Balance:** 5 temas naturales para Matemática, 8 para ambos públicos y 5 para Datos. Por tipo: 5 teóricos, 10 mixtos y 3 computacionales.

### 3.1 Análisis geométrico, probabilidad y teoría

**1. Prékopa–Leindler y Brascamp–Lieb vía transporte**
- *Qué es:* las formas funcionales de Brunn–Minkowski (log-concavidad de convoluciones, Brascamp–Lieb inversa), demostradas con el mapa de Brenier y la concavidad de det^{1/d}.
- *Tipo:* teórico.
- *Presupone:* caps. 9 y 11.
- *Público:* Matemática.
- *Referencias:* McCann (1997), "A convexity principle for interacting gases", *Adv. Math.*; Barthe (1998), "On a reverse form of the Brascamp–Lieb inequality", *Invent. Math.*; Gardner (2002), "The Brunn–Minkowski inequality", *Bull. AMS*.

**2. Desigualdades de Sobolev e isoperimétrica óptimas vía transporte**
- *Qué es:* la prueba de Cordero-Erausquin–Nazaret–Villani de la desigualdad de Sobolev con constante óptima y sus extremales, con la isoperimétrica como caso límite.
- *Tipo:* teórico.
- *Presupone:* caps. 9 y 11, y el Ap. D.
- *Público:* Matemática (Doctorado).
- *Referencias:* Cordero-Erausquin, Nazaret y Villani (2004), "A mass-transportation approach to sharp Sobolev and Gagliardo–Nirenberg inequalities", *Adv. Math.*; Figalli, Maggi y Pratelli (2010), "A mass transportation approach to quantitative isoperimetric inequalities", *Invent. Math.* (como extensión); Villani (2003), *Topics in Optimal Transportation*, cap. 6, "Geometric and Gaussian inequalities" (las notas ya citan ese capítulo en `obs.BM.general`).

**3. Desigualdad de Talagrand y concentración de la medida**
- *Qué es:* W₂(ν, γ)² ≤ 2 KL(ν | γ) para la gaussiana estándar, con prueba en 1D por el mapa monótono, tensorización y la consecuencia de concentración (argumento de Marton).
- *Tipo:* teórico.
- *Presupone:* caps. 8 y 10 (y el ejercicio de convexidad de la entropía del cap. 11).
- *Público:* Matemática (útil también para Datos).
- *Referencias:* Talagrand (1996), "Transportation cost for Gaussian and other product measures", *GAFA*; Marton (1996), "Bounding d̄-distance by informational divergence: a method to prove measure concentration", *Ann. Probab.*; Gozlan y Léonard (2010), "Transport inequalities. A survey", *Markov Process. Related Fields* (el volumen no lo recuerdo con certeza).

**4. El mapa de Knothe–Rosenblatt: de los cuerpos convexos a los flujos normalizantes**
- *Qué es:* el reordenamiento triangular de Knothe, su uso original en geometría convexa, su obtención como límite de mapas de Brenier con costos anisótropos, y por qué es la estructura de los flujos autorregresivos.
- *Tipo:* mixto.
- *Presupone:* caps. 8 y 9.
- *Público:* ambos.
- *Referencias:* Knothe (1957), "Contributions to the theory of convex bodies", *Michigan Math. J.*; Carlier, Galichon y Santambrogio (2010), "From Knothe's transport to Brenier's map and a continuation method for optimal transport", *SIAM J. Math. Anal.*; Papamakarios et al. (2021), "Normalizing flows for probabilistic modeling and inference", *JMLR*.

**5. La geometría de Bures–Wasserstein**
- *Qué es:* el espacio de gaussianas con W₂ como variedad de matrices definidas positivas (geodésicas, curvatura, baricentros por punto fijo) y su uso como métrica, incluida la FID.
- *Tipo:* mixto.
- *Presupone:* caps. 9, 10 y 12.
- *Público:* ambos.
- *Referencias:* Takatsu (2011), "Wasserstein geometry of Gaussian measures", *Osaka J. Math.*; Bhatia, Jain y Lim (2019), "On the Bures–Wasserstein distance between positive definite matrices", *Expo. Math.*; Álvarez-Esteban, del Barrio, Cuesta-Albertos y Matrán (2016), "A fixed-point approach to barycenters in Wasserstein space", *J. Math. Anal. Appl.* (ya está en la bibliografía de las notas).

**6. Transporte multimarginal con costo de Coulomb**
- *Qué es:* el límite de correlación fuerte de la teoría del funcional de la densidad como problema multimarginal con costo repulsivo; existencia, mapas de Monge en 1D y diferencias con el costo cuadrático.
- *Tipo:* teórico.
- *Presupone:* caps. 7, 8 y 12.
- *Público:* Matemática.
- *Referencias:* Buttazzo, De Pascale y Gori-Giorgi (2012), "Optimal-transport formulation of electronic density-functional theory", *Phys. Rev. A*; Cotar, Friesecke y Klüppelberg (2013), "Density functional theory and optimal transportation with Coulomb cost", *Comm. Pure Appl. Math.*; Pass (2015), "Multi-marginal optimal transport: theory and applications", *ESAIM: M2AN*.

**7. Transporte semidiscreto, celdas de Laguerre y el problema de Minkowski**
- *Qué es:* transporte de una densidad a una medida discreta; el dual es una función cóncava de dimensión finita, cuyo gradiente son las masas de celdas de Laguerre; algoritmo de Newton y conexión con el teorema de Minkowski sobre poliedros.
- *Tipo:* mixto.
- *Presupone:* caps. 4–6 y 9.
- *Público:* ambos.
- *Referencias:* Aurenhammer, Hoffmann y Aronov (1998), "Minkowski-type theorems and least-squares clustering", *Algorithmica*; Kitagawa, Mérigot y Thibert (2019), "Convergence of a Newton algorithm for semi-discrete optimal transport", *J. Eur. Math. Soc.*; Gu, Luo, Sun y Yau (2016), "Variational principles for Minkowski type problems, discrete optimal transport, and discrete Monge–Ampère equations", *Asian J. Math.* (el título menciona Monge–Ampère, pero la charla no lo necesita).

**8. La convergencia de Sinkhorn: métrica de Hilbert y teorema de Birkhoff–Hopf**
- *Qué es:* la demostración completa de la convergencia lineal que la Obs. `obs.sinkhorn.tasa` enuncia: contracción de matrices positivas en la métrica proyectiva de Hilbert, más un panorama de complejidad.
- *Tipo:* teórico.
- *Presupone:* cap. 13.
- *Público:* Matemática (interesa también a Datos).
- *Referencias:* Birkhoff (1957), "Extensions of Jentzsch's theorem", *Trans. AMS*; Franklin y Lorenz (1989), "On the scaling of multidimensional matrices", *Linear Algebra Appl.* (ya está en la bibliografía); Altschuler, Weed y Rigollet (2017), "Near-linear time approximation algorithms for optimal transport via Sinkhorn iteration", *NeurIPS*.

### 3.2 Estadística

**9. Medidas empíricas: tasas de convergencia y maldición de la dimensión**
- *Qué es:* E W_p(μₙ, μ) en función de n y d (n^{-1/2} en 1D, el caso crítico d = 2 de Ajtai–Komlós–Tusnády, n^{-1/d} en general), con experimento numérico.
- *Tipo:* mixto.
- *Presupone:* caps. 8 y 10.
- *Público:* ambos.
- *Referencias:* Dudley (1969), "The speed of mean Glivenko–Cantelli convergence", *Ann. Math. Statist.*; Fournier y Guillin (2015), "On the rate of convergence in Wasserstein distance of the empirical measure", *Probab. Theory Related Fields*; Weed y Bach (2019), "Sharp asymptotic and finite-sample rates of convergence of empirical measures in Wasserstein distance", *Bernoulli*. Complementos: Ajtai, Komlós y Tusnády (1984), "On optimal matchings", *Combinatorica*; Bobkov y Ledoux (2019), "One-dimensional empirical measures, order statistics, and Kantorovich transport distances", *Mem. AMS*.

**10. Cuantiles, rangos y signos multivariados vía Brenier**
- *Qué es:* definir "la función de cuantiles" en ℝ^d como el mapa de Brenier hacia una medida de referencia, y construir con ella rangos y tests libres de distribución.
- *Tipo:* mixto.
- *Presupone:* caps. 8 y 9.
- *Público:* ambos.
- *Referencias:* Chernozhukov, Galichon, Hallin y Henry (2017), "Monge–Kantorovich depth, quantiles, ranks and signs", *Ann. Statist.*; Hallin, del Barrio, Cuesta-Albertos y Matrán (2021), "Distribution and quantile functions, ranks and signs in dimension d: a measure transportation approach", *Ann. Statist.*

**11. Tests de bondad de ajuste y de dos muestras con W_p**
- *Qué es:* estadísticos basados en W_p (en 1D, vía cuantiles), su distribución asintótica en casos simples y comparación empírica con tests clásicos.
- *Tipo:* mixto (con fuerte componente computacional).
- *Presupone:* caps. 8 y 10.
- *Público:* Datos.
- *Referencias:* del Barrio, Cuesta-Albertos, Matrán y Rodríguez-Rodríguez (1999), "Tests of goodness of fit based on the L₂-Wasserstein distance", *Ann. Statist.*; Ramdas, García Trillos y Cuturi (2017), "On Wasserstein two-sample testing and related families of nonparametric tests", *Entropy*; Panaretos y Zemel (2019), "Statistical aspects of Wasserstein distances", *Annu. Rev. Stat. Appl.*

**12. Matching con utilidad transferible y el modelo de Choo–Siow**
- *Qué es:* el juego de asignación de Shapley–Shubik como transporte óptimo, y el modelo econométrico de Choo–Siow, cuyo equilibrio es exactamente un plan entrópico calculable con Sinkhorn.
- *Tipo:* mixto.
- *Presupone:* caps. 5, 7 y 13.
- *Público:* ambos.
- *Referencias:* Shapley y Shubik (1971), "The assignment game I: The core", *Int. J. Game Theory*; Choo y Siow (2006), "Who marries whom and why", *J. Polit. Econ.*; Galichon (2016), *Optimal Transport Methods in Economics*, Princeton University Press.

### 3.3 Cómputo y aprendizaje

**13. Wasserstein por proyecciones (*sliced*)**
- *Qué es:* promediar el W_p unidimensional sobre direcciones; propiedades métricas, complejidad muestral sin maldición de la dimensión y baricentros *sliced*.
- *Tipo:* mixto (computacional).
- *Presupone:* caps. 8, 10 y 12.
- *Público:* Datos.
- *Referencias:* Rabin, Peyré, Delon y Bernot (2012), "Wasserstein barycenter and its application to texture mixing", en *SSVM 2011*, LNCS; Bonneel, Rabin, Peyré y Pfister (2015), "Sliced and Radon Wasserstein barycenters of measures", *J. Math. Imaging Vision*; Nadjahi et al. (2020), "Statistical and topological properties of sliced probability divergences", *NeurIPS*.

**14. Divergencias de Sinkhorn: sesgo, MMD y complejidad muestral**
- *Qué es:* por qué OT_ε no es una distancia; la corrección S_ε, su interpolación entre OT y MMD, y su complejidad muestral independiente de la dimensión (con constantes que dependen de ε).
- *Tipo:* mixto.
- *Presupone:* cap. 13.
- *Público:* Datos (con buen contenido teórico para Matemática).
- *Referencias:* Genevay, Peyré y Cuturi (2018), "Learning generative models with Sinkhorn divergences", *AISTATS*; Feydy, Séjourné, Vialard, Amari, Trouvé y Peyré (2019), "Interpolating between optimal transport and MMD using Sinkhorn divergences", *AISTATS*; Genevay, Chizat, Bach, Cuturi y Peyré (2019), "Sample complexity of Sinkhorn divergences", *AISTATS*.

**15. Transporte desbalanceado y parcial**
- *Qué es:* relajar las marginales con penalización KL; Sinkhorn generalizado; robustez frente a valores atípicos; aplicación a trayectorias de células (Waddington-OT).
- *Tipo:* mixto.
- *Presupone:* cap. 13.
- *Público:* ambos (la distancia de Hellinger–Kantorovich es de interés teórico).
- *Referencias:* Chizat, Peyré, Schmitzer y Vialard (2018), "Scaling algorithms for unbalanced optimal transport problems", *Math. Comp.*; Liero, Mielke y Savaré (2018), "Optimal entropy-transport problems and a new Hellinger–Kantorovich distance between positive measures", *Invent. Math.*; Schiebinger et al. (2019), "Optimal-transport analysis of single-cell gene expression identifies developmental trajectories in reprogramming", *Cell*.

**16. Distancia de Gromov–Wasserstein**
- *Qué es:* comparar espacios métricos con medida que no viven en un mismo ambiente (formas, grafos); problema cuadrático, versión entrópica y aplicaciones a alineamiento.
- *Tipo:* mixto.
- *Presupone:* caps. 1, 10 y 13.
- *Público:* ambos.
- *Referencias:* Mémoli (2011), "Gromov–Wasserstein distances and the metric approach to object matching", *Found. Comput. Math.*; Peyré, Cuturi y Solomon (2016), "Gromov–Wasserstein averaging of kernel and distance matrices", *ICML*.

**17. Transferencia de color y adaptación de dominio con datos reales**
- *Qué es:* estimar el mapa entre dos distribuciones de píxeles, o de *features*, con la proyección baricéntrica del plan exacto o entrópico, y aplicarlo a imágenes reales o a un problema de clasificación con cambio de dominio.
- *Tipo:* computacional.
- *Presupone:* caps. 9, 12 y 13.
- *Público:* Datos.
- *Referencias:* Pitié, Kokaram y Dahyot (2007), "Automated colour grading using colour distribution transfer", *Comput. Vis. Image Underst.*; Ferradans, Papadakis, Peyré y Aujol (2014), "Regularized discrete optimal transport", *SIAM J. Imaging Sci.*; Courty, Flamary, Tuia y Rakotomamonjy (2017), "Optimal transport for domain adaptation", *IEEE TPAMI*.

**18. Modelos generativos: de WGAN a *flow matching* con acoplamientos óptimos**
- *Qué es:* W₁ como pérdida vía Kantorovich–Rubinstein (y por qué se obtiene una cota inferior), y *flow matching*, donde un acoplamiento óptimo (por minibatches) convierte las trayectorias lineales en interpolaciones de McCann.
- *Tipo:* mixto.
- *Presupone:* caps. 9, 10 y 13.
- *Público:* Datos.
- *Referencias:* Arjovsky, Chintala y Bottou (2017), "Wasserstein generative adversarial networks", *ICML*; Lipman, Chen, Ben-Hamu, Nickel y Le (2023), "Flow matching for generative modeling", *ICLR*; Tong et al. (2024), "Improving and generalizing flow-based generative models with minibatch optimal transport", *TMLR*.
- *Nota:* necesita una presentación mínima de la formulación dinámica. No son flujos gradiente, pero el autor decide si entra.

### 3.4 Lista de reserva (si hay más estudiantes o pedidos específicos)

- Optimización robusta distribucional con bolas de Wasserstein: Mohajerin Esfahani y Kuhn (2018), "Data-driven distributionally robust optimization using the Wasserstein metric...", *Math. Program.*
- *Fairness* vía baricentros: Gordaliza, del Barrio, Gamboa y Loubes (2019), "Obtaining fairness using optimal transport theory", *ICML*.
- Algoritmo de subasta para el problema de asignación: Bertsekas (1988), "The auction algorithm: a distributed relaxation method for the assignment problem", *Ann. Oper. Res.*
- Medias de Fréchet en Wasserstein y registro de procesos puntuales: Panaretos y Zemel (2016), "Amplitude and phase variation of point processes", *Ann. Statist.*
- Estimación estadística de mapas de transporte: Hütter y Rigollet (2021), "Minimax estimation of smooth optimal transport maps", *Ann. Statist.*
- Transporte martingala y cotas de precios de opciones: Beiglböck, Henry-Labordère y Penkner (2013), "Model-independent bounds for option prices—a mass transport approach", *Finance Stoch.*

---

## 4. Sugerencias sobre la organización de las exposiciones

1. **Publicar la lista cuanto antes** (idealmente antes del 26/10) y fijar la elección para el 4/11. Así hay unas 3 semanas de preparación antes de las primeras charlas, hacia el 23–25/11.
2. **Los temas que dependen del cap. 13** (8, 12, 14, 15, 16, 17 y 18) se preparan en paralelo al dictado de ese capítulo. Conviene avisar que las notas del cap. 13 ya están completas y que pueden leerse por adelantado.
3. **Requisito mínimo común**, para mantener el balance entre públicos: toda charla incluye **(i)** un enunciado preciso con la demostración de un caso, y **(ii)** un ejemplo calculado (a mano o en un cuaderno). El peso relativo lo elige cada estudiante según su carrera. Una charla teórica de Matemática puede tener un ejemplo de 5 minutos, y una computacional de Datos, un lema de 10 minutos.
4. **Equilibrio en la asignación.** Si dos estudiantes quieren el mismo tema, son buenos pares para partir los temas 9 (1D frente a d general), 15 (teoría HK frente a aplicación a células) y 18 (WGAN frente a *flow matching*).

---

## 5. Resumen: lo que haría primero

1. **Esta semana:** publicar la lista de 18 temas de exposición (§3), con plazo de elección al 4/11. Es lo que más rinde, porque las exposiciones son la evaluación principal.
2. **Cap. 10, ya:** agregar el corolario de consistencia de medidas empíricas, con prueba de 10 líneas que usa la recíproca en compactos ya demostrada, y la observación de tasas citada. Sumar el ejercicio 1D de tasa n^{-1/2} y `ejc.Wp.muestras` (ya prototipado, 3.6 s) a la próxima entrega. Corregir la observación de WGAN (cota inferior, condición Lipschitz).
3. **Antes de dar el cap. 13:** una página sobre las derivadas de OT_ε (Danskin; conecta con el algoritmo de soporte libre del cap. 12) y media página sobre el sesgo de OT_ε y la divergencia de Sinkhorn, si el autor no la considera una "variante". En clase cuesta unos 30 minutos en total.
4. **Retoques de costo nulo:** utilidad transferible con Shapley–Shubik en el cap. 7, FID en el cap. 9, una frase de complejidad en `obs.sinkhorn.tasa` y verificar la cita a Villani (Teo. 6.9 frente a 7.12) en el cap. 10.
5. **Para la versión siguiente:** cuaderno 07 de aplicaciones con datos reales (a partir de la mejor exposición), sección de medidas empíricas en el cuaderno 04 y, si se quiere, el ejercicio ★ de truncamiento.
6. **Retirado:** aligerar demostraciones, sacar Brunn–Minkowski, la "recíproca general" como defecto y las variantes dentro de las notas.
