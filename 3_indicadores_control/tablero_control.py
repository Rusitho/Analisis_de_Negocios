"""
Tablero de Control Empresarial — Business Operating System
Genera KPIs, semáforos de estado, detecta desviaciones y exporta reportes.
"""

import json
import csv
import random
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


# ─── Configuración de umbrales por KPI ───────────────────────────────────────

KPIS_CONFIG = {
    # Web Performance
    "visitas_mensuales":        {"verde": (50000, None),  "amarillo": (30000, 49999), "rojo": (None, 29999), "meta": 60000, "unidad": "sesiones",   "area": "Web"},
    "tasa_conversion_web":      {"verde": (3.5, None),    "amarillo": (2.0, 3.4),     "rojo": (None, 1.9),   "meta": 4.0,   "unidad": "%",          "area": "Web"},
    "bounce_rate":              {"verde": (None, 35),     "amarillo": (36, 55),       "rojo": (56, None),    "meta": 32,    "unidad": "%",          "area": "Web"},
    "leads_generados":          {"verde": (2000, None),   "amarillo": (1200, 1999),   "rojo": (None, 1199),  "meta": 2500,  "unidad": "leads",      "area": "Web"},
    # Operaciones
    "sla_cumplimiento_pct":     {"verde": (95, None),     "amarillo": (88, 94.9),     "rojo": (None, 87.9),  "meta": 96,    "unidad": "%",          "area": "Ops"},
    "tiempo_resolucion_h":      {"verde": (None, 3.5),    "amarillo": (3.6, 6.0),     "rojo": (6.1, None),   "meta": 3.0,   "unidad": "horas",      "area": "Ops"},
    "uptime_plataforma_pct":    {"verde": (99.5, None),   "amarillo": (98.0, 99.4),   "rojo": (None, 97.9),  "meta": 99.9,  "unidad": "%",          "area": "Tech"},
    "costo_por_viaje_usd":      {"verde": (None, 1.60),   "amarillo": (1.61, 1.90),   "rojo": (1.91, None),  "meta": 1.57,  "unidad": "USD",        "area": "Ops"},
    # Clientes
    "nps":                      {"verde": (65, None),     "amarillo": (45, 64),       "rojo": (None, 44),    "meta": 72,    "unidad": "puntos",     "area": "CX"},
    "csat":                     {"verde": (88, None),     "amarillo": (75, 87.9),     "rojo": (None, 74.9),  "meta": 92,    "unidad": "%",          "area": "CX"},
    "churn_rate_mensual":       {"verde": (None, 2.5),    "amarillo": (2.6, 4.0),     "rojo": (4.1, None),   "meta": 2.2,   "unidad": "%",          "area": "CX"},
    "usuarios_activos_mensuales":{"verde": (450000, None),"amarillo": (300000, 449999),"rojo": (None, 299999),"meta": 500000,"unidad": "usuarios",  "area": "CX"},
    # Finanzas
    "revenue_total_usd":        {"verde": (1150000, None),"amarillo": (900000, 1149999),"rojo": (None, 899999),"meta":1250000,"unidad":"USD",       "area": "Fin"},
    "cac_usd":                  {"verde": (None, 8.0),    "amarillo": (8.1, 12.0),    "rojo": (12.1, None),  "meta": 7.5,   "unidad": "USD",        "area": "Fin"},
    "ltv_promedio_usd":         {"verde": (130, None),    "amarillo": (90, 129),      "rojo": (None, 89),    "meta": 140,   "unidad": "USD",        "area": "Fin"},
    "ebitda_pct":               {"verde": (20, None),     "amarillo": (12, 19.9),     "rojo": (None, 11.9),  "meta": 22,    "unidad": "%",          "area": "Fin"},
    "roi_pct":                  {"verde": (25, None),     "amarillo": (15, 24.9),     "rojo": (None, 14.9),  "meta": 28,    "unidad": "%",          "area": "Fin"},
    "margen_bruto_pct":         {"verde": (45, None),     "amarillo": (35, 44.9),     "rojo": (None, 34.9),  "meta": 48,    "unidad": "%",          "area": "Fin"},
}


