from django.db import models
from django.core.validators import MinValueValidator

class editorial(models.Model):
    nombre = models.CharField('nombre',max_length=100,unique=True)

    class Meta:
        verbose_name = 'editorial'
        verbose_name_plural = 'editoriales' 
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class comic(models.Model):
    titulo = models.CharField('titulo',max_length=100,unique=True)
    editorial = models.ForeignKey(editorial, on_delete=models.CASCADE)
    portada = models.ImageField('portada',upload_to='portadas',null=True,blank=True)
    precio = models.PositiveIntegerField('precio',validators=[MinValueValidator(1)])
    tapa = models.BooleanField('tapa dura',default=False)
    stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    disponible = models.BooleanField('disponible',default=True)
    descripcion = models.TextField('descripcion',max_length=120,null=True,blank=True)
    numero_tomo = models.PositiveIntegerField('numero tomo',validators=[MinValueValidator(1)])
    
    class Meta:
        verbose_name = 'comic'
        verbose_name_plural = 'comics' 
        ordering = ['titulo','numero_tomo']
    
    def __str__(self):
        return f"{self.titulo} - Tomo {self.numero_tomo}"