"""
Forecast de Demanda — Business Operating System
Predicción de demanda operativa: viajes por zona, hora y día de la semana.
"""

import json
import math
import random
from datetime import datetime, date, timedelta
from pathlib import Path


# ─── Generador de datos de demanda ───────────────────────────────────────────

def generar_datos_demanda(dias: int = 90) -> list[dict]:
    """
    Genera datos históricos de demanda por día, zona y franja horaria.
    Simula patrones realistas de movilidad urbana.
    """
    random.seed(99)

    zonas = ["Centro", "Norte", "Sur", "Este", "Oeste", "Aeropuerto"]
    franjas = ["06-08", "08-10", "10-12", "12-14", "14-16", "16-18", "18-20", "20-22"]

    # Factor de demanda por día de la semana (0=lunes, 6=domingo)
    factor_dia = {0: 1.0, 1: 1.0, 2: 1.05, 3: 1.02, 4: 1.10, 5: 0.85, 6: 0.70}

    # Factor de demanda por franja horaria
    factor_franja = {
        "06-08": 1.3, "08-10": 1.8, "10-12": 1.1,
        "12-14": 1.2, "14-16": 0.9, "16-18": 1.1,
        "18-20": 1.7, "20-22": 1.0,
    }

    # Factor por zona (demanda base relativa)
    factor_zona = {
        "Centro": 1.5, "Norte": 1.0, "Sur": 0.8,
        "Este": 0.9, "Oeste": 1.1, "Aeropuerto": 0.4,
    }

    base_viajes_dia = 8000
    datos = []
    fecha_inicio = date(2026, 1, 1)

    for d in range(dias):
        fecha = fecha_inicio + timedelta(days=d)
        dia_semana = fecha.weekday()
        # Tendencia de crecimiento lineal suave
        factor_tendencia = 1 + d * 0.002

        for zona in zonas:
            for franja in franjas:
                base = base_viajes_dia / (len(zonas) * len(franjas))
                viajes = (
                    base
                    * factor_dia[dia_semana]
                    * factor_franja[franja]
                    * factor_zona[zona]
                    * factor_tendencia
                    * random.uniform(0.90, 1.10)
                )
                datos.append({
                    "fecha": fecha.isoformat(),
                    "dia_semana": dia_semana,
                    "dia_semana_nombre": ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"][dia_semana],
                    "zona": zona,
                    "franja_horaria": franja,
                    "viajes": int(viajes),
                    "conductores_disponibles": max(1, int(viajes * 1.2)),
                    "tasa_aceptacion_pct": round(random.uniform(75, 95), 1),
                })

    return datos


# ─── Agregaciones por patrón ─────────────────────────────────────────────────

def agregar_por_patron(datos: list[dict]) -> dict:
    """Calcula promedios de demanda por zona, franja y día de semana."""
    # Por zona
    por_zona = {}
    for r in datos:
        z = r["zona"]
        if z not in por_zona:
            por_zona[z] = []
        por_zona[z].append(r["viajes"])
    resumen_zona = {z: {
        "promedio_diario": round(sum(v) / len(v), 1),
        "maximo": max(v),
        "minimo": min(v),
    } for z, v in por_zona.items()}

    # Por franja horaria
    por_franja = {}
    for r in datos:
        f = r["franja_horaria"]
        if f not in por_franja:
            por_franja[f] = []
        por_franja[f].append(r["viajes"])
    resumen_franja = {f: {
        "promedio": round(sum(v) / len(v), 1),
        "maximo": max(v),
    } for f, v in por_franja.items()}

    # Por día de semana
    por_dia = {}
    for r in datos:
        d = r["dia_semana_nombre"]
        if d not in por_dia:
            por_dia[d] = []
        por_dia[d].append(r["viajes"])
    resumen_dia = {d: {
        "promedio": round(sum(v) / len(v), 1),
    } for d, v in por_dia.items()}

    return {
        "por_zona": resumen_zona,
        "por_franja_horaria": resumen_franja,
        "por_dia_semana": resumen_dia,
    }


# ─── Modelo de forecast de demanda ───────────────────────────────────────────

class ForecastDemanda:
    """
    Modelo de suavizado exponencial simple para forecast de demanda agregada.
    Incluye ajuste por estacionalidad semanal.
    """

    def __init__(self, alpha: float = 0.4):
        self.alpha = alpha
        self.nivel = None

    def ajustar(self, serie: list[float]):
        self.nivel = serie[0]
        for v in serie[1:]:
            self.nivel = self.alpha * v + (1 - self.alpha) * self.nivel
        return self

    def predecir(self, pasos: int, factor_tendencia: float = 1.002) -> list[float]:
        predicciones = []
        nivel = self.nivel
        for i in range(pasos):
            nivel = nivel * (factor_tendencia ** (i + 1))
            predicciones.append(round(nivel, 1))
        return predicciones


