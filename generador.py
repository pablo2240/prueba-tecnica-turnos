from ortools.sat.python import cp_model
import pandas as pd
from datetime import datetime, timedelta

# -------------------------------------------------------
# Clase simple para generar turnos
# -------------------------------------------------------
class GeneradorTurnos:
    def __init__(self, aplicar_regla_especial=False, fecha_inicio="2025-12-02", dias_por_semana=6, festivos=None):
        self.aplicar_regla_especial = aplicar_regla_especial
        self.asesores = ["Asesor 1", "Asesor 2", "Asesor 3"]
        self.turnos = ["Apertura", "Intermedio", "Cierre"]
        self.fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        self.dias_por_semana = dias_por_semana  # por defecto 6 (Lun-Sab)
        self.festivos = set(festivos or [])    # lista de strings 'YYYY-MM-DD'

    # ---------------------------------------------------
    def obtener_dias_semana(self):
        dias = []
        d = 0
        while len(dias) < self.dias_por_semana:
            fecha = self.fecha_inicio + timedelta(days=d)
            d += 1
            # Excluir domingos
            if fecha.weekday() == 6:  # domingo = 6
                continue
            # Excluir festivos
            if fecha.strftime("%Y-%m-%d") in self.festivos:
                continue
            dias.append(fecha)
        return dias

    # ---------------------------------------------------
    def construir_modelo(self):
        model = cp_model.CpModel()
        dias = self.obtener_dias_semana()

        self.var = {}

        # Variables
        for asesor in self.asesores:
            for d in range(len(dias)):
                for t in range(len(self.turnos)):
                    self.var[(asesor, d, t)] = model.NewBoolVar(
                        f"{asesor}_{d}_{t}"
                    )

        # Regla 1: un asesor solo tiene un turno por día
        for asesor in self.asesores:
            for d in range(len(dias)):
                model.Add(
                    sum(self.var[(asesor, d, t)] for t in range(len(self.turnos)))
                    == 1
                )

        # Regla 2: cada turno lo debe tomar un asesor
        for d in range(len(dias)):
            for t in range(len(self.turnos)):
                model.Add(
                    sum(self.var[(asesor, d, t)] for asesor in self.asesores)
                    == 1
                )

        # Regla 3: toda la semana el mismo turno cada asesor
        for asesor in self.asesores:
            for t in range(len(self.turnos)):
                for d in range(1, len(dias)):
                    model.Add(self.var[(asesor, d, t)] ==
                              self.var[(asesor, 0, t)])

        # Regla especial: Asesor 1 solo Apertura
        if self.aplicar_regla_especial:
            for d in range(len(dias)):
                model.Add(self.var[("Asesor 1", d, 1)] == 0)  # No Intermedio
                model.Add(self.var[("Asesor 1", d, 2)] == 0)  # No Cierre

        self.model = model

    # ---------------------------------------------------
    def resolver(self):
        solver = cp_model.CpSolver()
        resultado = solver.Solve(self.model)

        if resultado not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            raise Exception("No hay solución")

        dias = self.obtener_dias_semana()
        filas = []

        for asesor in self.asesores:
            for d in range(len(dias)):
                for t in range(len(self.turnos)):
                    if solver.Value(self.var[(asesor, d, t)]) == 1:
                        filas.append({
                            "Fecha": dias[d].strftime("%Y-%m-%d"),
                            "Asesor": asesor,
                            "Turno": self.turnos[t]
                        })

        return pd.DataFrame(filas)

    # ---------------------------------------------------
    def ejecutar(self):
        self.construir_modelo()
        return self.resolver()
