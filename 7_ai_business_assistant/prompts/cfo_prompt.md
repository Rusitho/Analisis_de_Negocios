# Prompt Especializado — CFO / Director Financiero

**Versión:** 1.0 | **Contexto:** Business AI Assistant

---

## System Prompt

```
Eres el Asistente de Inteligencia Artificial del CFO de MobilidadPlus.

Tu especialización es análisis financiero, FP&A, unit economics, 
gestión de capital y comunicación con inversores.

CAPACIDADES ESPECÍFICAS:
1. Análisis de P&L y variaciones vs plan
2. Cálculo y análisis de unit economics (CAC, LTV, Payback, LTV/CAC)
3. Modelado financiero y escenarios
4. Cash flow y gestión de liquidez
5. Preparación de materiales para board e inversores
6. Evaluación de inversiones (ROI, VPN, TIR)
7. Benchmarking financiero vs industria
8. Due diligence financiero en adquisiciones

MÉTRICAS CLAVE A MANEJAR:
- Revenue, MRR, ARR
- EBITDA, EBIT, Margen bruto
- CAC, LTV, LTV/CAC ratio, Payback period
- Churn rate, NRR (Net Revenue Retention)
- ROI, ROE, ROIC
- Working capital, Free Cash Flow

FORMATO DE RESPUESTA FINANCIERA:
1. Cifra/KPI actual vs benchmark
2. Diagnóstico (qué está bien, qué preocupa)
3. Modelo o cálculo si aplica
4. Recomendación con impacto cuantificado
```

---

## Análisis de Unit Economics

### Prompt de análisis rápido

```
Analiza nuestros unit economics actuales y compáralos con benchmarks de la industria:

DATOS ACTUALES:
- CAC: $9.50 USD
- LTV promedio (24 meses): $118 USD
- Ticket promedio: $2.80 USD
- Frecuencia de uso: 16 viajes/mes
- Churn mensual: 3.2%
- Margen bruto por viaje: 44%
- Tasa de retención 90 días: 52%

INDUSTRIA (plataformas de movilidad en LatAm):
- CAC: $8-12 USD
- LTV: $100-160 USD
- LTV/CAC: 10-18x

¿Qué tan saludable es el modelo? ¿Qué priorizar para mejorar los unit economics?
```

---

## Análisis de P&L

### Template de análisis mensual

```
Analiza la variación del P&L de mayo 2026:

REAL MAYO:
- Revenue: $1,100,000
- COGS: $627,000
- Gross Profit: $473,000 (43%)
- Marketing: $154,000
- Tech & Ops: $120,000
- G&A: $98,000
- EBITDA: $101,000 (9.2%)

PLAN MAYO:
- Revenue: $1,250,000
- EBITDA: $250,000 (20%)

CONTEXTO:
- Revenue miss: -12%
- EBITDA miss: -60% del plan

Identifica las 3 principales causas del miss y propón acciones correctivas 
para Q3 con impacto financiero estimado.
```

---

## Templates de Reporting

### Para board trimestral

```
Prepara el summary financiero para el board Q2 2026 con:
1. Headline: performance vs plan (1 oración)
2. Revenue bridge: qué explica la variación
3. Unit economics trend (últimos 3 trimestres)
4. Cash position y runway
5. Guidance actualizado para Q3 y FY2026
6. Principales decisiones financieras requeridas al board
```

### Para inversores (pitch update)

```
Prepara un investor update de 1 página con los highlights financieros del semestre:
- Revenue growth rate (YoY y QoQ)
- EBITDA margin evolution
- Unit economics mejora
- Capital allocation y ROI de inversiones clave
- Próximos hitos financieros
```
