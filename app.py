from flask import Flask, render_template_string, request
from generador import GeneradorTurnos
from datetime import datetime

app = Flask(__name__)

# Plantilla del index (input de fecha)
TEMPLATE_INDEX = """
<!DOCTYPE html>
<html>
<head>
    <title>Generador de Turnos</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css' rel='stylesheet'>
</head>
<body class='bg-light'>
    <div class='container mt-5'>
        <div class='card shadow p-4' style="max-width: 500px; margin: auto;">
            <h2 class='text-center mb-4'>Generar Planeación</h2>
            <form action="/generar" method="get">
                <div class="mb-3">
                    <label for="fecha" class="form-label">Fecha de Inicio:</label>
                    <input type="date" class="form-control" id="fecha" name="fecha" required value="{{ hoy }}">
                </div>
                <button type="submit" class="btn btn-primary w-100">Generar Turnos</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

# Plantilla de la tabla (resultados)
TEMPLATE_TABLA = """
<!DOCTYPE html>
<html>
<head>
    <title>Planeación Semanal</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css' rel='stylesheet'>
</head>
<body class='bg-light'>
    <div class='container mt-5'>
        <div class='card shadow p-4'>
            <h2 class='text-center mb-4'>Planeación Semanal</h2>
            <div class="table-responsive">
                <table class='table table-bordered table-striped'>
                    <thead class='table-dark'>
                        <tr>
                            <th>Fecha</th>
                            <th>Asesor</th>
                            <th>Turno</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for _, row in df.iterrows() %}
                        <tr>
                            <td>{{ row['Fecha'] }}</td>
                            <td>{{ row['Asesor'] }}</td>
                            <td>{{ row['Turno'] }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            <a href='/' class='btn btn-secondary mt-3'>Volver</a>
        </div>
    </div>
</body>
</html>
"""
# ----------------------
# Rutas
# ----------------------
@app.route('/')
def index():
    hoy = datetime.now().strftime("%Y-%m-%d")
    return render_template_string(TEMPLATE_INDEX, hoy=hoy)

@app.route('/generar')
def generar():
    try:
        # Obtener la fecha seleccionada por el usuario
        fecha_usuario = request.args.get('fecha')
        if not fecha_usuario:
            return "<h3>Debes seleccionar una fecha.</h3><a href='/'>Volver</a>"

        gen = GeneradorTurnos(aplicar_regla_especial=True, fecha_inicio=fecha_usuario)
        df = gen.ejecutar()
        return render_template_string(TEMPLATE_TABLA, df=df)
    except Exception as e:
        return f"<h3>Error al generar la planeación:</h3><p>{str(e)}</p><a href='/'>Volver</a>"

if __name__ == '__main__':
    app.run(debug=True)
