from django.shortcuts import render
from .models import Comic,Editorial
from django.shortcuts import get_object_or_404
from .forms import ReservaForm
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from .models import Reserva

def catalogo(request):
    q = request.GET.get("q", "").strip()
    editorial_id = request.GET.get("editorial", "").strip()
    comics = Comic.objects.filter(
        disponible=True
    ).select_related("editorial")
    if q:
        comics = comics.filter(titulo__icontains=q)
    if editorial_id:
        # Ignora identificadores mal formados; no provoca error 500.
        if editorial_id.isascii() and editorial_id.isdigit():
            if len(editorial_id) <= 9:
                comics = comics.filter(editorial_id=int(editorial_id))
            else:
                comics = comics.none()
        else:
            comics = comics.none()
    return render(request, "catalogo/catalogo.html", {
        "comics": comics,
        "editoriales": Editorial.objects.all(),
        "q": q,
        "editorial_id": editorial_id,
    })
    
def detalle(request, pk):
    comic = get_object_or_404(
    Comic.objects.select_related("editorial"),
    pk=pk, disponible=True,
    )
    return render(request, "catalogo/detalle.html", {"comic": comic})

def reservar(request, pk):
    comic = get_object_or_404(Comic, pk=pk, disponible=True)
    form = ReservaForm(request.POST if request.method == "POST" else None)
    if request.method == "POST":
        if comic.stock == 0:
            form.add_error(None, "Agotado. No se pueden hacer reservas.")
        elif form.is_valid():
            reserva = form.save(commit=False)
            reserva.comic = comic
            try:
                reserva.save()
            except ValidationError as error:
                form.add_error(None, "; ".join(error.messages))
            else:
                return redirect("catalogo:comprobante", codigo=reserva.codigo)
        comic.refresh_from_db()
    return render(request, "catalogo/reservar.html", {
        "comic": comic, "form": form,
})

def comprobante(request, codigo):
    reserva = get_object_or_404(
        Reserva.objects.select_related("comic"), codigo=codigo
    )
    return render(request, "catalogo/comprobante.html", {
        "reserva": reserva,
})