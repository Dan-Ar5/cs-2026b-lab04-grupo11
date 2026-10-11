# EcoRecicla AQP — Laboratorio 04: Fundamentos de arquitectura de software
Construcción de Software · EPIS-UNSA · 2026-B · Grupo 11

## Integrantes
| Nombre | Rol en el laboratorio |
|--------|-----------------------|
| Daniela Choquecondo Aspilcueta | Redacción de drivers, matriz de decisión, ADR y diagramas; gestión del repositorio y uso de IA |
| Daniel Bedregal Perez | Revisión y aprobación de Pull Requests; verificación de la bitácora de IA y de los diagramas |

## Caso
EcoRecicla AQP es una plataforma web (PWA) para el recojo de residuos reciclables con recicladores formalizados en distritos de Arequipa. Los vecinos solicitan recojos y acumulan puntos canjeables, los recicladores consultan su ruta del día y confirman el recojo con el peso, y la municipalidad configura distritos y reglas de puntos y consulta reportes de toneladas recicladas. El atributo de calidad crítico es la **modificabilidad**: incorporar un nuevo distrito o una nueva regla de puntos en ≤ 2 días-persona, sin modificar los demás módulos.

## Arquitectura elegida
Monolito modular (puntaje 4,10 en la [matriz de decisión](docs/architecture/matriz-decision.md)).

```mermaid
flowchart TB
    VE["Vecino"]
    RE["Reciclador"]
    MU["Municipalidad"]
    subgraph APP["EcoRecicla AQP — Monolito modular (un solo despliegue)"]
        API["Capa de presentación: API REST + PWA"]
        M1["Recojos"]
        M2["Rutas"]
        M3["Puntos"]
        M4["Distritos"]
        M5["Reportes"]
        INF["Capa de infraestructura: repositorios y adaptadores externos"]
    end
    DB[("PostgreSQL<br/>(un esquema por módulo)")]
    WA["WhatsApp / Notificaciones (servicio externo)"]
    MAPS["Servicio de mapas (servicio externo)"]
    VE & RE & MU --> API
    API --> M1 & M2 & M3 & M4 & M5
    M1 & M2 & M3 & M4 & M5 --> INF
    INF --> DB
    INF --> WA
    INF --> MAPS
    classDef mod fill:#E8F5E9,stroke:#2E7D32,color:#000
    classDef ext fill:#F2F2F2,stroke:#7F7F7F,color:#000,stroke-dasharray: 4 3
    classDef usr fill:#FDEDEC,stroke:#C8310E,color:#000
    class M1,M2,M3,M4,M5 mod
    class WA,MAPS ext
    class VE,RE,MU usr
```

## Documentación
- [Drivers y escenarios de calidad](docs/architecture/drivers.md)
- [Matriz de decisión](docs/architecture/matriz-decision.md)
- [Bitácora de uso de IA](docs/architecture/bitacora-ia.md)
- Diagramas: [Mermaid](docs/architecture/diagramas/arquitectura.mmd), [PlantUML (alternativa descartada)](docs/architecture/diagramas/alternativa.puml) y [vista de despliegue](docs/architecture/diagramas/despliegue.py)

## Decisiones arquitectónicas
- [ADR-001: Estilo arquitectónico (monolito modular)](docs/architecture/adr/001-estilo-arquitectonico.md)
- [ADR-002: Base de datos (PostgreSQL)](docs/architecture/adr/002-base-de-datos.md)
- [ADR-003: PWA con sincronización offline](docs/architecture/adr/003-pwa-offline.md)

## Reflexión sobre el uso de la IA
La IA nos ayudó a generar rápido las alternativas de arquitectura, los borradores de los documentos y el código de los diagramas, y a ver riesgos que no habíamos considerado, como la sincronización sin conexión. Pero cometió errores que tuvimos que detectar: la matriz entregó totales que no coincidían con el cálculo de pesos por puntajes, el primer código de PlantUML se dibujó sin ningún texto, y el script de despliegue usaba Django aunque nuestra restricción solo menciona Python. También nos sirvió para comprobar que una recomendación no se acepta sin verificarla. Verificamos en fuentes oficiales que import-linter controla importaciones entre módulos y que la Ley 29733 protege los datos personales. Aprendimos a recalcular a mano, a validar cada diagrama en su editor y a contrastar las propuestas de la IA con nuestras restricciones reales de plazo, equipo y presupuesto.

## Diseño UML (Lab 05)
Historia crítica: **HU-01, solicitar el recojo de reciclables** ([historia.md](docs/design/historia.md)). Máquina de estados de la `Solicitud`:

```mermaid
stateDiagram-v2
    [*] --> PENDIENTE : crear()
    PENDIENTE --> ASIGNADA : asignar() [reciclador de la ruta del distrito]
    ASIGNADA --> RECOGIDA : confirmarRecojo()
    RECOGIDA --> PESADA : registrarPeso() [pesoKg > 0]
    PESADA --> PUNTOS_ACREDITADOS : acreditarPuntos() [no acreditada antes]
    PENDIENTE --> CANCELADA : cancelar()
    ASIGNADA --> CANCELADA : cancelar()
    PUNTOS_ACREDITADOS --> [*]
    CANCELADA --> [*]
```

| Entregable | Código fuente | Imagen |
|---|---|---|
| E1 Clases | [clases.puml](docs/design/clases.puml) | [PNG](docs/design/img/clases-ecorecicla.png) |
| E2 Secuencia | [secuencia-solicitar-recojo.puml](docs/design/secuencia-solicitar-recojo.puml) | [PNG](docs/design/img/secuencia-solicitar-recojo.png) |
| E3 Estados | [estados-solicitud.mmd](docs/design/estados-solicitud.mmd) | [PNG](docs/design/img/estados-solicitud.png) |
| E4 Actividades | [actividades-ruta-diaria.puml](docs/design/actividades-ruta-diaria.puml) | [PNG](docs/design/img/actividades-ruta-diaria.png) |
| E5 Paquetes | [paquetes.puml](docs/design/paquetes.puml) | [PNG](docs/design/img/paquetes.png) |
| E6 Round-trip | [round-trip.md](docs/design/round-trip.md), código en [src/](src/) | [clases](docs/design/img/classes_ecorecicla.png), [paquetes](docs/design/img/packages_ecorecicla.png) |
| E7 Consistencia e IA | [consistencia.md](docs/design/consistencia.md), [bitacora-ia.md](docs/design/bitacora-ia.md) | — |

Decisión nueva: [ADR-004: referencias entre módulos por identificador](docs/architecture/adr/004-referencias-por-id-entre-modulos.md).
