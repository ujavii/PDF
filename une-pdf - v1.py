import sys
import PyPDF2
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, 
                             QListWidget, QMessageBox, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class AppPDFMerger(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Diseño vertical
        layout = QVBoxLayout()

        # Botón para agregar PDFs
        self.btnAdd = QPushButton('Agregar PDF', self)
        self.btnAdd.clicked.connect(self.addPDF)
        
        # Lista de archivos PDF agregados
        self.listWidget = QListWidget()
        self.listWidget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)  # Permitir múltiples selecciones
        self.listWidget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)     # Permitir reordenación
        
        # Botón para eliminar PDFs seleccionados de la lista
        self.btnDelete = QPushButton('Eliminar PDF seleccionado', self)
        self.btnDelete.clicked.connect(self.deleteSelectedPDF)

        # Botón para unir PDFs
        self.btnMerge = QPushButton('Unir PDFs', self)
        self.btnMerge.clicked.connect(self.mergePDFs)

        # Agregar widgets al layout
        layout.addWidget(self.btnAdd)
        layout.addWidget(self.listWidget)
        layout.addWidget(self.btnDelete)
        layout.addWidget(self.btnMerge)
        
        self.setLayout(layout)

        # Propiedades de la ventana
        self.setWindowTitle('Unir PDFs')
        self.setGeometry(100, 100, 400, 300)

    def addPDF(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccione PDFs", "", "PDF Files (*.pdf);;All Files (*)")
        if files:
            self.listWidget.addItems(files)

    def deleteSelectedPDF(self):
        # Eliminar los ítems seleccionados
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))

    def mergePDFs(self):
        if self.listWidget.count() == 0:
            QMessageBox.warning(self, 'Atención', 'Por favor, agregue al menos un archivo PDF.')
            return
        
        output_filename = self.getSaveFileName()
        if not output_filename:
            return

        if not self.combinePDFs(output_filename):
            return

        QMessageBox.information(self, 'Éxito', 'Los PDFs fueron unidos exitosamente.')

    def getSaveFileName(self):
        output_filename, _ = QFileDialog.getSaveFileName(self, "Guardar PDF unido", "", "PDF Files (*.pdf);;All Files (*)")
        if output_filename and not output_filename.endswith('.pdf'):
            output_filename += '.pdf'
        return output_filename

    def combinePDFs(self, output_filename):
        pdf_merger = PyPDF2.PdfMerger()
        for index in range(self.listWidget.count()):
            try:
                pdf_merger.append(self.listWidget.item(index).text())
            except PyPDF2.errors.PdfReadError:
                QMessageBox.warning(self, 'Error', f'Hubo un problema con el archivo {self.listWidget.item(index).text()}. Podría estar corrupto o ser inválido.')
                return False
        pdf_merger.write(output_filename)
        pdf_merger.close()
        return True

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Establecer el ícono de la aplicación y, por ende, de la ventana
    app.setWindowIcon(QIcon('C:/Users/JAVIER/Downloads/pdf_merge.ico'))

    ex = AppPDFMerger()
    ex.show()
    sys.exit(app.exec())

