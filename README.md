# 🧠 Planeador de Turnos usando OR-Tools + Flask + Festivos de Colombia
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![OR-Tools](https://img.shields.io/badge/OR--Tools-Google%20CP--SAT-orange?logo=google)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![holidays_co](https://img.shields.io/badge/Festivos-Colombia%20API-yellow?logo=calendar)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap)

Este proyecto es una solución a una prueba técnica donde se debe generar la planeación semanal de turnos para un punto de venta (PDV), cumpliendo reglas específicas y excluyendo automáticamente los **festivos oficiales de Colombia** mediante la librería `holidays_co`.

---

## 📌 Tecnologías utilizadas

- **Python 3**
- **Flask** (para el sitio web)
- **OR-Tools CP-SAT Solver** (asignación de turnos de manera óptima)
- **Pandas** (para construir tablas)
- **holidays_co** (para detectar días festivos en Colombia)
- **Bootstrap 5** (para interfaz visual)

---

## 🎯 Descripción de la solución

Se implementa una clase llamada **`GeneradorTurnos`**, que utiliza un modelo CP-SAT de OR-Tools para asignar turnos bajo las siguientes reglas:

### ✔ Reglas obligatorias

1. Cada asesor debe tener **un solo turno por día**.
2. Cada turno debe ser tomado por **exactamente un asesor**.
3. Durante la semana, cada asesor mantiene **el mismo turno todos los días**.
4. No se generan turnos los **domingos**.
5. No se generan turnos en **festivos oficiales de Colombia**, usando:
   ```python
   from holidays_co import is_holiday_date
