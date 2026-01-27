import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000/api/history/"
TOKEN = "841f7b990a37ab1487ba5d003cdd9961c48c5078"


class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.resize(800, 600)

        layout = QVBoxLayout()

        title = QLabel("Uploaded Dataset History")
        layout.addWidget(title)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        headers = {"Authorization": f"Token {TOKEN}"}
        response = requests.get(API_URL, headers=headers)

        if response.status_code != 200:
            QMessageBox.critical(self, "Error", "Failed to fetch data")
            return

        data = response.json()
        if not data:
            return

        latest = data[0]

        # Table
        self.table.setRowCount(1)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Filename", "Total", "Flowrate", "Pressure", "Temperature"]
        )

        self.table.setItem(0, 0, QTableWidgetItem(latest["filename"]))
        self.table.setItem(0, 1, QTableWidgetItem(str(latest["total_equipment"])))
        self.table.setItem(0, 2, QTableWidgetItem(str(latest["average_flowrate"])))
        self.table.setItem(0, 3, QTableWidgetItem(str(latest["average_pressure"])))
        self.table.setItem(0, 4, QTableWidgetItem(str(latest["average_temperature"])))

        # Chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        types = latest["type_distribution"]
        ax.bar(types.keys(), types.values())
        ax.set_title("Equipment Type Distribution")
        ax.set_ylabel("Count")

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopApp()
    window.show()
    sys.exit(app.exec_())
