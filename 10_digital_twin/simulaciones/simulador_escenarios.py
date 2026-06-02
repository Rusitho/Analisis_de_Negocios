"""
Digital Twin Empresarial — Simulador de Escenarios What-If
Permite simular el impacto de cambios en variables clave sobre KPIs financieros y operativos.
"""

import json
import math
from dataclasses import dataclass, field, asdict
from typing import Optional
from pathlib import Path
from datetime import datetime


# ─── Modelo base del negocio ──────────────────────────────────────────────────

@dataclass
class EstadoNegocio:
    """Snapshot del estado financiero y operativo del negocio."""
    # Métricas de demanda y volumen
    trafico_web_mensual: int = 55000
    tasa_conversion_pct: float = 3.8
    usuarios_activos_mensuales: int = 385000
    viajes_por_usuario_mes: float = 18.0
    ticket_promedio_usd: float = 2.80

    # Unit economics
    cac_usd: float = 9.0
    ltv_usd: float = 125.0
    churn_mensual_pct: float = 3.1
    margen_bruto_pct: float = 44.0

    # Operaciones
    conductores_activos: int = 2800
    utilizacion_flota_pct: float = 72.0
    costo_por_viaje_usd: float = 1.72
    sla_cumplimiento_pct: float = 92.0

    # Estructura de costos
    marketing_pct_revenue: float = 12.0
    tech_ops_pct_revenue: float = 10.0
    ga_pct_revenue: float = 8.0

    # Empleados
    headcount: int = 175
    productividad_usd_por_empleado: float = 85000.0

    def revenue_mensual(self) -> float:
        viajes = self.usuarios_activos_mensuales * self.viajes_por_usuario_mes
        return viajes * self.ticket_promedio_usd

    def ebitda_mensual(self) -> float:
        rev = self.revenue_mensual()
        gross_profit = rev * (self.margen_bruto_pct / 100)
        marketing = rev * (self.marketing_pct_revenue / 100)
        tech_ops = rev * (self.tech_ops_pct_revenue / 100)
        ga = rev * (self.ga_pct_revenue / 100)
        return gross_profit - marketing - tech_ops - ga

    def ebitda_margin_pct(self) -> float:
        rev = self.revenue_mensual()
        return (self.ebitda_mensual() / rev * 100) if rev > 0 else 0.0

    def roi_pct(self) -> float:
        inversion_total = self.cac_usd * (self.usuarios_activos_mensuales * 0.10)
        retorno = self.ltv_usd * (self.usuarios_activos_mensuales * 0.10) - inversion_total
        return (retorno / inversion_total * 100) if inversion_total > 0 else 0.0

    def ltv_cac_ratio(self) -> float:
        return self.ltv_usd / self.cac_usd if self.cac_usd > 0 else 0.0

    def viajes_diarios(self) -> int:
        return int((self.usuarios_activos_mensuales * self.viajes_por_usuario_mes) / 30)

    def costo_total_mensual(self) -> float:
        rev = self.revenue_mensual()
        cogs = rev * (1 - self.margen_bruto_pct / 100)
        opex = rev * ((self.marketing_pct_revenue + self.tech_ops_pct_revenue + self.ga_pct_revenue) / 100)
        return cogs + opex


# ─── Motor de simulación ──────────────────────────────────────────────────────

@dataclass
class ResultadoSimulacion:
    escenario: str
    descripcion: str
    cambios_aplicados: dict
    estado_base: dict
    estado_simulado: dict
    impacto: dict
    recomendacion: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


