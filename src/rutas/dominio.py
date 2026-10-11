"""Dominio del módulo Rutas."""
from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4

from recojos.dominio import EstadoSolicitud, Solicitud


@dataclass
class Reciclador:
    nombre: str
    celular: str
    id: UUID = field(default_factory=uuid4)


@dataclass
class Ruta:
    reciclador: Reciclador
    fecha: date
    paradas: list[Solicitud] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)

    def agregar_parada(self, s: Solicitud) -> None:
        s.asignar(self.reciclador.id)
        self.paradas.append(s)

    def siguiente_parada(self) -> Solicitud:
        for parada in self.paradas:
            if parada.estado is EstadoSolicitud.ASIGNADA:
                return parada
        raise LookupError("La ruta no tiene más paradas pendientes")
