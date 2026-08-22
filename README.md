<div align="center">

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Escudo_UACJ.svg/500px-Escudo_UACJ.svg.png" width="112" alt="Escudo de la Universidad Autónoma de Ciudad Juárez">

<h1>Métodos para Pronóstico y Analítica Avanzada</h1>

<p>
<b>Maestría en Inteligencia Artificial y Analítica de Datos</b><br>
Instituto de Ingeniería y Tecnología · Departamento de Ingeniería Eléctrica y Computación<br>
Universidad Autónoma de Ciudad Juárez
</p>

<p>
<img src="https://img.shields.io/badge/Semestre-2026--2-003DA6?style=flat-square">
<img src="https://img.shields.io/badge/Python-3.x-003DA6?style=flat-square&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/Entorno-Google%20Colab-B87E00?style=flat-square&logo=googlecolab&logoColor=white">
</p>

</div>

---

Entregables de la asignatura, resueltos y documentados. Cada libreta se ejecuta de principio a fin en Google Colab sin instalar nada: solo `numpy`, `pandas` y `matplotlib`.

| Dato | Valor |
|---|---|
| Asignatura | Métodos para Pronóstico y Analítica Avanzada |
| Programa | Maestría en Inteligencia Artificial y Analítica de Datos (MIAAD) |
| Institución | Universidad Autónoma de Ciudad Juárez |
| Periodo | Semestre 2026-2, agosto a diciembre de 2026 |
| Estudiante | Javier Augusto Rebull Saucedo |
| Docente | César Alonso Rivas Flores |

## Contenido

### Laboratorio 1 · Del dato histórico a una decisión de pronóstico

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jrebull/MIAAD_MetodosPronostico/blob/main/Laboratorio_1/263483_Rebull_Laboratorio1.ipynb)

Recorrido completo desde una serie observada hasta una decisión operativa, sobre un caso didáctico de deserción escolar agregada con 24 observaciones semestrales.

**Qué se hace**

1. Verificación de calidad y orden temporal de la serie.
2. Formulación del problema con un canvas de ocho elementos: decisión, variable, unidad, frecuencia, origen, horizonte, usuario y error más costoso.
3. Lectura de nivel, tendencia, estacionalidad y ruido, primero visual y después cuantificada.
4. Partición temporal sin fuga de información y dos baselines: naïve, $\hat{y}_t = y_{t-1}$, y estacional, $\hat{y}_t = y_{t-2}$.
5. Error periodo a periodo, MAE, RMSE y MAPE, y un costo asimétrico que penaliza el doble subestimar.
6. Validación *rolling-origin* sobre diez orígenes consecutivos.
7. Pronóstico de referencia y decisión de capacidad, separados de forma explícita.
8. Anexo voluntario: corrección del sesgo con una deriva estacional reestimada en cada origen.

**Resultados principales**

| Método | MAE prueba | RMSE prueba | MAPE prueba | MAE *rolling-origin* |
|---|---:|---:|---:|---:|
| Naïve | 5.25 | 5.41 | 8.09 % | 4.50 |
| Estacional | **2.25** | **2.29** | **3.48 %** | **2.30** |
| Estacional con deriva (anexo A) | n/d | n/d | n/d | 0.36 |

El anexo evalúa la variante con deriva solo bajo el esquema *rolling-origin*, que es donde la deriva se reestima en cada origen; de ahí las celdas sin dato. Su MAE de 0.36 es espectacular en buena medida porque la serie es simulada y su tendencia es casi perfectamente lineal, cosa que la propia libreta advierte.

El baseline estacional gana en nueve de los diez orígenes y empata en el restante. El pronóstico de referencia para 2027-1 es de **62 deserciones** y la decisión recomendada es reservar capacidad para **65**, es decir, el pronóstico más un margen igual al MAE histórico. Pronóstico y decisión se reportan por separado a propósito: el margen es una regla de decisión transparente, no un intervalo de predicción.

### Laboratorio 2 · Del dato observado al pronóstico con SMA, WMA y EMA

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jrebull/MIAAD_MetodosPronostico/blob/main/Laboratorio_2/263483_Rebull_Laboratorio2_Suavizado.ipynb)

