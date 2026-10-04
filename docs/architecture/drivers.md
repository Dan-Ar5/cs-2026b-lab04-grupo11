# Drivers arquitectónicos — EcoRecicla AQP

## 1. Requisitos funcionales clave
| ID    | Requisito                                                    | Actor         | Prioridad |
|-------|--------------------------------------------------------------|---------------|-----------|
| RF-01 | El vecino solicita el recojo de residuos reciclables         | Vecino        | Alta      |
| RF-02 | El reciclador consulta su ruta del día                       | Reciclador    | Alta      |
| RF-03 | El reciclador confirma el recojo y registra el peso          | Reciclador    | Alta      |
| RF-04 | El vecino acumula puntos y los canjea                        | Vecino        | Media     |
| RF-05 | La municipalidad consulta el reporte de toneladas recicladas | Municipalidad | Media     |
| RF-06 | La municipalidad configura distritos y reglas de puntos      | Municipalidad | Alta      |

## 2. Atributos de calidad (ordenados por prioridad)
1. Modificabilidad — es el atributo crítico: se deben incorporar distritos y reglas de puntos nuevas sin tocar el resto del sistema.
2. Capacidad de interacción (usabilidad) — vecinos y recicladores usan celulares de gama baja y tienen poca experiencia digital.
3. Fiabilidad — no se pueden perder recojos ni duplicar puntos, aun con conexión intermitente.
4. Rendimiento — la ruta y las solicitudes deben cargar rápido con 3G.
5. Seguridad — se manejan direcciones y datos personales de vecinos.

## 3. Restricciones
| ID   | Tipo        | Restricción                                              |
|------|-------------|----------------------------------------------------------|
| R-01 | Plazo       | MVP en producción en 1 mes                               |
| R-02 | Equipo      | 2 developer con experiencia en Python                    |
| R-03 | Presupuesto | Bajo: un solo servidor (VPS) o hosting gratuito          |
| R-04 | Normativa   | Ley 29733 de protección de datos personales              |

## 4. Escenarios de atributos de calidad
| ID    | Atributo        | Fuente        | Estímulo                                            | Entorno               | Artefacto                    | Respuesta                                                  | Medida                                                                 |
|-------|-----------------|---------------|-----------------------------------------------------|-----------------------|------------------------------|------------------------------------------------------------|------------------------------------------------------------------------|
| QA-01 | Modificabilidad | Municipalidad | Pide incorporar un nuevo distrito o regla de puntos | Desarrollo            | Módulo de Puntos y Distritos | Se implementa y despliega sin modificar los demás módulos  | ≤ 2 días-persona                                                       |
| QA-02 | Interacción     | Vecino        | Solicita un recojo desde su celular                 | Celular gama baja, 3G | PWA / interfaz web           | La solicitud queda registrada con confirmación en pantalla | ≤ 4 toques y ≤ 60 s                                                    |
| QA-03 | Fiabilidad      | Reciclador    | Confirma un recojo sin conexión                     | Zona sin señal        | Módulo de Recojos            | El recojo se guarda localmente y se sincroniza después     | 0 recojos perdidos o puntos duplicados; sincroniza ≤ 5 min tras señal  |