import cv2
import numpy as np
import svgwrite
import os
import hashlib

def generate_unique_filename(output_folder, image_path, extension):
    """Genera un nombre de archivo único basado en un hash SHA256 de la imagen."""
    os.makedirs(output_folder, exist_ok=True)  # Asegura que la carpeta exista

    # Leer la imagen en bytes para generar un hash único
    with open(image_path, "rb") as f:
        image_hash = hashlib.sha256(f.read()).hexdigest()[:10]  # Hash de 10 caracteres

    return os.path.join(output_folder, f"perfil_{image_hash}.{extension}")

def extract_left_profile(image_path, output_folder):
    """
    Extrae la mitad izquierda de un perfil cerámico, limpia el contorno
    y lo guarda en formato PNG y SVG con nombres únicos basados en un hash de la imagen.

    :param image_path: Ruta de la imagen de entrada.
    :param output_folder: Carpeta donde se guardarán los archivos.
    """

    # Verificar que la imagen existe
    if not os.path.exists(image_path):
        print(f"❌ Error: No se encontró la imagen {image_path}")
        return

    # Cargar la imagen en escala de grises
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"❌ Error: No se pudo cargar la imagen {image_path}")
        return

    # Obtener dimensiones de la imagen
    height, width = image.shape

    # Cortar la mitad izquierda de la imagen
    half_width = width // 2
    left_half = image[:, :half_width]

    # Aplicar umbral para binarizar
    _, binary_left = cv2.threshold(left_half, 128, 255, cv2.THRESH_BINARY_INV)

    # Remover ruido con operaciones morfológicas
    kernel = np.ones((3, 3), np.uint8)
    binary_cleaned = cv2.morphologyEx(binary_left, cv2.MORPH_OPEN, kernel)

    # Encontrar contornos en la mitad izquierda
    contours_left, _ = cv2.findContours(binary_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrar los contornos, eliminando líneas rectas verticales no deseadas
    filtered_contours = []
    for contour in contours_left:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = h / w if w > 0 else 0
        if aspect_ratio < 5:  # Filtra líneas verticales largas
            filtered_contours.append(contour)

    # Crear imagen limpia con contornos
    profile_cleaned_img = np.ones_like(left_half) * 255
    cv2.drawContours(profile_cleaned_img, filtered_contours, -1, (0, 0, 0), 1)

    # Generar nombres únicos con hash de la imagen
    output_png = generate_unique_filename(output_folder, image_path, "png")
    output_svg = generate_unique_filename(output_folder, image_path, "svg")

    # Guardar la imagen procesada
    cv2.imwrite(output_png, profile_cleaned_img)

    # Generar archivo SVG con los contornos limpios
    dwg = svgwrite.Drawing(output_svg, profile='tiny')
    for contour in filtered_contours:
        points = [(float(point[0][0]), float(point[0][1])) for point in contour]
        if len(points) > 1:  # Evitar contornos demasiado pequeños
            dwg.add(dwg.polyline(points, stroke='black', fill='none', stroke_width=1))
    dwg.save()

    print(f"✅ Perfil guardado: {output_png}")
    print(f"✅ SVG guardado: {output_svg}")

    return output_png, output_svg
