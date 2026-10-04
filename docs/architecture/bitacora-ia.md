# Bitácora de uso de IA — EcoRecicla AQP

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|-------|-------------|------------------|-------------------|------------------------------|----------|
| 1 | 04/10 | Claude | Prompt 1 adaptado: 3 alternativas de estilo para EcoRecicla AQP con 2 developers, 1 mes y presupuesto bajo | Monolito en capas, monolito modular y microservicios; recomendó el monolito modular | Comparamos con R-01, R-02 y R-03: los microservicios no caben en 1 mes con 2 personas; los puntajes de la matriz son estimaciones nuestras, no datos medidos | Aceptada |
| 2 | 04/10 | Claude | Prompt 2: abogado del diablo contra el monolito modular | 5 riesgos (acoplamiento, sincronización offline, punto único de falla, datos personales, plazo) con mitigaciones | Verificamos en import-linter.readthedocs.io que la herramienta comprueba contratos sobre las importaciones entre módulos y se ejecuta con lint-imports (confirmado). Ley 29733: confirmamos en la fuente oficial que su objeto es garantizar el derecho fundamental a la protección de los datos personales (art. 2, num. 6 de la Constitución) (confirmado) | Aceptada con verificación |
| 3 | 04/10 | Claude | Generación de matriz-decision.md con criterios, pesos y puntajes | Tabla con totales 3,85 y 4,25 que no coincidían con el cálculo mostrado debajo | Recalculamos a mano Σ(peso × puntaje): los totales correctos son A = 3,80, B = 4,10, C = 2,80 | Corregida |
| 4 | 04/10 | Claude | Generación de alternativa.puml (monolito en capas) | Código PlantUML que renderizó sin ningún texto (usaba \n dentro de corchetes) | Lo validamos en plantuml.com, vimos el diagrama vacío y usamos una versión con `component "..." as X` | Corregida |
| 5 | 04/10 | Claude | Generación de despliegue.py con Python Diagrams | Script con ícono de Django y Grafana como monitoreo | Nuestra restricción R-02 dice solo Python, no Django. Cambiamos el ícono de Django por Python y dejamos Grafana como monitoreo | Corregida |

## Anexo: prompts completos

### Prompt 1 — Generación de alternativas
Actúa como arquitecto de software senior con experiencia en sistemas para PYMES.
Contexto: plataforma "EcoRecicla AQP" para recolección de residuos reciclables con recicladores formalizados en distritos de Arequipa. Los vecinos solicitan recojo, los recicladores ven su ruta del día y confirman el recojo con el peso, los vecinos acumulan puntos canjeables y la municipalidad ve reportes de toneladas recicladas.
Restricciones: 2 developers con experiencia en Python, presupuesto bajo (un VPS o hosting gratuito), MVP en 1 mes, usuarios con celulares de gama baja y 3G.
Atributo crítico: modificabilidad (agregar un distrito o regla de puntos en <= 2 días-persona sin modificar otros módulos).
Tarea: propón 3 alternativas de estilo arquitectónico. Para cada una indica fortalezas, debilidades, riesgos y qué atributos de calidad favorece o penaliza.
Formato: tabla comparativa en Markdown y, al final, tu recomendación justificada.
No inventes APIs ni capacidades de servicios; si no estás seguro, indícalo.

### Prompt 2 — Crítica adversarial
Ahora actúa como "abogado del diablo". Critica duramente la alternativa que recomendaste: ¿qué supuestos no se cumplen con nuestras restricciones?, ¿qué podría fallar en producción?, ¿qué costo oculto tiene? Enumera los 5 riesgos más graves y, para cada uno, una táctica arquitectónica de mitigación.