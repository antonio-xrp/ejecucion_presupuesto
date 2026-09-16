import streamlit as st

import pandas as pd

from pathlib import Path

from components.kpi import render_kpi
from utils.styles import load_css

from utils.data import load_data
from utils.format import formato_monto

from charts.line import crear_line_chart
from charts.bar import crear_bar_chart

from services.presupuesto import (
    filtrar_presupuesto,
    filtrar_ejecucion,
    preparar_evolucion,
    calcular_kpis,
    agrupar_ejecucion
)


# CONFIGURACIÓN INICIAL
st.set_page_config(
    page_title = 'PRESUPUESTO Y EJECUCIÓN',
    page_icon="📊",
    layout="wide",
)


# RUTAS

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"

DATA_DIR = BASE_DIR / "data" / "processed"
load_css(APP_DIR / "styles" / "kpi.css")
 
# CONSTANTES DE DISEÑO
# Altura fija que comparten los 3 bloques de gráficos para que
# queden perfectamente alineados en ancho y alto.
CHART_HEIGHT = 470
# Alto interno de la figura (deja margen para el padding del container/border)
CHART_INNER_HEIGHT = CHART_HEIGHT - 40
 
 
def espacio_vertical(rem: float = 1.5) -> None:
    """Inserta un separador vertical consistente entre secciones."""
    st.markdown(
        f"<div style='margin-top: {rem}rem;'></div>",
        unsafe_allow_html=True,
    )

# CARGA DE DATOS

presupuesto, ejecucion_mensual = load_data(DATA_DIR)


# TITULO

st.title("PRESUPUESTO Y EJECUCIÓN - GOBIERNOS LOCALES - MUNICIPALIDADES 📊")
st.caption("Análisis de presupuesto y ejecución presupuestal")

# FILTROS

col1, col2, col3, col4 = st.columns(4)

with col1:
    departamentos = sorted(
        presupuesto["DEPARTAMENTO_EJECUTORA_NOMBRE"]
        .dropna()
        .unique())

    departamento = st.selectbox(
        "Departamento",
        departamentos
    )

with col2:
    provincias = sorted(
        presupuesto.loc[
            presupuesto["DEPARTAMENTO_EJECUTORA_NOMBRE"] == departamento, "PROVINCIA_EJECUTORA_NOMBRE"]
        .dropna()
        .unique())

    provincia = st.selectbox(
        "Provincia",
        ["Todas"] + provincias
    )

with col3:
    distritos = sorted(
        presupuesto.loc[
            (presupuesto["DEPARTAMENTO_EJECUTORA_NOMBRE"] == departamento) &
            (presupuesto["PROVINCIA_EJECUTORA_NOMBRE"] == provincia), 
            "DISTRITO_EJECUTORA_NOMBRE"]
        .dropna()
        .unique())

    distrito = st.selectbox(
        "Distrito",
        ["Todas"] + distritos
    )

with col4:
    meses = sorted(
        ejecucion_mensual["MES_EJE"]
        .dropna()
        .unique())

    mes = st.selectbox(
        "Mes",
        meses,
        format_func = lambda x : pd.to_datetime(str(x), format="%m")
        .strftime("%B").capitalize()
    )


presupuesto_filtrado = filtrar_presupuesto(
    presupuesto=presupuesto,
    departamento=departamento,
    provincia=provincia,
    distrito=distrito,
)

ejecucion_filtrada = filtrar_ejecucion(
    ejecucion=ejecucion_mensual,
    departamento=departamento,
    provincia=provincia,
    distrito=distrito,
    mes=mes,
)

# FILTRO PRESUPUESTO

kpis = calcular_kpis(
    presupuesto=presupuesto_filtrado,
    ejecucion=ejecucion_filtrada,
)


# SHOW KPIS

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5, gap="medium")

with kpi1:

    render_kpi(
        title="Presupuesto Inicial - PIA",
        value=formato_monto(kpis["pia"]),
        icon="💰",
        variant="blue"
    )


with kpi2:

    render_kpi(
        title="Presupuesto Modificado - PIM",
        value=formato_monto(kpis["pim"]),
        icon="📊",
        variant="purple"
    )


with kpi3:

    render_kpi(
        title="Gasto Ejecutado - Devengado",
        value=formato_monto(kpis["devengado"]),
        icon="💸",
        variant="red"
    )


with kpi4:

    render_kpi(
        title="Ejecución",
        value=(
            "N/D"
            if kpis["ejecucion"] is None
            else f'{kpis["ejecucion"]:.2f}%'
        ),
        icon="📈",
        variant="green"
    )


with kpi5:

    render_kpi(
        title="Saldo Pendiente",
        value=formato_monto(kpis["saldo"]),
        icon="⏳",
        variant="orange"
    )




