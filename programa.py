import requests
import time # Importamos 'time' para que el robot pueda esperar unos segundos si es necesario
# --- CONFIGURACIÓN ---
# En vez de escribir la API Key aquí, la pedimos al usuario
api_key = input("🔑 Introduce tu API Key de AEMET: ")

url_aemet = "https://opendata.aemet.es/opendata/api/observacion/convencional/todas"
headers = {'cache-control': "no-cache", 'api_key': api_key}


# --- VIAJE 1: Pedir permiso y dirección secreta ---
print("🤖 Robot: Hola AEMET, ¿me das permiso para ver el clima de hoy?")
respuesta_1 = requests.get(url_aemet, headers=headers)
datos_permiso = respuesta_1.json() # Convertimos la respuesta en un diccionario de Python

if datos_permiso['estado'] == 200:
    # Si el estado es 200, AEMET nos ha dado una URL secreta en el campo 'datos'
    url_secreta = datos_permiso['datos']
    print(f"✅ Robot: ¡Permiso concedido! La dirección del paquete es: {url_secreta}")

    # --- VIAJE 2: Ir a la dirección secreta a recoger el paquete ---
    print("🤖 Robot: Yendo a la dirección secreta a por los datos reales...")
    # No necesitamos enviar la API Key en este segundo viaje, la URL secreta ya es el permiso
    respuesta_final = requests.get(url_secreta)
    
    # Estos son nuestros datos climáticos reales
    datos_climaticos = respuesta_final.json()
    
    # Vamos a mostrar solo los primeros 2 registros para no llenar la pantalla
    print("📊 Robot: ¡He traído los datos! Aquí tienes una muestra de las primeras estaciones:")
    print(datos_climaticos[:2]) 

else:
    print(f"❌ Error: AEMET dice: {datos_permiso['descripcion']}")

import pandas as pd # Importamos Pandas con el apodo 'pd' (es el estándar)

# --- (Imagina que aquí arriba está el código del "Segundo Viaje" que ya hicimos) ---
# Supongamos que 'datos_climaticos' es la lista de fichas que trajo el robot

# 1. La magia de una sola línea:
# Le decimos a Pandas: "Coge esta lista de fichas (JSON) y conviértela en una tabla"
tabla_clima = pd.DataFrame(datos_climaticos)

# 2. El robot nos enseña la tabla limpia
print("✨ Robot: ¡Tachán! He organizado los datos en una tabla:")
print(tabla_clima.head()) # '.head()' le dice al robot: "enséñame solo las primeras 5 filas"

# 3. Guardar el trabajo para GitHub o Excel
# Podemos guardar esta tabla en un archivo .csv (compatible con Excel)
tabla_clima.to_csv("datos_aemet_final.csv", index=False)
print("💾 Robot: He guardado la tabla en un archivo llamado 'datos_aemet_final.csv'")
