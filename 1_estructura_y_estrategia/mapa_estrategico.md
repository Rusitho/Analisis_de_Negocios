# Mapa Estratégico — Balanced Scorecard

**Versión:** 1.0  
**Fecha:** 2026-06-02  
**Marco:** Balanced Scorecard (Kaplan & Norton)

---

## Mapa Estratégico Visual

```mermaid
graph TD
    subgraph F["💰 PERSPECTIVA FINANCIERA"]
        F1[Incrementar Ingresos<br/>Meta: $15M USD]
        F2[Mejorar Rentabilidad<br/>EBITDA ≥ 22%]
        F3[Optimizar Capital<br/>ROI ≥ 25%]
    end

    subgraph C["👥 PERSPECTIVA DE CLIENTES"]
        C1[Ser la app de movilidad<br/>preferida — NPS ≥ 72]
        C2[Crecer base de usuarios<br/>500K MAU]
        C3[Reducir Churn<br/>≤ 2.5% mensual]
        C4[Resolver problemas rápido<br/>90% en < 4h]
    end

    subgraph P["⚙️ PERSPECTIVA DE PROCESOS"]
        P1[Plataforma confiable<br/>Uptime 99.9%]
        P2[Operación eficiente<br/>Costo/viaje -15%]
        P3[SLAs cumplidos<br/>≥ 95%]
        P4[Procesos automatizados<br/>+30 procesos/año]
    end

    subgraph A["🎓 PERSPECTIVA DE APRENDIZAJE"]
        A1[Cultura data-driven<br/>100% C-suite con datos]
        A2[Capacidades de IA/ML<br/>5 modelos en prod.]
        A3[Talento de alto desempeño<br/>Engagement ≥ 80%]
        A4[Gobierno del dato<br/>85% datasets catalogados]
    end

    A1 --> P1
    A2 --> P2
    A2 --> P4
    A3 --> P3
    A4 --> P2
    P1 --> C1
    P2 --> C3
    P3 --> C4
    P4 --> C2
    C1 --> F1
    C2 --> F1
    C3 --> F2
    C4 --> F2
    F1 --> F3
    F2 --> F3
```

---

## Perspectiva Financiera

### Objetivo estratégico: Crecimiento sostenible y rentable

| KPI | Baseline | Meta 2026 | Tendencia objetivo |
|---|---|---|---|
| Ingresos totales | $10.5M | $15.0M (+43%) | ↑ |
| EBITDA margin | 17.5% | 22.0% | ↑ |
| ROI de inversiones | 18% | 25% | ↑ |
| Flujo de caja operativo | $1.8M | $3.2M | ↑ |
| CAC | $10.0 | $8.0 (-20%) | ↓ |
| LTV | $110 | $140 (+27%) | ↑ |
| LTV/CAC ratio | 11x | 17.5x | ↑ |

**Iniciativas financieras clave:**
1. Diversificación de ingresos (nuevos servicios premium)
2. Optimización de estructura de costos por automatización
3. Expansión geográfica con bajo CAPEX

---

## Perspectiva de Clientes

### Objetivo estratégico: Ser la plataforma de movilidad preferida

| KPI | Baseline | Meta 2026 | Tendencia objetivo |
|---|---|---|---|
| NPS | 58 | 72 | ↑ |
| CSAT (satisfacción por viaje) | 3.9/5 | 4.5/5 | ↑ |
| Usuarios Activos Mensuales | 320K | 500K | ↑ |
| Churn mensual | 4.2% | 2.5% | ↓ |
| Tiempo medio resolución | 6.2h | 3.5h | ↓ |
| First Contact Resolution | 62% | 82% | ↑ |
| Rating app store | 3.8 | 4.6 | ↑ |

**Iniciativas de clientes clave:**
1. Rediseño de experiencia en app (UX Research)
2. Programa de fidelización con beneficios tangibles
3. Canal de atención omnicanal con respuesta en < 2h
4. Personalización de la experiencia por segmento

---

## Perspectiva de Procesos Internos

### Objetivo estratégico: Operación confiable, eficiente y escalable

| KPI | Baseline | Meta 2026 | Tendencia objetivo |
|---|---|---|---|
| Uptime plataforma | 98.5% | 99.9% | ↑ |
| MTTR (Mean Time to Recover) | 4.2h | 1.5h | ↓ |
| Costo por viaje | $1.85 | $1.57 | ↓ |
| SLA cumplimiento % | 87% | 95% | ↑ |
| Procesos automatizados | 12 | 42 | ↑ |
| Lead time de nuevas features | 21 días | 10 días | ↓ |
| Incidentes críticos/mes | 3.2 | ≤ 1 | ↓ |

**Iniciativas de procesos clave:**
1. Implementación de plataforma DevOps/SRE
2. Automatización RPA de procesos administrativos
3. Optimización de rutas con ML (ahorro combustible)
4. Control tower operativo con alertas en tiempo real

---

## Perspectiva de Aprendizaje y Crecimiento

### Objetivo estratégico: Construir las capacidades del futuro

| KPI | Baseline | Meta 2026 | Tendencia objetivo |
|---|---|---|---|
| Employee Engagement | 64% | 82% | ↑ |
| Rotación voluntaria | 18% | ≤ 10% | ↓ |
| Horas capacitación/empleado/año | 24h | 48h | ↑ |
| Modelos ML en producción | 0 | 5 | ↑ |
| Datasets catalogados | 20% | 85% | ↑ |
| C-suite data-driven decisions | 30% | 100% | ↑ |
| Índice de innovación (ideas → prod) | 2% | 8% | ↑ |

**Iniciativas de aprendizaje clave:**
1. Academia interna de datos y analítica
2. Programa de AI Champions en cada área
3. Implementación de Data Lakehouse y gobierno del dato
4. Plan de carrera para retención de talento técnico

---

## Relaciones de Causalidad

```mermaid
flowchart LR
    A[Talento comprometido<br/>Engagement ↑] --> B[Procesos eficientes<br/>SLA ↑ / Costo ↓]
    C[Capacidades de datos<br/>ML en producción] --> B
    B --> D[Experiencia del cliente<br/>NPS ↑ / Churn ↓]
    D --> E[Crecimiento de ingresos<br/>Revenue ↑]
    E --> F[Rentabilidad<br/>EBITDA ↑]
    F --> G[Valor para accionistas<br/>ROI ↑]
    G -.->|Reinversión| A
```

---

## Temas Estratégicos

```mermaid
mindmap
  root((Estrategia<br/>2026))
    Crecimiento
      Expansión geográfica
      Nuevos segmentos
      Diversificación
    Eficiencia
      Automatización
      Optimización costos
      Calidad operativa
    Experiencia
      NPS líder
      Omnicanalidad
      Personalización
    Innovación
      AI/ML en producción
      Data como activo
      Nuevos modelos de negocio
    Gobierno
      Gestión de riesgos
      Cumplimiento
      Auditabilidad
```

---

*El Mapa Estratégico se revisa trimestralmente en el Comité Estratégico y se actualiza según los cambios en el contexto competitivo y los resultados obtenidos.*
