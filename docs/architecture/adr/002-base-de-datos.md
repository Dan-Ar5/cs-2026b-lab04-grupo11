# ADR-002: Usar PostgreSQL como base de datos

- Estado: Aceptado
- Fecha: 2026-10-04
- Decisores: Daniela Choquecondo Aspilcueta y Daniel Bedregal Perez

## Contexto
El sistema registra recojos, pesos, puntos y datos personales de vecinos (R-04). La fiabilidad exige no perder recojos ni duplicar puntos (QA-03), y los reportes de toneladas por distrito (RF-05) requieren consultas agregadas. Con presupuesto bajo (R-03) conviene una sola base de datos en el mismo servidor.

## Alternativas consideradas
1. Base de datos documental (por ejemplo MongoDB): flexible, pero con transacciones y consultas agregadas menos naturales para este caso.
2. PostgreSQL con un esquema por módulo: relacional, con transacciones y buen soporte para reportes.

## Decisión
Usaremos PostgreSQL, con un esquema por módulo para mantener los datos separados.

## Consecuencias
- Positivas: transacciones que evitan duplicar puntos o recojos; reportes con SQL; un solo motor que operar y respaldar.
- Negativas / riesgos: el esquema relacional requiere migraciones al cambiar datos; el servidor único es un punto de falla, por lo que se necesitan respaldos periódicos.