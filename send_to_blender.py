import os
import subprocess

# 📂 Configuración
OUTPUT_SVG = "output/imagen_limpiada.svg"
BLENDER_SCRIPT = "blender_revolve.py"
BLENDER_EXECUTABLE = "/mnt/c/Program Files/Blender Foundation/Blender 4.1/blender.exe"

def send_svg_to_blender(svg_path, blender_script_path):
    """Envía `imagen_limpiada.svg` a Blender."""
    if not os.path.exists(svg_path):
        print(f"❌ Error: No se encontró el archivo SVG {svg_path}")
        return

    if not os.path.exists(blender_script_path):
        print(f"❌ Error: No se encontró el script de Blender en {blender_script_path}")
        return

    # Convertir rutas de WSL a Windows
    svg_path_win = subprocess.run(["wslpath", "-w", svg_path], capture_output=True, text=True).stdout.strip()
    blender_script_win = subprocess.run(["wslpath", "-w", blender_script_path], capture_output=True, text=True).stdout.strip()

    print(f"🟢 Enviando {svg_path_win} a Blender")

    # Ejecutar Blender con el script
    subprocess.run([
        BLENDER_EXECUTABLE, "--factory-startup", "--python", blender_script_win
    ])

if __name__ == "__main__":
    send_svg_to_blender(OUTPUT_SVG, BLENDER_SCRIPT)
