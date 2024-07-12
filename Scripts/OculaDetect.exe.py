# interface.py
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QFrame, QMessageBox, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon, QPixmap, QAction
from PyQt6.QtCore import Qt
import sys

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

        # Añadir el texto "o" centrado horizontalmente
        label_or = QLabel(" o ")
        label_or.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_or.setStyleSheet("font-size: 16px;")
        layout.addWidget(label_or)

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

    def show_image(self, filepath):
        pixmap = QPixmap(filepath)
        pixmap = pixmap.scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Imagen", "", "Archivos de imagen (*.jpg *.png *.jpeg)")
        if file_path:
            print("Imagen seleccionada:", file_path)
            self.label.setText(f"Imagen seleccionada:\n{file_path}")
            self.show_image(file_path)
            self.file_path = file_path  # Añadido para retornar la ruta de la imagen seleccionada
        
    def get_file_path(self):
        return self.file_path

    def mostrar_resultados(self, predicted_labels, confidence_score):
        
        # Cerrar la ventana de resultados anterior si existe
        if self.results_window:
            self.results_window.close()

        # Crear una nueva ventana para mostrar los resultados
        self.results_window = QWidget(self)  # Establecer self como padre
        self.results_window.setObjectName("ResultsWindow")  # Establecer un nombre para identificar la ventana
        results_layout = QVBoxLayout(self.results_window)

        # Limpiar el contenido previo del layout
        for i in reversed(range(results_layout.count())):
            widget = results_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        frame = QFrame()
        frame.setStyleSheet("""
        QFrame {
            background-color: #EBF7EB;              
        }
        QLabel {
            font-size: 12px;
            color: black;
        }
        """)
        frame_layout = QVBoxLayout(frame)

        for label in predicted_labels:
            label_widget = QLabel(f"Etiqueta predicha: \n {label}")
            label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar el texto
            frame_layout.addWidget(label_widget)

        confidence_widget = QLabel(f"Confidence Score: \n {confidence_score}")
        confidence_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar el texto
        frame_layout.addWidget(confidence_widget)
        results_layout.addWidget(frame)

        self.results_window.setGeometry(0, 0, 150, 100)  # Ajustar tamaño y posición manualmente
        self.results_window.setWindowTitle("Resultados del Modelo")
        self.results_window.show()
        # Mostrar resultados

    def on_new_button_clicked(self):
        # Verificar si hay una imagen cargada
        if not self.file_path:
            QMessageBox.warning(self, "Advertencia", "Por favor, carga una imagen primero.")
            return

        # Ejecutar el modelo con la imagen seleccionada
        try:
            predicted_labels, confidence_score = ejecutar_modelo(self.file_path)

            # Mostrar los resultados en una nueva ventana
            self.mostrar_resultados(predicted_labels, confidence_score)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al ejecutar el modelo: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reconocimiento de Enfermedades Oculares")
        self.resize(700, 600)

        icon = QIcon("icono_app.png")
        self.setWindowIcon(icon)

        central_widget = DragDropWidget()
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
