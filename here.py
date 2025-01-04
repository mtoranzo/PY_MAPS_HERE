# python -m venv venv
# ./venv/Scripts/Activate.ps1
# pip install -r requirements.txt
# python here.py
# deactivate

import requests
import pandas as pd

# Reemplaza 'YOUR_API_KEY' con tu clave de API de HERE
API_KEY = 'TN9vy_HKyQ4e6lhLFQPpWYx1BlvH7gN4YwAb16tc_88'

# Define el bounding box que cubre toda la República Dominicana
# Las coordenadas son aproximadas y deben ajustarse según sea necesario
bbox = '17.5,-71.5;19.0,-68.0'  # Este es un ejemplo para el bounding box

# URL para obtener datos de flujo de tráfico
url = f'https://traffic.ls.hereapi.com/traffic/6.3/flow.json?apiKey={API_KEY}&bbox={bbox}'

# Realiza la solicitud a la API
response = requests.get(url)

# Verifica si la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()

    # Procesa los datos y almacena en un DataFrame
    traffic_data = []
    for flow in data['RWS'][0]['RW']:
        for fi in flow['FIS'][0]['FI']:
            properties = fi['TMC']['PC']
            traffic_data.append({
                'speed': properties['SP'],
                'jam_factor': properties['JF'],
                'length': properties['LE'],
                'road_name': properties.get('DE', 'N/A')  # Manejo de nombre de carretera opcional
            })

    # Crea un DataFrame y lo guarda como CSV
    df = pd.DataFrame(traffic_data)
    df.to_csv('republica_dominicana_traffic_data.csv', index=False)
    print("Datos de tráfico almacenados en republica_dominicana_traffic_data.csv")
else:
    print(f"Error en la solicitud: {response.status_code} - {response.text}")