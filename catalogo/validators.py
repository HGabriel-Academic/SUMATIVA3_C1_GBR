import re
from itertools import cycle
from django.core.exceptions import ValidationError
def validar_rut(valor):
    # Exige puntos y guion; permite DV k o K.
    patron = r"[1-9][0-9]?\.[0-9]{3}\.[0-9]{3}-[0-9Kk]"
    if not re.fullmatch(patron, valor):
        raise ValidationError("Usa el formato 12.345.678-5.")
    cuerpo, dv = valor.replace(".", "").split("-")
    suma = sum(
        int(digito) * factor
        for digito, factor in zip(reversed(cuerpo), cycle(range(2, 8)))
    )
    resultado = 11 - (suma % 11)
    esperado = "0" if resultado == 11 else (
        "K" if resultado == 10 else str(resultado)
    )
    if dv.upper() != esperado:
        raise ValidationError("El dígito verificador del RUT es incorrecto.")
