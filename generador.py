import pandas as pd
from ortools.sat.python import cp_model
from datetime import datetime, timedelta
from holidays_co import is_holiday_date



# Clase generadora de turnos con festivos de Colombia

class GeneradorTurnos:
    def __init__(self, aplicar_regla_especial=False, fecha_inicio="2025-12-02", dias_por_semana=6):
        """
        aplicar_regla_especial = True si Asesor 1 solo puede trabajar Apertura.
        fecha_inicio = fecha seleccionada por el usuario desde el formulario.
        dias_por_semana = normalmente 6 (Lun-Sab).
        """

        self.aplicar_regla_especial = aplicar_regla_especial
        self.asesores = ["Asesor 1", "Asesor 2", "Asesor 3"]
        self.turnos = ["Apertura", "Intermedio", "Cierre"]

        # Convertir fecha
        self.fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        self.dias_por_semana = dias_por_semana



    # Verifica si la fecha es festivo usando holidays_co

    def es_festivo(self, fecha_datetime):
        """Recibe datetime y evalúa si es festivo (usando holidays_co)."""
        return is_holiday_date(fecha_datetime.date())  # True/False



    # Genera los días laborales de la semana, excluyendo domingos y festivos

    def obtener_dias_semana(self):
        dias = []
        d = 0

        while len(dias) < self.dias_por_semana:
            fecha = self.fecha_inicio + timedelta(days=d)
            d += 1

            # Excluir domingo
            if fecha.weekday() == 6:
                continue

            # Excluir festivos colombianos
            if self.es_festivo(fecha):
                continue

            dias.append(fecha)

        return dias



    # Construcción del modelo CP-SAT

    def construir_modelo(self):
        model = cp_model.CpModel()
        dias = self.obtener_dias_semana()

        if len(dias) == 0:
            raise Exception("No hay días válidos esta semana (todos festivos o domingos).")

        self.var = {}

        # Variables
        for asesor in self.asesores:
            for d in range(len(dias)):
                for t in range(len(self.turnos)):
                    self.var[(asesor, d, t)] = model.NewBoolVar(f"{asesor}_{d}_{t}")

        # Regla 1: un asesor 1 turno por día
        for asesor in self.asesores:
            for d in range(len(dias)):
                model.Add(sum(self.var[(asesor, d, t)] for t in range(len(self.turnos))) == 1)

        # Regla 2: cada turno lo toma un asesor
        for d in range(len(dias)):
            for t in range(len(self.turnos)):
                model.Add(sum(self.var[(asesor, d, t)] for asesor in self.asesores) == 1)

        # Regla 3: mismo turno toda la semana
        for asesor in self.asesores:
            for t in range(len(self.turnos)):
                for d in range(1, len(dias)):
                    model.Add(self.var[(asesor, d, t)] == self.var[(asesor, 0, t)])

        # Regla Especial: Asesor 1 solo apertura
        if self.aplicar_regla_especial:
            for d in range(len(dias)):
                model.Add(self.var[("Asesor 1", d, 1)] == 0)
                model.Add(self.var[("Asesor 1", d, 2)] == 0)

        self.model = model
        self.dias = dias



    # Resolver CP-SAT

    def resolver(self):
        solver = cp_model.CpSolver()
        resultado = solver.Solve(self.model)

        if resultado not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            raise Exception("No hay solución factible para esta semana.")

        filas = []

        for asesor in self.asesores:
            for d in range(len(self.dias)):
                for t in range(len(self.turnos)):
                    if solver.Value(self.var[(asesor, d, t)]) == 1:
                        filas.append({
                            "Fecha": self.dias[d].strftime("%Y-%m-%d"),
                            "Asesor": asesor,
                            "Turno": self.turnos[t]
                        })

        return pd.DataFrame(filas)



    # Ejecutar todo el flujo

    def ejecutar(self):
        self.construir_modelo()
        return self.resolver()
