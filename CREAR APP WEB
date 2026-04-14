import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# --- TÍTULO DE LA WEB ---
st.set_page_config(page_title="Vigilante Climático AEMET", page_icon="🌤️")
st.title("🤖 Asistente Climático Inteligente")
st.markdown("Consulta datos en tiempo real y predicciones de la AEMET.")

# --- BARRA LATERAL (Consultas) ---
st.sidebar.header("Configuración")
api_key = st.sidebar.text_input("Introduce tu API Key de AEMET", type="password")
umbral_calor = st.sidebar.slider("Umbral de alerta (°C)", 20, 45, 30)

# --- LÓGICA PRINCIPAL ---
if api_key:
    st.success("Conectado a la API")
    
    # Aquí iría el código que ya tenemos para bajar los datos
    # (Simulamos una tabla para el ejemplo)
    datos = {'ubi': ['Tenerife', 'Madrid', 'Barcelona'], 'temp': [22.5, 31.0, 25.4]}
    df = pd.DataFrame(datos)
    
    # Mostrar la tabla en la web
    st.subheader("📊 Datos Actuales")
    st.dataframe(df)
    
    # Botón para lanzar la Alerta
    if st.button('Revisar Alertas'):
        alertas = df[df['temp'] >= umbral_calor]
        if not alertas.empty:
            st.error(f"⚠️ ¡Atención! Hay {len(alertas)} ciudades en alerta.")
        else:
            st.balloons() # ¡Efecto visual de globos si todo está bien!
            st.write("✅ Todo bajo control.")
            
else:
    st.warning("Por favor, introduce tu API Key en la izquierda para empezar.")
