"""Una prueba por transición del diagrama estados-solicitud.mmd (más las guardas y el flujo CA-1/CA-2/CA-3)."""
import sys
import unittest
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from puntos.dominio import CuentaPuntos, ReglaPuntos  # noqa: E402
from recojos.dominio import EstadoSolicitud, ItemSolicitud, Solicitud, TipoMaterial, TransicionInvalida  # noqa: E402
from recojos.puertos import Notificador, RepositorioSolicitudes  # noqa: E402
from recojos.servicio import DistritoNoHabilitado, ServicioRecojos  # noqa: E402


def solicitud_con_item() -> Solicitud:
    s = Solicitud.crear(uuid4(), uuid4(), "Calle 1")
    s.agregar_item(TipoMaterial.PAPEL, Decimal("2"))
    return s


class TestTransiciones(unittest.TestCase):
    def test_crear_deja_pendiente(self):
        self.assertIs(Solicitud.crear(uuid4(), uuid4(), "x").estado, EstadoSolicitud.PENDIENTE)

    def test_asignar(self):
        s = solicitud_con_item()
        s.asignar(uuid4())
        self.assertIs(s.estado, EstadoSolicitud.ASIGNADA)

    def test_asignar_sin_items_falla_c3(self):
        with self.assertRaises(ValueError):
            Solicitud.crear(uuid4(), uuid4(), "x").asignar(uuid4())

    def test_confirmar_recojo(self):
        s = solicitud_con_item()
        s.asignar(uuid4())
        s.confirmar_recojo()
        self.assertIs(s.estado, EstadoSolicitud.RECOGIDA)

    def test_registrar_peso_y_guarda(self):
        s = solicitud_con_item()
        s.asignar(uuid4())
        s.confirmar_recojo()
        with self.assertRaises(ValueError):
            s.registrar_peso(Decimal("0"))
        s.registrar_peso(Decimal("3.5"))
        self.assertIs(s.estado, EstadoSolicitud.PESADA)

    def test_acreditar_puntos_una_sola_vez(self):
        s = solicitud_con_item()
        s.asignar(uuid4())
        s.confirmar_recojo()
        s.registrar_peso(Decimal("3"))
        s.acreditar_puntos(30)
        self.assertIs(s.estado, EstadoSolicitud.PUNTOS_ACREDITADOS)
        with self.assertRaises(TransicionInvalida):
            s.acreditar_puntos(30)

    def test_cancelar_desde_pendiente_y_asignada(self):
        p = solicitud_con_item()
        p.cancelar("ya no")
        self.assertIs(p.estado, EstadoSolicitud.CANCELADA)
        a = solicitud_con_item()
        a.asignar(uuid4())
        a.cancelar("ya no")
        self.assertIs(a.estado, EstadoSolicitud.CANCELADA)

    def test_no_se_cancela_una_recogida(self):
        s = solicitud_con_item()
        s.asignar(uuid4())
        s.confirmar_recojo()
        with self.assertRaises(TransicionInvalida):
            s.cancelar("tarde")


class RepoFalso(RepositorioSolicitudes):
    def __init__(self):
        self.datos = {}

    def buscar(self, id):
        return self.datos[id]

    def guardar(self, s):
        self.datos[s.id] = s


class NotificadorFalso(Notificador):
    def __init__(self):
        self.avisos = []

    def notificar_solicitud_registrada(self, s):
        self.avisos.append(s.id)


class DistritosFalso:
    def __init__(self, habilitado):
        self.habilitado = habilitado

    def esta_habilitado(self, distrito_id):
        return self.habilitado


class PuntosFalso:
    """Stub que aplica la regla y la cuenta reales del dominio de puntos (sin repositorio)."""

    def __init__(self, distrito_id, vecino_id):
        self.regla = ReglaPuntos(distrito_id, 10, __import__("datetime").date(2026, 10, 1))
        self.cuenta = CuentaPuntos(vecino_id)

    def acreditar_por_recojo(self, solicitud_id, vecino_id, distrito_id, peso_kg):
        puntos = self.regla.calcular(peso_kg)
        self.cuenta.acreditar(puntos, solicitud_id)
        return puntos


class TestServicioRecojos(unittest.TestCase):
    def armar(self, habilitado=True):
        self.distrito, self.vecino = uuid4(), uuid4()
        self.repo, self.notif = RepoFalso(), NotificadorFalso()
        self.puntos = PuntosFalso(self.distrito, self.vecino)
        return ServicioRecojos(self.repo, self.notif, DistritosFalso(habilitado), self.puntos)

    def test_ca1_solicitud_pendiente_y_aviso(self):
        srv = self.armar()
        s = srv.solicitar_recojo(self.vecino, self.distrito, "Calle 1", [ItemSolicitud(TipoMaterial.VIDRIO, Decimal("1"))])
        self.assertIs(s.estado, EstadoSolicitud.PENDIENTE)
        self.assertEqual(self.notif.avisos, [s.id])

    def test_ca2_distrito_no_habilitado_no_crea_nada(self):
        srv = self.armar(habilitado=False)
        with self.assertRaises(DistritoNoHabilitado):
            srv.solicitar_recojo(self.vecino, self.distrito, "Calle 1", [ItemSolicitud(TipoMaterial.VIDRIO, Decimal("1"))])
        self.assertEqual(self.repo.datos, {})
        self.assertEqual(self.notif.avisos, [])

    def test_ca3_puntos_sin_duplicar(self):
        srv = self.armar()
        s = srv.solicitar_recojo(self.vecino, self.distrito, "Calle 1", [ItemSolicitud(TipoMaterial.METAL, Decimal("2"))])
        s.asignar(uuid4())
        srv.confirmar_recojo(s.id, Decimal("3"))
        self.assertIs(self.repo.datos[s.id].estado, EstadoSolicitud.PUNTOS_ACREDITADOS)
        self.assertEqual(self.puntos.cuenta.saldo, 30)
        with self.assertRaises(TransicionInvalida):  # reintento por sincronización doble
            srv.confirmar_recojo(s.id, Decimal("3"))
        self.assertEqual(self.puntos.cuenta.saldo, 30)


if __name__ == "__main__":
    unittest.main()
