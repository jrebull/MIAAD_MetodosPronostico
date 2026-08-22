#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publica un entregable de la materia en este repositorio.

Copia la libreta desde la carpeta de trabajo en iCloud, la valida, añade o
actualiza su sección en el README, hace el commit y empuja a GitHub.

Uso típico:

    ./tools/publicar.py "~/Library/Mobile Documents/.../263483_Rebull_Laboratorio2.ipynb" \\
        --titulo "Suavizamiento exponencial" \\
        --resumen "Ajuste de ETS sobre la serie semestral y comparación contra los baselines."

El número de entregable se deduce del nombre del archivo (Laboratorio2,
Actividad3...); si no aparece, hay que pasarlo con --num.

Validaciones que se corren antes de tocar nada: la libreta abre como nbformat 4,
ninguna celda de código quedó sin salida, ninguna salida es un error y los
contadores de ejecución van en orden. Es exactamente lo que pide la consigna del
curso, así que conviene que falle aquí y no en la revisión.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RAMA = "main"


def _remoto() -> tuple[str, str]:
    """owner/repo tomados del remoto de git, no del nombre de la carpeta local.

    Renombrar el clon no debe cambiar la URL del badge de Colab.
    """
    try:
        url = subprocess.run(["git", "-C", str(REPO), "remote", "get-url", "origin"],
                             capture_output=True, text=True, check=True).stdout.strip()
        m = re.search(r"[:/]([^/:]+)/([^/]+?)(?:\.git)?$", url)
        if m:
            return m.group(1), m.group(2)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return "jrebull", REPO.name


USUARIO, NOMBRE_REPO = _remoto()

BADGE = "https://colab.research.google.com/assets/colab-badge.svg"
COLAB = f"https://colab.research.google.com/github/{USUARIO}/{NOMBRE_REPO}/blob/{RAMA}"

ENCABEZADO_CONTENIDO = "## Contenido"
PATRON_SECCION = re.compile(r"^### (Laboratorio|Actividad|Proyecto) (\d+) · ", re.M)


# ── utilidades ────────────────────────────────────────────────────────────────

class Aborta(Exception):
    """Error previsto: se informa y se sale sin dejar el repo a medias."""


def ok(msg: str) -> None:
    print(f"  \033[32m✓\033[0m {msg}")


def aviso(msg: str) -> None:
    print(f"  \033[33m!\033[0m {msg}")


def paso(msg: str) -> None:
    print(f"\n\033[1m{msg}\033[0m")


def git(*args: str, capturar: bool = False) -> str:
    r = subprocess.run(["git", "-C", str(REPO), *args],
                       capture_output=capturar, text=True, check=True)
    return (r.stdout or "").strip() if capturar else ""


# ── validación de la libreta ──────────────────────────────────────────────────

