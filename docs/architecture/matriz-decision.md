# Matriz de decisión — EcoRecicla AQP

## Alternativas
- **A. Monolito en capas:** una sola aplicación dividida en presentación, lógica de negocio y acceso a datos. Un solo despliegue y una sola base de datos. Es la opción más simple, pero las capas tienden a mezclar la lógica de todos los dominios.
- **B. Monolito modular:** una sola aplicación y un solo despliegue, dividida en módulos de dominio (Recojos, Rutas, Puntos, Distritos, Reportes) con interfaces explícitas entre ellos. Equilibra simplicidad operativa y modificabilidad.
- **C. Microservicios:** servicios pequeños e independientes, cada uno con su propia base de datos, comunicados por HTTP o un broker. Máxima independencia, pero exige mucha operación y despliegues múltiples.

## Criterios y pesos (deben sumar 100 %)
| Criterio              | Peso | Justificación (driver relacionado)                                   |
|-----------------------|------|----------------------------------------------------------------------|
| Modificabilidad       | 30 % | QA-01: atributo crítico (nuevo distrito o regla en ≤ 2 días-persona) |
| Tiempo de entrega     | 25 % | R-01: el MVP debe salir en 1 mes                                     |
| Costo operativo       | 20 % | R-03: presupuesto bajo, un solo servidor                             |
| Simplicidad operativa | 15 % | R-02: solo 2 developers, sin equipo de DevOps                        |
| Escalabilidad         | 10 % | Carga moderada y predecible (una ciudad, pocos miles de usuarios)    |

## Matriz (puntaje 1 = muy malo … 5 = excelente)
| Criterio (peso)              | A. Capas | B. Monolito modular | C. Microservicios |
|------------------------------|----------|---------------------|-------------------|
| Modificabilidad (30 %)       | 2        | 4                   | 5                 |
| Tiempo de entrega (25 %)     | 5        | 4                   | 1                 |
| Costo operativo (20 %)       | 5        | 5                   | 2                 |
| Simplicidad operativa (15 %) | 5        | 4                   | 1                 |
| Escalabilidad (10 %)         | 2        | 3                   | 5                 |
| **Total ponderado**          | **3,80** | **4,10**            | **2,80**          |

Total ponderado = Σ (peso × puntaje).
- A: 0,30×2 + 0,25×5 + 0,20×5 + 0,15×5 + 0,10×2 = 0,60 + 1,25 + 1,00 + 0,75 + 0,20 = 3,80
- B: 0,30×4 + 0,25×4 + 0,20×5 + 0,15×4 + 0,10×3 = 1,20 + 1,00 + 1,00 + 0,60 + 0,30 = 4,10
- C: 0,30×5 + 0,25×1 + 0,20×2 + 0,15×1 + 0,10×5 = 1,50 + 0,25 + 0,40 + 0,15 + 0,50 = 2,80

## Conclusión
Elegimos el monolito modular (B) porque obtiene el mayor puntaje (4,10), es viable en 1 mes para dos developers y protege la modificabilidad, que es el atributo crítico. La segunda mejor alternativa es el monolito en capas (3,80). La IA también recomendó el monolito modular, y el equipo coincide tras revisar los puntajes. Ver [ADR-001](adr/001-estilo-arquitectonico.md).