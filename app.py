from flask import Flask, render_template, request
from generador import GeneradorTurnos
import pandas as pd

app = Flask(__name__)


# Página principal con formulario

@app.route("/", methods=["GET", "POST"])
def index():
    tabla_resultado = None
    error = None

    if request.method == "POST":

        try:
            # Capturar la fecha seleccionada por el usuario
            fecha_inicio = request.form.get("fecha_inicio")

            # Capturar si desea aplicar la regla especial
            aplicar_regla_especial = request.form.get("regla_especial") == "on"

            # Validación
            if not fecha_inicio:
                raise Exception("Debe seleccionar una fecha válida.")

            # Crear generador con los valores del usuario
            generador = GeneradorTurnos(
                aplicar_regla_especial=aplicar_regla_especial,
                fecha_inicio=fecha_inicio
            )

            # Ejecutar modelo
            df = generador.ejecutar()

            # Convertir resultado a HTML con estilos bootstrap
            tabla_resultado = df.to_html(
                classes="table table-striped table-bordered text-center",
                index=False
            )

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        tabla=tabla_resultado,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
