# ADR-001: Arquitectura de Plataforma de Datos — Lakehouse

**ID:** ADR-001  
**Título:** Adopción de arquitectura Lakehouse para la plataforma de datos  
**Estado:** Aprobado  
**Fecha:** 2026-06-02  
**Responsable:** CDO  
**Revisores:** CTO, CFO, COO

---

## Contexto

La organización requiere una plataforma de datos capaz de soportar:

1. Ingesta de datos en tiempo real y batch desde múltiples fuentes.
2. Almacenamiento escalable y económico.
3. Análisis histórico y en tiempo real.
4. Servir como base para modelos de ML y AI.
5. Cumplir con requisitos de gobernanza y auditoría.

Las opciones evaluadas fueron:

- **Data Warehouse tradicional** (Snowflake, BigQuery, Redshift)
- **Data Lake puro** (S3 + Glue/Athena)
- **Lakehouse** (Delta Lake + Databricks o Apache Iceberg + Spark)

---

## Decisión

**Se adopta arquitectura Lakehouse** con las siguientes capas:

```
raw/       → Datos brutos tal como llegan (Bronze)
clean/     → Datos validados y estandarizados (Silver)
curated/   → Modelos dimensionales listos para BI (Gold)
warehouse/ → Agregaciones y métricas pre-calculadas
```

**Stack tecnológico seleccionado:**

| Componente | Tecnología | Justificación |
|---|---|---|
| Storage | AWS S3 / Azure ADLS | Costo bajo, escalabilidad infinita |
| Table format | Delta Lake / Apache Iceberg | ACID transactions, time travel |
| Processing | Apache Spark (PySpark) | Escala batch y streaming |
| Orchestration | Apache Airflow | Open source, amplia comunidad |
| Serving layer | dbt + Trino/Athena | SQL estándar para analistas |
| BI/Dashboards | Apache Superset / Power BI | Libre + enterprise |
| ML Platform | MLflow + scikit-learn | Trazabilidad de experimentos |

---

## Motivo

### ¿Por qué Lakehouse sobre Data Warehouse puro?

| Criterio | Data Warehouse | Data Lake | Lakehouse |
|---|---|---|---|
| Costo almacenamiento | Alto | Bajo | Bajo |
| ACID transactions | Sí | No | Sí |
| Datos no estructurados | No | Sí | Sí |
| Performance analítica | Alta | Baja | Alta |
| Soporte ML/AI | Limitado | Sí | Sí |
| Gobernanza | Alta | Baja | Alta |
| Flexibilidad de esquema | Baja | Alta | Alta |

El Lakehouse combina lo mejor de ambos mundos: economía del Data Lake con capacidades ACID y gobernanza del Data Warehouse.

---

## Impacto Esperado

| Área | Impacto esperado | Indicador de éxito |
|---|---|---|
| Costos de infraestructura | -40% vs Data Warehouse tradicional | Factura mensual de cloud |
| Tiempo de onboarding de datos | -60% | Horas para integrar nueva fuente |
| Disponibilidad de datos para análisis | +80% | % datasets catalogados y usables |
| Capacidad ML/AI | Habilitada desde día 1 | Modelos en producción |
| Cumplimiento de auditoría | 100% trazable | Linaje de datos completo |

---

## Riesgos Asociados

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Curva de aprendizaje del equipo | Alta | Medio | Plan de capacitación 90 días |
| Deuda técnica en migración | Media | Alto | Migración incremental por dominio |
| Vendor lock-in cloud | Baja | Medio | Arquitectura cloud-agnostic con Delta/Iceberg |
| Costos de Spark en desarrollo | Media | Bajo | Entornos locales con Docker |

---

## KPIs Afectados

- `data_freshness_hours` — tiempo entre generación y disponibilidad en curated
- `pipeline_success_rate_%` — % de pipelines que completan sin error
- `data_quality_score_%` — score compuesto de calidad de datos
- `time_to_insight_hours` — desde evento de negocio hasta disponible en BI

---

## Alternativas Rechazadas

### Data Warehouse puro (Snowflake)

**Razón de rechazo:** Costo elevado para volúmenes grandes; no soporta nativamente datos no estructurados ni ML workloads de forma económica.

### Data Lake puro (S3 + Athena)

**Razón de rechazo:** Sin transacciones ACID, sin control de calidad de datos nativo, problema de "data swamp" sin gobernanza.

---

## Revisión

Esta decisión se revisará si:

- El costo mensual de infraestructura supera 2x el presupuesto aprobado.
- El equipo de datos no puede operar la plataforma efectivamente tras 6 meses.
- Surge una tecnología que cambie fundamentalmente el panorama (evaluar en revisión anual).

---

**Aprobado en reunión del Comité Estratégico del 2026-06-02**  
**Próxima revisión:** 2027-06-02