Doce semanas de solicitudes recibidas por una oficina de atención ciudadana, usadas para separar dos cosas que se confunden a menudo: describir el pasado y anticipar la semana que todavía no ocurre.

**Qué se hace**

1. Lectura de la serie antes de aplicar método alguno: dirección, avance medio y retrocesos.
2. Los tres métodos vistos como un reparto de pesos sobre el pasado, y el **retraso medio** que ese reparto implica: 1.00 semanas el SMA, 0.70 el WMA y 2.33 la EMA con $\alpha = 0.3$.
3. Valores suavizados, que usan el dato de su propia semana.
4. Conversión a pronósticos de un paso con `.shift(1)`, que es donde el retraso deja de ser gratis.
5. Comparación en una ventana común a los cinco métodos, con MAE, RMSE y sMAPE, más el error medio con signo.
6. Los mismos métodos sobre cuatro series construidas con estructuras distintas.
7. Selección de $\alpha$ con validación temporal y una única evaluación en prueba.
8. Anexo voluntario: se pone a prueba un ciclo aparente y se corrige el retraso del SMA con una deriva estimada solo con el pasado de cada origen.

**Resultados principales**

Ventana común de nueve semanas, de la 4 a la 12, idéntica para los cinco métodos.

| Método | RMSE | MAE | Error medio con signo |
|---|---:|---:|---:|
| Ingenuo | **5.33** | **4.89** | +3.11 |
| WMA | 5.84 | 5.09 | +4.96 |
| SMA | 6.37 | 5.78 | +5.78 |
| Estacional de periodo 2 | 6.57 | 5.56 | +5.56 |
| EMA, $\alpha = 0.3$ | 9.02 | 8.51 | +8.51 |

**Ningún método de suavizado supera a repetir el último dato.** El error medio es positivo en los cinco: todos se quedan cortos, siempre. Y el orden del sesgo reproduce el del retraso, porque la serie sube 3.09 solicitudes por semana y cada semana de retraso se paga en solicitudes que el pronóstico deja de contar.

Que el ganador depende de la estructura se comprueba sobre cuatro series sintéticas:

| Serie | Menor RMSE | Por qué |
|---|---|---|
| Tendencia pura | Ingenuo, 2.00 | Es el de menor retraso; su error es exactamente el incremento por periodo |
| Nivel estable | EMA, 1.13 | Sin tendencia el retraso no cuesta y promediar cancela ruido |
| Tendencia y periodo 2 | Estacional 2, 2.00 | Reproduce la alternancia; solo le queda el avance de dos periodos |
| Estacionalidad periodo 2 | Estacional 2, 0.00 | El dato de dos periodos atrás *es* el que se quiere predecir |

Los suavizados quedan por detrás de una referencia simple en tres de las cuatro series.

La selección de $\alpha$ eligió **0.05**, el valor más pequeño de la rejilla, y la curva de validación resulta monótona creciente: el mínimo cae en el borde, no en un punto interior. En la prueba final, periodos 17 a 20, rinde RMSE 1.178 frente a 1.258 del $\alpha = 0.3$ fijado al inicio y 1.323 del ingenuo. Promediar toda la historia disponible rinde 1.125, que es mejor todavía; la libreta lo reporta como límite del procedimiento en vez de presentar el 0.05 como un parámetro bien estimado.

El anexo cierra dos cabos. El ciclo de tres semanas que insinuaban los retrocesos **no se sostiene**: una referencia que repite el dato de tres semanas atrás da el peor RMSE del anexo, 8.46. En cambio el diagnóstico del retraso sí era correcto: sumando al SMA la deriva estimada con el pasado de cada origen, el RMSE baja de 6.02 a **3.56** y el sesgo pasa de +5.42 a −0.54. Con esa corrección el suavizado sí supera al ingenuo, sobre ocho semanas comparables.

## Cómo abrir las libretas

- **En Colab:** pulsa el badge de la libreta. No requiere clonar el repositorio.
- **En local:** `jupyter lab` sobre el `.ipynb`. Dependencias: `numpy`, `pandas`, `matplotlib`.

Las libretas se entregan ya ejecutadas, así que todas las celdas conservan su salida y pueden leerse sin correr nada.

