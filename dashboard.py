"""
╔══════════════════════════════════════════════════════════════════════╗
║          DASHBOARD EJECUTIVO FANERO  ·  Streamlit + Plotly          ║
║  Pestañas: MAYORISTAS | TPF | CONGRESO                              ║
║                                                                      ║
║  DEPLOY RÁPIDO:                                                      ║
║    1. pip install streamlit plotly pandas numpy                      ║
║    2. streamlit run dashboard.py                                     ║
║                                                                      ║
║  STREAMLIT CLOUD (link compartible):                                 ║
║    1. Sube este archivo + requirements.txt a un repo de GitHub       ║
║    2. Ve a https://share.streamlit.io → New app → selecciona repo   ║
║    3. Main file: dashboard.py → Deploy → ¡listo! Comparte el link   ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# ══════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Dashboard Ejecutivo | Fanero",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════
# PALETA CORPORATIVA
# ══════════════════════════════════════════════════════
C_PRIMARY   = "#1B3A6B"   # Azul marino oscuro
C_SECONDARY = "#2D6BB4"   # Azul medio
C_ACCENT    = "#C0392B"   # Rojo alerta
C_SUCCESS   = "#1A7A42"   # Verde cumplimiento
C_WARNING   = "#B7950B"   # Amarillo precaución
C_NEUTRAL   = "#5D6D7E"   # Gris neutro
C_LIGHT     = "#D5E8F4"   # Azul claro (cuota)
C_BG        = "#F2F5F9"   # Fondo página
C_CARD      = "#FFFFFF"   # Fondo tarjeta

# ══════════════════════════════════════════════════════
# ESTILOS CSS GLOBALES
# ══════════════════════════════════════════════════════
st.markdown(f"""
<style>
/* ── Base ─────────────────────────────────────────── */
.stApp {{ background-color: {C_BG}; }}
[data-testid="stToolbar"] {{ display: none; }}
#MainMenu, footer {{ visibility: hidden; }}
.stDeployButton {{ display: none !important; }}
div[data-testid="stSidebarContent"] {{ display: none; }}

/* ── Header ───────────────────────────────────────── */
.exec-header {{
  background: linear-gradient(135deg, {C_PRIMARY} 0%, {C_SECONDARY} 100%);
  padding: 1.1rem 2rem;
  border-radius: 12px;
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 14px rgba(27,58,107,0.22);
}}
.exec-header h1 {{
  color: #fff;
  font-size: 1.55rem;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.3px;
}}
.exec-header p {{
  color: rgba(255,255,255,0.75);
  font-size: 0.82rem;
  margin: 0.15rem 0 0;
}}
.exec-badge {{
  background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 6px;
  padding: 0.35rem 0.9rem;
  color: #fff;
  font-size: 0.78rem;
  font-weight: 600;
  white-space: nowrap;
}}

/* ── KPI Cards ────────────────────────────────────── */
.kpi-card {{
  background: {C_CARD};
  border-radius: 10px;
  padding: 1.1rem 1.3rem 0.9rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  border-left: 4px solid {C_SECONDARY};
  height: 100%;
  transition: box-shadow .2s;
}}
.kpi-card:hover {{ box-shadow: 0 4px 14px rgba(0,0,0,0.12); }}
.kpi-label {{
  font-size: 0.7rem;
  font-weight: 700;
  color: {C_NEUTRAL};
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin-bottom: 0.25rem;
}}
.kpi-value {{
  font-size: 1.85rem;
  font-weight: 700;
  color: {C_PRIMARY};
  line-height: 1.1;
}}
.kpi-delta {{
  font-size: 0.78rem;
  margin-top: 0.3rem;
  font-weight: 600;
}}
.kpi-delta.up   {{ color: {C_SUCCESS}; }}
.kpi-delta.dn   {{ color: {C_ACCENT};  }}
.kpi-delta.neu  {{ color: {C_NEUTRAL}; }}

/* ── Section titles ───────────────────────────────── */
.sec-title {{
  font-size: 0.95rem;
  font-weight: 700;
  color: {C_PRIMARY};
  border-bottom: 2px solid {C_SECONDARY};
  padding-bottom: 0.28rem;
  margin: 1.2rem 0 0.75rem;
  letter-spacing: -0.2px;
}}

