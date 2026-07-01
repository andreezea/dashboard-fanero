"""
╔══════════════════════════════════════════════════════════════════════╗
║        DASHBOARD EJECUTIVO FANERO  v2  ·  Streamlit + Plotly        ║
║  Pestañas: MAYORISTAS | TPF | CONGRESO                               ║
║                                                                      ║
║  DEPLOY LOCAL:                                                       ║
║    pip install -r requirements.txt                                   ║
║    streamlit run dashboard.py                                        ║
║                                                                      ║
║  STREAMLIT CLOUD (link compartible):                                 ║
║    1. Sube este archivo + requirements.txt a GitHub                  ║
║    2. share.streamlit.io → Create app → selecciona repo              ║
║    3. Main file: dashboard.py → Deploy                               ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import io
import streamlit as st
import pandas as pd
import numpy as np
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
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════
# PALETA CORPORATIVA
# ══════════════════════════════════════════════════════
C_PRIMARY   = "#1B3A6B"
C_SECONDARY = "#2D6BB4"
C_ACCENT    = "#C0392B"
C_SUCCESS   = "#1A7A42"
C_WARNING   = "#B7950B"
C_NEUTRAL   = "#5D6D7E"
C_LIGHT     = "#D5E8F4"
C_BG        = "#F2F5F9"
C_CARD      = "#FFFFFF"
C_YELLOW    = "#F4D03F"

# ══════════════════════════════════════════════════════
# ESTILOS CSS
# ══════════════════════════════════════════════════════
st.markdown(f"""
<style>
/* ── Base ─────────────────────────────────────────── */
.stApp {{ background-color:{C_BG}; }}
[data-testid="stToolbar"], footer, #MainMenu {{ visibility:hidden; }}
.stDeployButton {{ display:none !important; }}

