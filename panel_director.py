
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="CRM Empresarial", layout="wide")

st.title("📊 PANEL DE CONTROL - EQUIPO DE VENTAS")
st.markdown(f"### 📅 {datetime.now().strftime('%d de %B de %Y')}")
st.markdown("---")

archivo = st.file_uploader("Carga el archivo con datos del equipo", type=['xlsx', 'csv'])

if archivo is not None:
    df = pd.read_excel(archivo) if archivo.name.endswith('.xlsx') else pd.read_csv(archivo)
    
    # Métricas
    tratos_activos = df[df['etapa'].isin(['Nuevo', 'Propuesta', 'Negociacion'])]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tratos", len(df))
    with col2:
        st.metric("Tratos Activos", len(tratos_activos))
    with col3:
        st.metric("Valor Pipeline", f"${tratos_activos['monto'].sum():,.0f}")
    with col4:
        prob = tratos_activos['probabilidad'].mean() if len(tratos_activos) > 0 else 0
        st.metric("Prob. Promedio", f"{prob:.0f}%")
    
    st.markdown("---")
    
    # Tratos por vendedor
    st.subheader("👥 TRATOS POR VENDEDOR")
    resumen = df.groupby('vendedor').agg({
        'cliente': 'count',
        'monto': lambda x: x[df.loc[x.index, 'etapa'].isin(['Nuevo', 'Propuesta', 'Negociacion'])].sum(),
    }).rename(columns={'cliente': 'Tratos', 'monto': 'Pipeline'})
    st.dataframe(resumen)
    
    st.markdown("---")
    
    # Detalle de tratos
    st.subheader("📋 DETALLE DE TRATOS")
    st.dataframe(df)
    
    # Pipeline por etapa
    st.subheader("📈 PIPELINE POR ETAPA")
    pipeline = tratos_activos.groupby('etapa')['monto'].sum().reset_index()
    st.bar_chart(pipeline.set_index('etapa'))
    
    # Motivos de pérdida
    if 'motivo_perdida' in df.columns and df['motivo_perdida'].notna().any():
        st.subheader("❌ MOTIVOS DE PÉRDIDA")
        perdidos = df[df['motivo_perdida'].notna()].groupby('motivo_perdida')['monto'].sum()
        st.dataframe(perdidos)
    
    # Motivos de ganancia
    if 'motivo_ganado' in df.columns and df['motivo_ganado'].notna().any():
        st.subheader("✅ MOTIVOS DE CIERRE")
        ganados = df[df['motivo_ganado'].notna()].groupby('motivo_ganado')['monto'].sum()
        st.dataframe(ganados)
    
else:
    st.info("👈 Sube el archivo Excel con los datos de tu equipo")
