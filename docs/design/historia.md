# Historia de usuario crítica — EcoRecicla AQP (Lab 05)

Caso 10 de la Tabla 7. Cubre RF-01 (solicitar recojo), RF-03 (confirmar recojo con peso) y RF-04 (acumular puntos),
y protege el escenario QA-03 (0 recojos perdidos o puntos duplicados). Módulos del ADR-001 involucrados:
Recojos, Rutas, Puntos y Distritos.

```
HU-01: Como vecino, quiero solicitar el recojo de mis residuos reciclables desde mi celular
       para que un reciclador los recoja y yo acumule puntos.

Criterios de aceptación
- CA-1 (éxito)
  Dado un vecino con un distrito habilitado y al menos un material por recoger,
  cuando solicita el recojo,
  entonces la solicitud queda en estado PENDIENTE, se muestra la confirmación en pantalla
  y se avisa por WhatsApp (de forma asíncrona).
- CA-2 (error)
  Dado un vecino cuyo distrito no está habilitado por la municipalidad,
  cuando solicita el recojo,
  entonces no se crea ninguna solicitud y se muestra el motivo del rechazo.
- CA-3 (puntos sin duplicar)
  Dada una solicitud RECOGIDA, cuando el reciclador registra el peso (aun si sincroniza después, sin señal),
  entonces la solicitud pasa a PESADA, se acreditan los puntos según la regla vigente del distrito
  y la solicitud queda en PUNTOS_ACREDITADOS; una misma solicitud nunca acredita puntos dos veces.
```

## Supuestos (marcados para validar con el docente)
- Los tipos de material (`TipoMaterial`) son papel, cartón, plástico, vidrio y metal. Es un supuesto; el caso solo dice "reciclables".
- El vecino puede cancelar una solicitud mientras esté PENDIENTE o ASIGNADA (estado `CANCELADA`). No figura en los estados sugeridos de la Tabla 7; se agrega para modelar el camino alterno.
- La regla de puntos es un valor de puntos por kilogramo, configurado por distrito (RF-06).
- El cálculo de la ruta usa el servicio de mapas externo del ADR-001; no se modela aquí porque no interviene en esta historia.

## Alcance excluido a propósito (MVP de 1 mes)
- Canje de puntos (parte de RF-04) y reportes de toneladas (RF-05): el módulo Reportes aparece en el diagrama de paquetes, pero no en las clases.
