from django.urls import path
from . import views

app_name = "catalogo"
urlpatterns = [
    path("", views.catalogo, name="inicio"),
    path("comics/<int:pk>/", views.detalle, name="detalle"),
    
]