## Publicar un entregable

<details>
<summary><code>tools/publicar.py</code> copia la libreta, la valida, actualiza este README, hace el commit y empuja.</summary>

<br>

```bash
./tools/publicar.py "~/Library/Mobile Documents/com~apple~CloudDocs/.../263483_Rebull_Laboratorio2.ipynb" \
    --titulo "Suavizamiento exponencial" \
    --resumen "Ajuste de ETS sobre la serie semestral y comparación contra los baselines."
```

El número del entregable se deduce del nombre del archivo y el título, de la portada de la libreta, así que en el caso normal basta con la ruta.

> **Cada libreta vive en su carpeta** `<Clase>_<N>/`, que es a donde apuntan los badges de arriba. Si guardas desde Colab con *Guardar una copia en GitHub*, indica esa misma carpeta en la ruta del archivo: dejarla en la raíz crea una segunda copia que acaba divergiendo de la de trabajo.

Antes de tocar nada comprueba que la libreta abra como `nbformat` 4, que **ninguna celda de código se haya quedado sin salida**, que no haya salidas de error y que los contadores de ejecución vayan en orden. Es lo mismo que pide la consigna del curso, y conviene que falle aquí y no en la revisión.

Si el entregable ya tiene sección en el README, solo refresca el encabezado y el badge: el cuerpo redactado a mano se conserva. Con `--rehacer` se regenera desde cero.

| Opción | Para qué |
|---|---|
| `--num N` | forzar el número si no aparece en el nombre del archivo |
| `--clase` | `Laboratorio` (por defecto), `Actividad` o `Proyecto` |
| `--titulo`, `--resumen` | texto de la sección del README |
| `--carpeta` | carpeta destino, por defecto `<Clase>_<N>` |
| `--permitir-sin-salida` | seguir aunque falte alguna salida |
| `--rehacer` | regenerar la sección del README completa |
| `--sin-push` | dejar el commit sin empujar |
| `-y` | no pedir confirmación |

</details>

## Aviso sobre los datos

> Los casos de ambos laboratorios utilizan **datos didácticos, construidos para el ejercicio**. Las cifras no representan registros de la Universidad Autónoma de Ciudad Juárez ni deben interpretarse como resultados institucionales. Reproducen la *forma* de una serie real (deserción agregada en el primero, demanda de un servicio en el segundo) para practicar el razonamiento de pronóstico, no para estimar nada del mundo real. Las cuatro series comparativas del Laboratorio 2 son deterministas por diseño.

Las libretas parten de las plantillas que entrega el docente y lo que aquí se publica son las respuestas, el análisis y las figuras del estudiante. El material didáctico original del curso (consignas en formato editable, presentaciones y lecturas) es del docente y no se redistribuye en este repositorio.

## Referencias principales

- Hyndman, R. J. y Athanasopoulos, G. (2021). *Forecasting: Principles and Practice*, 3.ª ed. OTexts. <https://otexts.com/fpp3/>
- Hyndman, R. J. y Koehler, A. B. (2006). Another look at measures of forecast accuracy. *International Journal of Forecasting*, 22(4), 679–688. <https://doi.org/10.1016/j.ijforecast.2006.03.001>
- Tashman, L. J. (2000). Out-of-sample tests of forecasting accuracy: an analysis and review. *International Journal of Forecasting*, 16(4), 437–450. <https://doi.org/10.1016/S0169-2070(00)00065-0>
- Brown, R. G. (1963). *Smoothing, Forecasting and Prediction of Discrete Time Series*. Prentice-Hall. Origen de la forma recursiva del suavizado exponencial.
- Makridakis, S., Spiliotis, E. y Assimakopoulos, V. (2020). The M4 Competition: 100,000 time series and 61 forecasting methods. *International Journal of Forecasting*, 36(1), 54–74. <https://doi.org/10.1016/j.ijforecast.2019.04.014>
- Bergmeir, C. y Benítez, J. M. (2012). On the use of cross-validation for time series predictor evaluation. *Information Sciences*, 191, 192–213. <https://doi.org/10.1016/j.ins.2011.12.028>

La bibliografía completa, numerada por orden de primera aparición, va dentro de cada libreta.
