import uuid
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from .validators import validar_rut
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F

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
    rut = models.CharField("RUT", max_length=12, validators=[validar_rut])
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
    def clean(self):
        super().clean()
        if not self._state.adding:
            return
        if not self.comic_id or self.cantidad is None:
            return
        comic = Comic.objects.filter(pk=self.comic_id).first()
        if comic is None:
            return  # La validación de ForeignKey informará el error.
        if not comic.disponible:
            raise ValidationError("Este cómic no está disponible.")
        if self.cantidad > comic.stock:
            raise ValidationError(
                f"Solo hay {comic.stock} ejemplares disponibles."
    )
    def save(self, *args, **kwargs):
        if not self._state.adding:
            return super().save(*args, **kwargs)
        with transaction.atomic():
            self.full_clean()
            actualizados = Comic.objects.filter(
                pk=self.comic_id,
                disponible=True,
                stock__gte=self.cantidad,
            ).update(stock=F("stock") - self.cantidad)
            if actualizados != 1:
                stock = Comic.objects.filter(
                    pk=self.comic_id
                ).values_list("stock", flat=True).first()
                raise ValidationError(
                    f"No se pudo reservar. Stock disponible: {stock or 0}."
                )
            self.precio_unitario = Comic.objects.values_list(
                "precio", flat=True
            ).get(pk=self.comic_id)
            return super().save(*args, **kwargs)