def valida(ruta: Path, permitir_sin_salida: bool) -> dict:
    """Comprueba que la libreta esté completa y devuelve sus cuentas."""
    try:
        nb = json.loads(ruta.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise Aborta(f"no es JSON válido: {e}")

    if nb.get("nbformat") != 4:
        raise Aborta(f"nbformat {nb.get('nbformat')}; se esperaba 4")

    celdas = nb.get("cells", [])
    codigo = [c for c in celdas if c.get("cell_type") == "code"]
    if not codigo:
        raise Aborta("la libreta no tiene celdas de código")

    sin_salida = [i for i, c in enumerate(celdas)
                  if c.get("cell_type") == "code" and not c.get("outputs")]
    if sin_salida:
        m = f"{len(sin_salida)} celdas de código sin salida (índices {sin_salida[:8]})"
        if permitir_sin_salida:
            aviso(m + "; se continúa por --permitir-sin-salida")
        else:
            raise Aborta(m + ". Ejecútala completa antes de publicar, "
                             "o pasa --permitir-sin-salida si es a propósito")

    errores = [(i, o.get("ename"), o.get("evalue"))
               for i, c in enumerate(celdas) if c.get("cell_type") == "code"
               for o in c.get("outputs", []) if o.get("output_type") == "error"]
    if errores:
        raise Aborta("hay celdas con error: "
                     + "; ".join(f"celda {i}: {n}: {v}" for i, n, v in errores[:3]))

    cuentas = [c.get("execution_count") for c in codigo]
    if cuentas != list(range(1, len(codigo) + 1)):
        aviso(f"los contadores de ejecución no van 1..{len(codigo)}: {cuentas}. "
              "Reinicia el kernel y ejecuta todo si quieres un historial limpio")
    else:
        ok(f"{len(codigo)} celdas de código ejecutadas en orden, todas con salida")

    figuras = sum(1 for c in codigo for o in c.get("outputs", [])
                  if "image/png" in o.get("data", {}))
    impresas = sum(1 for c in codigo
                   if any(o.get("output_type") == "stream" for o in c.get("outputs", [])))
    ok(f"{len(celdas)} celdas en total · {figuras} figuras · {impresas} bloques impresos")
    ok(f"{ruta.stat().st_size / 1_048_576:.2f} MB")

    return {"celdas": len(celdas), "codigo": len(codigo),
            "figuras": figuras, "impresas": impresas}


def titulo_de_la_portada(ruta: Path) -> str | None:
    """Recupera el título grande de la portada, si la libreta lo trae."""
    nb = json.loads(ruta.read_text(encoding="utf-8"))
    for c in nb.get("cells", [])[:3]:
        if c.get("cell_type") != "markdown":
            continue
        fuente = "".join(c.get("source", []))
        m = re.search(r'font-size:3[0-9]px[^>]*>(.*?)</div>', fuente, re.S)
        if m:
            t = re.sub(r"<br\s*/?>", " ", m.group(1))
            t = re.sub(r"<[^>]+>", "", t)
            t = re.sub(r"\s+", " ", t).strip()
            if t:
                return t
    return None


# ── README ────────────────────────────────────────────────────────────────────

def bloque_readme(clase: str, num: int, titulo: str, ruta_rel: str, resumen: str) -> str:
    enlace = f"{COLAB}/{ruta_rel}"
    partes = [f"### {clase} {num} · {titulo}",
              "",
              f"[![Abrir en Colab]({BADGE})]({enlace})",
              ""]
    if resumen:
        partes += [resumen, ""]
    return "\n".join(partes)


def refresca(seccion: str, clase: str, num: int, titulo: str, ruta_rel: str) -> str:
    """Actualiza encabezado y badge de una sección existente, sin tocar su cuerpo.

    El cuerpo de cada entregable se redacta a mano (qué se hace, tablas de
    resultados); regenerarlo lo perdería. Solo se rehacen las dos líneas que
    este script sabe producir.
    """
    lineas = seccion.split("\n")
    for i, l in enumerate(lineas):
        if PATRON_SECCION.match(l + "\n"):
            lineas[i] = f"### {clase} {num} · {titulo}"
        elif l.startswith("[![Abrir en Colab]"):
            lineas[i] = f"[![Abrir en Colab]({BADGE})]({COLAB}/{ruta_rel})"
    if not any(l.startswith("[![Abrir en Colab]") for l in lineas):
        lineas[1:1] = ["", f"[![Abrir en Colab]({BADGE})]({COLAB}/{ruta_rel})"]
    return "\n".join(lineas)


def actualiza_readme(clase: str, num: int, titulo: str, ruta_rel: str,
                     resumen: str, rehacer: bool = False) -> bool:
    """Inserta o reemplaza la sección del entregable. Devuelve True si cambió algo."""
    readme = REPO / "README.md"
    texto = readme.read_text(encoding="utf-8")

    if ENCABEZADO_CONTENIDO not in texto:
        raise Aborta(f"el README no tiene un encabezado «{ENCABEZADO_CONTENIDO}»")

    ini = texto.index(ENCABEZADO_CONTENIDO) + len(ENCABEZADO_CONTENIDO)
    m_fin = re.search(r"^## ", texto[ini:], re.M)
    fin = ini + (m_fin.start() if m_fin else len(texto) - ini)
    cuerpo = texto[ini:fin]

    # Trocea el cuerpo en secciones ### para poder reemplazar u ordenar.
    marcas = [(m.start(), int(m.group(2))) for m in PATRON_SECCION.finditer(cuerpo)]
    secciones: list[tuple[int, str]] = []
    for k, (pos, n) in enumerate(marcas):
        hasta = marcas[k + 1][0] if k + 1 < len(marcas) else len(cuerpo)
        secciones.append((n, cuerpo[pos:hasta].rstrip() + "\n"))

    nueva = bloque_readme(clase, num, titulo, ruta_rel, resumen)
    reemplazo = any(n == num for n, _ in secciones)
    if reemplazo:
        secciones = [(n, (refresca(s, clase, num, titulo, ruta_rel) if not rehacer else nueva)
                      if n == num else s)
                     for n, s in secciones]
    else:
        secciones.append((num, nueva))

    secciones.sort(key=lambda t: t[0])
    cuerpo_nuevo = "\n\n" + "\n".join(s for _, s in secciones).rstrip() + "\n\n"
    texto_nuevo = texto[:ini] + cuerpo_nuevo + texto[fin:]

    if texto_nuevo == texto:
        return False
    readme.write_text(texto_nuevo, encoding="utf-8")
    ok(("sección reemplazada" if reemplazo else "sección añadida") +
       f": «{clase} {num} · {titulo}»")
    return True


# ── principal ─────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Publica un entregable de la materia en este repositorio.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Uso típico:")[1] if "Uso típico:" in __doc__ else None)
    ap.add_argument("libreta", help="ruta al .ipynb ya ejecutado")
    ap.add_argument("--num", type=int, help="número del entregable (si no se deduce del nombre)")
    ap.add_argument("--clase", default="Laboratorio",
                    choices=["Laboratorio", "Actividad", "Proyecto"],
                    help="tipo de entregable (por defecto: Laboratorio)")
    ap.add_argument("--titulo", help="título para el README (por defecto, el de la portada)")
    ap.add_argument("--resumen", default="", help="una o dos frases para el README")
    ap.add_argument("--carpeta", help="carpeta destino (por defecto: <Clase>_<N>)")
    ap.add_argument("--permitir-sin-salida", action="store_true",
                    help="no abortar si alguna celda de código no tiene salida")
    ap.add_argument("--rehacer", action="store_true",
                    help="regenerar la sección del README desde cero, descartando el cuerpo redactado a mano")
    ap.add_argument("--sin-push", action="store_true", help="hacer el commit pero no empujar")
    ap.add_argument("-y", "--si", action="store_true", help="no pedir confirmación")
    a = ap.parse_args()

    origen = Path(a.libreta).expanduser().resolve()
    if not origen.is_file():
        raise Aborta(f"no existe: {origen}")
    if origen.suffix != ".ipynb":
        raise Aborta(f"no es una libreta: {origen.name}")

    num = a.num
    if num is None:
        m = re.search(r"(?:laboratorio|actividad|proyecto)[ _-]?(\d+)", origen.stem, re.I)
        if not m:
            raise Aborta("no pude deducir el número del nombre del archivo; usa --num")
        num = int(m.group(1))

    carpeta = a.carpeta or f"{a.clase}_{num}"
    destino = REPO / carpeta / origen.name
    ruta_rel = f"{carpeta}/{origen.name}"

    paso(f"1 · Validando {origen.name}")
    cuentas = valida(origen, a.permitir_sin_salida)

    titulo = a.titulo or titulo_de_la_portada(origen) or f"{a.clase} {num}"
    ok(f"título: «{titulo}»")

    paso("2 · Plan")
    print(f"  origen   : {origen}")
    print(f"  destino  : {destino.relative_to(REPO)}")
    print(f"  README   : {a.clase} {num} · {titulo}")
    print(f"  Colab    : {COLAB}/{ruta_rel}")
    print(f"  push     : {'no' if a.sin_push else f'origin {RAMA}'}")
    if not a.si:
        if input("\n  ¿Continuar? [s/N] ").strip().lower() not in ("s", "si", "sí", "y"):
            print("  cancelado")
            return 1

    paso("3 · Copiando y actualizando el README")
    destino.parent.mkdir(parents=True, exist_ok=True)
    if origen == destino.resolve():
        ok(f"la libreta ya está en su sitio: {destino.relative_to(REPO)}")
    else:
        shutil.copy2(origen, destino)
        ok(f"copiada a {destino.relative_to(REPO)}")
    actualiza_readme(a.clase, num, titulo, ruta_rel, a.resumen, rehacer=a.rehacer)

    paso("4 · Commit")
    git("add", "--", str(destino.relative_to(REPO)), "README.md")
    if not git("diff", "--cached", "--name-only", capturar=True):
        aviso("no hay cambios que registrar; el repositorio ya estaba al día")
        return 0
    print(git("diff", "--cached", "--stat", capturar=True))

    cuerpo = [f"{a.clase} {num}: {titulo}", ""]
    if a.resumen:
        cuerpo += [a.resumen, ""]
    cuerpo.append(
        f"Las {cuentas['codigo']} celdas de código se ejecutaron en orden y conservan "
        f"su salida: {cuentas['impresas']} bloques de resultados y {cuentas['figuras']} figuras.")
    # Sin trailer de coautoría: el historial atribuye el trabajo al autor.
    git("commit", "-m", "\n".join(cuerpo))
    ok(git("log", "-1", "--oneline", capturar=True))

    if a.sin_push:
        aviso("no se empujó (--sin-push). Cuando quieras: git push origin " + RAMA)
        return 0

    paso("5 · Push")
    git("push", "origin", RAMA)
    ok(f"https://github.com/{USUARIO}/{NOMBRE_REPO}/blob/{RAMA}/{ruta_rel}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Aborta as e:
        print(f"\n\033[31m✗ {e}\033[0m", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"\n\033[31m✗ falló: {' '.join(e.cmd)}\033[0m", file=sys.stderr)
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n  interrumpido")
        sys.exit(130)
