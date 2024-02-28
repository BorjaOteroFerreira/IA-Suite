import json
import os
import sys
import atexit
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon
from flask import request
from IASuite import IASuiteApi

class EmbeddedFlaskApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Configurar la aplicación Flask
        self.flask_app = IASuiteApi()
        # Configurar la interfaz de PyQt
        self.init_ui()

    def init_ui(self):
        # Crear un widget contenedor
        container = QWidget(self)
        self.setCentralWidget(container)

        # Crear un diseño vertical para el widget contenedor
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        # Crear un visor web utilizando WebEngineView
        web_view = QWebEngineView(self)
        web_view.load(QUrl("http://127.0.0.1:8080")) 
        #web_view.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        layout.addWidget(web_view)
        

        self.setGeometry(100, 100, 1920, 1080)
        web_view.setZoomFactor(0.95)  
     
        style_sheet = """
            QMainWindow {
                background-color: #011627;

            }
        """
        app.setStyleSheet(style_sheet)
        self.setWindowIcon(QIcon('static/favicon.ico'))
        # Conectar la señal aboutToQuit de QApplication al método cleanup
        app.aboutToQuit.connect(self.cleanup)

    def run_flask_app(self):
        # Ejecutar la aplicación Flask en un hilo separado
        from threading import Thread
        flask_thread = Thread(target=lambda: self.flask_app.app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False))
        flask_thread.start()

    def cleanup(self):
        self.flask_app.stop_server()

if __name__ == '__main__':
    app = QApplication([])

    # Cambiar el nombre que se muestra en la barra de tareas de Mac
    app.setApplicationDisplayName("IALab_Suite")

    main_window = EmbeddedFlaskApp()
    main_window.run_flask_app()
    main_window.show()
    sys.exit(app.exec_())