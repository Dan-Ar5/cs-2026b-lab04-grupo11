"""Adaptador del puerto Notificador hacia WhatsApp (servicio externo, ADR-001)."""
from recojos.dominio import Solicitud
from recojos.puertos import Notificador


class WhatsAppAdapter(Notificador):
    def notificar_solicitud_registrada(self, s: Solicitud) -> None:
        raise NotImplementedError("Integrar con el proveedor de mensajería elegido")