# ─── Modelos de datos ─────────────────────────────────────────────────────────

@dataclass
class KPIResult:
    nombre: str
    valor: float
    meta: float
    unidad: str
    area: str
    semaforo: str  # "VERDE" | "AMARILLO" | "ROJO"
    desviacion_pct: float
    alerta: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# ─── Generador de datos simulados ────────────────────────────────────────────

def generar_datos_simulados() -> dict:
    """Genera un snapshot de KPIs con valores realistas y algo de varianza."""
    base = {
        "visitas_mensuales":         random.randint(42000, 68000),
        "tasa_conversion_web":       round(random.uniform(2.8, 4.5), 2),
        "bounce_rate":               round(random.uniform(28, 52), 1),
        "leads_generados":           random.randint(1600, 3000),
        "sla_cumplimiento_pct":      round(random.uniform(88, 98), 1),
        "tiempo_resolucion_h":       round(random.uniform(2.0, 7.0), 1),
        "uptime_plataforma_pct":     round(random.uniform(98.5, 99.99), 2),
        "costo_por_viaje_usd":       round(random.uniform(1.45, 2.10), 2),
        "nps":                       random.randint(48, 78),
        "csat":                      round(random.uniform(72, 96), 1),
        "churn_rate_mensual":        round(random.uniform(1.8, 5.2), 2),
        "usuarios_activos_mensuales": random.randint(280000, 520000),
        "revenue_total_usd":         random.randint(850000, 1400000),
        "cac_usd":                   round(random.uniform(6.5, 14.0), 2),
        "ltv_promedio_usd":          round(random.uniform(80, 165), 1),
        "ebitda_pct":                round(random.uniform(10, 28), 1),
        "roi_pct":                   round(random.uniform(12, 35), 1),
        "margen_bruto_pct":          round(random.uniform(38, 55), 1),
    }
    return base


# ─── Motor de semáforo ────────────────────────────────────────────────────────

def evaluar_semaforo(nombre: str, valor: float) -> str:
    """
    Retorna 'VERDE', 'AMARILLO' o 'ROJO' comparando el valor contra umbrales.
    Umbrales con None = sin límite en esa dirección.
    """
    cfg = KPIS_CONFIG[nombre]

    def en_rango(v, rango):
        lo, hi = rango
        if lo is not None and v < lo:
            return False
        if hi is not None and v > hi:
            return False
        return True

    if en_rango(valor, cfg["verde"]):
        return "VERDE"
    if en_rango(valor, cfg["amarillo"]):
        return "AMARILLO"
    return "ROJO"


def calcular_desviacion(valor: float, meta: float) -> float:
    """Retorna el % de desviación respecto a la meta (positivo = sobre meta)."""
    if meta == 0:
        return 0.0
    return round(((valor - meta) / meta) * 100, 2)


# ─── Generador de alertas ─────────────────────────────────────────────────────

MENSAJES_ALERTA = {
    "visitas_mensuales":          "⚠️ Tráfico web bajo el umbral — revisar campañas y SEO",
    "tasa_conversion_web":        "⚠️ Conversión baja — auditar landing pages y funnel",
    "bounce_rate":                "⚠️ Bounce rate elevado — revisar experiencia y relevancia del contenido",
    "leads_generados":            "⚠️ Generación de leads insuficiente — activar campañas adicionales",
    "sla_cumplimiento_pct":       "🔴 SLA comprometido — revisar operaciones y capacidad",
    "tiempo_resolucion_h":        "⚠️ Tiempo de resolución fuera de SLA — reforzar equipo de CS",
    "uptime_plataforma_pct":      "🔴 Disponibilidad de plataforma comprometida — escalada a CTO",
    "costo_por_viaje_usd":        "⚠️ Costo por viaje elevado — revisar eficiencia operativa",
    "nps":                        "🔴 NPS por debajo del objetivo — revisar experiencia del cliente",
    "csat":                       "⚠️ Satisfacción del cliente baja — análisis de puntos de dolor",
    "churn_rate_mensual":         "🔴 Churn elevado — activar programa de retención urgente",
    "usuarios_activos_mensuales": "⚠️ MAU por debajo del objetivo — revisar activación y retención",
    "revenue_total_usd":          "🔴 Revenue bajo el objetivo — revisar pipeline comercial",
    "cac_usd":                    "⚠️ CAC elevado — optimizar canales de adquisición",
    "ltv_promedio_usd":           "⚠️ LTV bajo — trabajar retención y upselling",
    "ebitda_pct":                 "🔴 EBITDA bajo objetivo — revisar estructura de costos",
    "roi_pct":                    "⚠️ ROI insuficiente — revisar eficiencia de inversiones",
    "margen_bruto_pct":           "⚠️ Margen bruto bajo — revisar costos directos del servicio",
}