def simular_escenario(
    estado_base: EstadoNegocio,
    modificaciones: dict,
    nombre_escenario: str,
    descripcion: str,
    recomendacion: str,
) -> ResultadoSimulacion:
    """
    Aplica modificaciones al estado base y calcula el impacto en KPIs.
    Las modificaciones son factores multiplicativos o valores absolutos.
    """
    import copy
    estado_sim = copy.deepcopy(estado_base)

    # Aplicar modificaciones
    for campo, valor in modificaciones.items():
        if hasattr(estado_sim, campo):
            valor_actual = getattr(estado_sim, campo)
            if isinstance(valor, dict) and valor.get("tipo") == "delta_pct":
                nuevo_valor = valor_actual * (1 + valor["valor"] / 100)
            elif isinstance(valor, dict) and valor.get("tipo") == "absoluto":
                nuevo_valor = valor["valor"]
            else:
                nuevo_valor = valor
            setattr(estado_sim, campo, nuevo_valor)

    # Calcular estado base
    base_snapshot = {
        "revenue_mensual_usd": round(estado_base.revenue_mensual(), 2),
        "ebitda_mensual_usd": round(estado_base.ebitda_mensual(), 2),
        "ebitda_margin_pct": round(estado_base.ebitda_margin_pct(), 2),
        "roi_pct": round(estado_base.roi_pct(), 2),
        "ltv_cac_ratio": round(estado_base.ltv_cac_ratio(), 2),
        "viajes_diarios": estado_base.viajes_diarios(),
        "costo_total_mensual_usd": round(estado_base.costo_total_mensual(), 2),
        "usuarios_activos_mensuales": estado_base.usuarios_activos_mensuales,
        "cac_usd": estado_base.cac_usd,
        "churn_mensual_pct": estado_base.churn_mensual_pct,
    }

    # Calcular estado simulado
    sim_snapshot = {
        "revenue_mensual_usd": round(estado_sim.revenue_mensual(), 2),
        "ebitda_mensual_usd": round(estado_sim.ebitda_mensual(), 2),
        "ebitda_margin_pct": round(estado_sim.ebitda_margin_pct(), 2),
        "roi_pct": round(estado_sim.roi_pct(), 2),
        "ltv_cac_ratio": round(estado_sim.ltv_cac_ratio(), 2),
        "viajes_diarios": estado_sim.viajes_diarios(),
        "costo_total_mensual_usd": round(estado_sim.costo_total_mensual(), 2),
        "usuarios_activos_mensuales": estado_sim.usuarios_activos_mensuales,
        "cac_usd": round(estado_sim.cac_usd, 2),
        "churn_mensual_pct": round(estado_sim.churn_mensual_pct, 2),
    }

    # Calcular impacto
    impacto = {}
    for key in base_snapshot:
        base_val = base_snapshot[key]
        sim_val = sim_snapshot[key]
        if isinstance(base_val, (int, float)) and base_val != 0:
            delta_abs = sim_val - base_val
            delta_pct = (delta_abs / abs(base_val)) * 100
            impacto[key] = {
                "delta_absoluto": round(delta_abs, 2),
                "delta_pct": round(delta_pct, 2),
                "direccion": "↑" if delta_abs > 0 else "↓" if delta_abs < 0 else "→",
            }

    return ResultadoSimulacion(
        escenario=nombre_escenario,
        descripcion=descripcion,
        cambios_aplicados=modificaciones,
        estado_base=base_snapshot,
        estado_simulado=sim_snapshot,
        impacto=impacto,
        recomendacion=recomendacion,
    )


# ─── Escenarios predefinidos ──────────────────────────────────────────────────

