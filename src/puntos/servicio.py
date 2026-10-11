"""Servicio público del módulo Puntos."""
from decimal import Decimal
from uuid import UUID


class ServicioPuntos:
    def acreditar_por_recojo(
        self, solicitud_id: UUID, vecino_id: UUID, distrito_id: UUID, peso_kg: Decimal
    ) -> int:
        raise NotImplementedError("Leer la regla del distrito y la cuenta del vecino del repositorio")