def forecast_por_zona(datos: list[dict], dias_forecast: int = 14) -> dict:
    """Genera forecast de demanda para cada zona."""
    zonas = list(set(d["zona"] for d in datos))
    resultados = {}

    for zona in zonas:
        # Agregar viajes diarios por zona
        viajes_por_fecha = {}
        for r in datos:
            if r["zona"] == zona:
                f = r["fecha"]
                viajes_por_fecha[f] = viajes_por_fecha.get(f, 0) + r["viajes"]

        serie = list(viajes_por_fecha.values())
        modelo = ForecastDemanda(alpha=0.35)
        modelo.ajustar(serie)
        predicciones = modelo.predecir(dias_forecast)

        # Generar fechas futuras
        ultima_fecha = date.fromisoformat(max(viajes_por_fecha.keys()))
        fechas = [(ultima_fecha + timedelta(days=i+1)).isoformat() for i in range(dias_forecast)]

        resultados[zona] = [
            {
                "fecha": f,
                "viajes_forecast": p,
                "conductores_recomendados": max(1, int(p * 1.25)),
                "zona": zona,
            }
            for f, p in zip(fechas, predicciones)
        ]

    return resultados


# ─── Modelo de optimización de flota ─────────────────────────────────────────

def optimizar_asignacion_flota(forecast_zonas: dict) -> list[dict]:
    """
    Dado el forecast por zona, determina la asignación óptima de conductores.
    Usa proporcionalidad ponderada.
    """
    recomendaciones = []

    # Agrupar por fecha
    fechas = list(set(r["fecha"] for zone_data in forecast_zonas.values() for r in zone_data))

    for fecha in sorted(fechas):
        total_viajes = sum(
            next((r["viajes_forecast"] for r in zone_data if r["fecha"] == fecha), 0)
            for zone_data in forecast_zonas.values()
        )
        for zona, zone_data in forecast_zonas.items():
            registro = next((r for r in zone_data if r["fecha"] == fecha), None)
            if registro:
                proporcion = registro["viajes_forecast"] / total_viajes if total_viajes > 0 else 0
                recomendaciones.append({
                    "fecha": fecha,
                    "zona": zona,
                    "viajes_forecast": registro["viajes_forecast"],
                    "conductores_recomendados": registro["conductores_recomendados"],
                    "proporcion_demanda_pct": round(proporcion * 100, 1),
                })

    return recomendaciones


# ─── Display ──────────────────────────────────────────────────────────────────

def imprimir_resumen_demanda(patrones: dict, forecast: dict):
    """Imprime resumen de análisis de demanda."""
    print("\n" + "═" * 70)
    print("  🗺️  ANÁLISIS DE DEMANDA POR ZONA")
    print("═" * 70)
    print(f"\n  {'Zona':<15} {'Prom. diario':>14} {'Máximo':>10}")
    print("  " + "─" * 44)
    for zona, stats in sorted(patrones["por_zona"].items(), key=lambda x: -x[1]["promedio_diario"]):
        print(f"  {zona:<15} {stats['promedio_diario']:>14.0f} {stats['maximo']:>10}")

    print(f"\n  {'Franja':<10} {'Prom. viajes':>14} {'Pico':>10}")
    print("  " + "─" * 38)
    for franja, stats in sorted(patrones["por_franja_horaria"].items()):
        print(f"  {franja:<10} {stats['promedio']:>14.0f} {stats['maximo']:>10}")

    print("\n  📅 FORECAST PRÓXIMOS 7 DÍAS (Zona Centro)")
    print(f"\n  {'Fecha':<12} {'Viajes':>10} {'Conductores rec.':>18}")
    print("  " + "─" * 44)
    for r in forecast.get("Centro", [])[:7]:
        print(f"  {r['fecha']:<12} {r['viajes_forecast']:>10,.0f} {r['conductores_recomendados']:>18}")
    print("═" * 70 + "\n")


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    print("\n🚀 Iniciando pipeline de Forecast de Demanda\n")

    datos = generar_datos_demanda(dias=90)
    print(f"  ✓ Datos históricos: {len(datos):,} registros (90 días × 6 zonas × 8 franjas)")

    patrones = agregar_por_patron(datos)
    print("  ✓ Patrones de demanda calculados")

    forecast = forecast_por_zona(datos, dias_forecast=14)
    print("  ✓ Forecast generado para 14 días y 6 zonas")

    recomendaciones = optimizar_asignacion_flota(forecast)
    print(f"  ✓ Optimización de flota: {len(recomendaciones)} recomendaciones generadas")

    imprimir_resumen_demanda(patrones, forecast)

    # Exportar
    output_dir = Path(__file__).parent / "datasets"
    output_dir.mkdir(parents=True, exist_ok=True)
    fecha_str = datetime.now().strftime("%Y%m%d")
    resultado = {
        "generado_en": datetime.now().isoformat(),
        "datos_historicos_registros": len(datos),
        "patrones_demanda": patrones,
        "forecast_por_zona": forecast,
        "recomendaciones_flota": recomendaciones[:50],  # muestra
    }
    with open(output_dir / f"forecast_demanda_{fecha_str}.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Resultados exportados a datasets/")
    print("  ✅ Forecast de demanda completado.\n")


if __name__ == "__main__":
    main()