# ─── Motor principal del tablero ──────────────────────────────────────────────

def calcular_kpis(datos: dict) -> list[KPIResult]:
    """Procesa los datos crudos y retorna una lista de KPIResult con semáforos."""
    resultados = []
    for nombre, valor in datos.items():
        if nombre not in KPIS_CONFIG:
            continue
        cfg = KPIS_CONFIG[nombre]
        semaforo = evaluar_semaforo(nombre, valor)
        desviacion = calcular_desviacion(valor, cfg["meta"])
        alerta = MENSAJES_ALERTA.get(nombre) if semaforo in ("AMARILLO", "ROJO") else None
        resultados.append(KPIResult(
            nombre=nombre,
            valor=valor,
            meta=cfg["meta"],
            unidad=cfg["unidad"],
            area=cfg["area"],
            semaforo=semaforo,
            desviacion_pct=desviacion,
            alerta=alerta,
        ))
    return resultados


# ─── Exportadores ─────────────────────────────────────────────────────────────

def exportar_csv(resultados: list[KPIResult], ruta: str):
    """Exporta los resultados a un archivo CSV."""
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "area", "kpi", "valor", "meta", "unidad",
                          "semaforo", "desviacion_pct", "alerta"])
        for r in resultados:
            writer.writerow([r.timestamp, r.area, r.nombre, r.valor, r.meta,
                              r.unidad, r.semaforo, r.desviacion_pct,
                              r.alerta or ""])
    print(f"  ✓ CSV exportado: {ruta}")


def exportar_json(resultados: list[KPIResult], ruta: str):
    """Exporta los resultados a un archivo JSON."""
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generado_en": datetime.now().isoformat(),
        "total_kpis": len(resultados),
        "resumen": {
            "verde": sum(1 for r in resultados if r.semaforo == "VERDE"),
            "amarillo": sum(1 for r in resultados if r.semaforo == "AMARILLO"),
            "rojo": sum(1 for r in resultados if r.semaforo == "ROJO"),
        },
        "kpis": [
            {
                "nombre": r.nombre, "area": r.area, "valor": r.valor,
                "meta": r.meta, "unidad": r.unidad, "semaforo": r.semaforo,
                "desviacion_pct": r.desviacion_pct, "alerta": r.alerta,
                "timestamp": r.timestamp,
            }
            for r in resultados
        ],
    }
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"  ✓ JSON exportado: {ruta}")


# ─── Display ─────────────────────────────────────────────────────────────────

ICONOS = {"VERDE": "🟢", "AMARILLO": "🟡", "ROJO": "🔴"}
COLORES_CONSOLA = {
    "VERDE":    "\033[92m",
    "AMARILLO": "\033[93m",
    "ROJO":     "\033[91m",
    "RESET":    "\033[0m",
}


