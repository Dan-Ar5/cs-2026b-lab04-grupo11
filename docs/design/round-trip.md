# Round-trip: del diagrama al código y de vuelta (E6)

**Ingeniería directa:** `clases.puml` → esqueleto Python 3.10+ (dataclasses y type hints) en `src/{recojos,rutas,puntos,distritos,infraestructura}/`.
Los puertos son clases abstractas (ABC) y los adaptadores/servicios sin implementar lanzan `NotImplementedError`.

**Ingeniería inversa** (desde la raíz del repo):

```bash
pip install pylint
pyreverse -o puml -p ecorecicla -d docs/design/img \
  src/recojos src/rutas src/puntos src/distritos src/infraestructura
java -jar plantuml.jar -tpng docs/design/img/classes_ecorecicla.puml docs/design/img/packages_ecorecicla.puml
```

Resultado: `img/classes_ecorecicla.png` y `img/packages_ecorecicla.png` (pyreverse analizó 14 módulos).
Las 11 pruebas de `tests/test_solicitud.py` pasan (`python3 -m unittest discover -s tests`).

## Tabla de diferencias código-diagrama

| # | Diferencia observada | Causa | Acción |
|---|----------------------|-------|--------|
| 1 | No aparecen la composición `Solicitud`–`ItemSolicitud`, la agregación `Ruta`–`Solicitud` ni la asociación `Vecino`–`Solicitud`: el código tiene `items: list[ItemSolicitud]`, `paradas: list[Solicitud]` y `vecino_id: UUID`. | pyreverse no infiere asociaciones desde colecciones tipadas ni desde identificadores (`UUID`). Además, entre módulos las referencias son por identificador (ADR-004). | Ninguna: limitación de la herramienta; el diagrama de diseño se mantiene. |
| 2 | No hay multiplicidades en ninguna relación. | El código no expresa multiplicidades. | Se agregó la validación de `1..*` en `Solicitud.asignar()` y en `ServicioRecojos.solicitar_recojo()` (C3) y una prueba (`test_asignar_sin_items_falla_c3`). |
| 3 | `Solicitud` tiene el atributo `distrito_id` y `CuentaPuntos` tiene `solicitudes_acreditadas`; ninguno estaba en el diagrama de clases. | El diseño omitió el distrito de la solicitud (necesario para la regla de puntos) y el control de acreditaciones que exige QA-03 (0 puntos duplicados). | **Corregir el diagrama:** se agregaron `distritoId` a `Solicitud` y `solicitudesAcreditadas` a `CuentaPuntos` en `clases.puml`. |
| 4 | `Notificador` y `RepositorioSolicitudes` aparecen como clases con métodos abstractos, no como interfaces `<<puerto>>`. | Python implementa interfaces con ABC. | Aceptable en Python; se documenta. |
| 5 | `ServicioDistritos`, `ServicioPuntos` y `WhatsAppAdapter` muestran sus operaciones como abstractas (cursiva) aunque son clases concretas. | pyreverse trata como abstracto un método que solo lanza `NotImplementedError`. | Documentar; desaparecerá cuando se implementen con su repositorio. |
| 6 | No se ven las dependencias de `ServicioRecojos` hacia `Solicitud`, los puertos y los servicios de Distritos y Puntos. | pyreverse no dibuja dependencias por parámetros ni por inyección en el constructor (atributos privados filtrados). | Documentar. Los imports reales sí se comprueban en el diagrama de paquetes inverso (ver abajo). |
| 7 | Aparecen `DistritoNoHabilitado` y `TransicionInvalida` (en rojo, por heredar de `Exception`); no existen en el diagrama. | El código necesita excepciones para CA-2 y para transiciones inválidas; el diagrama no las modela a propósito. | Documentar; las excepciones no se modelan en este laboratorio. |
| 8 | `Ruta` apunta a `Reciclador` (atributo `reciclador`); en el diseño la asociación es `Reciclador 1 -- 0..* Ruta`, sin navegabilidad. | La implementación eligió navegar de `Ruta` a `Reciclador`. | Aceptable; se documenta la dirección de navegación. |
| 9 | Se pierden visibilidad (+/−), estereotipos (`<<servicio>>`, `<<puerto>>`, `<<adaptador>>`) y la agrupación por paquetes; `{static}` de `crear()` no se marca. | pyreverse muestra solo nombres públicos y tipos; los paquetes van en otro diagrama. | Documentar. |
| 10 | Nombres en snake_case (`agregar_item`, `registrar_peso`) frente a camelCase en el diagrama. | Convención de Python. | Aceptable; se documenta la equivalencia (C5). |

## Paquetes (C4): diseño frente a imports reales

| Dependencia | Diagrama de paquetes | Imports reales (pyreverse) |
|-------------|:--------------------:|:--------------------------:|
| rutas → recojos | sí | sí |
| recojos → distritos | sí | sí |
| recojos → puntos | sí | sí |
| infraestructura → recojos (realiza puertos) | sí | sí |
| reportes → recojos / distritos | sí | no (el módulo no tiene código: fuera del alcance de HU-01) |

Ni el diseño ni el código tienen ciclos.
