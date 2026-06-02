# Log de Cambios y Decisiones Estratégicas

> Registro histórico de decisiones, cambios de política y modificaciones relevantes al BOS.  
> Este archivo se actualiza con cada cambio significativo. Para cambios en código y datos, el historial de Git es la fuente primaria.

---

## Formato de Registro

```
### [YYYY-MM-DD] — Tipo: [Estratégico|Operacional|Técnico|Governance]
**Responsable:** [Nombre/Rol]
**Descripción:** Qué cambió y por qué.
**Impacto:** KPIs o áreas afectadas.
**ADR relacionado:** ADR-XXX (si aplica)
```

---

## Historial

---

### [2026-06-02] — Tipo: Estratégico
**Responsable:** CEO + Comité Estratégico  
**Descripción:** Lanzamiento del Business Operating System v1.0. Implementación de la arquitectura completa del BOS con todos sus módulos: Gobierno, Estrategia, Madurez, KPIs, Auditoría, Web, Analítica, AI, Datos, Observabilidad y Digital Twin.  
**Impacto:** Todos los KPIs ahora son trazables. Primera línea base establecida para todos los indicadores estratégicos.  
**ADR relacionado:** ADR-001 (Arquitectura Lakehouse)

---

### [2026-06-02] — Tipo: Governance
**Responsable:** CRO  
**Descripción:** Publicación de la primera versión de la Matriz de Riesgos. Se identificaron 7 riesgos principales, 4 en nivel Alto y 3 en nivel Medio. Ningún riesgo crítico activo.  
**Impacto:** KRIs comenzarán a medirse a partir de esta fecha. Línea base de gestión de riesgos establecida.  
**ADR relacionado:** N/A

---

### [2026-06-02] — Tipo: Técnico
**Responsable:** CDO  
**Descripción:** Definición del diccionario de KPIs v1.0 con 32 indicadores en 5 categorías. Implementación del tablero de control automatizado en Python con semáforos, alertas y exportación CSV/JSON.  
**Impacto:** Los 32 KPIs ahora tienen definición, fórmula, umbral y responsable asignado.  
**ADR relacionado:** ADR-001

---

## Próximas actualizaciones programadas

| Fecha | Tipo | Descripción | Responsable |
|---|---|---|---|
| 2026-07-01 | Estratégico | Review Q2 OKRs — ajuste de metas si es necesario | CEO |
| 2026-09-01 | Técnico | Implementación de modelos ML v1 (forecast ingresos y demanda) | CDO |
| 2026-09-02 | Governance | Revisión semestral de políticas corporativas | CRO |
| 2026-10-01 | Estratégico | Lanzamiento de segunda ciudad operativa | COO + CMO |
| 2026-12-01 | Estratégico | Cierre anual — review de OKRs y planeación 2027 | CEO |
