# Tienda de cómics
Integrante: Gabriel Benavides Ramirez
Evaluacion sumativa 3 TI3041 C1.
## Instalación
1. Clonar el repositorio y entrar a la carpeta.
2. Crear entorno: python -m venv .venv
3. Activar el entorno según el sistema operativo.
4. Instalar: python -m pip install -r requirements.txt
5. Aplicar migraciones: python manage.py migrate
6. Verificar: python manage.py check
7. Ejecutar: python manage.py runserver
## Pruebas
python manage.py test catalogo
## Usuarios de demostración
admin / Inacap.2026 (superusuario)
tienda / Inacap.2026 (staff, grupo Tienda)
Ruts cargados en la base de datos fueron creados con un generador de ruts online, pues el algoritmo de validación de rut es el que utiliza el SII y no se pueden cargar ruts inventados.