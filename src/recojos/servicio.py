"""Servicio de aplicación del módulo Recojos."""
from decimal import Decimal
from uuid import UUID

from distritos.servicio import ServicioDistritos
from puntos.servicio import ServicioPuntos
from recojos.dominio import ItemSolicitud, Solicitud
from recojos.puertos import Notificador, RepositorioSolicitudes


class DistritoNoHabilitado(Exception):
    """Criterio de aceptación CA-2: el distrito no está habilitado por la municipalidad."""


class ServicioRecojos:
    def __init__(
        self,
        repositorio: RepositorioSolicitudes,
        notificador: Notificador,
        servicio_distritos: ServicioDistritos,
        servicio_puntos: ServicioPuntos,
    ) -> None:
        self._repositorio = repositorio
        self._notificador = notificador
        self._servicio_distritos = servicio_distritos
        self._servicio_puntos = servicio_puntos

    def solicitar_recojo(
        self, vecino_id: UUID, distrito_id: UUID, direccion: str, items: list[ItemSolicitud]
    ) -> Solicitud:
        if not items:  # C3: al menos un material (1..*)
            raise ValueError("Indique al menos un material por recoger")
        if not self._servicio_distritos.esta_habilitado(distrito_id):
            raise DistritoNoHabilitado(str(distrito_id))
        solicitud = Solicitud.crear(vecino_id, distrito_id, direccion)
        for item in items:
            solicitud.agregar_item(item.material, item.peso_estimado_kg)
        self._repositorio.guardar(solicitud)
        self._notificador.notificar_solicitud_registrada(solicitud)  # asíncrono en la práctica
        return solicitud

    def confirmar_recojo(self, solicitud_id: UUID, peso_kg: Decimal) -> Solicitud:
        solicitud = self._repositorio.buscar(solicitud_id)
        solicitud.confirmar_recojo()
        solicitud.registrar_peso(peso_kg)
        puntos = self._servicio_puntos.acreditar_por_recojo(
            solicitud.id, solicitud.vecino_id, solicitud.distrito_id, peso_kg
        )
        solicitud.acreditar_puntos(puntos)
        self._repositorio.guardar(solicitud)
        return solicitud
