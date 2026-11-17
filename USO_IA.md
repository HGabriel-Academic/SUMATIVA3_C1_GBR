# Uso de inteligencia artificial
## Herramientas
- Perplexity: guía por etapas y explicaciones de código.
## Partes asistidas
- Se uso principalmente para repartir la evalucion por etapas y así poder trabajar de manera ordenada y eficaz.
- En la creacion del html basico de cada template.
- Para el codigo del archivo test.py y para solucionar problemas que fueran surgiendo entre etapas.
## Verificación personal
- Comandos ejecutados y pruebas realizadas: todo el checkeo de python,las cargas paulatinas y testeos por etapas del codigo.
- Correcciones y decisiones propias: la decision inical de llamar tienda y no catalogo a la app principal, pero la ver que tienda era un concepto demasiado repetido en el proyecto decidi cambiarlo a "catalogo" que era el termino explicito en el pdf del taller, esto me trajo un problema con como se había establecido ya la base de datos, se soluciono generando un sinonimo para esta, así la base de datos mantenia la referencia historica "tienda" pero la ubicacion del codigo se encontraba en /catalogo y el nombre visible en el administrador era "catalogo" .
    Correcciones menores de indentacion o por mala redacción identificadas con "python manage.py check" y con la funcion "python manage.py test catalogo" que automatiza pruebas para el codigo(no así la carga de imagenes).