def definir_escenarios() -> list[dict]:
    """Define todos los escenarios what-if del Digital Twin."""
    return [
        {
            "nombre": "ESC-001: Aumento de tráfico web +30%",
            "descripcion": "¿Qué ocurre si se incrementa el tráfico web en un 30% manteniendo la tasa de conversión?",
            "modificaciones": {
                "trafico_web_mensual": {"tipo": "delta_pct", "valor": 30},
                "usuarios_activos_mensuales": {"tipo": "delta_pct", "valor": 30 * 0.038 * 0.7},
            },
            "recomendacion": "Invertir en SEO y campañas paid con ROAS > 3x para lograr este crecimiento de forma rentable.",
        },
        {
            "nombre": "ESC-002: CAC sube 40% (competencia agresiva)",
            "descripcion": "¿Qué ocurre si el CAC aumenta un 40% por entrada de competidor con subsidios?",
            "modificaciones": {
                "cac_usd": {"tipo": "delta_pct", "valor": 40},
                "marketing_pct_revenue": {"tipo": "delta_pct", "valor": 35},
            },
            "recomendacion": "Si el CAC sube 40%, redirigir presupuesto a retención (retener es 5x más barato que adquirir). Activar programa de referidos.",
        },
        {
            "nombre": "ESC-003: Caída de conversión -25%",
            "descripcion": "¿Qué ocurre si la tasa de conversión cae un 25% (nuevo competidor, mala experiencia)?",
            "modificaciones": {
                "tasa_conversion_pct": {"tipo": "delta_pct", "valor": -25},
                "usuarios_activos_mensuales": {"tipo": "delta_pct", "valor": -15},
            },
            "recomendacion": "Auditar el funnel inmediatamente. A/B test de landing pages. Revisar calidad del tráfico pagado.",
        },
        {
            "nombre": "ESC-004: Contratación de +50 empleados",
            "descripcion": "¿Qué ocurre si contratamos 50 empleados adicionales (expansión)?",
            "modificaciones": {
                "headcount": {"tipo": "delta_pct", "valor": 29},
                "ga_pct_revenue": {"tipo": "delta_pct", "valor": 20},
            },
            "recomendacion": "Contratar solo si el crecimiento de revenue puede absorber el ~$3.5M adicional anual en nómina. Hacer análisis de ROI por función.",
        },
        {
            "nombre": "ESC-005: Aumento de demanda +50% en diciembre",
            "descripcion": "¿Qué ocurre en el mes de mayor demanda con un pico del 50% en viajes?",
            "modificaciones": {
                "usuarios_activos_mensuales": {"tipo": "delta_pct", "valor": 15},
                "viajes_por_usuario_mes": {"tipo": "delta_pct", "valor": 30},
                "ticket_promedio_usd": {"tipo": "delta_pct", "valor": 12},
                "conductores_activos": {"tipo": "delta_pct", "valor": 20},
                "costo_por_viaje_usd": {"tipo": "delta_pct", "valor": 5},
            },
            "recomendacion": "Preparar plan de contingencia de flota: +20% conductores activos, surge pricing moderado (1.2x-1.5x). El EBITDA mejora significativamente.",
        },
        {
            "nombre": "ESC-006: Churn sube al 6% mensual",
            "descripcion": "¿Qué ocurre si el churn mensual sube de 3.1% a 6% (crisis de experiencia)?",
            "modificaciones": {
                "churn_mensual_pct": {"tipo": "absoluto", "valor": 6.0},
                "usuarios_activos_mensuales": {"tipo": "delta_pct", "valor": -18},
                "ltv_usd": {"tipo": "delta_pct", "valor": -35},
            },
            "recomendacion": "Churn de 6% es crítico — activar protocolo de retención de emergencia. El impacto en LTV y revenue puede ser devastador si no se corrige en < 60 días.",
        },
        {
            "nombre": "ESC-007: Reducción de costos operativos -15%",
            "descripcion": "¿Qué impacto tiene lograr -15% en el costo por viaje via automatización?",
            "modificaciones": {
                "costo_por_viaje_usd": {"tipo": "delta_pct", "valor": -15},
                "margen_bruto_pct": {"tipo": "delta_pct", "valor": 12},
            },
            "recomendacion": "Esta mejora de eficiencia es la palanca con mayor impacto en EBITDA. Invertir en automatización de procesos tiene payback < 12 meses.",
        },
        {
            "nombre": "ESC-008: Expansión a nueva ciudad (costo +$1.5M anual)",
            "descripcion": "¿Qué ocurre si abrimos una nueva ciudad con inversión de $1.5M/año y 12% de revenue adicional en 18 meses?",
            "modificaciones": {
                "ga_pct_revenue": {"tipo": "delta_pct", "valor": 15},
                "marketing_pct_revenue": {"tipo": "delta_pct", "valor": 20},
                "usuarios_activos_mensuales": {"tipo": "delta_pct", "valor": 8},
            },
            "recomendacion": "La expansión impacta negativamente el EBITDA en los primeros 12 meses. Asegurarse de tener runway de 18+ meses antes de ejecutar.",
        },
    ]


