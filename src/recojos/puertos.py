"""Puertos del módulo Recojos (ADR-001: integraciones externas mediante puertos y adaptadores)."""
from abc import ABC, abstractmethod
from uuid import UUID

from recojos.dominio import Solicitud


class RepositorioSolicitudes(ABC):
    @abstractmethod
    def buscar(self, id: UUID) -> Solicitud: ...

    @abstractmethod
    def guardar(self, s: Solicitud) -> None: ...


class Notificador(ABC):
    @abstractmethod
    def notificar_solicitud_registrada(self, s: Solicitud) -> None: ...
