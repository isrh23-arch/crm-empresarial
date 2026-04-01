
import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

st.set_page_config(page_title="CRM Agricola", layout="wide")

st.title("🌾 CRM AGRICOLA - VENDEDOR")
st.markdown(f"### 📅 {datetime.now().strftime('%d de %B de %Y')}")
st.markdown("---")

st.info("""
### COMO USAR:
1. Sube tu archivo Excel con tus clientes y tratos
2. El sistema te mostrara las prioridades
3. Contacta a tus clientes con WhatsApp
""")

archivo = st.file_uploader("Carga tu archivo Excel", type=['xlsx', 'csv'])

if archivo is not None:
    try:
        if archivo.name.endswith('.xlsx'):
            df = pd.read_excel(archivo)
        else:
            df = pd.read_csv(archivo)
        
        st.success(f"Archivo cargado: {len(df)} registros")
        
        with st.expander("Ver datos"):
            st.dataframe(df.head())
        
        st.markdown("---")
        st.subheader("📋 PRIORIDADES DEL DIA")
        
        for i in range(min(10, len(df))):
            row = df.iloc[i]
            nombre = row.get('cliente', row.get('nombre', 'Cliente'))
            monto = row.get('monto', 0)
            descripcion = row.get('descripcion', '')
            telefono = row.get('telefono', '521234567890')
            
            monto_str = f"${monto:,.0f}" if monto > 0 else "$0"
            mensaje = f"Hola {nombre}, te contacto por tu trato de {monto_str} ({descripcion})"
            whatsapp_link = f"https://wa.me/{telefono}?text={urllib.parse.quote(mensaje)}"
            
            st.markdown(f"""
            ---
            **{nombre}**  
            - Trato: {monto_str} - {descripcion}  
            - [Contactar por WhatsApp]({whatsapp_link})
            """)
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Sube un archivo Excel para comenzar")
