"""Revisión mecánica de las reglas C1-C5 del Lab 05 sobre docs/design y el código de src/.

Uso (desde la raíz del repo):
    pyreverse -o puml -p ecorecicla -d docs/design/img src/recojos src/rutas src/puntos src/distritos src/infraestructura
    python3 tools/verificar_consistencia.py

Es una revisión ingenua a propósito: reporta TODO lo sospechoso y el equipo decide qué es hallazgo real
y qué es falso positivo (ver docs/design/consistencia.md).
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
D = RAIZ / "docs" / "design"


def snake(nombre: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", nombre).lower()


def leer(ruta: Path) -> str:
    return ruta.read_text(encoding="utf-8")


def clases_diseno() -> dict[str, set[str]]:
    clases: dict[str, set[str]] = {}
    actual = None
    for linea in leer(D / "clases.puml").splitlines():
        m = re.match(r"\s*(?:class|interface|enum)\s+(\w+)", linea)
        if m:
            actual = m.group(1)
            clases[actual] = set()
            continue
        op = re.match(r"\s*\+\s*(?:\{static\}\s*)?(\w+)\(", linea)
        if op and actual:
            clases[actual].add(op.group(1))
    return clases


def c1(clases: dict[str, set[str]]) -> list[str]:
    hallazgos = []
    alias = {}
    texto = leer(D / "secuencia-solicitar-recojo.puml")
    for m in re.finditer(r'participant\s+"([^"]+)"\s+as\s+(\w+)', texto):
        alias[m.group(2)] = m.group(1).split("\\n")[0]
    for n, m in enumerate(re.finditer(r"^\s*(\w+)\s+(->>?)\s+(\w+)\s*:\s*(.+)$", texto, re.M), 1):
        origen, _, destino, mensaje = m.groups()
        if destino not in alias:
            continue
        clase = alias[destino]
        op = re.match(r"(\w+)\(", mensaje.strip())
        if clase not in clases:
            hallazgos.append(f"C1 | '{mensaje.strip()}' -> {clase}: la clase no está en el diagrama de clases")
        elif not op or op.group(1) not in clases[clase]:
            hallazgos.append(f"C1 | '{mensaje.strip()}' -> {clase}: no es una operación de {clase}")
    return hallazgos


def c2(clases: dict[str, set[str]]) -> list[str]:
    hallazgos = []
    texto = leer(D / "estados-solicitud.mmd")
    estados = set()
    for m in re.finditer(r"^\s*(\[\*\]|\w+)\s+-->\s+(\[\*\]|\w+)(?:\s*:\s*(.+))?$", texto, re.M):
        a, b, etiqueta = m.groups()
        estados |= {x for x in (a, b) if x != "[*]"}
        op = re.match(r"(\w+)\(", (etiqueta or "").strip())
        if not op or op.group(1) not in clases["Solicitud"]:
            hallazgos.append(f"C2 | transición {a} -> {b} '{(etiqueta or '').strip()}': no es una operación de Solicitud")
    enum = set()
    en_enum = False
    for linea in leer(D / "clases.puml").splitlines():
        if re.match(r"\s*enum\s+EstadoSolicitud", linea):
            en_enum = True
            continue
        if en_enum:
            if "}" in linea:
                break
            if linea.strip():
                enum.add(linea.strip())
    if estados != enum:
        hallazgos.append(f"C2 | estados del diagrama {sorted(estados ^ enum)} no coinciden con la enumeración")
    return hallazgos


def c3() -> list[str]:
    hallazgos = []
    for linea in leer(D / "clases.puml").splitlines():
        if re.search(r"\s(--|\*--|o--)\s", linea) and not linea.strip().startswith("'"):
            if len(re.findall(r'"[^"]+"', linea)) < 2:
                hallazgos.append(f"C3 | asociación sin multiplicidad en ambos extremos: {linea.strip()}")
    return hallazgos


def aristas_paquetes() -> set[tuple[str, str]]:
    texto = leer(D / "paquetes.puml")
    alias = dict((m.group(2), m.group(1).split("\\n")[0]) for m in re.finditer(r'package\s+"([^"]+)"\s+as\s+(\w+)', texto))
    modulos = {"REC", "RUT", "PUN", "DIS", "REP"}
    return {(a, b) for a, b in re.findall(r"^\s*(\w+)\s+\.\.>\s+(\w+)", texto, re.M) if a in modulos and b in modulos}


def hay_ciclo(aristas: set[tuple[str, str]]) -> bool:
    grafo: dict[str, set[str]] = {}
    for a, b in aristas:
        grafo.setdefault(a, set()).add(b)
    visitado, pila = set(), set()

    def dfs(n: str) -> bool:
        visitado.add(n)
        pila.add(n)
        for v in grafo.get(n, ()):
            if v in pila or (v not in visitado and dfs(v)):
                return True
        pila.discard(n)
        return False

    return any(dfs(n) for n in list(grafo) if n not in visitado)


def c4() -> list[str]:
    hallazgos = []
    dis = aristas_paquetes()
    if hay_ciclo(dis):
        hallazgos.append("C4 | el diagrama de paquetes de diseño tiene un ciclo")
    nombre = {"REC": "recojos", "RUT": "rutas", "PUN": "puntos", "DIS": "distritos", "REP": "reportes"}
    diseno = {(nombre[a], nombre[b]) for a, b in dis}
    real_txt = D / "img" / "packages_ecorecicla.puml"
    if not real_txt.exists():
        return hallazgos + ["C4 | falta docs/design/img/packages_ecorecicla.puml (ejecute pyreverse)"]
    real = set()
    for a, b in re.findall(r"^(\S+)\s+-->\s+(\S+)$", leer(real_txt), re.M):
        ma, mb = a.split(".")[0], b.split(".")[0]
        if ma != mb and ma in nombre.values() and mb in nombre.values():
            real.add((ma, mb))
    if hay_ciclo(real):
        hallazgos.append("C4 | los imports reales del código tienen un ciclo")
    for dep in sorted(real - diseno):
        hallazgos.append(f"C4 | el código importa {dep[0]} -> {dep[1]} y el diagrama de paquetes no lo muestra")
    for dep in sorted(diseno - real):
        hallazgos.append(f"C4 | el diagrama muestra {dep[0]} -> {dep[1]} y el código no lo importa")
    return hallazgos


def c5(clases: dict[str, set[str]]) -> list[str]:
    hallazgos = []
    real = leer(D / "img" / "classes_ecorecicla.puml") if (D / "img" / "classes_ecorecicla.puml").exists() else ""
    nombres_real = set(re.findall(r'^class "(?:<color:red>)?(\w+)', real, re.M))
    for c in sorted(set(clases) ^ nombres_real):
        donde = "solo en el diagrama" if c in clases else "solo en el código"
        hallazgos.append(f"C5 | clase {c}: {donde}")
    for c, ops in clases.items():
        bloque = re.search(r'class "(?:<color:red>)?%s(?:</color>)?" as [\w.]+ \{(.*?)\n\}' % c, real, re.S)
        if not bloque:
            continue
        ops_real = set(re.findall(r"^\s+(?:\{abstract\})?(\w+)\(", bloque.group(1), re.M))
        for op in sorted(ops):
            if snake(op) not in ops_real:
                hallazgos.append(f"C5 | {c}.{op}() del diagrama no existe como {snake(op)}() en el código")
        for op in sorted(ops_real):
            if op not in {snake(x) for x in ops}:
                hallazgos.append(f"C5 | {c}.{op}() existe en el código y no en el diagrama")
    return hallazgos


def main() -> int:
    clases = clases_diseno()
    todos = c1(clases) + c2(clases) + c3() + c4() + c5(clases)
    for h in todos:
        print(h)
    print(f"\n{len(todos)} hallazgo(s) para revisar")
    return 0


if __name__ == "__main__":
    sys.exit(main())
