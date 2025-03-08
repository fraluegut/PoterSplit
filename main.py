import cv2
import numpy as np
import os
import shutil

# 📂 Configuración de rutas
INPUT_IMAGE = "images/image.jpg"
OUTPUT_FOLDER = "output"
OUTPUT_SVG = os.path.join(OUTPUT_FOLDER, "imagen_limpiada.svg")

def clear_output_folder(output_folder):
    """Elimina todos los archivos dentro de la carpeta de salida y la recrea."""
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

def preprocess_image(image_path, output_path):
    """Voltea la imagen horizontalmente antes de procesarla."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"❌ Error: No se pudo cargar la imagen {image_path}")
        return None

    flipped_image = cv2.flip(image, 1)  # Voltea la imagen
    cv2.imwrite(output_path, flipped_image)
    print(f"🔄 Imagen volteada y guardada en {output_path}")
    return output_path

def extract_left_profile(input_image, output_svg):
    """Procesa la imagen volteada y extrae el perfil izquierdo en formato SVG."""
    image = cv2.imread(input_image, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"❌ Error: No se pudo cargar la imagen {input_image}")
        return None

    _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print("❌ No se encontraron contornos en la imagen.")
        return None

    contour = max(contours, key=cv2.contourArea)

    with open(output_svg, "w") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">\n')
        f.write('<path d="M ' + ' '.join(f"{p[0][0]},{p[0][1]}" for p in contour) + '" stroke="black" fill="none"/>\n')
        f.write("</svg>\n")

    print(f"✅ Perfil guardado en {output_svg}")
    return output_svg

def main():
    """Proceso principal"""
    clear_output_folder(OUTPUT_FOLDER)

    flipped_image = os.path.join(OUTPUT_FOLDER, "perfil_flipped.jpg")
    processed_image = preprocess_image(INPUT_IMAGE, flipped_image)

    if processed_image:
        extract_left_profile(processed_image, OUTPUT_SVG)

if __name__ == "__main__":
    main()
