from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from .forms import ReservaForm
from .models import Comic, Editorial, Reserva
from .validators import validar_rut

class TiendaTests(TestCase):
    def setUp(self):
        self.editorial = Editorial.objects.create(nombre="Prueba")
        self.comic = Comic.objects.create(
            titulo="Aventura", editorial=self.editorial,
            portada="portadas/prueba.jpg", precio=12990,
            numero_tomo=1, stock=5, disponible=True,
        )
        self.datos = {
            "nombre": "Persona de prueba", "correo": "prueba@example.com",
            "rut": "12.345.678-5", "cantidad": 2,
        }
    def crear_reserva(self, cantidad=2):
        return Reserva.objects.create(
            comic=self.comic, **{**self.datos, "cantidad": cantidad}
        )
    def test_rut(self):
        validar_rut("12.345.678-5")
        for rut in ["12.345.678-9", "12345678-5", "abc"]:
            with self.assertRaises(ValidationError):
                validar_rut(rut)
    def test_formulario_invalido(self):
        for cambios in [
            {"cantidad": 0}, {"cantidad": 4},
            {"correo": "mal"}, {"rut": "12.345.678-9"},
        ]:
            form = ReservaForm(data={**self.datos, **cambios})
            self.assertFalse(form.is_valid())
        self.assertEqual(Reserva.objects.count(), 0)
    
    def test_descuento_y_precio_historico(self):
        reserva = self.crear_reserva()
        self.comic.refresh_from_db()
        self.assertEqual(self.comic.stock, 3)
        self.assertEqual(reserva.total, 25980)
        self.comic.precio = 15000
        self.comic.save()
        reserva.refresh_from_db()
        self.assertEqual(reserva.total, 25980)
        reserva.nombre = "Otro nombre de prueba"
        reserva.save()
        self.comic.refresh_from_db()
        self.assertEqual(self.comic.stock, 3)
    def test_stock_insuficiente(self):
        self.comic.stock = 1
        self.comic.save()
        with self.assertRaises(ValidationError):
            self.crear_reserva(2)
        self.comic.refresh_from_db()
        self.assertEqual(self.comic.stock, 1)
        self.assertEqual(Reserva.objects.count(), 0)
    def test_post_y_recarga(self):
        url = reverse("catalogo:reservar", args=[self.comic.pk])
        respuesta = self.client.post(url, self.datos)
        self.assertEqual(respuesta.status_code, 302)
        for _ in range(3):
            self.assertEqual(
            self.client.get(respuesta.url).status_code, 200
        )
        self.assertEqual(Reserva.objects.count(), 1)
        self.comic.refresh_from_db()
        self.assertEqual(self.comic.stock, 3)
    def test_agotado_y_oculto(self):
        self.comic.stock = 0
        self.comic.save()
        inicio = reverse("catalogo:inicio")
        self.assertContains(self.client.get(inicio), "Agotado")
        url = reverse("catalogo:reservar", args=[self.comic.pk])
        self.client.post(url, self.datos)
        self.assertEqual(Reserva.objects.count(), 0)
        self.comic.disponible = False
        self.comic.save()
        detalle = reverse("catalogo:detalle", args=[self.comic.pk])
        self.assertEqual(self.client.get(detalle).status_code, 404)
        self.assertNotContains(self.client.get(inicio), "Aventura")
    def test_cascada(self):
        self.crear_reserva()
        self.editorial.delete()
        self.assertEqual(Comic.objects.count(), 0)
        self.assertEqual(Reserva.objects.count(), 0)