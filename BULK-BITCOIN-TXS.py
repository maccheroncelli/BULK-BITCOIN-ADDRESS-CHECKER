import sys
import requests
import csv
import re
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

class BitcoinAddressChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.selectedFileName = ""

    def initUI(self):
        self.setWindowTitle('Bitcoin Address Checker')
        self.setGeometry(100, 100, 1500, 1000)  # Set window width to 2370 pixels

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.openFileButton = QPushButton('Select File')
        self.openFileButton.clicked.connect(self.openFileNameDialog)
        self.layout.addWidget(self.openFileButton)

        self.submitButton = QPushButton('Submit Addresses')
        self.submitButton.clicked.connect(self.submitAddresses)
        self.layout.addWidget(self.submitButton)

        self.exportButton = QPushButton('Export Results')
        self.exportButton.clicked.connect(self.exportResults)
        self.layout.addWidget(self.exportButton)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['Address', 'n_tx', 'total_received', 'total_sent', 'final_balance'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSortingEnabled(False)  # Disable column header sorting
        self.layout.addWidget(self.tableWidget)

        self.addresses = []

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select File with Bitcoin Addresses", "", "Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            self.selectedFileName = fileName
            with open(fileName, 'r') as file:
                self.addresses = []
                line_num = 1
                for line in file:
                    address = line.strip()
                    if self.isValidBTCAddress(address):
                        self.addresses.append(address)
                    else:
                        print(f"Invalid BTC address on line {line_num}: {address}")
                    line_num += 1
                self.openFileButton.setText(f"'{fileName.split('/')[-1]}' has been selected. Submit to continue or reselect...")
                self.updateStatus(f"Loaded {len(self.addresses)} addresses.")

    def isValidBTCAddress(self, address):
        btc_pattern = r'^(1|3)[a-km-zA-HJ-NP-Z1-9]{25,34}$|^(bc1)[0-9a-z]{39,59}$'
        return re.match(btc_pattern, address) is not None

    def submitAddresses(self):
        if not self.addresses:
            self.updateStatus("No addresses loaded.")
            return

        self.submitButton.setText('API Query in process, please be patient...')
        QApplication.processEvents()

        self.tableWidget.setRowCount(0)
        all_data = []

        for i in range(0, len(self.addresses), 50):
            batch = self.addresses[i:i+50]
            addresses_str = '|'.join(batch)
            response = requests.get(f"https://blockchain.info/multiaddr?active={addresses_str}")
            if response.status_code == 200:
                data = response.json()['addresses']
                all_data.extend(data)
            else:
                print(f"Status Code: {response.status_code}, Response: {response.text}")
                self.updateStatus(f"Failed to fetch data for addresses {i+1} to {i+len(batch)}")
            
            time.sleep(1)  # Delay to avoid hitting API rate limits

        # Sort data by 'n_tx' as integers before populating table
        sorted_data = sorted(all_data, key=lambda x: x['n_tx'], reverse=True)
        for address in sorted_data:
            self.populateTable(address)

        self.submitButton.setText('Submit Addresses')

    def populateTable(self, address):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        
        # Center the address
        self.setCenteredItem(rowPosition, 0, address['address'])
        
        # Center the 'n_tx' value
        self.setCenteredItem(rowPosition, 1, str(address['n_tx']))
        
        total_received_btc = address['total_received'] / 100000000
        total_sent_btc = address['total_sent'] / 100000000
        final_balance_btc = address['final_balance'] / 100000000
        
        # Center the BTC values
        self.setCenteredItem(rowPosition, 2, f"{total_received_btc:.8f} BTC")
        self.setCenteredItem(rowPosition, 3, f"{total_sent_btc:.8f} BTC")
        self.setCenteredItem(rowPosition, 4, f"{final_balance_btc:.8f} BTC")

    def setCenteredItem(self, row, column, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tableWidget.setItem(row, column, item)

    def exportResults(self):
        options = QFileDialog.Options()
        # Generate the default filename based on the selected file name
        if self.selectedFileName:
            defaultFileName = self.selectedFileName.rsplit('/', 1)[-1].rsplit('.', 1)[0] + " processed.csv"
        else:
            defaultFileName = "export.csv"
        
        fileName, _ = QFileDialog.getSaveFileName(self, "Export Results to CSV", defaultFileName, "CSV Files (*.csv);;All Files (*)", options=options)
        if fileName:
            with open(fileName, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Address', 'n_tx', 'total_received', 'total_sent', 'final_balance'])
                for row in range(self.tableWidget.rowCount()):
                    row_data = []
                    for column in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(row, column)
                        if item is not None:
                            row_data.append(item.text().replace(" BTC", ""))
                        else:
                            row_data.append('')
                    writer.writerow(row_data)
            self.updateStatus(f"Exported results to {fileName}")

    def updateStatus(self, message):
        print(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BitcoinAddressChecker()
    ex.show()
    sys.exit(app.exec_())
