"""
Servidor web simple para servir archivos estáticos durante el desarrollo
"""
from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='./')
CORS(app)  # Habilita CORS para todas las rutas

@app.route('/')
def index():
    """Sirve la página principal"""
    return send_from_directory('./', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Sirve cualquier archivo estático solicitado"""
    return send_from_directory('./', path)

if __name__ == '__main__':
    print("Servidor iniciado en http://localhost:5001")
    print("Presiona CTRL+C para detener el servidor")
    # Ejecuta el servidor en el puerto 5001 para no interferir con tu API en el puerto 5000
    app.run(host='0.0.0.0', port=5001, debug=True)