"""Dominio del módulo Puntos. Referencia a vecinos, distritos y solicitudes solo por UUID (ADR-004)."""
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID


@dataclass
class ReglaPuntos:
    distrito_id: UUID
    puntos_por_kg: int
    vigente_desde: date

    def calcular(self, peso_kg: Decimal) -> int:
        return int(peso_kg * self.puntos_por_kg)


@dataclass
class CuentaPuntos:
    vecino_id: UUID
    saldo: int = 0
    solicitudes_acreditadas: set[UUID] = field(default_factory=set)

    def acreditar(self, puntos: int, solicitud_id: UUID) -> None:
        if solicitud_id in self.solicitudes_acreditadas:  # QA-03: 0 puntos duplicados
            return
        self.solicitudes_acreditadas.add(solicitud_id)
        self.saldo += puntos
