import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- CONFIGURACIÓN STREAMLIT ---
st.set_page_config(page_title="🌡️ Clima AEMET", layout="wide")
st.title("🌡️ Monitor del Clima en Canarias")

# Sidebar para la API Key
st.sidebar.header("⚙️ Configuración")
api_key = st.sidebar.text_input("🔑 API Key de AEMET:", type="password")

st.sidebar.markdown("---")
st.sidebar.info("📌 Obtén tu API Key en:\nhttps://opendata.aemet.es/")

# Validar que hay API Key
if not api_key:
    st.warning("⚠️ Introduce tu API Key de AEMET en el panel lateral")
    st.markdown("""
    ### 📋 ¿Cómo obtener tu API Key?
    1. Ve a https://opendata.aemet.es/
    2. Regístrate o inicia sesión  
    3. Copia tu API Key
    4. Pégala en el campo de arriba
    """)
    st.stop()

# Ejecutar la aplicación
try:
    st.info("🔄 Conectando con AEMET...")
    
    url_aemet = "https://opendata.aemet.es/opendata/api/observacion/convencional/todas"
    headers = {'cache-control': "no-cache", 'api_key': api_key}
    
    respuesta_1 = requests.get(url_aemet, headers=headers, timeout=10)
    datos_permiso = respuesta_1.json()

    if datos_permiso.get('estado') == 200:
        url_secreta = datos_permiso['datos']
        st.success("✅ Conectado con AEMET")

        st.info("📥 Descargando datos...")
        respuesta_final = requests.get(url_secreta, timeout=15)
        datos_climaticos = respuesta_final.json()
        
        tabla_clima = pd.DataFrame(datos_climaticos)
        st.success(f"✅ Datos cargados: {len(tabla_clima)} estaciones")
        
        # --- TABS ---
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Gráfico", "📈 Datos", "🌡️ Estadísticas", "💾 Descargar"])
        
        with tab1:
            st.subheader("Temperatura - Tenerife")
            tenerife = tabla_clima[tabla_clima['ubi'].str.contains('Tenerife', case=False, na=False)]
            
            if len(tenerife) > 0:
                top_10 = tenerife.head(10)
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.bar(top_10['ubi'], top_10['ta'], color='coral')
                ax.set_title('Temperatura en Tenerife', fontsize=14, fontweight='bold')
                ax.set_xlabel('Estación', fontsize=12)
                ax.set_ylabel('Temperatura (°C)', fontsize=12)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.info("Sin datos de Tenerife")
        
        with tab2:
            st.subheader("Datos - Primeras 20 Estaciones")
            st.dataframe(tabla_clima.head(20), use_container_width=True)
            st.write(f"Total: {len(tabla_clima)} estaciones")
        
        with tab3:
            st.subheader("Temperaturas")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🔥 Máxima", f"{tabla_clima['ta'].max():.1f}°C")
            with col2:
                st.metric("🧊 Mínima", f"{tabla_clima['ta'].min():.1f}°C")
            with col3:
                st.metric("📊 Promedio", f"{tabla_clima['ta'].mean():.1f}°C")
            
            st.divider()
            st.write("**Tenerife:**")
            tenerife = tabla_clima[tabla_clima['ubi'].str.contains('Tenerife', case=False, na=False)]
            
            if len(tenerife) > 0:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("🌡️ Max Tenerife", f"{tenerife['ta'].max():.1f}°C")
                with col2:
                    st.metric("❄️ Min Tenerife", f"{tenerife['ta'].min():.1f}°C")
                
                idx_max = tenerife['ta'].idxmax()
                idx_min = tenerife['ta'].idxmin()
                
                st.write(f"🔥 **Más calor:** {tabla_clima.loc[idx_max, 'ubi']} → {tabla_clima.loc[idx_max, 'ta']:.1f}°C")
                st.write(f"❄️ **Más frío:** {tabla_clima.loc[idx_min, 'ubi']} → {tabla_clima.loc[idx_min, 'ta']:.1f}°C")
        
        with tab4:
            st.subheader("Descargar Datos")
            fecha = datetime.now().strftime("%Y-%m-%d")
            archivo = f"clima_canarias_{fecha}.csv"
            
            csv = tabla_clima.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name=archivo,
                mime="text/csv"
            )

    else:
        st.error(f"❌ Error de AEMET: {datos_permiso.get('descripcion', 'Error desconocido')}")

except requests.exceptions.Timeout:
    st.error("❌ Tiempo agotado - el servidor no responde")
except requests.exceptions.ConnectionError:
    st.error("❌ Error de conexión")
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.info("Verifica tu API Key y conexión")
