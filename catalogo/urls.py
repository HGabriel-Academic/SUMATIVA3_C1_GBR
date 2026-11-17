from django.urls import path
from . import views

app_name = "catalogo"
urlpatterns = [
    path("", views.catalogo, name="inicio"),
    path("comics/<int:pk>/", views.detalle, name="detalle"),
    path("comics/<int:pk>/reservar/", views.reservar, name="reservar"),
    path( "reservas/<uuid:codigo>/comprobante/",views.comprobante,name="comprobante",
),

]
