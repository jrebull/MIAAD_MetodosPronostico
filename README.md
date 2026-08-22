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

> El caso del Laboratorio 1 utiliza **datos simulados exclusivamente con fines didácticos**. Las cifras no representan registros de la Universidad Autónoma de Ciudad Juárez ni deben interpretarse como resultados institucionales. Reproducen la *forma* de una serie de deserción agregada para practicar el razonamiento de pronóstico, no para estimar la deserción real de la institución.

Las libretas parten de las plantillas que entrega el docente y lo que aquí se publica son las respuestas, el análisis y las figuras del estudiante. El material didáctico original del curso (consignas en formato editable, presentaciones y lecturas) es del docente y no se redistribuye en este repositorio.

## Referencias principales

- Hyndman, R. J. y Athanasopoulos, G. (2021). *Forecasting: Principles and Practice*, 3.ª ed. OTexts. <https://otexts.com/fpp3/>
- Hyndman, R. J. y Koehler, A. B. (2006). Another look at measures of forecast accuracy. *International Journal of Forecasting*, 22(4), 679–688. <https://doi.org/10.1016/j.ijforecast.2006.03.001>
- Tashman, L. J. (2000). Out-of-sample tests of forecasting accuracy: an analysis and review. *International Journal of Forecasting*, 16(4), 437–450. <https://doi.org/10.1016/S0169-2070(00)00065-0>
- Bergmeir, C. y Benítez, J. M. (2012). On the use of cross-validation for time series predictor evaluation. *Information Sciences*, 191, 192–213. <https://doi.org/10.1016/j.ins.2011.12.028>

La bibliografía completa, numerada por orden de primera aparición, va dentro de cada libreta.
