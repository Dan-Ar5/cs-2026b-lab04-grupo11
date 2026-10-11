# Revisión de consistencia C1–C5 (E7)

**Cómo se hizo:** revisión del asistente de IA (Prompt IA 3) apoyada en una revisión mecánica y deliberadamente ingenua
(`tools/verificar_consistencia.py`) que reporta todo lo sospechoso. Salida real del script: **9 sospechas** sobre los cinco diagramas
y el código. Cada una se verificó a mano; el resultado es el siguiente.

## Hallazgos y verificación del equipo

| Regla | Hallazgo de la IA / script | Verificación del equipo | Veredicto |
|-------|----------------------------|-------------------------|-----------|
| C1 | `Solicitar recojo (...)` → PWA: la clase no está en el diagrama de clases. | La PWA y el `SolicitudController` son líneas de vida de frontera (interfaz y API REST), no clases de dominio; el diagrama de clases solo modela el interior de los módulos. Los 6 mensajes dirigidos a clases de dominio (`estaHabilitado`, `crear`, `agregarItem`, `guardar`, `notificarSolicitudRegistrada`, `solicitarRecojo`) sí son operaciones. | **Falso positivo** |
| C1 | `POST /solicitudes` → SolicitudController: la clase no está en el diagrama. | Igual que el anterior: es un mensaje HTTP hacia la capa de presentación. | **Falso positivo** |
| C2 | Transiciones `PUNTOS_ACREDITADOS → [*]` y `CANCELADA → [*]` no tienen operación. | Una transición hacia el estado final de UML no la provoca un evento de la clase; las operaciones que cierran el ciclo son `acreditarPuntos()` y `cancelar()`, ya presentes. Los 6 estados coinciden con la enumeración `EstadoSolicitud`. | **Falso positivo** |
| C3 | Ninguno: todas las asociaciones tienen multiplicidad en ambos extremos. | Se confirma; la regla `1..*` (Solicitud–ItemSolicitud) además se valida en código y se prueba. | Sin hallazgo |
| C4 | El diagrama muestra `reportes → recojos` y `reportes → distritos`, pero el código no los importa. | Reportes (RF-05) queda fuera de HU-01 y no tiene código en esta práctica. | **Real, aceptado** (el diagrama de diseño se mantiene) |
| C4 | Ciclos en paquetes. | Ninguno, ni en el diseño ni en los imports reales; las referencias entre módulos son por UUID (ADR-004). | Sin hallazgo |
| C5 | Clases `DistritoNoHabilitado` y `TransicionInvalida` existen solo en el código. | Son excepciones que implementan CA-2 y las transiciones inválidas; no se modelan en el diagrama. | **Real, documentado** (ver `round-trip.md`, fila 7) |
| C5 | `WhatsAppAdapter.notificar_solicitud_registrada()` existe en el código y no en el diagrama. | El adaptador realiza el puerto `Notificador`: hereda su operación; el diagrama muestra la realización. La herramienta no resuelve la herencia. | **Falso positivo** |
| C5 | Nombres snake_case frente a camelCase. | Todas las operaciones del diagrama tienen su equivalente en snake_case en el código (convención de Python). | Sin hallazgo |

## Resumen

- 9 sospechas revisadas: **5 falsos positivos** de la herramienta (2 de C1, 2 de C2 y 1 de C5) y **4 diferencias reales** que se documentaron sin cambiar ningún diagrama (2 de C4 por Reportes sin código y 2 de C5 por las excepciones solo presentes en el código).
- **Qué habría pasado de aceptarlos sin verificar:** se habría forzado a agregar la PWA y el controlador como clases de dominio (contaminando el diagrama con la capa de presentación) y a inventar operaciones para las transiciones a estado final.
- Los hallazgos que sí cambiaron el diseño salieron del round-trip, no de esta revisión (`distritoId` y `solicitudesAcreditadas`; ver `round-trip.md`, fila 3).
