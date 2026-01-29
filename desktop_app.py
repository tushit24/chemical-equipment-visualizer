import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QMessageBox, QPushButton, QFileDialog,
    QHBoxLayout, QComboBox, QStatusBar
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# -------------------- CONFIG --------------------
API_HISTORY_URL = "http://127.0.0.1:8000/api/history/"
API_UPLOAD_URL = "http://127.0.0.1:8000/api/upload/"
API_PDF_URL = "http://127.0.0.1:8000/api/pdf/"
TOKEN = "841f7b990a37ab1487ba5d003cdd9961c48c5078"

HEADERS = {"Authorization": f"Token {TOKEN}"}

# -------------------- MAIN APP --------------------
class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.resize(1000, 720)

        self.dark_mode = False
        self.datasets = []

        self.init_ui()
        self.load_data()

    # -------------------- UI --------------------
    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Chemical Equipment Parameter Visualizer")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        subtitle = QLabel("Upload • Analyze • Visualize • Export")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray;")
        layout.addWidget(subtitle)

        # Buttons Row
        btn_row = QHBoxLayout()

        upload_btn = QPushButton("Upload CSV Dataset")
        upload_btn.clicked.connect(self.upload_csv)

        self.dark_btn = QPushButton("🌙 Dark Mode")
        self.dark_btn.clicked.connect(self.toggle_dark_mode)

        export_btn = QPushButton("Export Chart as Image")
        export_btn.clicked.connect(self.export_chart)

        btn_row.addWidget(upload_btn)
        btn_row.addWidget(export_btn)
        btn_row.addWidget(self.dark_btn)

        layout.addLayout(btn_row)

        # Dataset selector
        self.dataset_selector = QComboBox()
        self.dataset_selector.currentIndexChanged.connect(self.update_chart_from_dropdown)
        layout.addWidget(self.dataset_selector)

        # Table
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Chart
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Status bar
        self.status = QStatusBar()
        self.status.showMessage("🔌 Connecting to API...")
        layout.addWidget(self.status)

        self.setLayout(layout)

    # -------------------- DATA --------------------
    def load_data(self):
        try:
            self.status.showMessage("📡 Fetching datasets...")
            res = requests.get(API_HISTORY_URL, headers=HEADERS)

            if res.status_code != 200:
                raise Exception("API error")

            self.datasets = res.json()
            self.populate_table()
            self.populate_dropdown()
            self.plot_chart(self.datasets[0] if self.datasets else None)

            self.status.showMessage("✅ API connected")

        except Exception as e:
            self.status.showMessage("❌ API connection failed")
            QMessageBox.critical(self, "Error", str(e))

    # -------------------- TABLE --------------------
    def populate_table(self):
        self.table.setRowCount(len(self.datasets))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Filename", "Total", "Flowrate", "Pressure", "Temperature", "PDF"
        ])

        for row, d in enumerate(self.datasets):
            self.table.setItem(row, 0, QTableWidgetItem(d["filename"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(d["total_equipment"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(d["average_flowrate"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(d["average_pressure"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(d["average_temperature"])))

            btn = QPushButton("Download PDF")
            btn.clicked.connect(lambda _, did=d["id"]: self.download_pdf(did))
            self.table.setCellWidget(row, 5, btn)

        self.table.resizeColumnsToContents()

    # -------------------- DROPDOWN --------------------
    def populate_dropdown(self):
        self.dataset_selector.clear()
        for d in self.datasets:
            self.dataset_selector.addItem(
                f'{d["filename"]} ({d["uploaded_at"]})', d
            )

    def update_chart_from_dropdown(self):
        dataset = self.dataset_selector.currentData()
        if dataset:
            self.plot_chart(dataset)

    # -------------------- CHART --------------------
    def plot_chart(self, dataset):
        if not dataset:
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        types = dataset["type_distribution"]
        labels = list(types.keys())
        values = list(types.values())

        ax.bar(range(len(labels)), values, color="#5DA9FF")
        ax.set_ylabel("Count")
        ax.set_title("Equipment Type Distribution")

        # ✅ Correct tick handling (NO warnings)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=30, ha="right")

        self.figure.tight_layout()
        self.canvas.draw()

    # -------------------- CSV UPLOAD --------------------
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return

        try:
            self.status.showMessage("⬆ Uploading CSV...")
            with open(file_path, "rb") as f:
                res = requests.post(API_UPLOAD_URL, files={"file": f}, headers=HEADERS)

            if res.status_code == 200:
                QMessageBox.information(self, "Success", "CSV uploaded successfully")
                self.load_data()
            else:
                raise Exception("Upload failed")

        except Exception as e:
            self.status.showMessage("❌ Upload failed")
            QMessageBox.critical(self, "Error", str(e))

    # -------------------- PDF --------------------
    def download_pdf(self, dataset_id):
        try:
            self.status.showMessage("⬇ Downloading PDF...")
            res = requests.get(f"{API_PDF_URL}{dataset_id}/", headers=HEADERS)

            if res.status_code != 200:
                raise Exception("PDF download failed")

            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save PDF", f"dataset_{dataset_id}.pdf", "PDF Files (*.pdf)"
            )

            if file_path:
                with open(file_path, "wb") as f:
                    f.write(res.content)

                QMessageBox.information(self, "Success", "PDF downloaded successfully")
                self.status.showMessage("✅ PDF downloaded")

        except Exception as e:
            self.status.showMessage("❌ PDF download failed")
            QMessageBox.critical(self, "Error", str(e))

    # -------------------- EXPORT CHART --------------------
    def export_chart(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Chart Image", "chart.png", "PNG Files (*.png)"
        )
        if file_path:
            self.figure.savefig(file_path)
            QMessageBox.information(self, "Success", "Chart exported as image")

    # -------------------- DARK MODE --------------------
    def toggle_dark_mode(self):
        if not self.dark_mode:
            self.setStyleSheet("""
                QWidget { background-color: #121212; color: white; }
                QPushButton { background-color: #1f6feb; color: white; padding: 6px; }
                QTableWidget { background-color: #1e1e1e; }
            """)
            self.dark_btn.setText("☀ Light Mode")
        else:
            self.setStyleSheet("")
            self.dark_btn.setText("🌙 Dark Mode")

        self.dark_mode = not self.dark_mode


# -------------------- RUN --------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopApp()
    window.show()
    sys.exit(app.exec_())