/* ── Filter bar ───────────────────────────────────── */
.filter-bar {{
  background: {C_CARD};
  border-radius: 10px;
  padding: 0.85rem 1.2rem;
  box-shadow: 0 1px 5px rgba(0,0,0,0.06);
  margin-bottom: 1rem;
}}

/* ── Tabs ─────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{
  gap: 6px;
  background: {C_CARD};
  border-radius: 10px;
  padding: 5px 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.07);
  margin-bottom: 0.9rem;
}}
.stTabs [data-baseweb="tab"] {{
  height: 42px;
  border-radius: 7px;
  font-weight: 600;
  font-size: 0.88rem;
  color: {C_NEUTRAL};
  background: transparent;
  border: none !important;
  padding: 0 1.2rem;
}}
.stTabs [aria-selected="true"] {{
  background: {C_PRIMARY} !important;
  color: #fff !important;
  box-shadow: 0 2px 6px rgba(27,58,107,0.25);
}}

/* ── Congress placeholder ─────────────────────────── */
.congress-wrap {{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 52vh;
  text-align: center;
}}
.congress-wrap .icon {{ font-size: 4.5rem; margin-bottom: 1rem; }}
.congress-wrap h2 {{
  color: {C_PRIMARY};
  font-size: 1.9rem;
  font-weight: 700;
  margin-bottom: 0.4rem;
}}
.congress-wrap p {{ color: {C_NEUTRAL}; font-size: 1rem; line-height: 1.6; }}

/* ── Dataframe ─────────────────────────────────────── */
[data-testid="stDataFrame"] {{ border-radius: 8px; overflow: hidden; }}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# CONSTANTES
# ══════════════════════════════════════════════════════
DEPARTMENTS = [
    "Amazonas", "Cajamarca", "Huancavelica", "Huánuco",
    "Junín", "Loreto", "Pasco", "San Martín", "Ucayali",
]
PRODUCTS_M = ["Prepago", "Porta Prepago", "Postpago", "OSS"]

CLUSTERS: dict[str, list[str]] = {
    "IQUITOS": [
        "TOTTUS_PU_LAMARINA", "TPF IQUITOS", "TPF MAP IQUITOS",
    ],
    "PUCALLPA": [
        "PLAZAVEAORIENTE_PUCALLPA", "TPF PUCALLPA",
    ],
    "HUANUCO & TINGO MARÍA": [
        "IS_RPHUANUCO", "PLAZAVEAORIENTE_HUANUCO", "TPF-TC TINGOMARIA",
    ],
    "OPEN PLAZA PUCALLPA & UCAPORTILLO": [
        "IS_OPPUCALLPA", "TOTTUS_PUCALLPA", "TPF-TC UCAPORTILLO",
    ],
    "OPEN PLAZA HUANUCO": [
        "TPF HUANUCO",
    ],
}
PRODUCTS_T = [
    "SS", "LLAA", "C PORTA SS", "EQUIPOS TOTAL", "RENO SS",
    "VR + PORTA OPP", "PREPAGO", "ACCE", "SEGUROS", "MISS IN",
]


# ══════════════════════════════════════════════════════
# GENERACIÓN DE DATOS SIMULADOS
# ══════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def generate_mayoristas() -> pd.DataFrame:
    np.random.seed(42)
    months = pd.date_range("2023-01-01", "2026-06-01", freq="MS")

    base: dict[str, float] = {
        "Amazonas": 190_000, "Cajamarca": 430_000, "Huancavelica": 98_000,
        "Huánuco": 315_000, "Junín": 590_000, "Loreto": 660_000,
        "Pasco": 135_000, "San Martín": 285_000, "Ucayali": 380_000,
    }
    pmix: dict[str, float] = {
        "Prepago": 0.44, "Porta Prepago": 0.26, "Postpago": 0.20, "OSS": 0.10,
    }
    records = []
    for m in months:
        elapsed = (m.year - 2023) * 12 + m.month - 1
        trend    = 1 + 0.005 * elapsed
        seasonal = 1 + 0.09 * np.sin(2 * np.pi * m.month / 12)
        for dept in DEPARTMENTS:
            for prod, mix in pmix.items():
                noise  = np.random.normal(1.0, 0.055)
                ventas = base[dept] * mix * trend * seasonal * noise
                cuota  = ventas * np.random.uniform(0.91, 1.19)
                records.append({
                    "Fecha": m, "Mes": m.strftime("%b %Y"), "Año": m.year,
                    "Departamento": dept, "Producto": prod,
                    "Ventas": max(round(ventas), 0),
                    "Cuota":  max(round(cuota),  0),
                })

    df = pd.DataFrame(records)
    df["Cumplimiento"] = (df["Ventas"] / df["Cuota"] * 100).round(1)

    # Fanero = consolidado total
    fan = (
        df.groupby(["Fecha", "Mes", "Año", "Producto"], as_index=False)
          .agg(Ventas=("Ventas", "sum"), Cuota=("Cuota", "sum"))
    )
    fan["Departamento"] = "Fanero"
    fan["Cumplimiento"] = (fan["Ventas"] / fan["Cuota"] * 100).round(1)
    return pd.concat([df, fan], ignore_index=True)


