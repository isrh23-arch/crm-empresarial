
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
    
    st.success(f"✅ Archivo cargado: {len(df)} registros")
    
    # Mostrar columnas disponibles para debug
    with st.expander("Ver estructura del archivo"):
        st.write("**Columnas encontradas:**")
        st.write(list(df.columns))
        st.write("**Primeras filas:**")
        st.dataframe(df.head())
    
    # Verificar qué columnas existen
    tiene_etapa = 'etapa' in df.columns
    tiene_prob = 'probabilidad' in df.columns
    tiene_motivo_perdida = 'motivo_perdida' in df.columns
    tiene_motivo_ganado = 'motivo_ganado' in df.columns
    tiene_vendedor = 'vendedor' in df.columns
    
    # 1. MÉTRICAS GENERALES
    st.subheader("📈 MÉTRICAS GENERALES")
    
    if tiene_etapa:
        tratos_activos = df[df['etapa'].isin(['Nuevo', 'Propuesta', 'Negociacion'])]
        valor_pipeline = tratos_activos['monto'].sum() if 'monto' in df.columns else 0
        total_tratos = len(df)
        activos = len(tratos_activos)
    else:
        # Si no hay etapa, todos son activos
        tratos_activos = df
        valor_pipeline = df['monto'].sum() if 'monto' in df.columns else 0
        total_tratos = len(df)
        activos = len(df)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tratos", total_tratos)
    with col2:
        st.metric("Tratos Activos", activos)
    with col3:
        st.metric("Valor Pipeline", f"${valor_pipeline:,.0f}" if valor_pipeline > 0 else "$0")
    with col4:
        if tiene_prob and len(tratos_activos) > 0:
            prob_prom = tratos_activos['probabilidad'].mean()
            st.metric("Prob. Promedio", f"{prob_prom:.0f}%")
        else:
            st.metric("Prob. Promedio", "N/A")
    
    st.markdown("---")
    
    # 2. TRATOS POR VENDEDOR
    if tiene_vendedor and 'monto' in df.columns:
        st.subheader("👥 TRATOS POR VENDEDOR")
        if tiene_etapa:
            resumen = df.groupby('vendedor').agg({
                'cliente': 'count',
                'monto': lambda x: x[df.loc[x.index, 'etapa'].isin(['Nuevo', 'Propuesta', 'Negociacion'])].sum(),
            }).rename(columns={'cliente': 'Tratos', 'monto': 'Pipeline'}).reset_index()
        else:
            resumen = df.groupby('vendedor').agg({
                'cliente': 'count',
                'monto': 'sum'
            }).rename(columns={'cliente': 'Tratos', 'monto': 'Pipeline'}).reset_index()
        st.dataframe(resumen, use_container_width=True)
        st.markdown("---")
    
    # 3. DETALLE DE TRATOS
    st.subheader("📋 DETALLE DE TRATOS")
    columnas_a_mostrar = []
    for col in ['vendedor', 'cliente', 'monto', 'descripcion', 'etapa', 'probabilidad', 'telefono', 'motivo_perdida', 'motivo_ganado']:
        if col in df.columns:
            columnas_a_mostrar.append(col)
    
    if columnas_a_mostrar:
        st.dataframe(df[columnas_a_mostrar], use_container_width=True)
    else:
        st.dataframe(df)
    
    st.markdown("---")
    
    # 4. PIPELINE POR ETAPA (si existe la columna)
    if tiene_etapa and 'monto' in df.columns:
        st.subheader("📈 PIPELINE POR ETAPA")
        pipeline = df[df['etapa'].isin(['Nuevo', 'Propuesta', 'Negociacion'])].groupby('etapa')['monto'].sum().reset_index()
        if len(pipeline) > 0:
            st.bar_chart(pipeline.set_index('etapa'))
        else:
            st.info("No hay datos para mostrar")
    
    # 5. MOTIVOS DE PÉRDIDA
    if tiene_motivo_perdida and df['motivo_perdida'].notna().any():
        st.subheader("❌ MOTIVOS DE PÉRDIDA")
        perdidos = df[df['motivo_perdida'].notna()].groupby('motivo_perdida')['monto'].sum().reset_index()
        st.dataframe(perdidos, use_container_width=True)
    
    # 6. MOTIVOS DE GANANCIA
    if tiene_motivo_ganado and df['motivo_ganado'].notna().any():
        st.subheader("✅ MOTIVOS DE CIERRE")
        ganados = df[df['motivo_ganado'].notna()].groupby('motivo_ganado')['monto'].sum().reset_index()
        st.dataframe(ganados, use_container_width=True)
    
else:
    st.info("👈 Sube el archivo Excel con los datos de tu equipo")
