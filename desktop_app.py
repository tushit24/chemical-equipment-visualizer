import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QMessageBox, QPushButton, QFileDialog, QHBoxLayout
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# -----------------------------
# API CONFIG
# -----------------------------
API_HISTORY_URL = "http://127.0.0.1:8000/api/history/"
API_UPLOAD_URL = "http://127.0.0.1:8000/api/upload/"
API_PDF_URL = "http://127.0.0.1:8000/api/pdf/"
TOKEN = "841f7b990a37ab1487ba5d003cdd9961c48c5078"


class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chemical Equipment Visualizer")
        self.resize(950, 720)

        main_layout = QVBoxLayout()

        # -----------------------------
        # HEADER
        # -----------------------------
        title = QLabel("Chemical Equipment Parameter Visualizer")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        main_layout.addWidget(title)

        subtitle = QLabel("Upload • Analyze • Visualize • Export")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray; margin-bottom: 15px;")
        main_layout.addWidget(subtitle)

        # -----------------------------
        # UPLOAD BUTTON
        # -----------------------------
        upload_btn = QPushButton("Upload CSV Dataset")
        upload_btn.setFixedWidth(200)
        upload_btn.clicked.connect(self.upload_csv)
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #2e7dff;
                color: white;
                padding: 8px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1c5fd4;
            }
        """)

        upload_layout = QHBoxLayout()
        upload_layout.addStretch()
        upload_layout.addWidget(upload_btn)
        upload_layout.addStretch()
        main_layout.addLayout(upload_layout)

        # -----------------------------
        # TABLE TITLE
        # -----------------------------
        table_title = QLabel("Uploaded Dataset History")
        table_title.setStyleSheet("font-size:14px; font-weight:bold; margin-top:15px;")
        main_layout.addWidget(table_title)

        # -----------------------------
        # TABLE
        # -----------------------------
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Filename", "Total", "Flowrate", "Pressure", "Temperature", "PDF"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.table)

        # -----------------------------
        # CHART TITLE
        # -----------------------------
        chart_title = QLabel("Equipment Type Distribution")
        chart_title.setStyleSheet("font-size:14px; font-weight:bold; margin-top:15px;")
        main_layout.addWidget(chart_title)

        # -----------------------------
        # CHART
        # -----------------------------
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)

        # Load initial data
        self.load_data()

    # -----------------------------
    # CSV UPLOAD
    # -----------------------------
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            headers = {"Authorization": f"Token {TOKEN}"}
            with open(file_path, "rb") as f:
                response = requests.post(
                    API_UPLOAD_URL,
                    headers=headers,
                    files={"file": f},
                )

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "CSV uploaded successfully")
                self.load_data()
            else:
                QMessageBox.warning(self, "Error", "CSV upload failed")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    def load_data(self):
        headers = {"Authorization": f"Token {TOKEN}"}
        response = requests.get(API_HISTORY_URL, headers=headers)

        if response.status_code != 200:
            QMessageBox.critical(self, "Error", "Failed to fetch dataset history")
            return

        data = response.json()
        if not data:
            return

        # Populate table
        self.table.setRowCount(len(data))

        for row, d in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(d["filename"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(d["total_equipment"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(d["average_flowrate"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(d["average_pressure"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(d["average_temperature"])))

            btn = QPushButton("⬇ Download PDF")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2ecc71;
                    color: white;
                    padding: 6px;
                    border-radius: 5px;
                }
            """)
            btn.clicked.connect(lambda _, id=d["id"]: self.download_pdf(id))
            self.table.setCellWidget(row, 5, btn)

        # Plot latest dataset
        self.plot_chart(data[0])

    # -----------------------------
    # PDF DOWNLOAD
    # -----------------------------
    def download_pdf(self, dataset_id):
        headers = {"Authorization": f"Token {TOKEN}"}
        response = requests.get(
            f"{API_PDF_URL}{dataset_id}/",
            headers=headers,
            stream=True
        )

        if response.status_code != 200:
            QMessageBox.warning(self, "Error", "PDF download failed")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", f"dataset_{dataset_id}_report.pdf", "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        QMessageBox.information(self, "Success", "PDF downloaded successfully")

    # -----------------------------
    # CHART PLOT (FIXED LABELS)
    # -----------------------------
    def plot_chart(self, dataset):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        types = dataset["type_distribution"]

        ax.bar(types.keys(), types.values(), color="#5DA9FF")
        ax.set_ylabel("Count")
        ax.set_title("Equipment Distribution")

        # ✅ FIX: prevent label cutoff
        ax.set_xticklabels(types.keys(), rotation=30, ha="right")
        self.figure.tight_layout()

        self.canvas.draw()


# -----------------------------
# APP START
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopApp()
    window.show()
    sys.exit(app.exec_())