@st.cache_data(show_spinner=False)
def generate_tpf() -> pd.DataFrame:
    np.random.seed(7)
    months = pd.date_range("2023-01-01", "2026-06-01", freq="MS")

    base_cl: dict[str, float] = {
        "IQUITOS": 460_000,
        "PUCALLPA": 390_000,
        "HUANUCO & TINGO MARÍA": 295_000,
        "OPEN PLAZA PUCALLPA & UCAPORTILLO": 330_000,
        "OPEN PLAZA HUANUCO": 185_000,
    }
    pmix_t: dict[str, float] = {
        "SS": 0.22, "LLAA": 0.15, "C PORTA SS": 0.12, "EQUIPOS TOTAL": 0.10,
        "RENO SS": 0.09, "VR + PORTA OPP": 0.08, "PREPAGO": 0.07,
        "ACCE": 0.07, "SEGUROS": 0.05, "MISS IN": 0.05,
    }
    records = []
    for m in months:
        elapsed  = (m.year - 2023) * 12 + m.month - 1
        trend    = 1 + 0.004 * elapsed
        seasonal = 1 + 0.07 * np.sin(2 * np.pi * m.month / 12)
        for cluster, subs in CLUSTERS.items():
            n = len(subs)
            for sub in subs:
                sub_ratio = np.random.uniform(0.28, 0.58)
                base_sub  = (base_cl[cluster] / n) * sub_ratio * 2
                for prod, mix in pmix_t.items():
                    noise  = np.random.normal(1.0, 0.08)
                    ventas = max(base_sub * mix * trend * seasonal * noise, 0)
                    cuota  = ventas * np.random.uniform(0.87, 1.23)
                    records.append({
                        "Fecha": m, "Mes": m.strftime("%b %Y"), "Año": m.year,
                        "Cluster": cluster, "Subcluster": sub, "Producto": prod,
                        "Ventas": round(ventas), "Cuota": round(max(cuota, 0)),
                    })

    df = pd.DataFrame(records)
    df["Cumplimiento"] = (df["Ventas"] / df["Cuota"] * 100).round(1)
    return df


df_may = generate_mayoristas()
df_tpf = generate_tpf()


# ══════════════════════════════════════════════════════
# UTILIDADES
# ══════════════════════════════════════════════════════
def fmt(v: float) -> str:
    """Formatea números como moneda abreviada."""
    if v >= 1_000_000:
        return f"S/ {v/1_000_000:.2f}M"
    if v >= 1_000:
        return f"S/ {v/1_000:.1f}K"
    return f"S/ {v:,.0f}"


def kpi(label: str, value: str, delta: float | None = None,
        dlabel: str = "", color: str = C_SECONDARY) -> str:
    """Genera HTML de una tarjeta KPI."""
    d_html = ""
    if delta is not None:
        cls  = "up" if delta >= 0 else "dn"
        icon = "▲" if delta >= 0 else "▼"
        d_html = f'<div class="kpi-delta {cls}">{icon} {abs(delta):.1f}% {dlabel}</div>'
    return (
        f'<div class="kpi-card" style="border-left-color:{color}">'
        f'  <div class="kpi-label">{label}</div>'
        f'  <div class="kpi-value">{value}</div>'
        f'  {d_html}'
        f'</div>'
    )


def compliance_color(pct: float) -> str:
    if pct >= 100:  return C_SUCCESS
    if pct >= 85:   return C_WARNING
    return C_ACCENT


BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, Segoe UI, Arial", size=12, color="#2C3E50"),
    margin=dict(l=45, r=20, t=40, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font_size=11),
    hoverlabel=dict(bgcolor="white", font_size=12, bordercolor="#ddd"),
)


# ══════════════════════════════════════════════════════
# HEADER GLOBAL
# ══════════════════════════════════════════════════════
now_str = datetime.now().strftime("%d %b %Y · %H:%M")
st.markdown(f"""
<div class="exec-header">
  <div>
    <h1>📊 Dashboard Ejecutivo &nbsp;·&nbsp; Fanero</h1>
    <p>Análisis de desempeño comercial &nbsp;|&nbsp; Datos actualizados al {now_str}</p>
  </div>
  <div class="exec-badge">⚡ Vista Gerencial</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["🏬  MAYORISTAS", "🏪  TPF", "🏛️  CONGRESO"])


# ─────────────────────────────────────────────────────
# TAB 1 · MAYORISTAS
# ─────────────────────────────────────────────────────
with tab1:

    # ── Filtros ────────────────────────────────────────
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.8, 2.2, 2, 2])

    all_years = sorted(df_may["Año"].unique())
    sel_years = c1.multiselect("Año", all_years, default=all_years, key="m_yr")

    months_available = sorted(
        df_may[df_may["Año"].isin(sel_years)]["Mes"].unique(),
        key=lambda x: pd.to_datetime(x, format="%b %Y"),
    )
    default_months = months_available[-6:] if len(months_available) > 6 else months_available
    sel_months = c2.multiselect("Mes", months_available, default=default_months, key="m_mo")

    dept_opts = ["Fanero"] + DEPARTMENTS
    sel_dept = c3.selectbox("Departamento", dept_opts, index=0, key="m_dep")

    sel_prod = c4.multiselect("Producto", PRODUCTS_M, default=PRODUCTS_M, key="m_pr")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Filtrado ───────────────────────────────────────
    df_f = df_may[
        df_may["Año"].isin(sel_years) &
        df_may["Mes"].isin(sel_months) &
        (df_may["Departamento"] == sel_dept) &
        df_may["Producto"].isin(sel_prod)
    ].copy()

    if df_f.empty:
        st.warning("⚠️ Sin datos para la selección actual.")
        st.stop()

    # ── KPIs ───────────────────────────────────────────
    total_v = df_f["Ventas"].sum()
    total_c = df_f["Cuota"].sum()
    cumpl   = total_v / total_c * 100 if total_c else 0
    brecha  = total_c - total_v

    # Período anterior (misma cantidad de meses)
    n_sel = len(sel_months)
    prev_idx  = max(0, months_available.index(sel_months[0]) - n_sel) if sel_months else 0
    prev_mos  = months_available[prev_idx: prev_idx + n_sel]
    prev_v = df_may[
        df_may["Mes"].isin(prev_mos) &
        (df_may["Departamento"] == sel_dept) &
        df_may["Producto"].isin(sel_prod)
    ]["Ventas"].sum()
    delta_v = (total_v - prev_v) / prev_v * 100 if prev_v else 0

    st.markdown('<div class="sec-title">📌 Indicadores Clave del Período</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi("Ventas Totales",   fmt(total_v), delta_v, "vs período ant."), unsafe_allow_html=True)
    k2.markdown(kpi("Cuota Total",      fmt(total_c)), unsafe_allow_html=True)
    k3.markdown(kpi("% Cumplimiento",   f"{cumpl:.1f}%", color=compliance_color(cumpl)), unsafe_allow_html=True)
    k4.markdown(kpi("Brecha vs Cuota",  fmt(abs(brecha)),
                    color=C_ACCENT if brecha > 0 else C_SUCCESS), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tendencia mensual ──────────────────────────────
    st.markdown('<div class="sec-title">📈 Tendencia Mensual · Ventas vs Cuota</div>', unsafe_allow_html=True)

    trend = (
        df_f.groupby("Fecha")
            .agg(Ventas=("Ventas", "sum"), Cuota=("Cuota", "sum"))
            .reset_index()
            .sort_values("Fecha")
    )
    trend["Cumplimiento"] = trend["Ventas"] / trend["Cuota"] * 100

    fig_tr = make_subplots(specs=[[{"secondary_y": True}]])
    fig_tr.add_trace(go.Bar(
        x=trend["Fecha"], y=trend["Cuota"],
        name="Cuota", marker_color=C_LIGHT, opacity=0.85,
    ), secondary_y=False)
    fig_tr.add_trace(go.Bar(
        x=trend["Fecha"], y=trend["Ventas"],
        name="Ventas", marker_color=C_PRIMARY, opacity=0.92,
    ), secondary_y=False)
    fig_tr.add_trace(go.Scatter(
        x=trend["Fecha"], y=trend["Cumplimiento"],
        name="% Cumplimiento", mode="lines+markers",
        line=dict(color=C_ACCENT, width=2.5),
        marker=dict(size=6, color=C_ACCENT),
    ), secondary_y=True)
    fig_tr.add_hline(y=100, line_dash="dot", line_color=C_SUCCESS,
                     secondary_y=True,
                     annotation_text=" Meta 100%",
                     annotation_position="top right",
                     annotation_font_color=C_SUCCESS)
    fig_tr.update_layout(**BASE_LAYOUT, height=360, barmode="overlay")
    fig_tr.update_yaxes(title_text="Monto (S/)",         secondary_y=False, tickformat=",.0f", gridcolor="#E8EDF2")
    fig_tr.update_yaxes(title_text="Cumplimiento (%)",   secondary_y=True,  showgrid=False)
    st.plotly_chart(fig_tr, use_container_width=True)

    # ── Departamentos + Mix ────────────────────────────
    ca, cb = st.columns([3, 2])

    with ca:
        st.markdown('<div class="sec-title">🗺️ Desempeño por Departamento</div>', unsafe_allow_html=True)
        dept_agg = (
            df_may[
                df_may["Mes"].isin(sel_months) &
                df_may["Producto"].isin(sel_prod) &
                (df_may["Departamento"] != "Fanero")
            ]
            .groupby("Departamento")
            .agg(Ventas=("Ventas", "sum"), Cuota=("Cuota", "sum"))
            .reset_index()
        )
        dept_agg["Cumplimiento"] = dept_agg["Ventas"] / dept_agg["Cuota"] * 100
        dept_agg = dept_agg.sort_values("Cumplimiento", ascending=True)
        bar_colors = dept_agg["Cumplimiento"].apply(compliance_color).tolist()

        fig_dep = go.Figure()
        fig_dep.add_trace(go.Bar(
            y=dept_agg["Departamento"], x=dept_agg["Cuota"],
            name="Cuota", orientation="h", marker_color=C_LIGHT,
        ))
        fig_dep.add_trace(go.Bar(
            y=dept_agg["Departamento"], x=dept_agg["Ventas"],
            name="Ventas", orientation="h", marker_color=bar_colors,
            text=[f"{c:.0f}%" for c in dept_agg["Cumplimiento"]],
            textposition="inside", textfont=dict(color="white", size=11, family="Inter"),
        ))
        fig_dep.update_layout(**BASE_LAYOUT, height=330, barmode="overlay",
                              xaxis=dict(tickformat=",.0f", gridcolor="#E8EDF2"))
        st.plotly_chart(fig_dep, use_container_width=True)

    with cb:
        st.markdown('<div class="sec-title">🛒 Mix de Productos</div>', unsafe_allow_html=True)
        prod_agg = df_f.groupby("Producto").agg(Ventas=("Ventas", "sum")).reset_index()
        fig_pie = px.pie(
            prod_agg, names="Producto", values="Ventas",
            color_discrete_sequence=[C_PRIMARY, C_SECONDARY, "#4A90D9", "#7EB3E2"],
            hole=0.48,
        )
        fig_pie.update_traces(
            textposition="inside",
            textinfo="percent+label",
            textfont_size=11,
            marker=dict(line=dict(color="white", width=2)),
        )
        fig_pie.update_layout(
            **BASE_LAYOUT, height=330, showlegend=False,
            annotations=[dict(text="<b>Ventas</b>", x=0.5, y=0.5,
                              font_size=13, showarrow=False, font_color=C_PRIMARY)],
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Heatmap cumplimiento ───────────────────────────
    st.markdown('<div class="sec-title">🔥 Mapa de Cumplimiento · Departamento × Mes</div>', unsafe_allow_html=True)

    heat_raw = (
        df_may[
            df_may["Mes"].isin(sel_months) &
            df_may["Producto"].isin(sel_prod) &
            (df_may["Departamento"] != "Fanero")
        ]
        .groupby(["Departamento", "Fecha"])
        .agg(Ventas=("Ventas", "sum"), Cuota=("Cuota", "sum"))
        .reset_index()
    )
    heat_raw["Cumplimiento"] = heat_raw["Ventas"] / heat_raw["Cuota"] * 100
    heat_piv = heat_raw.pivot(index="Departamento", columns="Fecha", values="Cumplimiento")
    heat_piv.columns = [c.strftime("%b %y") for c in heat_piv.columns]

    fig_heat = px.imshow(
        heat_piv, text_auto=".0f",
        color_continuous_scale=[
            [0.00, C_ACCENT],
            [0.85, "#F4D03F"],
            [1.00, C_SUCCESS],
        ],
        zmin=70, zmax=115, aspect="auto",
    )
    fig_heat.update_layout(**BASE_LAYOUT, height=310,
                           coloraxis_colorbar=dict(title="Cumpl. %", ticksuffix="%"))
    st.plotly_chart(fig_heat, use_container_width=True)

    # ── Tabla detalle ──────────────────────────────────
    st.markdown('<div class="sec-title">📋 Resumen por Producto</div>', unsafe_allow_html=True)
    tbl = (
        df_f.groupby("Producto")
            .agg(Ventas=("Ventas", "sum"), Cuota=("Cuota", "sum"))
            .reset_index()
    )
    tbl["% Cumplimiento"] = (tbl["Ventas"] / tbl["Cuota"] * 100).round(1)
    tbl["Ventas"] = tbl["Ventas"].apply(fmt)
    tbl["Cuota"]  = tbl["Cuota"].apply(fmt)
    st.dataframe(tbl, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────
# TAB 2 · TPF
# ─────────────────────────────────────────────────────
with tab2:

    # ── Filtros ────────────────────────────────────────
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    t1, t2, t3, t4 = st.columns([1.8, 2.2, 2, 2])

    t_years = sorted(df_tpf["Año"].unique())
    sel_ty  = t1.multiselect("Año", t_years, default=t_years, key="t_yr")

    t_mos_avail = sorted(
        df_tpf[df_tpf["Año"].isin(sel_ty)]["Mes"].unique(),
        key=lambda x: pd.to_datetime(x, format="%b %Y"),
    )
    default_tm = t_mos_avail[-6:] if len(t_mos_avail) > 6 else t_mos_avail
    sel_tm = t2.multiselect("Mes", t_mos_avail, default=default_tm, key="t_mo")

    clust_opts = ["Todos"] + list(CLUSTERS.keys())
    sel_cl = t3.selectbox("Cluster", clust_opts, key="t_cl")

    sub_pool = (
        [s for subs in CLUSTERS.values() for s in subs]
        if sel_cl == "Todos"
        else CLUSTERS[sel_cl]
    )
    sel_sub = t4.multiselect("Subcluster", sub_pool, default=sub_pool, key="t_sub")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Filtrado ───────────────────────────────────────
    tmask = (
        df_tpf["Año"].isin(sel_ty) &
        df_tpf["Mes"].isin(sel_tm) &
        df_tpf["Subcluster"].isin(sel_sub)
    )
    if sel_cl != "Todos":
        tmask = tmask & (df_tpf["Cluster"] == sel_cl)
    df_tf = df_tpf[tmask].copy()

    if df_tf.empty:
        st.warning("⚠️ Sin datos para la selección actual.")
        st.stop()

    # ── KPIs ───────────────────────────────────────────
    tv = df_tf["Ventas"].sum()
    tc = df_tf["Cuota"].sum()
    tp = tv / tc * 100 if tc else 0

    st.markdown('<div class="sec-title">📌 Indicadores Clave del Período</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi("Ventas Totales",    fmt(tv)), unsafe_allow_html=True)
    k2.markdown(kpi("Cuota Total",       fmt(tc)), unsafe_allow_html=True)
    k3.markdown(kpi("% Cumplimiento",    f"{tp:.1f}%", color=compliance_color(tp)), unsafe_allow_html=True)
    k4.markdown(kpi("Subclusters",       str(df_tf["Subcluster"].nunique()), color=C_NEUTRAL), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Comparativo por cluster ────────────────────────
    st.markdown('<div class="sec-title">📊 Comparativo por Cluster</div>', unsafe_allow_html=True)

    cl_agg = (
        df_tf.groupby("Cluster")
             .agg(Ventas=("Ventas", "sum"), Cuota=("Cuota", "sum"))
             .reset_index()
    )
    cl_agg["Cumplimiento"] = cl_agg["Ventas"] / cl_agg["Cuota"] * 100
    cl_agg = cl_agg.sort_values("Ventas", ascending=False)

    fig_cl = make_subplots(specs=[[{"secondary_y": True}]])
    fig_cl.add_trace(go.Bar(
        x=cl_agg["Cluster"], y=cl_agg["Cuota"],
        name="Cuota", marker_color=C_LIGHT,
    ), secondary_y=False)
    fig_cl.add_trace(go.Bar(
        x=cl_agg["Cluster"], y=cl_agg["Ventas"],
        name="Ventas", marker_color=C_PRIMARY, opacity=0.92,
    ), secondary_y=False)
    fig_cl.add_trace(go.Scatter(
        x=cl_agg["Cluster"], y=cl_agg["Cumplimiento"],
        name="% Cumplimiento", mode="lines+markers",
        line=dict(color=C_ACCENT, width=2.5),
        marker=dict(size=8, color=C_ACCENT),
    ), secondary_y=True)
    fig_cl.add_hline(y=100, line_dash="dot", line_color=C_SUCCESS,
                     secondary_y=True,
                     annotation_text=" Meta 100%",
                     annotation_position="top right",
                     annotation_font_color=C_SUCCESS)
    fig_cl.update_layout(**BASE_LAYOUT, height=360, barmode="overlay")
    fig_cl.update_yaxes(title_text="Monto (S/)",       secondary_y=False, tickformat=",.0f", gridcolor="#E8EDF2")
    fig_cl.update_yaxes(title_text="Cumplimiento (%)", secondary_y=True,  showgrid=False)
    st.plotly_chart(fig_cl, use_container_width=True)

    # ── Subcluster + Producto ──────────────────────────
    cc, cd = st.columns([3, 2])

    with cc:
        st.markdown('<div class="sec-title">🏪 Desempeño por Subcluster</div>', unsafe_allow_html=True)
        sub_agg = (
            df_tf.groupby(["Cluster", "Subcluster"])
                 .agg(Ventas=("Ventas", "sum"), Cuota=("Cuota", "sum"))
                 .reset_index()
        )
        sub_agg["Cumplimiento"] = sub_agg["Ventas"] / sub_agg["Cuota"] * 100
        sub_agg = sub_agg.sort_values("Cumplimiento", ascending=True)
        sub_colors = sub_agg["Cumplimiento"].apply(compliance_color).tolist()

        fig_sub = go.Figure(go.Bar(
            y=sub_agg["Subcluster"], x=sub_agg["Ventas"],
            orientation="h", marker_color=sub_colors,
            text=[f"{c:.0f}%" for c in sub_agg["Cumplimiento"]],
            textposition="inside",
            textfont=dict(color="white", size=10, family="Inter"),
        ))
        fig_sub.update_layout(**BASE_LAYOUT, height=340, showlegend=False,
                              xaxis=dict(tickformat=",.0f", gridcolor="#E8EDF2"))
        st.plotly_chart(fig_sub, use_container_width=True)

    with cd:
        st.markdown('<div class="sec-title">🛒 Ventas por Producto</div>', unsafe_allow_html=True)
        prod_t = (
            df_tf.groupby("Producto")
                 .agg(Ventas=("Ventas", "sum"))
                 .reset_index()
                 .sort_values("Ventas", ascending=True)
        )
        fig_prt = go.Figure(go.Bar(
            x=prod_t["Ventas"], y=prod_t["Producto"],
            orientation="h", marker_color=C_SECONDARY,
            text=[fmt(v) for v in prod_t["Ventas"]],
            textposition="outside",
            textfont=dict(size=9, family="Inter"),
        ))
        fig_prt.update_layout(**BASE_LAYOUT, height=340, showlegend=False,
                              xaxis=dict(tickformat=",.0f", title="Ventas (S/)",
                                         gridcolor="#E8EDF2"))
        st.plotly_chart(fig_prt, use_container_width=True)

    # ── Tendencia mensual TPF ──────────────────────────
    st.markdown('<div class="sec-title">📈 Tendencia Mensual TPF</div>', unsafe_allow_html=True)

    tr_t = (
        df_tf.groupby("Fecha")
             .agg(Ventas=("Ventas", "sum"), Cuota=("Cuota", "sum"))
             .reset_index()
             .sort_values("Fecha")
    )
    tr_t["Cumplimiento"] = tr_t["Ventas"] / tr_t["Cuota"] * 100

    fig_trt = make_subplots(specs=[[{"secondary_y": True}]])
    fig_trt.add_trace(go.Bar(x=tr_t["Fecha"], y=tr_t["Cuota"],
                              name="Cuota", marker_color=C_LIGHT), secondary_y=False)
    fig_trt.add_trace(go.Bar(x=tr_t["Fecha"], y=tr_t["Ventas"],
                              name="Ventas", marker_color=C_PRIMARY, opacity=0.92), secondary_y=False)
    fig_trt.add_trace(go.Scatter(
        x=tr_t["Fecha"], y=tr_t["Cumplimiento"],
        name="% Cumplimiento", mode="lines+markers",
        line=dict(color=C_ACCENT, width=2.5),
        marker=dict(size=6, color=C_ACCENT),
    ), secondary_y=True)
    fig_trt.add_hline(y=100, line_dash="dot", line_color=C_SUCCESS, secondary_y=True)
    fig_trt.update_layout(**BASE_LAYOUT, height=320, barmode="overlay")
    fig_trt.update_yaxes(title_text="Monto (S/)",       secondary_y=False, tickformat=",.0f", gridcolor="#E8EDF2")
    fig_trt.update_yaxes(title_text="Cumplimiento (%)", secondary_y=True,  showgrid=False)
    st.plotly_chart(fig_trt, use_container_width=True)

    # ── Heatmap producto × cluster ─────────────────────
    st.markdown('<div class="sec-title">🔥 Mapa de Cumplimiento · Producto × Cluster</div>', unsafe_allow_html=True)

    ht2 = (
        df_tf.groupby(["Cluster", "Producto"])
             .agg(Ventas=("Ventas", "sum"), Cuota=("Cuota", "sum"))
             .reset_index()
    )
    ht2["Cumplimiento"] = ht2["Ventas"] / ht2["Cuota"] * 100
    ht2_piv = ht2.pivot(index="Cluster", columns="Producto", values="Cumplimiento")

    fig_ht2 = px.imshow(
        ht2_piv, text_auto=".0f",
        color_continuous_scale=[
            [0.00, C_ACCENT],
            [0.85, "#F4D03F"],
            [1.00, C_SUCCESS],
        ],
        zmin=70, zmax=115, aspect="auto",
    )
    fig_ht2.update_layout(**BASE_LAYOUT, height=260,
                           coloraxis_colorbar=dict(title="Cumpl. %", ticksuffix="%"))
    st.plotly_chart(fig_ht2, use_container_width=True)

    # ── Tabla resumen ──────────────────────────────────
    st.markdown('<div class="sec-title">📋 Resumen por Subcluster</div>', unsafe_allow_html=True)
    tbl_t = (
        df_tf.groupby(["Cluster", "Subcluster"])
             .agg(Ventas=("Ventas", "sum"), Cuota=("Cuota", "sum"))
             .reset_index()
    )
    tbl_t["% Cumplimiento"] = (tbl_t["Ventas"] / tbl_t["Cuota"] * 100).round(1)
    tbl_t["Ventas"] = tbl_t["Ventas"].apply(fmt)
    tbl_t["Cuota"]  = tbl_t["Cuota"].apply(fmt)
    st.dataframe(tbl_t, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────
# TAB 3 · CONGRESO
# ─────────────────────────────────────────────────────
with tab3:
    st.markdown("""
    <div class="congress-wrap">
      <div class="icon">🏛️</div>
      <h2>Información en proceso de carga</h2>
      <p>Los datos del módulo Congreso estarán disponibles próximamente.<br>
         Por favor, vuelva a consultar en la próxima actualización.</p>
    </div>
    """, unsafe_allow_html=True)
