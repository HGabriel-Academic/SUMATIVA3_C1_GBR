from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["nombre", "correo", "rut", "cantidad"]
        widgets = {
            "cantidad": forms.NumberInput(attrs={"min": 1, "max": 3}),
            "rut": forms.TextInput(
                attrs={"placeholder": "12.345.678-5"}
            ),
}
    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if not nombre:
            raise forms.ValidationError("Ingresa tu nombre.")
        return nombre