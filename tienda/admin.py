from django.contrib import admin
from .models import Comic, Editorial

@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)
    ordering = ("nombre",)

@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = (
        "titulo", "editorial", "numero_tomo", "stock",
        "precio_clp", "tapa_dura", "disponible",
    )
    list_filter = ("editorial", "tapa_dura")
    search_fields = ("titulo",)
    list_select_related = ("editorial",)
    ordering = ("titulo", "numero_tomo")
    @admin.display(description="Precio", ordering="precio")
    def precio_clp(self, obj):
        return f"${obj.precio:,}".replace(",", ".")