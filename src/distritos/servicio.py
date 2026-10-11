"""Servicio público del módulo Distritos (interfaz que usan los demás módulos)."""
from uuid import UUID


class ServicioDistritos:
    def esta_habilitado(self, distrito_id: UUID) -> bool:
        raise NotImplementedError("Consultar el distrito en el repositorio")
