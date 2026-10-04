# Borrador de prompts (material para la bitácora)

Fecha: 04/10/2026 · Herramienta: Claude

## Respuesta al Prompt 1
| | A. Monolito en capas | B. Monolito modular | C. Microservicios |
|---|---|---|---|
| Idea | Una app dividida en presentación, lógica y datos | Una app con módulos de dominio e interfaces explícitas | Servicios independientes, cada uno con su base de datos |
| Fortalezas | Muy simple, rápida, costo mínimo | Un solo despliegue, buena modificabilidad | Escala y se despliega por partes |
| Debilidades | La lógica de puntos, distritos y recojos se mezcla | Exige disciplina con los límites entre módulos | Mucha complejidad operativa y de red |
| Riesgos | Cambiar una regla puede romper otras partes | Los módulos se acoplan si nadie vigila | No llega al MVP en 1 mes con 2 personas |
| Favorece | Costo, tiempo, simplicidad | Modificabilidad, costo, tiempo | Escalabilidad, modificabilidad |
| Penaliza | Modificabilidad | Escalabilidad fina | Costo, tiempo, simplicidad operativa |

Recomendación de la IA: B, monolito modular.

## Respuesta al Prompt 2 (riesgos del monolito modular)
| # | Riesgo | Mitigación |
|---|---|---|
| 1 | Los módulos se acoplan en la práctica | Interfaces públicas y revisión de importaciones en la CI |
| 2 | La sincronización offline es difícil (duplicados, conflictos) | IDs únicos generados en el celular y reglas de conflicto |
| 3 | Un solo servidor es punto único de falla | Respaldos automáticos y monitoreo con alertas |
| 4 | Datos personales de vecinos (Ley 29733) | Cifrado, acceso por roles, recolectar solo lo necesario |
| 5 | Un mes puede no alcanzar para todo | Priorizar RF de prioridad alta, dejar lo demás para la versión 2 |