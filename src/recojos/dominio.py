"""Dominio del módulo Recojos (generado a partir de docs/design/clases.puml y revisado)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4


class EstadoSolicitud(Enum):
    PENDIENTE = "PENDIENTE"
    ASIGNADA = "ASIGNADA"
    RECOGIDA = "RECOGIDA"
    PESADA = "PESADA"
    PUNTOS_ACREDITADOS = "PUNTOS_ACREDITADOS"
    CANCELADA = "CANCELADA"


class TipoMaterial(Enum):
    PAPEL = "PAPEL"
    CARTON = "CARTON"
    PLASTICO = "PLASTICO"
    VIDRIO = "VIDRIO"
    METAL = "METAL"


class TransicionInvalida(Exception):
    """La operación no está permitida desde el estado actual (ver estados-solicitud.mmd)."""


@dataclass
class Vecino:
    nombre: str
    celular: str
    direccion: str
    id: UUID = field(default_factory=uuid4)


@dataclass
class ItemSolicitud:
    material: TipoMaterial
    peso_estimado_kg: Decimal


@dataclass
class Solicitud:
    vecino_id: UUID
    distrito_id: UUID
    direccion_recojo: str
    items: list[ItemSolicitud] = field(default_factory=list)
    estado: EstadoSolicitud = EstadoSolicitud.PENDIENTE
    reciclador_id: UUID | None = None
    peso_kg: Decimal | None = None
    puntos_otorgados: int | None = None
    fecha_solicitud: datetime = field(default_factory=datetime.now)
    id: UUID = field(default_factory=uuid4)

    @staticmethod
    def crear(vecino_id: UUID, distrito_id: UUID, direccion: str) -> Solicitud:
        return Solicitud(vecino_id=vecino_id, distrito_id=distrito_id, direccion_recojo=direccion)

    def agregar_item(self, material: TipoMaterial, peso_estimado_kg: Decimal) -> None:
        self._exigir(EstadoSolicitud.PENDIENTE)
        self.items.append(ItemSolicitud(material, peso_estimado_kg))

    def asignar(self, reciclador_id: UUID) -> None:
        self._exigir(EstadoSolicitud.PENDIENTE)
        if not self.items:  # regla C3: una solicitud tiene al menos un ítem (1..*)
            raise ValueError("La solicitud debe tener al menos un material")
        self.reciclador_id = reciclador_id
        self.estado = EstadoSolicitud.ASIGNADA

    def confirmar_recojo(self) -> None:
        self._exigir(EstadoSolicitud.ASIGNADA)
        self.estado = EstadoSolicitud.RECOGIDA

    def registrar_peso(self, peso_kg: Decimal) -> None:
        self._exigir(EstadoSolicitud.RECOGIDA)
        if peso_kg <= 0:  # guarda [pesoKg > 0]
            raise ValueError("El peso debe ser mayor que cero")
        self.peso_kg = peso_kg
        self.estado = EstadoSolicitud.PESADA

    def acreditar_puntos(self, puntos: int) -> None:
        self._exigir(EstadoSolicitud.PESADA)  # guarda [no acreditada antes]: solo desde PESADA
        self.puntos_otorgados = puntos
        self.estado = EstadoSolicitud.PUNTOS_ACREDITADOS

    def cancelar(self, motivo: str) -> None:
        if self.estado not in (EstadoSolicitud.PENDIENTE, EstadoSolicitud.ASIGNADA):
            raise TransicionInvalida(f"No se puede cancelar desde {self.estado.value}: {motivo}")
        self.estado = EstadoSolicitud.CANCELADA

    def _exigir(self, esperado: EstadoSolicitud) -> None:
        if self.estado is not esperado:
            raise TransicionInvalida(f"Se esperaba {esperado.value} y está en {self.estado.value}")