# Separación consistente entre los KPIs y la fila de gráficos
espacio_vertical(2)

# GRÁFICOS

grafico1, grafico2, grafico3 = st.columns(
    [1, 1.2, 1], gap="medium")


# GRAFICOS LINEAL - EVOLUCION ACUMULADA DEVENGADOS

with grafico1:
    with st.container(height=CHART_HEIGHT, border=True):
        evolucion = preparar_evolucion(
            ejecucion_filtrada
        )
 
        fig = crear_line_chart(
            df=evolucion,
            x="FECHA",
            y=[
                "MONTO_DEVENGADO",
                "MONTO_DEVENGADO_ACUMULADO",
            ],
            title="Evolución mensual y acumulada del devengado",
            labels={
                "FECHA": "Mes",
                "value": "Monto",
                "variable": "Indicador",
                "MONTO_DEVENGADO": "Devengado mensual",
                "MONTO_DEVENGADO_ACUMULADO": "Devengado acumulado",
            },
            height=CHART_INNER_HEIGHT,
            xaxis_title="",
            yaxis_title="Monto (S/)",
            legend_title="",
            legend_orientation="h",
            legend_x=0,
            legend_y=1.02,
            hovertemplate="S/ %{y:,.0f}<extra></extra>",
        )
 
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )


# GRAFICO DE BARRAS HORIZONTALES - EJECUCION POR DISTRITO

with grafico2:
    with st.container(height=CHART_HEIGHT, border=True):

        ejecucion_entidad = agrupar_ejecucion(
            presupuesto_filtrado,
            ejecucion_filtrada,
        )
 
        # Selector
        vista_ranking = st.segmented_control(
            "Mostrar",
            options=["Todos", "Top 10"],
            default="Top 10",
            key="ranking_ejecucion",
        )
 
        # Aplicar Top 10 / Todos y definir la altura real de la figura.
        # Cuando se muestran todos los distritos la figura crece según
        # el número de filas; al estar dentro de un container de altura
        # fija, el excedente se muestra con scroll interno en lugar de
        # descuadrar el ancho/alto del bloque.
        if vista_ranking == "Top 10":
            ejecucion_entidad = (
                ejecucion_entidad
                .sort_values("EJECUCION_%", ascending=False)
                .head(10)
                .sort_values("EJECUCION_%", ascending=True)
            )
            altura_fig = CHART_INNER_HEIGHT - 60
 
        else:
            ejecucion_entidad = (
                ejecucion_entidad
                .sort_values("EJECUCION_%", ascending=True)
            )
            # Altura proporcional al número de distritos para que cada
            # barra tenga espacio legible; el scroll lo da el container.
            altura_fig = max(
                CHART_INNER_HEIGHT - 60,
                len(ejecucion_entidad) * 28
            )
 
        fig = crear_bar_chart(
            df=ejecucion_entidad,
            x="EJECUCION_%",
            y="DISTRITO_EJECUTORA_NOMBRE",
            text="EJECUCION_%",
            title="RANKING POR EJECUCIÓN",
            labels={
                "DISTRITO_EJECUTORA_NOMBRE": "DISTRITO",
                "EJECUCION_%": "EJECUCIÓN"
            },
            text_template="%{text:.1f}",
            text_position="outside",
            height=altura_fig,
            xaxis_title="",
            yaxis_title="",
            hover_template="%{y}: %{x:.1f}%",
            xaxis_ticksuffix="%",
        )
 
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )
 
# TABLA 3 

with grafico3:
    with st.container(height=CHART_HEIGHT, border=True):
        st.markdown("**RANKING POR FUNCIÓN**")
 
        funcion = (
            ejecucion_filtrada
            .groupby("FUNCION_NOMBRE")
            .agg(
                MONTO_DEVENGADO=("MONTO_DEVENGADO", "sum")
            )
            .reset_index()
            .sort_values(
                by="MONTO_DEVENGADO",
                ascending=False
            )
        )
 
        funcion["DEVENGADO (S/)"] = funcion["MONTO_DEVENGADO"].apply(
            formato_monto
        )
        funcion = funcion.drop(columns="MONTO_DEVENGADO")
 
        st.dataframe(
            funcion,
            use_container_width=True,
            hide_index=True,
            height=CHART_INNER_HEIGHT - 50,
            column_config={
                "FUNCION_NOMBRE": st.column_config.TextColumn(
                    "FUNCIÓN",
                    width="large",
                ),
                "DEVENGADO (S/)": st.column_config.TextColumn(
                    "GASTO EJECUTADO ACU (S/)",
                    width="medium",
                ),
            },
        )