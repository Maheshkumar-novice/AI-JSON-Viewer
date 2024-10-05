import sys
import os
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QComboBox, QTextEdit, QFileDialog, QLabel)
from PyQt6.QtGui import QColor, QTextCharFormat, QSyntaxHighlighter
from PyQt6.QtCore import QRegularExpression

class JsonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#CC7832"))
        keywords = ["true", "false", "null"]
        for word in keywords:
            pattern = QRegularExpression(r'\b' + word + r'\b')
            self.highlighting_rules.append((pattern, keyword_format))

        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#6897BB"))
        self.highlighting_rules.append((QRegularExpression(r'\b[0-9]+\b'), number_format))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#6A8759"))
        self.highlighting_rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            matches = pattern.globalMatch(text)
            while matches.hasNext():
                match = matches.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class JsonViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON Viewer")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.folder_button = QPushButton("Select Folder")
        self.folder_button.clicked.connect(self.select_folder)
        layout.addWidget(self.folder_button)

        self.folder_label = QLabel("No folder selected")
        layout.addWidget(self.folder_label)

        self.file_combo = QComboBox()
        self.file_combo.currentIndexChanged.connect(self.load_json)
        layout.addWidget(self.file_combo)

        self.json_view = QTextEdit()
        self.json_view.setReadOnly(True)
        layout.addWidget(self.json_view)

        self.highlighter = JsonHighlighter(self.json_view.document())

        self.current_folder = ""

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.current_folder = folder
            self.folder_label.setText(f"Selected folder: {folder}")
            self.update_file_list()

    def update_file_list(self):
        self.file_combo.clear()
        json_files = [f for f in os.listdir(self.current_folder) if f.endswith('.json')]
        self.file_combo.addItems(json_files)

    def load_json(self, index):
        if index >= 0:
            file_name = self.file_combo.currentText()
            file_path = os.path.join(self.current_folder, file_name)
            try:
                with open(file_path, 'r') as f:
                    json_content = json.load(f)
                    formatted_json = json.dumps(json_content, indent=2)
                    self.json_view.setPlainText(formatted_json)
            except Exception as e:
                self.json_view.setPlainText(f"Error loading JSON: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = JsonViewer()
    viewer.show()
    sys.exit(app.exec())
