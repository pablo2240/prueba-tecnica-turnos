# Prueba Técnica - Generador de Turnos (Python)

Descripción
-----------
Proyecto sencillo que resuelve la asignación de turnos para 3 asesores usando OR-Tools CP-SAT y muestra el resultado con Flask.

Requisitos
----------
- Python 3.8+
- pip

Instalación
----------
1. Clonar el repositorio:
   git clone <URL_DEL_REPOSITORIO>
2. Entrar a la carpeta:
   cd proyecto_turnos
3. Instalar dependencias:
   pip install -r requirements.txt

Archivos importantes
--------------------
- generador.py  -> Clase GeneradorTurnos (construye y resuelve el modelo)
- app.py        -> Interfaz Flask para generar y mostrar la planeación
- requirements.txt
- README.md

Cómo ejecutar
-------------
1. Ejecuta la aplicación:
   python app.py
2. Abre en el navegador:
   http://127.0.0.1:5000

Notas técnicas
--------------
- Se usa OR-Tools CP-SAT para modelar restricciones: 1 turno por asesor por día, cada turno ocupado por un asesor, turno constante durante la semana, domingos excluidos.
- Existe opción para fijar que una asesora trabaje siempre Apertura (parametro `aplicar_regla_especial=True`).
- Manejo de errores básico incluido; si no hay solución, se muestra excepción.

Posibles mejoras
----------------
- Añadir manejo de festivos (lista de fechas).
- Implementar rotación semanal (planeación mensual).
- Mejorar interfaz con HTML/CSS (Bootstrap).
