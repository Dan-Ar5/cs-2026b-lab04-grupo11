# ADR-001: Adoptar un monolito modular para el MVP de EcoRecicla AQP

- Estado: Aceptado
- Fecha: 2026-10-04
- Decisores: Daniela Choquecondo Aspilcueta y Daniel Bedregal Perez

## Contexto
El MVP debe salir en 1 mes (R-01) con 2 developers con experiencia en Python (R-02) y presupuesto bajo, con un solo servidor (R-03). El atributo crítico es la modificabilidad (QA-01): agregar un distrito o una regla de puntos en ≤ 2 días-persona sin tocar otros módulos. Los requisitos RF-01 a RF-06 se agrupan de forma natural en dominios (recojos, rutas, puntos, distritos, reportes).

## Alternativas consideradas
1. Monolito en capas (3,80): simple y barato, pero la lógica de todos los dominios quedaría mezclada y penaliza la modificabilidad.
2. Microservicios (2,80): máxima independencia, pero excede el plazo, el presupuesto y la capacidad operativa de 2 developers.
3. Monolito modular (4,10): elegido.

## Decisión
Usaremos un monolito modular en Python con 5 módulos (Recojos, Rutas, Puntos, Distritos, Reportes). Los módulos se comunican solo mediante interfaces públicas, y las integraciones externas se implementan como adaptadores.

## Consecuencias
- Positivas: un solo despliegue, bajo costo, entrega rápida; la lógica de puntos y distritos queda aislada (QA-01); los módulos podrían extraerse como servicios en el futuro.
- Negativas / riesgos: el equipo debe respetar los límites entre módulos (se revisarán las importaciones en la CI); una falla grave afecta a todo el sistema.