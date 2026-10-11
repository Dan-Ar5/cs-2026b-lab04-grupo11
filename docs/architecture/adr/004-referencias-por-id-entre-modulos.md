# ADR-004: Referenciar entre módulos solo por identificador (UUID) para evitar ciclos

- Estado: Propuesto (por confirmar con el equipo)
- Fecha: 2026-10-11
- Decisores: por confirmar (Daniela Choquecondo Aspilcueta y Daniel Bedregal Perez)

## Contexto
El ADR-001 exige que los módulos Recojos, Rutas, Puntos, Distritos y Reportes se comuniquen solo por interfaces públicas y que no haya
dependencias cíclicas, para cumplir la modificabilidad (QA-01: agregar un distrito o una regla de puntos en ≤ 2 días-persona sin tocar otros módulos).
Al diseñar el detalle (Lab 05) aparecieron dos ciclos posibles: Rutas ↔ Recojos (una `Solicitud` que conociera al `Reciclador`, mientras
la `Ruta` agrupa solicitudes) y Recojos ↔ Puntos (Puntos leyendo la `Solicitud` para calcular, y Recojos llamando a Puntos para acreditar).

## Alternativas consideradas
1. Referencias por objeto entre módulos: simple de navegar, pero crea ciclos y acopla los módulos.
2. Referencias por identificador (UUID) y servicios públicos con parámetros primitivos: sin ciclos; hay que consultar por id.
3. Un paquete `compartido` con las entidades comunes: quita el ciclo, pero concentra el acoplamiento en un solo lugar.

## Decisión
Se usa la alternativa 2. `Solicitud` guarda `recicladorId`, `distritoId` y `vecinoId` como UUID; `ServicioPuntos.acreditarPorRecojo()` recibe
`solicitudId`, `vecinoId`, `distritoId` y `pesoKg` (no la `Solicitud`). Las únicas dependencias permitidas son:
rutas → recojos, recojos → distritos, recojos → puntos, reportes → recojos y distritos (solo lectura); infraestructura realiza los puertos.

## Consecuencias
- Positivas: el diagrama de paquetes y los imports reales no tienen ciclos (verificado con pyreverse); Puntos y Distritos se pueden cambiar sin tocar Recojos o Rutas (QA-01).
- Negativas / riesgos: los datos de otro módulo requieren una consulta por id; hay que cuidar la consistencia de los identificadores (se revisarán las importaciones en la CI, como indica el ADR-001).