/* ── Header ───────────────────────────────────────── */
.exec-header {{
  background: linear-gradient(135deg,{C_PRIMARY} 0%,{C_SECONDARY} 100%);
  padding:1.1rem 2rem; border-radius:12px; margin-bottom:1.2rem;
  display:flex; align-items:center; justify-content:space-between;
  box-shadow:0 4px 14px rgba(27,58,107,.22);
}}
.exec-header h1 {{ color:#fff; font-size:1.5rem; font-weight:700; margin:0; }}
.exec-header p  {{ color:rgba(255,255,255,.75); font-size:.82rem; margin:.1rem 0 0; }}
.exec-badge {{
  background:rgba(255,255,255,.15); border:1px solid rgba(255,255,255,.3);
  border-radius:6px; padding:.35rem .9rem; color:#fff;
  font-size:.78rem; font-weight:600; white-space:nowrap;
}}

/* ── KPI Cards ────────────────────────────────────── */
.kpi-card {{
  background:{C_CARD}; border-radius:10px; padding:1.1rem 1.3rem .9rem;
  box-shadow:0 2px 8px rgba(0,0,0,.07); border-left:4px solid {C_SECONDARY};
}}
.kpi-label  {{ font-size:.7rem; font-weight:700; color:{C_NEUTRAL}; text-transform:uppercase; letter-spacing:.6px; margin-bottom:.25rem; }}
.kpi-value  {{ font-size:1.85rem; font-weight:700; color:{C_PRIMARY}; line-height:1.1; }}
.kpi-delta  {{ font-size:.78rem; margin-top:.3rem; font-weight:600; }}
.kpi-delta.up {{ color:{C_SUCCESS}; }}
.kpi-delta.dn {{ color:{C_ACCENT};  }}
.kpi-delta.neu{{ color:{C_NEUTRAL}; }}

/* ── Section titles ───────────────────────────────── */
.sec-title {{
  font-size:.95rem; font-weight:700; color:{C_PRIMARY};
  border-bottom:2px solid {C_SECONDARY}; padding-bottom:.28rem;
  margin:1.2rem 0 .75rem;
}}

/* ── Filter bar ───────────────────────────────────── */
.filter-bar {{
  background:{C_CARD}; border-radius:10px; padding:.85rem 1.2rem;
  box-shadow:0 1px 5px rgba(0,0,0,.06); margin-bottom:1rem;
}}

/* ── Tabs ─────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{
  gap:6px; background:{C_CARD}; border-radius:10px;
  padding:5px 8px; box-shadow:0 1px 4px rgba(0,0,0,.07); margin-bottom:.9rem;
}}
.stTabs [data-baseweb="tab"] {{
  height:42px; border-radius:7px; font-weight:600; font-size:.88rem;
  color:{C_NEUTRAL}; background:transparent; border:none !important; padding:0 1.2rem;
}}
.stTabs [aria-selected="true"] {{
  background:{C_PRIMARY} !important; color:#fff !important;
  box-shadow:0 2px 6px rgba(27,58,107,.25);
}}

/* ══ PIVOT TABLE ══════════════════════════════════════ */
.pivot-wrap {{ overflow-x:auto; border-radius:9px; box-shadow:0 2px 10px rgba(0,0,0,.1); }}
.pivot-tbl  {{ border-collapse:collapse; width:100%; font-size:.8rem; font-family:Inter,Arial,sans-serif; white-space:nowrap; }}

/* Header rows */
.pivot-tbl .th-first {{
  background:{C_PRIMARY}; color:#fff; text-align:left;
  padding:.55rem .9rem; border:1px solid #2D5A9E;
  font-weight:700; font-size:.78rem; text-transform:uppercase;
  letter-spacing:.5px; min-width:190px; position:sticky; left:0; z-index:2;
}}
.pivot-tbl .th-prod {{
  background:{C_PRIMARY}; color:#fff; text-align:center;
  padding:.5rem .4rem; border:1px solid #2D5A9E;
  font-weight:700; font-size:.76rem; text-transform:uppercase;
  letter-spacing:.4px;
}}
.pivot-tbl .th-sub {{
  background:{C_SECONDARY}; color:#fff; text-align:center;
  padding:.35rem .3rem; border:1px solid #4A85C5;
  font-size:.72rem; font-weight:600;
}}
.pivot-tbl .th-first-sub {{
  background:{C_PRIMARY}; color:#fff; font-size:.72rem; font-weight:600;
  padding:.35rem .9rem; border:1px solid #2D5A9E;
  position:sticky; left:0; z-index:2;
}}

/* Cluster / Summary row */
.pivot-tbl .tr-cluster td {{
  background:{C_PRIMARY}; color:{C_YELLOW};
  font-weight:700; border:1px solid #2D5A9E;
}}
.pivot-tbl .tr-cluster .td-first {{
  background:{C_PRIMARY}; color:{C_YELLOW};
  text-align:left; padding:.45rem .9rem;
  font-weight:700; position:sticky; left:0; z-index:1;
}}
.pivot-tbl .tr-cluster .td-num {{
  text-align:center; padding:.4rem .35rem;
}}
.pivot-tbl .tr-cluster .td-cumpl {{
  text-align:center; padding:.4rem .35rem; font-weight:800; font-size:.82rem;
}}

/* Sub rows */
.pivot-tbl .tr-sub td {{ border:1px solid #E0E7EF; }}
.pivot-tbl .tr-sub:nth-child(even) td {{ background:#F7FAFC; }}
.pivot-tbl .tr-sub:hover td {{ background:#E8EDF5; }}
.pivot-tbl .tr-sub .td-first {{
  text-align:left; padding:.38rem .9rem .38rem 1.8rem;
  font-weight:500; color:{C_PRIMARY};
  background:inherit; position:sticky; left:0; z-index:1;
  border-right:2px solid #D0D9E8;
}}
.pivot-tbl .tr-sub .td-num   {{ text-align:center; padding:.35rem .3rem; color:#34495E; }}
.pivot-tbl .tr-sub .td-cumpl {{ text-align:center; padding:.35rem .3rem; font-weight:700; font-size:.82rem; }}

/* ── Congress ─────────────────────────────────────── */
.congress-wrap {{
  display:flex; flex-direction:column; align-items:center;
  justify-content:center; min-height:52vh; text-align:center;
}}
.congress-wrap h2 {{ color:{C_PRIMARY}; font-size:1.9rem; font-weight:700; margin-bottom:.4rem; }}
.congress-wrap p  {{ color:{C_NEUTRAL}; font-size:1rem; line-height:1.6; }}

/* ── Sidebar upload ───────────────────────────────── */
.upload-title {{ font-weight:700; font-size:.85rem; color:{C_PRIMARY}; }}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# CONSTANTES
# ══════════════════════════════════════════════════════
DEPARTMENTS = [
    "Amazonas","Cajamarca","Huancavelica","Huánuco",
    "Junín","Loreto","Pasco","San Martín","Ucayali",
]
PRODUCTS_M = ["Prepago","Porta Prepago","Postpago","OSS"]

CLUSTERS: dict[str, list[str]] = {
    "IQUITOS":                              ["TOTTUS_PU_LAMARINA","TPF IQUITOS","TPF MAP IQUITOS"],
    "PUCALLPA":                             ["PLAZAVEAORIENTE_PUCALLPA","TPF PUCALLPA"],
    "HUANUCO & TINGO MARÍA":               ["IS_RPHUANUCO","PLAZAVEAORIENTE_HUANUCO","TPF-TC TINGOMARIA"],
    "OPEN PLAZA PUCALLPA & UCAPORTILLO":   ["IS_OPPUCALLPA","TOTTUS_PUCALLPA","TPF-TC UCAPORTILLO"],
    "OPEN PLAZA HUANUCO":                  ["TPF HUANUCO"],
}
PRODUCTS_T = ["SS","LLAA","C PORTA SS","EQUIPOS TOTAL","RENO SS",
               "VR + PORTA OPP","PREPAGO","ACCE","SEGUROS","MISS IN"]

COLS_MAY = ["Fecha","Departamento","Producto","Ventas","Cuota"]
COLS_TPF = ["Fecha","Cluster","Subcluster","Producto","Ventas","Cuota"]

# ══════════════════════════════════════════════════════
# GENERACIÓN DE DATOS SIMULADOS
# ══════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def generate_mayoristas() -> pd.DataFrame:
    """Genera datos en UNIDADES (activaciones/conexiones), no monetarios."""
    np.random.seed(42)
    months = pd.date_range("2023-01-01","2026-06-01",freq="MS")
    # Unidades base por departamento y mes (rango realista: 40-200 u/producto)
    base   = {"Amazonas":120,"Cajamarca":115,"Huancavelica":48,
               "Huánuco":98,"Junín":170,"Loreto":185,
               "Pasco":55,"San Martín":88,"Ucayali":118}
    pmix   = {"Prepago":.44,"Porta Prepago":.26,"Postpago":.20,"OSS":.10}
    rows   = []
    for m in months:
        elapsed  = (m.year-2023)*12 + m.month-1
        trend    = 1 + .004*elapsed
        seasonal = 1 + .08*np.sin(2*np.pi*m.month/12)
        for dept in DEPARTMENTS:
            for prod,mix in pmix.items():
                v = max(base[dept]*mix*trend*seasonal*np.random.normal(1,.07), 0)
                c = v*np.random.uniform(.91,1.20)
                rows.append({"Fecha":m,"Mes":m.strftime("%b %Y"),"Año":m.year,
                              "Departamento":dept,"Producto":prod,
                              "Ventas":round(v),"Cuota":round(c)})
    df = pd.DataFrame(rows)
    df["Cumplimiento"] = (df["Ventas"]/df["Cuota"]*100).round(1)
    # Fanero = total consolidado
    fan = (df.groupby(["Fecha","Mes","Año","Producto"],as_index=False)
             .agg(Ventas=("Ventas","sum"),Cuota=("Cuota","sum")))
    fan["Departamento"] = "Fanero"
    fan["Cumplimiento"] = (fan["Ventas"]/fan["Cuota"]*100).round(1)
    return pd.concat([df,fan],ignore_index=True)


@st.cache_data(show_spinner=False)
def generate_tpf() -> pd.DataFrame:
    np.random.seed(7)
    months  = pd.date_range("2023-01-01","2026-06-01",freq="MS")
    base_cl = {"IQUITOS":460_000,"PUCALLPA":390_000,
                "HUANUCO & TINGO MARÍA":295_000,
                "OPEN PLAZA PUCALLPA & UCAPORTILLO":330_000,
                "OPEN PLAZA HUANUCO":185_000}
    pmix_t  = {"SS":.22,"LLAA":.15,"C PORTA SS":.12,"EQUIPOS TOTAL":.10,
                "RENO SS":.09,"VR + PORTA OPP":.08,"PREPAGO":.07,
                "ACCE":.07,"SEGUROS":.05,"MISS IN":.05}
    rows = []
    for m in months:
        elapsed  = (m.year-2023)*12 + m.month-1
        trend    = 1 + .004*elapsed
        seasonal = 1 + .07*np.sin(2*np.pi*m.month/12)
        for cluster,subs in CLUSTERS.items():
            n = len(subs)
            for sub in subs:
                ratio   = np.random.uniform(.28,.58)
                base_s  = (base_cl[cluster]/n)*ratio*2
                for prod,mix in pmix_t.items():
                    v = max(base_s*mix*trend*seasonal*np.random.normal(1,.08),0)
                    c = max(v*np.random.uniform(.87,1.23),0)
                    rows.append({"Fecha":m,"Mes":m.strftime("%b %Y"),"Año":m.year,
                                  "Cluster":cluster,"Subcluster":sub,"Producto":prod,
                                  "Ventas":round(v),"Cuota":round(c)})
    df = pd.DataFrame(rows)
    df["Cumplimiento"] = (df["Ventas"]/df["Cuota"]*100).round(1)
    return df


# ══════════════════════════════════════════════════════
# UTILIDADES
# ══════════════════════════════════════════════════════
def fmt(v: float) -> str:
    if v >= 1_000_000: return f"S/ {v/1_000_000:.2f}M"
    if v >= 1_000:     return f"S/ {v/1_000:.1f}K"
    return f"S/ {v:,.0f}"

def fmt_tbl(v, units:bool=False) -> str:
    """Formato para celdas de tabla. units=True → entero puro sin símbolo."""
    if v is None or (isinstance(v, float) and np.isnan(v)): return "–"
    if units: return f"{int(round(v)):,}"
    if v >= 1_000_000: return f"{v/1_000_000:.1f}M"
    if v >= 1_000:     return f"{v/1_000:.1f}K"
    return f"{v:,.0f}"

def kpi(label:str, value:str, delta:float|None=None,
        dlabel:str="", color:str=C_SECONDARY) -> str:
    d = ""
    if delta is not None:
        cls  = "up" if delta>=0 else "dn"
        icon = "▲" if delta>=0 else "▼"
        d = f'<div class="kpi-delta {cls}">{icon} {abs(delta):.1f}% {dlabel}</div>'
    return (f'<div class="kpi-card" style="border-left-color:{color}">'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div>{d}</div>')

def cc(pct:float) -> str:
    """Color de cumplimiento."""
    if pct>=100: return C_SUCCESS
    if pct>=85:  return C_WARNING
    return C_ACCENT

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter,Arial",size=12,color="#2C3E50"),
    margin=dict(l=45,r=20,t=40,b=40),
    legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,font_size=11),
    hoverlabel=dict(bgcolor="white",font_size=12,bordercolor="#ddd"),
)

# ── Pivot table builder ───────────────────────────────
def build_pivot_html(df_data:pd.DataFrame, products:list[str],
                     group_col:str, sub_col:str|None,
                     group_map:dict|None, units:bool=False) -> str:
    """
    Construye una tabla HTML estilizada tipo gerencial.
    group_col  : columna de agrupación principal (Cluster / Fanero)
    sub_col    : columna de detalle (Subcluster / Departamento)
    group_map  : dict grupo → [sub1, sub2, ...]  (para orden)
    units      : True → mostrar enteros puros (sin símbolo monetario)
    """
    # Agregados nivel grupo
    grp_agg = (
        df_data.groupby([group_col,"Producto"],as_index=False)
               .agg(Ventas=("Ventas","sum"),Cuota=("Cuota","sum"))
    )
    grp_agg["Cumpl"] = grp_agg["Ventas"]/grp_agg["Cuota"].replace(0,np.nan)*100

    # Agregados nivel subgrupo
    sub_agg = None
    if sub_col:
        sub_agg = (
            df_data.groupby([group_col,sub_col,"Producto"],as_index=False)
                   .agg(Ventas=("Ventas","sum"),Cuota=("Cuota","sum"))
        )
        sub_agg["Cumpl"] = sub_agg["Ventas"]/sub_agg["Cuota"].replace(0,np.nan)*100

    def row_vals(df, filters:dict, prod:str):
        mask = pd.Series([True]*len(df), index=df.index)
        for col,val in filters.items():
            mask &= df[col]==val
        r = df[mask & (df["Producto"]==prod)]
        if r.empty: return None,None,None
        return r["Cuota"].iat[0], r["Ventas"].iat[0], r["Cumpl"].iat[0]

    def _f(v): return fmt_tbl(v, units=units)

    # ── HTML ──────────────────────────────────────────
    H = ['<div class="pivot-wrap"><table class="pivot-tbl">']

    # Header row 1 — nombre de producto
    H.append('<thead><tr>')
    H.append('<th class="th-first" rowspan="2">CLUSTER / SUBCLUSTER</th>')
    for p in products:
        H.append(f'<th class="th-prod" colspan="3">{p}</th>')
    H.append('</tr><tr>')
    for _ in products:
        H.append('<th class="th-sub">Cuota</th>'
                 '<th class="th-sub">Ventas</th>'
                 '<th class="th-sub">Cumpl%</th>')
    H.append('</tr></thead><tbody>')

    groups = list(group_map.keys()) if group_map else grp_agg[group_col].unique()

    for grp in groups:
        # ── Fila resumen de grupo ─────────────────────
        H.append('<tr class="tr-cluster">')
        H.append(f'<td class="td-first">▼ 🔵 {grp}</td>')
        for p in products:
            c,v,pct = row_vals(grp_agg,{group_col:grp},p)
            H.append(f'<td class="td-num">{_f(c)}</td>'
                     f'<td class="td-num">{_f(v)}</td>')
            if pct is not None:
                H.append(f'<td class="td-cumpl" style="color:{cc(pct)}">{pct:.0f}%</td>')
            else:
                H.append('<td class="td-cumpl">–</td>')
        H.append('</tr>')

        # ── Filas de subgrupos ────────────────────────
        if sub_col and sub_agg is not None:
            subs = group_map[grp] if group_map else \
                   sub_agg[sub_agg[group_col]==grp][sub_col].unique()
            for sub in subs:
                H.append('<tr class="tr-sub">')
                H.append(f'<td class="td-first">{sub}</td>')
                for p in products:
                    c,v,pct = row_vals(sub_agg,{group_col:grp,sub_col:sub},p)
                    H.append(f'<td class="td-num">{_f(c)}</td>'
                             f'<td class="td-num">{_f(v)}</td>')
                    if pct is not None:
                        H.append(f'<td class="td-cumpl" style="color:{cc(pct)}">{pct:.0f}%</td>')
                    else:
                        H.append('<td class="td-cumpl">–</td>')
                H.append('</tr>')

    H.append('</tbody></table></div>')
    return "".join(H)


# ── Plantillas Excel ──────────────────────────────────
def make_template(cols:list[str], sample_rows:list[dict]) -> bytes:
    buf = io.BytesIO()
    pd.DataFrame(sample_rows, columns=cols).to_excel(buf, index=False, engine="openpyxl")
    return buf.getvalue()

TMPL_MAY = make_template(COLS_MAY, [
    {"Fecha":"2024-01-01","Departamento":"Amazonas","Producto":"Prepago",    "Ventas":15000,"Cuota":18000},
    {"Fecha":"2024-01-01","Departamento":"Cajamarca","Producto":"Postpago",  "Ventas":22000,"Cuota":20000},
    {"Fecha":"2024-02-01","Departamento":"Loreto",   "Producto":"OSS",       "Ventas":9000, "Cuota":10000},
])
TMPL_TPF = make_template(COLS_TPF, [
    {"Fecha":"2024-01-01","Cluster":"IQUITOS",   "Subcluster":"TPF IQUITOS",  "Producto":"SS",   "Ventas":5000,"Cuota":6000},
    {"Fecha":"2024-01-01","Cluster":"PUCALLPA",  "Subcluster":"TPF PUCALLPA", "Producto":"LLAA", "Ventas":8000,"Cuota":7500},
    {"Fecha":"2024-02-01","Cluster":"IQUITOS",   "Subcluster":"TPF IQUITOS",  "Producto":"SS",   "Ventas":5500,"Cuota":6000},
])

def load_uploaded(file, required_cols:list[str]) -> pd.DataFrame|None:
    try:
        df = pd.read_csv(file) if file.name.endswith(".csv") else \
             pd.read_excel(file, engine="openpyxl")
        df.columns = df.columns.str.strip()
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            st.sidebar.error(f"⚠️ Faltan columnas: {', '.join(missing)}")
            return None
        df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
        df.dropna(subset=["Fecha"], inplace=True)
        df["Mes"] = df["Fecha"].dt.strftime("%b %Y")
        df["Año"] = df["Fecha"].dt.year
        if "Cuota" not in df.columns:
            df["Cuota"] = df["Ventas"] * 1.10
        df["Cumplimiento"] = (df["Ventas"] / df["Cuota"] * 100).round(1)
        return df
    except Exception as e:
        st.sidebar.error(f"Error al leer archivo: {e}")
        return None


# ══════════════════════════════════════════════════════
# SIDEBAR — CARGA DE DATOS
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"## 📂 Cargar Datos Reales")
    st.caption("Sube tu Excel o CSV para reemplazar los datos de demo.")

    st.markdown("---")
    st.markdown("### 🏬 Mayoristas")
    may_file = st.file_uploader("Archivo Mayoristas (.xlsx / .csv)",
                                 type=["xlsx","csv"], key="up_may",
                                 help=f"Columnas requeridas: {', '.join(COLS_MAY)}")
    st.download_button("⬇️ Descargar plantilla Mayoristas", TMPL_MAY,
                        "plantilla_mayoristas.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="dl_may")

    st.markdown("---")
    st.markdown("### 🏪 TPF")
    tpf_file = st.file_uploader("Archivo TPF (.xlsx / .csv)",
                                  type=["xlsx","csv"], key="up_tpf",
                                  help=f"Columnas requeridas: {', '.join(COLS_TPF)}")
    st.download_button("⬇️ Descargar plantilla TPF", TMPL_TPF,
                        "plantilla_tpf.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="dl_tpf")

    st.markdown("---")
    st.caption("ℹ️ Los datos cargados se mantienen mientras la sesión esté activa.")

    # Indicador de estado
    may_status = "✅ Datos reales" if may_file else "🔵 Datos demo"
    tpf_status = "✅ Datos reales" if tpf_file else "🔵 Datos demo"
    st.markdown(f"**Mayoristas:** {may_status}  \n**TPF:** {tpf_status}")


# ══════════════════════════════════════════════════════
# CARGAR / GENERAR DATOS
# ══════════════════════════════════════════════════════
df_may_base = generate_mayoristas()
df_tpf_base = generate_tpf()

if may_file:
    _up = load_uploaded(may_file, COLS_MAY)
    if _up is not None:
        # Añadir fila Fanero
        fan = (_up.groupby(["Fecha","Mes","Año","Producto"],as_index=False)
                  .agg(Ventas=("Ventas","sum"),Cuota=("Cuota","sum")))
        fan["Departamento"] = "Fanero"
        fan["Cumplimiento"] = (fan["Ventas"]/fan["Cuota"]*100).round(1)
        df_may_base = pd.concat([_up, fan], ignore_index=True)
        st.sidebar.success("Mayoristas cargado correctamente ✓")

if tpf_file:
    _up = load_uploaded(tpf_file, COLS_TPF)
    if _up is not None:
        df_tpf_base = _up
        st.sidebar.success("TPF cargado correctamente ✓")


# ══════════════════════════════════════════════════════
# HEADER GLOBAL
# ══════════════════════════════════════════════════════
now_str = datetime.now().strftime("%d %b %Y · %H:%M")
st.markdown(f"""
<div class="exec-header">
  <div>
    <h1>📊 Dashboard Ejecutivo &nbsp;·&nbsp; Fanero</h1>
    <p>Análisis de desempeño comercial &nbsp;|&nbsp; Actualizado: {now_str}</p>
  </div>
  <div class="exec-badge">⚡ Vista Gerencial</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["🏬  MAYORISTAS","🏪  TPF","🏛️  CONGRESO"])


# ────────────────────────────────────────────────────
# TAB 1 · MAYORISTAS
# ────────────────────────────────────────────────────
with tab1:

    # ── FILTROS ────────────────────────────────────────
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    all_yr  = sorted(df_may_base["Año"].unique(), reverse=True)
    sel_yr  = c1.selectbox("📅 Año", all_yr, key="m_yr")

    all_mo_yr = ["Acumulado"] + sorted(
        df_may_base[df_may_base["Año"]==sel_yr]["Mes"].unique(),
        key=lambda x: pd.to_datetime(x, format="%b %Y"),
    )
    sel_mo  = c2.selectbox("🗓️ Mes", all_mo_yr, key="m_mo")

    sel_dep = c3.selectbox("🗺️ Departamento", ["Todos (Fanero)"]+DEPARTMENTS, key="m_dep")

    # Segmentación de productos — pills
    sel_pr = st.pills(
        "🛒 Producto",
        PRODUCTS_M,
        selection_mode="multi",
        default=PRODUCTS_M,
        key="m_pr",
    )
    if not sel_pr:
        st.info("Selecciona al menos un producto.")
        st.stop()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── FILTRADO ───────────────────────────────────────
    # Datos base sin Fanero (calculamos Fanero como suma)
    df_base = df_may_base[
        (df_may_base["Año"]==sel_yr) &
        (df_may_base["Departamento"]!="Fanero") &
        df_may_base["Producto"].isin(sel_pr)
    ].copy()
    if sel_mo != "Acumulado":
        df_base = df_base[df_base["Mes"]==sel_mo]

    if df_base.empty:
        st.warning("⚠️ Sin datos para la selección actual.")
        st.stop()

    # Datos del departamento seleccionado para KPIs
    if sel_dep == "Todos (Fanero)":
        df_kpi = df_base.copy()
    else:
        df_kpi = df_base[df_base["Departamento"]==sel_dep].copy()

    # ── KPIs ───────────────────────────────────────────
    tv = df_kpi["Ventas"].sum()
    tc = df_kpi["Cuota"].sum()
    cp = tv/tc*100 if tc else 0
    br = tc - tv

    # Delta vs mes anterior (si se filtra por mes específico)
    if sel_mo != "Acumulado":
        mo_idx   = all_mo_yr.index(sel_mo)
        prev_mo  = all_mo_yr[mo_idx-1] if mo_idx > 1 else None  # idx=0 es "Acumulado"
        if prev_mo and prev_mo != "Acumulado":
            df_prev = df_may_base[
                (df_may_base["Año"]==sel_yr) &
                (df_may_base["Mes"]==prev_mo) &
                df_may_base["Producto"].isin(sel_pr) &
                (df_may_base["Departamento"] == (
                    "Fanero" if sel_dep=="Todos (Fanero)" else sel_dep))
            ]
            pv = df_prev["Ventas"].sum()
        else:
            pv = 0
    else:
        pv = 0
    dv = (tv-pv)/pv*100 if pv else None

    st.markdown('<div class="sec-title">📌 Indicadores Clave</div>', unsafe_allow_html=True)
    k1,k2,k3,k4 = st.columns(4)
    k1.markdown(kpi("Ventas (Unid.)",  f"{int(tv):,}", dv, "vs mes ant."),             unsafe_allow_html=True)
    k2.markdown(kpi("Cuota (Unid.)",   f"{int(tc):,}"),                                 unsafe_allow_html=True)
    k3.markdown(kpi("% Cumplimiento",  f"{cp:.1f}%",   color=cc(cp)),                  unsafe_allow_html=True)
    k4.markdown(kpi("Brecha (Unid.)",  f"{int(abs(br)):,}",
                    color=C_ACCENT if br>0 else C_SUCCESS),                             unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TABLA PIVOTE ───────────────────────────────────
    st.markdown('<div class="sec-title">📊 Tabla de Desempeño por Departamento</div>', unsafe_allow_html=True)

    df_tbl = df_base.rename(columns={"Departamento":"Sub"}).copy()
    df_tbl["Grupo"] = "Fanero (Total)"

    html_may = build_pivot_html(
        df_data   = df_tbl,
        products  = list(sel_pr),
        group_col = "Grupo",
        sub_col   = "Sub",
        group_map = {"Fanero (Total)": DEPARTMENTS},
        units     = True,   # ← unidades puras, sin símbolo monetario
    )
    st.markdown(html_may, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── GRÁFICOS ───────────────────────────────────────
    gc1, gc2 = st.columns([3, 2])

    # Gráfico de columnas — Ventas vs Cuota por Departamento
    with gc1:
        st.markdown('<div class="sec-title">📊 Gráfico de Columnas · Ventas vs Cuota</div>', unsafe_allow_html=True)
        da = (df_base.groupby("Departamento")
                     .agg(Ventas=("Ventas","sum"), Cuota=("Cuota","sum"))
                     .reset_index())
        da["Cumpl"] = da["Ventas"]/da["Cuota"]*100
        da = da.sort_values("Ventas", ascending=False)

        fig_col = go.Figure()
        fig_col.add_trace(go.Bar(
            x=da["Departamento"], y=da["Cuota"],
            name="Cuota", marker_color=C_LIGHT,
            text=da["Cuota"].apply(lambda v: f"{int(v):,}"),
            textposition="outside", textfont=dict(size=10),
        ))
        fig_col.add_trace(go.Bar(
            x=da["Departamento"], y=da["Ventas"],
            name="Ventas", marker_color=C_PRIMARY, opacity=0.92,
            text=[f"{c:.0f}%" for c in da["Cumpl"]],
            textposition="inside", textfont=dict(color="white", size=11),
        ))
        fig_col.update_layout(
            **BASE_LAYOUT, height=340, barmode="group",
            yaxis=dict(title="Unidades", tickformat=",", gridcolor="#E8EDF2"),
            xaxis=dict(tickangle=-20),
        )
        st.plotly_chart(fig_col, use_container_width=True)

    # Gráfico circular — Mix de ventas por Producto
    with gc2:
        st.markdown('<div class="sec-title">🥧 Mix de Ventas por Producto</div>', unsafe_allow_html=True)
        pa = (df_base.groupby("Producto")
                     .agg(Ventas=("Ventas","sum"))
                     .reset_index())
        fig_pie = go.Figure(go.Pie(
            labels=pa["Producto"],
            values=pa["Ventas"],
            hole=0.46,
            marker=dict(
                colors=[C_PRIMARY, C_SECONDARY, "#4A90D9", "#7EB3E2"],
                line=dict(color="white", width=2),
            ),
            textinfo="percent+label",
            textfont=dict(size=11),
            textposition="inside",
        ))
        total_u = int(pa["Ventas"].sum())
        fig_pie.update_layout(
            **BASE_LAYOUT, height=340, showlegend=False,
            annotations=[dict(
                text=f"<b>{total_u:,}</b><br>unid.",
                x=0.5, y=0.5, font_size=13, showarrow=False,
                font_color=C_PRIMARY,
            )],
        )
        st.plotly_chart(fig_pie, use_container_width=True)


# ────────────────────────────────────────────────────
# TAB 2 · TPF
# ────────────────────────────────────────────────────
with tab2:

    # Filtros
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    t1,t2,t3,t4 = st.columns([1.8,2.2,2,2])
    t_yr_all = sorted(df_tpf_base["Año"].unique())
    sel_ty   = t1.multiselect("Año", t_yr_all, default=t_yr_all, key="t_yr")
    t_mo_all = sorted(df_tpf_base[df_tpf_base["Año"].isin(sel_ty)]["Mes"].unique(),
                      key=lambda x: pd.to_datetime(x,format="%b %Y"))
    def_tm   = t_mo_all[-6:] if len(t_mo_all)>6 else t_mo_all
    sel_tm   = t2.multiselect("Mes", t_mo_all, default=def_tm, key="t_mo")
    cl_opts  = ["Todos"]+list(CLUSTERS.keys())
    sel_cl   = t3.selectbox("Cluster", cl_opts, key="t_cl")
    sub_pool = ([s for ss in CLUSTERS.values() for s in ss]
                if sel_cl=="Todos" else CLUSTERS[sel_cl])
    sel_sub  = t4.multiselect("Subcluster", sub_pool, default=sub_pool, key="t_sub")

    # Productos a mostrar
    sel_tpr = st.multiselect("Productos a mostrar en tabla",
                              PRODUCTS_T, default=PRODUCTS_T, key="t_pr")
    st.markdown('</div>', unsafe_allow_html=True)

    # Filtrado
    tmask = (df_tpf_base["Año"].isin(sel_ty) &
             df_tpf_base["Mes"].isin(sel_tm) &
             df_tpf_base["Subcluster"].isin(sel_sub))
    if sel_cl!="Todos":
        tmask &= df_tpf_base["Cluster"]==sel_cl
    df_tf = df_tpf_base[tmask].copy()

    if df_tf.empty:
        st.warning("⚠️ Sin datos para la selección actual.")
        st.stop()

    # KPIs
    tv=df_tf["Ventas"].sum(); tc=df_tf["Cuota"].sum()
    tp=tv/tc*100 if tc else 0

    st.markdown('<div class="sec-title">📌 Indicadores Clave del Período</div>', unsafe_allow_html=True)
    k1,k2,k3,k4 = st.columns(4)
    k1.markdown(kpi("Ventas Totales",fmt(tv)),                           unsafe_allow_html=True)
    k2.markdown(kpi("Cuota Total",fmt(tc)),                              unsafe_allow_html=True)
    k3.markdown(kpi("% Cumplimiento",f"{tp:.1f}%",color=cc(tp)),        unsafe_allow_html=True)
    k4.markdown(kpi("Subclusters",str(df_tf["Subcluster"].nunique()),
                    color=C_NEUTRAL),                                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TABLA PIVOTE PRINCIPAL ────────────────────────
    st.markdown('<div class="sec-title">📊 Tabla de Desempeño por Cluster y Subcluster</div>', unsafe_allow_html=True)

    df_tbl = df_tf[df_tf["Producto"].isin(sel_tpr)].copy()

    # Mapa cluster → subclusters (respetando los filtros aplicados)
    active_map = {
        cl: [s for s in subs if s in sel_sub]
        for cl, subs in CLUSTERS.items()
        if (sel_cl=="Todos" or cl==sel_cl)
        and any(s in sel_sub for s in subs)
    }

    if not df_tbl.empty and sel_tpr:
        html_tpf = build_pivot_html(
            df_data   = df_tbl,
            products  = sel_tpr,
            group_col = "Cluster",
            sub_col   = "Subcluster",
            group_map = active_map,
        )
        st.markdown(html_tpf, unsafe_allow_html=True)
    else:
        st.info("Selecciona al menos un producto para ver la tabla.")

    # ── Gráficos complementarios ──────────────────────
    with st.expander("📈 Ver gráficos de tendencia y comparativo", expanded=False):

        st.markdown('<div class="sec-title">Comparativo por Cluster</div>', unsafe_allow_html=True)
        cl_agg = (df_tf.groupby("Cluster").agg(Ventas=("Ventas","sum"),Cuota=("Cuota","sum")).reset_index())
        cl_agg["Cumpl"] = cl_agg["Ventas"]/cl_agg["Cuota"]*100

        fig_cl = make_subplots(specs=[[{"secondary_y":True}]])
        fig_cl.add_trace(go.Bar(x=cl_agg["Cluster"],y=cl_agg["Cuota"],name="Cuota",marker_color=C_LIGHT),secondary_y=False)
        fig_cl.add_trace(go.Bar(x=cl_agg["Cluster"],y=cl_agg["Ventas"],name="Ventas",marker_color=C_PRIMARY,opacity=.92),secondary_y=False)
        fig_cl.add_trace(go.Scatter(x=cl_agg["Cluster"],y=cl_agg["Cumpl"],name="% Cumpl.",mode="lines+markers",
                                     line=dict(color=C_ACCENT,width=2.5),marker=dict(size=8)),secondary_y=True)
        fig_cl.add_hline(y=100,line_dash="dot",line_color=C_SUCCESS,secondary_y=True)
        fig_cl.update_layout(**BASE_LAYOUT,height=320,barmode="overlay")
        fig_cl.update_yaxes(title_text="Monto (S/)",secondary_y=False,tickformat=",.0f",gridcolor="#E8EDF2")
        fig_cl.update_yaxes(title_text="Cumplimiento (%)",secondary_y=True,showgrid=False)
        st.plotly_chart(fig_cl,use_container_width=True)

        st.markdown('<div class="sec-title">Tendencia Mensual</div>', unsafe_allow_html=True)
        tr_t = (df_tf.groupby("Fecha").agg(Ventas=("Ventas","sum"),Cuota=("Cuota","sum"))
                     .reset_index().sort_values("Fecha"))
        tr_t["Cumpl"] = tr_t["Ventas"]/tr_t["Cuota"]*100
        fig_t = make_subplots(specs=[[{"secondary_y":True}]])
        fig_t.add_trace(go.Bar(x=tr_t["Fecha"],y=tr_t["Cuota"],name="Cuota",marker_color=C_LIGHT),secondary_y=False)
        fig_t.add_trace(go.Bar(x=tr_t["Fecha"],y=tr_t["Ventas"],name="Ventas",marker_color=C_PRIMARY,opacity=.92),secondary_y=False)
        fig_t.add_trace(go.Scatter(x=tr_t["Fecha"],y=tr_t["Cumpl"],name="% Cumpl.",mode="lines+markers",
                                    line=dict(color=C_ACCENT,width=2.5),marker=dict(size=6)),secondary_y=True)
        fig_t.add_hline(y=100,line_dash="dot",line_color=C_SUCCESS,secondary_y=True)
        fig_t.update_layout(**BASE_LAYOUT,height=300,barmode="overlay")
        fig_t.update_yaxes(title_text="Monto (S/)",secondary_y=False,tickformat=",.0f",gridcolor="#E8EDF2")
        fig_t.update_yaxes(title_text="Cumplimiento (%)",secondary_y=True,showgrid=False)
        st.plotly_chart(fig_t,use_container_width=True)


# ────────────────────────────────────────────────────
# TAB 3 · CONGRESO
# ────────────────────────────────────────────────────
with tab3:
    st.markdown("""
    <div class="congress-wrap">
      <div style="font-size:4.5rem;margin-bottom:1rem">🏛️</div>
      <h2>Información en proceso de carga</h2>
      <p>Los datos del módulo Congreso estarán disponibles próximamente.<br>
         Por favor, vuelva a consultar en la próxima actualización.</p>
    </div>
    """, unsafe_allow_html=True)
