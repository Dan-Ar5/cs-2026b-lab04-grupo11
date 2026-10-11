"""Dominio del módulo Distritos."""
from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Distrito:
    nombre: str
    habilitado: bool = False
    id: UUID = field(default_factory=uuid4)

    def habilitar(self) -> None:
        self.habilitado = True

    def deshabilitar(self) -> None:
        self.habilitado = False

    def esta_habilitado(self) -> bool:
        return self.habilitado
