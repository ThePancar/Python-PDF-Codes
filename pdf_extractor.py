import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QWidget, QLineEdit
from PyPDF2 import PdfReader, PdfWriter

class PDFPageExtractor(QMainWindow):
    def __init__(self):
        super(PDFPageExtractor, self).__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Semih PDF Page Extractor')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)

        self.page_input = QLineEdit()
        self.page_input.setPlaceholderText("Enter page numbers to extract (e.g., 1, 3, 5)")
        self.layout.addWidget(self.page_input)  # Corrected "this" to "self"

        self.extract_button = QPushButton('Extract Pages')
        self.extract_button.clicked.connect(self.extract_pages)
        self.layout.addWidget(self.extract_button)

        self.open_file_button = QPushButton('Open PDF File')
        self.open_file_button.clicked.connect(self.open_file)
        self.layout.addWidget(self.open_file_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog(self, options=options)
        file_dialog.setNameFilter('PDF Files (*.pdf)')

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.text_edit.setPlainText(file_path)
            self.pdf_file_path = file_path

    def extract_pages(self):
        try:
            if hasattr(self, 'pdf_file_path'):
                pdf_file = open(self.pdf_file_path, 'rb')
                pdf_reader = PdfReader(pdf_file)

                # Get the user-input page numbers
                pages_to_extract = self.page_input.text().strip().split(',')
                pages_to_extract = [int(page.strip()) - 1 for page in pages_to_extract]

                pdf_writer = PdfWriter()

                for page_num in pages_to_extract:
                    pdf_writer.add_page(pdf_reader.pages[page_num])

                # Prompt the user to select a save path
                save_path, _ = QFileDialog.getSaveFileName(self, 'Save Extracted PDF', filter='PDF Files (*.pdf)')
                if save_path:
                    with open(save_path, 'wb') as output_pdf:
                        pdf_writer.write(output_pdf)
                    self.text_edit.setPlainText("Pages extracted and saved successfully!")
                else:
                    self.text_edit.setPlainText("Extraction canceled.")
            else:
                self.text_edit.setPlainText("Please select a PDF file first.")
        except Exception as e:
            self.text_edit.setPlainText("Error: " + str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFPageExtractor()
    window.show()
    sys.exit(app.exec_())