# interface.py
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QFrame, QMessageBox, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon, QPixmap, QAction, QImage
from PyQt6.QtCore import Qt
import sys
import numpy as np
from PIL import Image
from modelo import ejecutar_modelo


class DragDropWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.results_window = None
        # Agregar un espacio vertical
        layout.addSpacing(25)

        self.label = QLabel("Arrastra la imagen aquí")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFixedSize(325, 325)
        self.label.setStyleSheet("""
            QLabel {
                background-color: #EBF7EB;
                font-size: 16px;
                color: black;
                font-family: Arial
            }
        """)

        # Crear un QHBoxLayout y agregar el QLabel para centrarlo horizontalmente
        label_hbox = QHBoxLayout()
        label_hbox.addStretch()
        label_hbox.addWidget(self.label)
        label_hbox.addStretch()
        layout.addLayout(label_hbox)  # Agregar el QHBoxLayout al QVBoxLayout

        # Agregar un espacio vertical
        layout.addSpacing(5)

        self.button = QPushButton("Abre la imágen directamente de una carpeta")
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 12px; /* Reducir el padding interno */
                text-align: center;
                text-decoration: none;
                font-size: 14px; /* Reducir el tamaño de la fuente */
                margin: 4px 2px;
                min-width: 120px;
                min-height: 40px; /* Reducir la altura mínima */
                max-width: 300px;
            }
            QPushButton:hover {
                background-color: white;
                color: black;
                border: 2px solid #4CAF50;
            }
        """)

        # Establecer tamaño mínimo y tamaño por defecto para el botón
        self.button.setMinimumSize(750, 50)
        self.button.resize(150, 75)
        self.button.setMaximumWidth(300)
        self.button.setMaximumHeight(50)

        # Crear un QHBoxLayout y agregar el botón para centrarlo horizontalmente
        button_hbox = QHBoxLayout()
        button_hbox.addStretch()
        button_hbox.addWidget(self.button)
        button_hbox.addStretch()
        layout.addLayout(button_hbox)  # Agregar el QHBoxLayout al QVBoxLayout

        # Agregar un espacio vertical
        layout.addSpacing(50)

        self.button.clicked.connect(self.open_file)

        # Crear un QFrame como línea divisora horizontal
        divider_line = QFrame()
        divider_line.setFrameShape(QFrame.Shape.HLine)  # Línea horizontal
        divider_line.setFrameShadow(QFrame.Shadow.Sunken)  # Sombra hundida
        layout.addWidget(divider_line)

        # Agregar un espacio vertical
        layout.addSpacing(20)

        # Agregar el nuevo botón debajo de la línea divisora
        self.new_button = QPushButton("Ejecutar Modelo")
        self.new_button.setStyleSheet("""
            QPushButton {
                background-color: #808080;
                color: white;
                border: none;
                padding: 8px 16px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 10px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #A9A9A9;
            }
        """)
        layout.addWidget(self.new_button)

        # Conectar el nuevo botón a una función para manejar su funcionalidad futura
        self.new_button.clicked.connect(self.on_new_button_clicked)

        self.setAcceptDrops(True)
        self.file_path = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.label.setStyleSheet("""
                QLabel {
                    background-color: white;
                    color: black;
                    border: 2px solid #4CAF50;
                    font-size: 16px;
                }
            """)

    def dragLeaveEvent(self, event):
        self.label.setStyleSheet("""
            QLabel {
                background-color: #EBF7EB;
                border: 2px dashed #4CAF50;
                font-size: 16px;
            }
        """)

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            filepath = url.toLocalFile()
            print("Imagen arrastrada:", filepath)
            self.show_image(filepath)
            self.file_path = filepath
        
        # Restablecer el estilo de self.label después del drop
        self.label.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 2px dashed #4CAF50;
                font-size: 16px;
            }
        """)

    def show_image(self, filepath, processed_image = None):

        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None and isinstance(widget, QLabel) and widget != self.label:  # Asegúrate de no eliminar self.label
                widget.deleteLater()

        pixmap = QPixmap(filepath)
        pixmap = pixmap.scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if processed_image is not None:
        # Escalar la imagen de 0-1 a 0-255
            processed_image = (processed_image[0] * 255).astype(np.uint8)  # Quitar la dimensión de batch y escalar
            processed_image = Image.fromarray(processed_image)  # Convertir a objeto PIL

        # Redimensionar la imagen procesada
            processed_image = processed_image.resize((400, 300), Image.LANCZOS)  # Ajustar el tamaño según sea necesario
            processed_qimage = QImage(processed_image.tobytes(), processed_image.width, processed_image.height, QImage.Format.Format_RGB888)

        # Crear un QLabel para la imagen procesada
            processed_label = QLabel()
            processed_label.setFixedSize(400, 300)  # Ajustar el tamaño del QLabel al de la imagen procesada
            processed_label.setPixmap(QPixmap.fromImage(processed_qimage))
            processed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Añadir el QFrame con el layout procesado a tu layout principal
            self.layout().addWidget(processed_label)  # Usar el layout para añadir el QLabel

        # Añadir espacio adicional para garantizar que no haya solapamientos
            self.layout().addSpacing(5) 

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Imagen", "", "Archivos de imagen (*.jpg *.png *.jpeg)")
        if file_path:
            print("Imagen seleccionada:", file_path)
            self.label.setText(f"Imagen seleccionada:\n{file_path}")
            self.show_image(file_path)
            self.file_path = file_path  # Añadido para retornar la ruta de la imagen seleccionada
        

    def mostrar_resultados(self, predicted_labels, confidence_scores):

        # Crear una nueva ventana si no existe
        if not self.results_window:
            self.results_window = QWidget(self)  # Establecer self como padre
            self.results_window.setWindowTitle("Resultados del Modelo")
            self.results_layout = QVBoxLayout(self.results_window)

            self.results_window.setGeometry(100, 100, 300, 200)  # Ajustar tamaño y posición
            self.results_window.setStyleSheet("""
                QFrame {
                    background-color: #EBF7EB;
                }
                QLabel {
                    font-size: 14px;
                    color: black;
                }
            """)

        # Limpiar el layout anterior para evitar que se superpongan los resultados
        for i in reversed(range(self.results_layout.count())):
            widget = self.results_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Crear un QFrame para contener los resultados
        frame = QFrame()
        frame_layout = QVBoxLayout(frame)

        if float(confidence_scores[0]) < 0.75:
            for label, confidence in zip(predicted_labels, confidence_scores):
        # Mostrar la etiqueta predicha
                label_widget = QLabel(f"Etiqueta predicha: {label}")
                label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                frame_layout.addWidget(label_widget)

        # Mostrar la puntuación de confianza correspondiente a esa etiqueta
                confidence_widget = QLabel(f"Confianza: {confidence}")
                confidence_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                frame_layout.addWidget(confidence_widget)

        else:
            label_widget = QLabel(f"Etiqueta predicha: {predicted_labels[0]}")
            label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            frame_layout.addWidget(label_widget)
            confidence_widget = QLabel(f"Confianza: {confidence_scores[0]}")
            confidence_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            frame_layout.addWidget(confidence_widget)

        # Añadir el frame al layout de la ventana de resultados
        self.results_layout.addWidget(frame)

        # Mostrar la ventana
        self.results_window.show()

    def on_new_button_clicked(self):
        # Verificar si hay una imagen cargada
        if not self.file_path:
            QMessageBox.warning(self, "Advertencia", "Por favor, carga una imagen primero.")
            return

        # Ejecutar el modelo con la imagen seleccionada
        try:
            predicted_labels, confidence_score, processed_image = ejecutar_modelo(self.file_path)

            self.show_image(self.file_path, processed_image)

            # Mostrar los resultados en una nueva ventana
            self.mostrar_resultados(predicted_labels, confidence_score)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al ejecutar el modelo: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reconocimiento de Enfermedades Oculares")
        self.resize(1200, 900)

        icon = QIcon("icono_app.png")
        self.setWindowIcon(icon)

        central_widget = DragDropWidget()
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
