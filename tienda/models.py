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