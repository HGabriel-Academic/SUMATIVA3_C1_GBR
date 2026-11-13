import uuid
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

class Editorial(models.Model):
    nombre = models.CharField("nombre", max_length=100, unique=True)
    class Meta:
        verbose_name = "editorial"
        verbose_name_plural = "editoriales"
        ordering = ["nombre"]
    def __str__(self):
        return self.nombre

class Comic(models.Model):
    titulo = models.CharField("título", max_length=200)
    editorial = models.ForeignKey(
        Editorial,
        on_delete=models.CASCADE,
        related_name="comics",
        verbose_name="editorial",
    )
    portada = models.ImageField("portada", upload_to="portadas/")
    precio = models.PositiveIntegerField(
        "precio en pesos", validators=[MinValueValidator(1)]
    )
    numero_tomo = models.PositiveIntegerField(
        "número de tomo", default=1,
        validators=[MinValueValidator(1)],
    )
    tapa_dura = models.BooleanField("tapa dura", default=False)
    stock = models.PositiveIntegerField("stock", default=0)
    disponible = models.BooleanField("disponible", default=True)
    descripcion = models.TextField("descripción", blank=True)
    
    class Meta:
        verbose_name = "cómic"
        verbose_name_plural = "cómics"
        ordering = ["titulo", "numero_tomo"]
    def __str__(self):
        return f"{self.titulo} - Tomo {self.numero_tomo}"
    
class Reserva(models.Model):
    comic = models.ForeignKey(
        Comic, on_delete=models.CASCADE, related_name="reservas"
    )
    nombre = models.CharField(max_length=120)
    correo = models.EmailField()
    rut = models.CharField("RUT", max_length=12)
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )
    fecha = models.DateTimeField(auto_now_add=True)
    codigo = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False
    )
    precio_unitario = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ["-fecha"]
    @property
    def total(self):
        return self.precio_unitario * self.cantidad
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"