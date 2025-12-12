from flask import Flask, render_template
import pandas as pd
import io
import requests

app = Flask(__name__)

# --- CONFIGURACIÓN ---
# 1. Crea tu Google Sheet con encabezados: titulo, contenido, autor, fecha, imagen_url
# 2. Ve a Archivo > Compartir > Publicar en la web > Formato CSV (.csv)
# 3. Pega el enlace aquí abajo:
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTBc3CqHDM29kPOcJofzndMKYISmii03_AiukbEiRp9pgRqiSHoKlut8oAtgwbH6QtnWbR5kV2a2wkG/pub?output=csv"

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/data')
def data():
    articulos = []
    try:
        # Descargamos el CSV directamente desde Google
        response = requests.get(SHEET_URL)
        response.encoding = 'utf-8' # Asegurar acentos
        if response.status_code == 200:
            # Convertimos el CSV a una lista de diccionarios para Python
            df = pd.read_csv(io.StringIO(response.text))
            # Rellenar valores vacíos para que no de error
            df = df.fillna('') 
            articulos = df.to_dict(orient='records')
    except Exception as e:
        print(f"Error cargando Google Sheet: {e}")
        # Datos de prueba por si falla la conexión
        articulos = [
            {'titulo': 'Error de Conexión', 'contenido': 'No se pudo cargar la hoja de cálculo.', 'autor': 'Sistema', 'fecha': 'Hoy'}
        ]

    return render_template('data.html', articulos=articulos)

# Rutas para los perfiles (opcional, para mantener tus otras páginas)
@app.route('/perfil/<nombre>')
def perfil(nombre):
    # Aquí podrías cargar Wurst.html o Mich.html dinámicamente
    return render_template(f'{nombre}.html')

if __name__ == '__main__':
    app.run()