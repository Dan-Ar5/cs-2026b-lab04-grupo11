# Bitácora de uso de IA — Lab 05 (EcoRecicla AQP)

> Registra la sesión del 11/10/2026 en la que se entregó a Claude la guía del Lab 05 y el repositorio del Lab 04 para generar los borradores
> de E1–E8. Cada propuesta se verificó con las reglas C1–C5, renderizando los diagramas y ejecutando el código. El equipo debe leerla y ajustarla
> a lo que realmente hizo cada integrante antes de entregarla. No se ingresaron datos personales de vecinos ni de recicladores en ningún prompt.

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|-------|-------------|------------------|-------------------|------------------------------|----------|
| 1 | 11/10 | Claude | Prompt IA 1 adaptado: historia HU-01 (solicitar recojo), ADR-001 de EcoRecicla AQP y pedido de un diagrama de clases PlantUML con enumeración, puertos y multiplicidades | `historia.md` con 3 criterios y `clases.puml` con 12 clases, 2 interfaces `<<puerto>>` y 2 enumeraciones | Se detectó una composición `CuentaPuntos *-- ReglaPuntos` sin sentido (la regla pertenece al distrito) y se eliminó. Las referencias entre módulos se dejaron por UUID para evitar ciclos (ADR-004). Se marcaron como supuestos `TipoMaterial` y el estado `CANCELADA` | Corregida |
| 2 | 11/10 | Claude | Generación de `secuencia-solicitar-recojo.puml`, `estados-solicitud.mmd` y `paquetes.puml` a partir del diagrama de clases | Tres diagramas con `alt`, `loop`, mensaje asíncrono, 3 guardas y 5 módulos del ADR-001 | Se renderizaron los tres y se revisó que cada mensaje fuera una operación (C1) y que cada transición usara una operación de `Solicitud` (C2). Los 6 estados coinciden con `EstadoSolicitud` | Aceptada |
| 3 | 11/10 | Claude | Generación de `actividades-ruta-diaria.puml` (3 carriles, 2 decisiones y un fork/join) | Código PlantUML que renderizó con "Arma la ruta del día" en el carril del Reciclador en vez de Sistema (el cambio de carril de una rama del `if` se heredó a la otra) | Se vio en el PNG; se agregó `\|Sistema\|` al inicio de la rama "sí" y se volvió a renderizar | Corregida |
| 4 | 11/10 | Claude | Prompt IA 2 (ingeniería directa): esqueleto Python 3.10 con dataclasses, ABC para los puertos y `NotImplementedError` en adaptadores | Código en `src/` para los cinco paquetes | Se corrigió `Ruta.siguiente_parada()` (comparaba con el texto `"ASIGNADA"` en lugar del enum) y se quitaron métodos privados que no estaban en el diagrama (lógica no pedida). Se escribieron 11 pruebas (una por transición y los criterios CA-1 a CA-3): todas pasan | Corregida |
| 5 | 11/10 | Claude + pyreverse | Ingeniería inversa del código y comparación con el diseño | Diagramas `classes_ecorecicla` y `packages_ecorecicla`; 10 diferencias (ver `round-trip.md`) | Dos eran errores del diseño: faltaban `distritoId` en `Solicitud` y `solicitudesAcreditadas` en `CuentaPuntos` (QA-03); se corrigió `clases.puml`. Los imports reales coinciden con el diagrama de paquetes y no hay ciclos | Corregida |
| 6 | 11/10 | Claude + script | Prompt IA 3 (auditor de consistencia C1–C5) apoyado en `tools/verificar_consistencia.py` | 9 sospechas | 5 eran falsos positivos (PWA y controlador no son clases de dominio, transiciones al estado final, operación heredada por el adaptador) y 4 eran diferencias reales sin cambio de diagrama (ver `consistencia.md`) | Aceptada con verificación |

## Anexo: prompts base de la guía (adaptados al caso)

### Prompt IA 1 — Diagrama de clases
Actúa como diseñador de software orientado a objetos. Contexto: módulos Recojos, Rutas, Puntos y Distritos de un monolito modular
(ADR-001: puertos y adaptadores para integraciones externas). Historia y criterios: [pegar historia.md].
Tarea: genera un diagrama de clases en PlantUML con atributos tipados, operaciones, multiplicidades, una enumeración para el estado de la solicitud
y una interfaz (puerto) para el servicio externo de notificaciones (WhatsApp).
Formato: solo el código PlantUML. No agregues clases que no se deriven de la historia; si asumes algo, indícalo en un comentario.

### Prompt IA 2 — Ingeniería directa
Genera el esqueleto en Python 3.10 (dataclasses y type hints) del siguiente diagrama de clases. Respeta exactamente los nombres de clases, atributos y
operaciones (en snake_case), las enumeraciones, las interfaces como clase abstracta (ABC) y las multiplicidades. Implementa solo la lógica mínima de las
operaciones de la Solicitud; los adaptadores deben lanzar NotImplementedError. [pegar clases.puml]

### Prompt IA 3 — Auditor de consistencia
Actúa como revisor de diseño. Te paso cinco diagramas UML en PlantUML/Mermaid: [pegar los cinco archivos]. Verifica estas reglas y responde en una tabla
(regla, elemento, problema, corrección sugerida): C1 cada mensaje de secuencia es una operación de la clase receptora; C2 cada transición de estados
corresponde a una operación de la clase; C3 multiplicidades coherentes con los criterios de aceptación; C4 paquetes sin ciclos; C5 nombres consistentes.
No reescribas los diagramas; solo reporta hallazgos y cita la línea.
