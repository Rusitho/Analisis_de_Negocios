# Proceso de Ventas — BPMN

**Proceso:** Ciclo completo de ventas B2C y B2B  
**Versión:** 1.0  
**Propietario:** CMO / CCO  
**Última actualización:** 2026-06-02

---

## Proceso B2C — Adquisición y Primer Viaje

```mermaid
flowchart TD
    START([Usuario descubre la app]) --> D1{¿Canal de llegada?}
    D1 -->|Orgánico/Referido| REG[Registro en app]
    D1 -->|Paid/SEM| LP[Landing page]
    LP --> REG
    REG --> VER[Verificación email/teléfono]
    VER --> ACT{¿Completa activación?}
    ACT -->|No| NUR[Email nurturing D+1, D+3, D+7]
    NUR --> ACT2{¿Regresa?}
    ACT2 -->|No después de 14 días| CHURN_P[Pérdida de prospecto]
    ACT2 -->|Sí| PRIM[Solicitar primer viaje]
    ACT -->|Sí| PRIM
    PRIM --> MATCH[Sistema hace match con conductor]
    MATCH --> VIA[Viaje completado]
    VIA --> RAT[Usuario califica]
    RAT --> NPS_CHECK{¿Rating ≥ 4?}
    NPS_CHECK -->|Sí| REF[Enviar programa de referidos]
    NPS_CHECK -->|No| REC[Equipo CX contacta en < 2h]
    REF --> RET[Secuencia retención D+3]
    REC --> RET
    RET --> END([Usuario retenido / activo])
```

---

## Proceso B2B — Venta Corporativa

```mermaid
flowchart TD
    START([Lead corporativo identificado]) --> QUAL{¿Calificación?}
    QUAL -->|Empresa < 10 empleados| SELF[Self-service en web]
    QUAL -->|Empresa 10-100| INSIDE[Inside Sales — llamada 30 min]
    QUAL -->|Empresa > 100| FIELD[Field Sales — reunión presencial]
    
    INSIDE --> DEM[Demo del portal corporativo]
    FIELD --> DEM
    SELF --> ONB_SELF[Onboarding automatizado]
    
    DEM --> PROP[Envío de propuesta comercial]
    PROP --> NEG{¿Negociación?}
    NEG -->|Acuerda precio estándar| CONT[Firma de contrato]
    NEG -->|Requiere personalización| APPR[Aprobación gerencial]
    APPR --> CONT
    NEG -->|No cierra| LOSE[CRM — nurturing 90 días]
    
    CONT --> SETUP[Setup de cuenta corporativa]
    SETUP --> ONB[Capacitación de administrador]
    ONB --> PILOT[Piloto 30 días]
    PILOT --> REV{¿Review piloto positivo?}
    REV -->|Sí| FULL[Despliegue completo]
    REV -->|No| SUPP[Soporte especializado + ajustes]
    SUPP --> FULL
    FULL --> CS[Asignación de Customer Success Manager]
    CS --> END([Cuenta activa y satisfecha])
```

---

## Proceso de Atención al Cliente

```mermaid
flowchart TD
    INC([Incidente o consulta del usuario]) --> CH{¿Canal de contacto?}
    CH -->|Chat in-app| BOT[Chatbot IA — resolución automática]
    CH -->|Email| TK[Ticket creado en CRM]
    CH -->|Teléfono| AG[Agente humano]
    
    BOT --> BOT_RES{¿Resuelto por bot?}
    BOT_RES -->|Sí — 65% casos| CLOSE[Caso cerrado — CSAT automático]
    BOT_RES -->|No| TK
    
    TK --> PRIO{¿Prioridad?}
    PRIO -->|Crítico — seguridad| ESC[Escalada inmediata al supervisor]
    PRIO -->|Alto — cargo incorrecto| AG
    PRIO -->|Bajo — información| AG
    
    AG --> RES{¿Resuelto en primer contacto?}
    RES -->|Sí| CSAT[Encuesta CSAT]
    RES -->|No| L2[Escalada L2 / Especialista]
    L2 --> RES2{¿Resuelto?}
    RES2 -->|Sí| CSAT
    RES2 -->|No| L3[Escalada L3 / Gerencia]
    L3 --> CSAT
    
    CSAT --> ANALY[Análisis de feedback]
    ANALY --> KB[Actualizar base de conocimiento]
    KB --> END([Proceso completado])
```

---

## KPIs del Proceso de Ventas

| KPI | Meta | Fórmula |
|---|---|---|
| Tasa de conversión Lead → Cliente | ≥ 25% | (Clientes nuevos / Leads) × 100 |
| Tiempo promedio de cierre B2B | ≤ 21 días | Fecha cierre - Fecha primer contacto |
| Costo de adquisición (CAC) | ≤ $8 USD | Gasto marketing+ventas / Clientes nuevos |
| Activación (primer viaje en 7 días) | ≥ 70% | (Usuarios con 1+ viaje en 7d / Registros) × 100 |
| First Contact Resolution | ≥ 80% | (Casos resueltos en 1er contacto / Total) × 100 |
| SLA respuesta CS | ≤ 4 horas | Tiempo promedio primera respuesta |

---

## Métricas del Embudo de Ventas

```
100 visitantes al sitio
    ↓ CVR 20%
 20 registros
    ↓ Activación 70%
 14 usuarios activos
    ↓ Retención 30d 55%
  8 usuarios retenidos
    ↓ LTV $140
$1,120 ingreso esperado por cohorte de 100 visitantes
```

**CPA efectivo:** $8/100 visitantes × ($1,120 LTV) = ROI 14x por visitante convertido
