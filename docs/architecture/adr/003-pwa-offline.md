# ADR-003: Usar una PWA con sincronización offline en lugar de una app nativa

- Estado: Aceptado
- Fecha: 2026-10-04
- Decisores: Daniela Choquecondo Aspilcueta y Daniel Bedregal Perez

## Contexto
Vecinos y recicladores usan celulares de gama baja con 3G y poca experiencia digital (QA-02). Los recicladores deben confirmar recojos aun sin señal, sin perder datos (QA-03, RF-03). El plazo es de 1 mes (R-01) con 2 developers (R-02), por lo que no es viable mantener dos apps nativas.

## Alternativas consideradas
1. App nativa (Android): mejor acceso al dispositivo, pero requiere más desarrollo, publicación en tienda y más peso para equipos de gama baja.
2. PWA con almacenamiento local y sincronización: un solo código, sin instalación desde tienda, funciona sin conexión.

## Decisión
Usaremos una PWA que guarde los recojos localmente y los sincronice al recuperar señal, con identificadores únicos generados en el celular para evitar duplicados.

## Consecuencias
- Positivas: un solo código para todos los dispositivos; no depende de tiendas de apps; cumple el escenario sin conexión (QA-03).
- Negativas / riesgos: la sincronización con conflictos es compleja y debe probarse pronto; algunas funciones del dispositivo pueden ser más limitadas que en una app nativa.