# ─── Display ──────────────────────────────────────────────────────────────────

def imprimir_resultado(resultado: ResultadoSimulacion):
    """Imprime el resultado de un escenario en consola."""
    print(f"\n{'═' * 72}")
    print(f"  🔬  {resultado.escenario}")
    print(f"  {resultado.descripcion}")
    print(f"{'─' * 72}")
    print(f"\n  {'KPI':<35} {'Base':>12} {'Simulado':>12} {'Impacto':>10}")
    print(f"  {'─' * 72}")

    kpis_mostrar = [
        ("Revenue mensual (USD)", "revenue_mensual_usd", "${:,.0f}"),
        ("EBITDA mensual (USD)", "ebitda_mensual_usd", "${:,.0f}"),
        ("EBITDA margin %", "ebitda_margin_pct", "{:.1f}%"),
        ("ROI %", "roi_pct", "{:.1f}%"),
        ("LTV/CAC ratio", "ltv_cac_ratio", "{:.1f}x"),
        ("Viajes diarios", "viajes_diarios", "{:,.0f}"),
        ("Usuarios activos", "usuarios_activos_mensuales", "{:,.0f}"),
        ("CAC (USD)", "cac_usd", "${:.2f}"),
        ("Churn mensual %", "churn_mensual_pct", "{:.1f}%"),
    ]

    for label, key, fmt in kpis_mostrar:
        base = resultado.estado_base.get(key, 0)
        sim = resultado.estado_simulado.get(key, 0)
        imp = resultado.impacto.get(key, {})
        delta = imp.get("delta_pct", 0)
        dir_arrow = imp.get("direccion", "→")
        color_str = f"{dir_arrow} {delta:+.1f}%" if delta != 0 else "→ sin cambio"
        try:
            base_str = fmt.format(base)
            sim_str = fmt.format(sim)
        except Exception:
            base_str = str(base)
            sim_str = str(sim)
        print(f"  {label:<35} {base_str:>12} {sim_str:>12} {color_str:>10}")

    print(f"\n  💡 RECOMENDACIÓN: {resultado.recomendacion}")


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    print("\n🚀 Digital Twin Empresarial — Simulador de Escenarios What-If")
    print("=" * 72)

    # Estado base del negocio
    estado_base = EstadoNegocio()
    print(f"\n  📊 Estado Base del Negocio:")
    print(f"     Revenue mensual:    ${estado_base.revenue_mensual():>12,.0f} USD")
    print(f"     EBITDA mensual:     ${estado_base.ebitda_mensual():>12,.0f} USD")
    print(f"     EBITDA margin:      {estado_base.ebitda_margin_pct():>11.1f}%")
    print(f"     LTV/CAC ratio:      {estado_base.ltv_cac_ratio():>11.1f}x")
    print(f"     Viajes diarios:     {estado_base.viajes_diarios():>12,}")

    # Ejecutar todos los escenarios
    escenarios_config = definir_escenarios()
    resultados = []

    print(f"\n  ⚙️  Ejecutando {len(escenarios_config)} escenarios...\n")

    for cfg in escenarios_config:
        resultado = simular_escenario(
            estado_base=estado_base,
            modificaciones=cfg["modificaciones"],
            nombre_escenario=cfg["nombre"],
            descripcion=cfg["descripcion"],
            recomendacion=cfg["recomendacion"],
        )
        resultados.append(resultado)
        imprimir_resultado(resultado)

    # Exportar resultados
    output_dir = Path(__file__).parent.parent / "escenarios"
    output_dir.mkdir(parents=True, exist_ok=True)
    fecha_str = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = output_dir / f"simulacion_{fecha_str}.json"

    payload = {
        "generado_en": datetime.now().isoformat(),
        "estado_base": asdict(estado_base),
        "escenarios": [asdict(r) for r in resultados],
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"\n  ✅ {len(resultados)} escenarios simulados y exportados a: {output_path}\n")


if __name__ == "__main__":
    main()
