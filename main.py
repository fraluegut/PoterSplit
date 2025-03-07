from extractor import extract_left_profile
import os

# Definir rutas de entrada y salida
input_folder = "images/"
output_folder = "output/"

# Crear la carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Procesar todas las imágenes en la carpeta de entrada
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_folder, filename)
        print(f"📌 Procesando {filename}...")
        extract_left_profile(input_path, output_folder)
