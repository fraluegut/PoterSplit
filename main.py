import sys
import os
import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QSlider, QHBoxLayout
from PySide6.QtGui import QPixmap, QImage, QPainter, QPen
from PySide6.QtCore import Qt

# 📂 Configuración de rutas
INPUT_IMAGE = "images/image.jpg"
OUTPUT_FOLDER = "output"
OUTPUT_IMAGE = os.path.join(OUTPUT_FOLDER, "imagen_limpiada.jpg")
OUTPUT_SVG = os.path.join(OUTPUT_FOLDER, "imagen_limpiada.svg")

class ImageSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seleccionar Base y Eje de Rotación")
        self.setGeometry(100, 100, 900, 700)

        self.image_path = INPUT_IMAGE
        self.image = None
        self.pixmap = None

        # 📌 Variables de las líneas base y eje
        self.image_height = 500  # Altura fija para la imagen
        self.image_width = 500   # Ancho fijo para la imagen
        self.base_y = self.image_height // 2  # Base centrada inicialmente
        self.axis_x = self.image_width // 2   # Eje centrado inicialmente

        self.initUI()

    def initUI(self):
        # Layout principal
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # 📌 Barra deslizante para la base (vertical, ahora con dirección correcta)
        self.slider_base = QSlider(Qt.Vertical)
        self.slider_base.setMinimum(0)
        self.slider_base.setMaximum(self.image_height)
        self.slider_base.setValue(self.image_height - self.base_y)  # Invertido para corregir dirección
        self.slider_base.valueChanged.connect(self.update_base)
        left_layout.addWidget(self.slider_base)

        # 📌 Imagen centrada
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.label)

        # 📌 Barra deslizante para el eje (horizontal)
        self.slider_axis = QSlider(Qt.Horizontal)
        self.slider_axis.setMinimum(0)
        self.slider_axis.setMaximum(self.image_width)
        self.slider_axis.setValue(self.axis_x)
        self.slider_axis.valueChanged.connect(self.update_axis)
        right_layout.addWidget(self.slider_axis)

        # 📌 Agregar layouts
        main_layout.addLayout(left_layout)  # Barra vertical a la izquierda
        main_layout.addLayout(right_layout)  # Imagen y barra horizontal

        # 📌 Contenedor central
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # 📌 Layout inferior con botones
        button_layout = QVBoxLayout()
        self.btn_select = QPushButton("Seleccionar Imagen", self)
        self.btn_select.clicked.connect(self.load_image)
        button_layout.addWidget(self.btn_select)

        self.btn_reset = QPushButton("Resetear Selección", self)
        self.btn_reset.clicked.connect(self.reset_selection)
        button_layout.addWidget(self.btn_reset)

        self.btn_save = QPushButton("Guardar Imagen y SVG", self)
        self.btn_save.clicked.connect(self.save_image_and_svg)
        button_layout.addWidget(self.btn_save)

        # 📌 Agregar botones al layout principal
        right_layout.addLayout(button_layout)

    def load_image(self):
        """Carga una imagen desde el explorador de archivos y la centra."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            self.image_path = file_name
            self.image = cv2.imread(self.image_path)
            self.display_image()

    def display_image(self):
        """Convierte la imagen de OpenCV a un formato compatible con PySide6 y la centra en la ventana."""
        if self.image is None:
            return

        # 📌 Redimensionar la imagen
        self.image = cv2.resize(self.image, (self.image_width, self.image_height), interpolation=cv2.INTER_AREA)

        height, width, channel = self.image.shape
        bytes_per_line = 3 * width
        qimg = QImage(self.image.data, width, height, bytes_per_line, QImage.Format_BGR888)
        self.pixmap = QPixmap.fromImage(qimg)

        self.update_display()

    def update_display(self):
        """Redibuja la imagen con las líneas de selección alineadas correctamente."""
        if self.pixmap is None:
            return

        pixmap_copy = self.pixmap.copy()
        painter = QPainter(pixmap_copy)
        pen = QPen(Qt.red, 2, Qt.SolidLine)

        # 📌 Dibujar línea base (horizontal)
        painter.setPen(pen)
        painter.drawLine(0, self.base_y, self.image_width, self.base_y)

        # 📌 Dibujar línea del eje de rotación (vertical)
        pen.setColor(Qt.blue)
        painter.setPen(pen)
        painter.drawLine(self.axis_x, 0, self.axis_x, self.image_height)

        painter.end()
        self.label.setPixmap(pixmap_copy)

    def update_base(self, value):
        """📌 Ajusta la posición de la línea base asegurando que esté alineada con la barra correctamente."""
        self.base_y = self.image_height - value  # Ahora se mueve correctamente
        self.update_display()

    def update_axis(self, value):
        """📌 Ajusta la posición de la línea del eje de rotación."""
        self.axis_x = value
        self.update_display()

    def reset_selection(self):
        """📌 Resetea la selección de base y eje."""
        self.base_y = self.image_height // 2
        self.axis_x = self.image_width // 2
        self.slider_base.setValue(self.image_height - self.base_y)
        self.slider_axis.setValue(self.axis_x)
        self.update_display()

    def save_image_and_svg(self):
        """📌 Recorta solo la esquina superior izquierda, la voltea horizontalmente y la guarda como SVG."""
        if self.image is None:
            print("⚠️ No se seleccionó una imagen.")
            return

        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        # 📌 Recortar **solo** la esquina superior izquierda
        cropped_image = self.image[0:self.base_y, 0:self.axis_x]

        # 📌 Voltear horizontalmente
        flipped_image = cv2.flip(cropped_image, 1)

        # 📌 Guardar la imagen procesada
        cv2.imwrite(OUTPUT_IMAGE, flipped_image)
        print(f"✅ Imagen guardada correctamente en {OUTPUT_IMAGE}")

        # 📌 Generar el SVG con el perfil
        self.create_svg(flipped_image, OUTPUT_SVG)
        print(f"✅ SVG guardado en {OUTPUT_SVG}")

        self.close()

    def create_svg(self, image, output_svg):
        """Extrae el perfil de la imagen en blanco y negro y lo guarda en formato SVG."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            print("❌ No se encontraron contornos en la imagen.")
            return

        contour = max(contours, key=cv2.contourArea)

        with open(output_svg, "w") as f:
            f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">\n')
            f.write('<path d="M ' + ' '.join(f"{p[0][0]},{p[0][1]}" for p in contour) + '" stroke="black" fill="none"/>\n')
            f.write("</svg>\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageSelector()
    window.show()
    sys.exit(app.exec())