def imprimir_tablero(resultados: list[KPIResult]):
    """Imprime el tablero de control en consola con formato legible."""
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
    verde   = sum(1 for r in resultados if r.semaforo == "VERDE")
    amarillo = sum(1 for r in resultados if r.semaforo == "AMARILLO")
    rojo    = sum(1 for r in resultados if r.semaforo == "ROJO")

    print("\n" + "═" * 80)
    print(f"  📊  TABLERO DE CONTROL EMPRESARIAL — BOS  │  {ahora}")
    print("═" * 80)
    print(f"  Resumen:  🟢 {verde} Verde   🟡 {amarillo} Amarillo   🔴 {rojo} Rojo   │ Total: {len(resultados)} KPIs")
    print("─" * 80)

    areas = sorted(set(r.area for r in resultados))
    for area in areas:
        kpis_area = [r for r in resultados if r.area == area]
        print(f"\n  ▶ ÁREA: {area}")
        print(f"  {'KPI':<32} {'Valor':>12} {'Meta':>10} {'Dev%':>8}  Estado")
        print("  " + "─" * 74)
        for r in kpis_area:
            icono = ICONOS[r.semaforo]
            dev_str = f"{'+' if r.desviacion_pct >= 0 else ''}{r.desviacion_pct:.1f}%"
            color = COLORES_CONSOLA[r.semaforo]
            reset = COLORES_CONSOLA["RESET"]
            print(f"  {r.nombre:<32} {r.valor:>10.2f} {r.meta:>10.2f} {dev_str:>8}  {color}{icono} {r.semaforo}{reset}")

    alertas = [r for r in resultados if r.alerta]
    if alertas:
        print("\n" + "─" * 80)
        print("  🚨  ALERTAS ACTIVAS")
        print("─" * 80)
        for r in alertas:
            print(f"  [{r.semaforo}] {r.nombre}: {r.alerta}")

    print("\n" + "═" * 80 + "\n")


# ─── Análisis de tendencias ───────────────────────────────────────────────────

def analizar_tendencias(periodos: int = 3) -> list[dict]:
    """
    Simula múltiples períodos y detecta KPIs con tendencia deteriorante.
    Retorna lista de KPIs con tendencia negativa.
    """
    historico = [calcular_kpis(generar_datos_simulados()) for _ in range(periodos)]
    tendencias = []

    for nombre in KPIS_CONFIG:
        valores = []
        for snapshot in historico:
            for r in snapshot:
                if r.nombre == nombre:
                    valores.append(r.valor)
        if len(valores) < 2:
            continue
        # Tendencia: compara último valor vs promedio de anteriores
        prom_prev = sum(valores[:-1]) / len(valores[:-1])
        ultimo = valores[-1]
        cambio_pct = ((ultimo - prom_prev) / prom_prev * 100) if prom_prev != 0 else 0

        cfg = KPIS_CONFIG[nombre]
        # Para KPIs donde "menor = mejor" (bounce_rate, churn, cac, etc.)
        kpis_invertidos = {"bounce_rate", "churn_rate_mensual", "cac_usd",
                           "costo_por_viaje_usd", "tiempo_resolucion_h"}
        deterioro = cambio_pct < -3 if nombre not in kpis_invertidos else cambio_pct > 3

        if deterioro:
            tendencias.append({
                "kpi": nombre,
                "area": cfg["area"],
                "cambio_pct": round(cambio_pct, 2),
                "alerta": f"Tendencia deteriorante: {cambio_pct:+.1f}% vs períodos anteriores"
            })

    return tendencias


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    print("\n🚀 Iniciando Business Operating System — Tablero de Control\n")

    # 1. Generar datos del período actual
    datos = generar_datos_simulados()

    # 2. Calcular KPIs y semáforos
    resultados = calcular_kpis(datos)

    # 3. Mostrar tablero en consola
    imprimir_tablero(resultados)

    # 4. Analizar tendencias
    print("  📈 Analizando tendencias (últimos 3 períodos)...")
    tendencias = analizar_tendencias(periodos=3)
    if tendencias:
        print(f"  ⚠️  {len(tendencias)} KPI(s) con tendencia deteriorante:")
        for t in tendencias:
            print(f"     • [{t['area']}] {t['kpi']}: {t['alerta']}")
    else:
        print("  ✅ Sin tendencias deteriorantes detectadas")

    # 5. Exportar resultados
    fecha_str = datetime.now().strftime("%Y%m%d_%H%M")
    output_dir = Path(__file__).parent / "data"
    exportar_csv(resultados, str(output_dir / f"kpis_{fecha_str}.csv"))
    exportar_json(resultados, str(output_dir / f"kpis_{fecha_str}.json"))

    print("\n  ✅ Tablero de control ejecutado exitosamente.\n")


if __name__ == "__main__":
    main()
