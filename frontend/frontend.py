# frontend.py
import sys
import requests
import json
import socket
import time
from datetime import datetime

# ==================== FRONTEND CONFIG ====================
RUST_IP = "192.168.100.161"
RUST_PORT = 8080

# ==================== ARDUINO DIRECT CONTROL ====================
ARDUINO_IP = "192.168.1.122"
ARDUINO_PORT = 8082

# ==================== EDGE IMPULSE CONFIG ====================
EI_API_KEY = "ei_bf401cc81aec83ef5d47055abbb90a596ad1d26f1c5f4306"
EI_PROJECT_ID = "819619"
EI_HMAC_KEY = "5ac940e46d7acb60201701a7f6d3dff3"
EI_DEVICE_ID = "enosev1"

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QTimer
import pyqtgraph as pg

class EdgeImpulseIntegration:
    # ✅ PERBAIKAN 3: Hanya ada satu __init__
    def __init__(self):
        self.api_key = EI_API_KEY
        self.project_id = EI_PROJECT_ID
        
        # Endpoint ingestion yang benar (menggunakan Device ID)
        self.correct_endpoint = f"https://ingestion.edgeimpulse.com/v1/devices/{EI_DEVICE_ID}/data"

        # List endpoint palsu (dipertahankan sesuai struktur kode asli)
        self.endpoints = [
            f"https://ingestion.edgeimpulse.com/api/{self.project_id}/device-data",
            f"https://ingestion.edgeimpulse.com/api/{self.project_id}/training",
            f"https://ingestion.edgeimpulse.com/api/{self.project_id}/raw",
            f"https://ingestion.edgeimpulse.com/api/{self.project_id}/data",
            f"https://ingestion.edgeimpulse.com/api/{self.project_id}/sensors"
        ]
        
    def send_sensor_data(self, sensor_values):
        """✅ PERBAIKAN 4: Menyederhanakan logika — cukup panggil sekali ke endpoint yang benar."""
        return self._try_endpoint(self.correct_endpoint, sensor_values)

    def _try_endpoint(self, endpoint, sensor_values):
        """Metode ini sekarang menerima endpoint yang benar secara langsung."""
        try:
            real_endpoint = endpoint # real_endpoint sekarang sama dengan endpoint (self.correct_endpoint)

            payload = {
                "protected": {
                    "ver": "v1",
                    "alg": "none",
                    "iat": int(time.time())
                },
                "signature": "0",
                "payload": {
                    "device_type": "ENose",
                    "device_name": "e-nose-arduino-01",
                    "interval_ms": 1000,
                    "sensors": [
                        "GMXXX_NO2", "GMXXX_Ethanol", "GMXXX_VOC", "GMXXX_CO",
                        "MiCS5524_CO", "MiCS5524_Ethanol", "MiCS5524_VOC"
                    ],
                    # ✅ PERBAIKAN 5: Hapus kurung siku ganda pada values
                    "values": sensor_values 
                }
            }

            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "x-file-name": "enose.json"
            }

            # Debug prints
            print(f"➡️  Sending to real endpoint: {real_endpoint}")
            
            try:
                response = requests.post(
                    real_endpoint,
                    json=payload,
                    headers=headers,
                    timeout=10
                )
            except requests.exceptions.RequestException as re:
                print(f"❌ requests exception when posting to {real_endpoint}: {re}")
                return False

            print(f"Response: {response.status_code} - {response.text}")

            if response.status_code in [200, 201]:
                print(f"✅ SUCCESS sending data.")
                return True
            else:
                print(f"❌ Failed with status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error during Edge Impulse API call: {e}")
            return False

# =====================================================

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("E-NOSE Monitor - Direct Arduino Control + Edge Impulse")
        self.resize(1400, 900)
        
        # === DARK THEME STYLE (HANYA STYLE, TIDAK MENGUBAH LOGIKA) ===
        self.setStyleSheet("""
            QMainWindow { background-color: #0f172a; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #1e293b;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: #0b1220;
                color: #e2e8f0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #f8fafc;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton {
                background-color: #3b82f6;
                border: none;
                color: white;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: bold;
                margin: 2px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #2563eb; }
            QPushButton:pressed { background-color: #1d4ed8; }
            QPushButton:disabled { background-color: #475569; color: #94a3b8; }
            QLineEdit {
                padding: 6px;
                border: 1px solid #334155;
                border-radius: 4px;
                background-color: #071026;
                color: #e2e8f0;
            }
            QLabel { color: #e2e8f0; font-size: 11px; }
            QToolTip { color: #e2e8f0; background-color: #111827; border: 1px solid #374151; }
        """)
        
        # Central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Header
        header_layout = QtWidgets.QHBoxLayout()
        title_label = QtWidgets.QLabel("E-NOSE Monitor - Direct Arduino Control + Edge Impulse")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e6eef8;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        self.connection_status = QtWidgets.QLabel("🔴 Disconnected")
        self.connection_status.setStyleSheet("font-weight: bold; padding: 4px 8px; background-color: #7f1d1d; border-radius: 4px; color: #fff;")
        header_layout.addWidget(self.connection_status)
        layout.addLayout(header_layout)

        # Controls Section
        controls_layout = QtWidgets.QHBoxLayout()

        # Backend Configuration
        config_group = QtWidgets.QGroupBox("Backend Configuration")
        config_layout = QtWidgets.QFormLayout(config_group)
        self.backend_ip = QtWidgets.QLineEdit(RUST_IP)
        self.backend_port = QtWidgets.QLineEdit(str(RUST_PORT))
        config_layout.addRow("Rust IP:", self.backend_ip)
        config_layout.addRow("Rust Port:", self.backend_port)
        self.btn_test = QtWidgets.QPushButton("Test Connection")
        self.btn_test.clicked.connect(self.test_connection)
        config_layout.addRow("", self.btn_test)
        controls_layout.addWidget(config_group)

        # Control Buttons
        button_group = QtWidgets.QGroupBox("Monitoring Control")
        button_layout = QtWidgets.QGridLayout(button_group)
        
        self.btn_start = QtWidgets.QPushButton("📡 START MONITOR")
        self.btn_stop = QtWidgets.QPushButton("⏹ STOP MONITOR") 
        self.btn_status = QtWidgets.QPushButton("📊 GET STATUS")
        self.btn_export = QtWidgets.QPushButton("💾 EXPORT CSV")
        
        self.btn_start.setStyleSheet("background-color: #10b981;")
        self.btn_stop.setStyleSheet("background-color: #ef4444;")
        self.btn_status.setStyleSheet("background-color: #3b82f6;")
        self.btn_export.setStyleSheet("background-color: #f59e0b;")
        
        self.btn_start.clicked.connect(self.start_monitoring)
        self.btn_stop.clicked.connect(self.stop_monitoring)
        self.btn_status.clicked.connect(self.get_status)
        self.btn_export.clicked.connect(self.export_csv)
        
        button_layout.addWidget(self.btn_start, 0, 0)
        button_layout.addWidget(self.btn_stop, 0, 1)
        button_layout.addWidget(self.btn_status, 1, 0)
        button_layout.addWidget(self.btn_export, 1, 1)
        controls_layout.addWidget(button_group)

        # ✅ Sampling Control Section
        sampling_group = QtWidgets.QGroupBox("Sampling Control - DIRECT to Arduino")
        sampling_layout = QtWidgets.QGridLayout(sampling_group)
        
        self.btn_start_sampling = QtWidgets.QPushButton("START")
        self.btn_stop_sampling = QtWidgets.QPushButton("STOP")
        self.sampling_status = QtWidgets.QLabel("Status: IDLE")
        self.actuator_status = QtWidgets.QLabel("Actuator: -")
        
        self.btn_start_sampling.setStyleSheet("background-color: #10b981; font-weight: bold;")
        self.btn_stop_sampling.setStyleSheet("background-color: #ef4444; font-weight: bold;")
        self.sampling_status.setStyleSheet("padding: 4px; background-color: #071026; border-radius: 3px; font-weight: bold; color: #c7f0e1;")
        self.actuator_status.setStyleSheet("padding: 4px; background-color: #071026; border-radius: 3px; font-weight: bold; color: #c7f0e1;")
        
        self.btn_start_sampling.clicked.connect(self.start_sampling_direct)
        self.btn_stop_sampling.clicked.connect(self.stop_sampling_direct)
        
        sampling_layout.addWidget(self.btn_start_sampling, 0, 0)
        sampling_layout.addWidget(self.btn_stop_sampling, 0, 1)
        sampling_layout.addWidget(self.sampling_status, 1, 0)
        sampling_layout.addWidget(self.actuator_status, 1, 1)
        controls_layout.addWidget(sampling_group)

        # ✅ Edge Impulse Section
        ei_group = QtWidgets.QGroupBox("Edge Impulse Integration")
        ei_layout = QtWidgets.QGridLayout(ei_group)
        
        self.btn_enable_ei = QtWidgets.QPushButton("Enable EI")
        self.btn_disable_ei = QtWidgets.QPushButton("Disable EI")
        self.btn_test_ei = QtWidgets.QPushButton("🧪 Test EI")
        self.ei_status = QtWidgets.QLabel("Status: DISABLED")
        self.ei_count = QtWidgets.QLabel("Data Sent: 0")
        
        self.btn_enable_ei.setStyleSheet("background-color: #10b981;")
        self.btn_disable_ei.setStyleSheet("background-color: #ef4444;")
        self.btn_test_ei.setStyleSheet("background-color: #8b5cf6;")
        self.ei_status.setStyleSheet("padding: 4px; background-color: #071026; border-radius: 3px; color: #c7f0e1;")
        self.ei_count.setStyleSheet("padding: 4px; background-color: #071026; border-radius: 3px; color: #c7f0e1;")
        
        self.btn_enable_ei.clicked.connect(self.enable_edge_impulse)
        self.btn_disable_ei.clicked.connect(self.disable_edge_impulse)
        self.btn_test_ei.clicked.connect(self.test_edge_impulse_manual)
        
        ei_layout.addWidget(self.btn_enable_ei, 0, 0)
        ei_layout.addWidget(self.btn_disable_ei, 0, 1)
        ei_layout.addWidget(self.btn_test_ei, 0, 2)
        ei_layout.addWidget(self.ei_status, 1, 0)
        ei_layout.addWidget(self.ei_count, 1, 1)
        controls_layout.addWidget(ei_group)

        # System Status
        status_group = QtWidgets.QGroupBox("System Status")
        status_layout = QtWidgets.QGridLayout(status_group)
        self.state_label = QtWidgets.QLabel("State: IDLE")
        self.level_label = QtWidgets.QLabel("Level: 0")
        self.data_count_label = QtWidgets.QLabel("Data Points: 0")
        self.session_label = QtWidgets.QLabel("Session: None")
        
        status_labels = [self.state_label, self.level_label, self.data_count_label, self.session_label]
        for label in status_labels:
            label.setStyleSheet("padding: 4px; background-color: #071026; border-radius: 3px; color: #c7f0e1;")
        
        status_layout.addWidget(self.state_label, 0, 0)
        status_layout.addWidget(self.level_label, 0, 1)
        status_layout.addWidget(self.data_count_label, 1, 0)
        status_layout.addWidget(self.session_label, 1, 1)
        controls_layout.addWidget(status_group)
        layout.addLayout(controls_layout)

        # Sensor Values Display
        values_layout = QtWidgets.QHBoxLayout()

        # GM-XXX Sensors
        gm_group = QtWidgets.QGroupBox("GM-XXX Sensors")
        gm_layout = QtWidgets.QFormLayout(gm_group)
        self.no2_label = QtWidgets.QLabel("0.000")
        self.eth_gm_label = QtWidgets.QLabel("0.000")
        self.voc_gm_label = QtWidgets.QLabel("0.000")
        self.co_gm_label = QtWidgets.QLabel("0.000")
        gm_layout.addRow("NO₂ (ppm):", self.no2_label)
        gm_layout.addRow("Ethanol (ppm):", self.eth_gm_label)
        gm_layout.addRow("VOC (ppm):", self.voc_gm_label)
        gm_layout.addRow("CO (ppm):", self.co_gm_label)
        values_layout.addWidget(gm_group)

        # MiCS-5524 Sensors
        mics_group = QtWidgets.QGroupBox("MiCS-5524 Sensors")
        mics_layout = QtWidgets.QFormLayout(mics_group)
        self.co_mics_label = QtWidgets.QLabel("0.000")
        self.eth_mics_label = QtWidgets.QLabel("0.000")
        self.voc_mics_label = QtWidgets.QLabel("0.000")
        mics_layout.addRow("CO (ppm):", self.co_mics_label)
        mics_layout.addRow("Ethanol (ppm):", self.eth_mics_label)
        mics_layout.addRow("VOC (ppm):", self.voc_mics_label)
        values_layout.addWidget(mics_group)

        # Timing Info
        time_group = QtWidgets.QGroupBox("Timing Information")
        time_layout = QtWidgets.QVBoxLayout(time_group)
        self.elapsed_label = QtWidgets.QLabel("Elapsed: 00:00")
        self.step_label = QtWidgets.QLabel("Current Step: -")
        self.progress_label = QtWidgets.QLabel("Progress: 0%")
        
        time_labels = [self.elapsed_label, self.step_label, self.progress_label]
        for label in time_labels:
            label.setStyleSheet("padding: 4px; background-color: #071026; border-radius: 3px; color: #c7f0e1;")
        
        time_layout.addWidget(self.elapsed_label)
        time_layout.addWidget(self.step_label)
        time_layout.addWidget(self.progress_label)
        values_layout.addWidget(time_group)
        layout.addLayout(values_layout)

        # Plot Area
        plot_group = QtWidgets.QGroupBox("Real-time Sensor Data")
        plot_layout = QtWidgets.QVBoxLayout(plot_group)
        self.combined_plot = pg.PlotWidget()
        # background dark to match theme
        self.combined_plot.setBackground('#0f172a')
        self.combined_plot.addLegend(offset=(10, 10))
        self.combined_plot.setLabel('left', 'Concentration (ppm)', color='#e2e8f0')
        self.combined_plot.setLabel('bottom', 'Time (samples)', color='#e2e8f0')
        self.combined_plot.showGrid(x=True, y=True, alpha=0.3)
        
        # Create plots for all 7 sensors (pens unchanged — visual only)
        self.curve_no2 = self.combined_plot.plot(pen=pg.mkPen('#ef4444', width=2), name="NO₂ GM")
        self.curve_eth_gm = self.combined_plot.plot(pen=pg.mkPen('#10b981', width=2), name="Ethanol GM")
        self.curve_voc_gm = self.combined_plot.plot(pen=pg.mkPen('#3b82f6', width=2), name="VOC GM")
        self.curve_co_gm = self.combined_plot.plot(pen=pg.mkPen('#f59e0b', width=2), name="CO GM")
        self.curve_co_mics = self.combined_plot.plot(pen=pg.mkPen('#8b5cf6', width=2), name="CO MiCS")
        self.curve_eth_mics = self.combined_plot.plot(pen=pg.mkPen('#ec4899', width=2), name="Ethanol MiCS")
        self.curve_voc_mics = self.combined_plot.plot(pen=pg.mkPen('#06b6d4', width=2), name="VOC MiCS")
        
        plot_layout.addWidget(self.combined_plot)
        layout.addWidget(plot_group)

        # Data buffers
        self.timestamps = []
        self.no2_data = []
        self.eth_gm_data = []
        self.voc_gm_data = []
        self.co_gm_data = []
        self.co_mics_data = []
        self.eth_mics_data = []
        self.voc_mics_data = []
        
        self.data_count = 0
        self.max_data_points = 500
        self.monitoring_active = False
        
        # Timer for periodic updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.poll_sensor_data)
        
        self.elapsed_timer = QTimer()
        self.elapsed_timer.timeout.connect(self.update_elapsed_time)
        self.elapsed_time = 0

        # ✅ BARU: Arduino Direct Control
        self.arduino_socket = None

        # ✅ BARU: Edge Impulse Integration
        self.edge_impulse = EdgeImpulseIntegration()
        self.ei_enabled = False
        self.ei_data_count = 0

        # Test connection on startup
        QtCore.QTimer.singleShot(1000, self.test_connection)

    def get_backend_url(self, endpoint=""):
        """Get backend URL for HTTP requests"""
        # .strip() di sini membantu membersihkan input dari QLineEdit
        ip = self.backend_ip.text().strip() or RUST_IP 
        port = self.backend_port.text().strip() or str(RUST_PORT)
        return f"http://{ip}:{port}{endpoint}"

    def test_connection(self):
        """Test connection to Rust backend via HTTP"""
        try:
            response = requests.get(self.get_backend_url("/api/status"), timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.connection_status.setText("🟢 Connected")
                self.connection_status.setStyleSheet("font-weight: bold; padding: 4px 8px; background-color: #065f46; border-radius: 4px; color: #e2f7ef;")
                self.update_status_display(data)
                QtWidgets.QMessageBox.information(self, "Success", "Connected to Rust backend via HTTP API!")
                return True
        except Exception as e:
            print(f"Connection test failed: {e}")
        
        self.connection_status.setText("🔴 Disconnected")
        self.connection_status.setStyleSheet("font-weight: bold; padding: 4px 8px; background-color: #7f1d1d; border-radius: 4px; color: #fff;")
        QtWidgets.QMessageBox.warning(self, "Connection Failed", 
            f"Cannot connect to Rust backend!\n"
            f"URL: {self.get_backend_url('/api/status')}\n"
            f"Error: {str(e)}")
        return False

    def start_monitoring(self):
        """Start monitoring data from Rust backend"""
        self.monitoring_active = True
        self.update_timer.start(1000)  # Poll every 1 second
        self.elapsed_time = 0
        self.elapsed_timer.start(1000)
        QtWidgets.QMessageBox.information(self, "Monitoring Started", 
            "Now monitoring data from Rust backend\n"
            "Arduino should be started separately via Serial")

    def stop_monitoring(self):
        """Stop monitoring data"""
        self.monitoring_active = False
        self.update_timer.stop()
        self.elapsed_timer.stop()
        QtWidgets.QMessageBox.information(self, "Monitoring Stopped", "Stopped monitoring data")

    def get_status(self):
        """Get status from Rust backend"""
        try:
            response = requests.get(self.get_backend_url("/api/status"), timeout=5)
            if response.status_code == 200:
                data = response.json()
                status_text = f"""Backend Status:
Arduino Connected: {data.get('arduino_connected', False)}
Current Level: {data.get('current_level', 0)}
Current State: {data.get('current_state', 0)}
Data Points: {data.get('data_points', 0)}"""
                QtWidgets.QMessageBox.information(self, "Status", status_text)
                self.update_status_display(data)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to get status:\n{str(e)}")

    def export_csv(self):
        """Export CSV from Rust backend"""
        try:
            response = requests.get(self.get_backend_url("/api/csv"), timeout=10)
            if response.status_code == 200:
                filename = f"enose_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                with open(filename, 'w', newline='') as f:
                    f.write(response.text)
                QtWidgets.QMessageBox.information(self, "Exported", f"Data exported to {filename}")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to export data:\n{str(e)}")

    # ✅ DIRECT ARDUINO CONTROL METHODS
    def send_direct_to_arduino(self, command):
        """Kirim command langsung ke Arduino via TCP"""
        try:
            if self.arduino_socket is None:
                self.arduino_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.arduino_socket.settimeout(5)
                # KONEKSI KE IP DAN PORT ARDUINO
                self.arduino_socket.connect((ARDUINO_IP, ARDUINO_PORT))
                print(f"✅ Connected to Arduino {ARDUINO_IP}:{ARDUINO_PORT}")
            
            self.arduino_socket.sendall(f"{command}\n".encode())
            print(f"✅ Direct to Arduino: {command}")
            return True
            
        except Exception as e:
            print(f"❌ Direct Arduino failed: {e}")
            self.arduino_socket = None
            QtWidgets.QMessageBox.warning(self, "Direct Control Error", 
                f"Failed to send command to Arduino:\n{str(e)}")
            return False

    def start_sampling_direct(self):
        """Start sampling langsung ke Arduino"""
        if self.send_direct_to_arduino("START_SAMPLING"):
            self.sampling_status.setText("Status: RUNNING")
            self.sampling_status.setStyleSheet("padding: 4px; background-color: #065f46; border-radius: 3px; font-weight: bold; color: #e6fff3;")
            QtWidgets.QMessageBox.information(self, "Direct Control", 
                "Sampling started via DIRECT Arduino connection!\n"
                "• Kipas 2 menit → Pompa 4 menit → Repeat\n"
                "• Sensor data tetap dikirim ke Rust untuk monitoring")

    def stop_sampling_direct(self):
        """Stop sampling langsung ke Arduino"""
        if self.send_direct_to_arduino("STOP_SAMPLING"):
            self.sampling_status.setText("Status: STOPPED")
            self.sampling_status.setStyleSheet("padding: 4px; background-color: #7f1d1d; border-radius: 3px; font-weight: bold; color: #fff;")
            self.actuator_status.setText("Actuator: -")

    # ✅ EDGE IMPULSE METHODS
    def enable_edge_impulse(self):
        """Enable Edge Impulse integration"""
        self.ei_enabled = True
        self.ei_status.setText("Status: ENABLED")
        self.ei_status.setStyleSheet("padding: 4px; background-color: #065f46; border-radius: 3px; color: #e6fff3;")
        QtWidgets.QMessageBox.information(self, "Edge Impulse", 
            "Edge Impulse integration ENABLED!\n"
            "Sensor data will be sent to Edge Impulse for training.")

    def disable_edge_impulse(self):
        """Disable Edge Impulse integration"""
        self.ei_enabled = False
        self.ei_status.setText("Status: DISABLED")
        self.ei_status.setStyleSheet("padding: 4px; background-color: #7f1d1d; border-radius: 3px; color: #fff;")

    def test_edge_impulse_manual(self):
        """Test manual Edge Impulse integration"""
        try:
            print("🧪 TESTING EDGE IMPULSE MANUALLY...")
            
            # Sample data (7 nilai)
            test_values = [1.23, 4.56, 7.89, 1.23, 4.56, 7.89, 1.23]
            success = self.edge_impulse.send_sensor_data(test_values)
            
            if success:
                QtWidgets.QMessageBox.information(self, "Test Success", 
                    "✅ Edge Impulse integration WORKING!\nData successfully sent.")
            else:
                QtWidgets.QMessageBox.warning(self, "Test Failed", 
                    "❌ Edge Impulse integration FAILED.\nCheck console for error details.")
                    
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Test Error", 
                f"🚨 Manual test error: {str(e)}")

    def send_to_edge_impulse(self, sensor_data):
        """Kirim data ke Edge Impulse jika enabled"""
        if not self.ei_enabled:
            return
            
        try:
            # Extract 7 sensor values dalam urutan yang benar (sesuai payload di EdgeImpulseIntegration)
            sensor_values = [
                float(sensor_data.get('no2', 0)),
                float(sensor_data.get('eth_gm', 0)),  
                float(sensor_data.get('voc_gm', 0)),
                float(sensor_data.get('co_gm', 0)),
                float(sensor_data.get('co_m', 0)),
                float(sensor_data.get('eth_m', 0)),
                float(sensor_data.get('voc_m', 0))
            ]
            
            print(f"📡 Sending to Edge Impulse: {sensor_values}")
            
            # Kirim ke Edge Impulse
            success = self.edge_impulse.send_sensor_data(sensor_values)
            
            if success:
                self.ei_data_count += 1
                self.ei_count.setText(f"Data Sent: {self.ei_data_count}")
            else:
                print("❌ Failed to send to Edge Impulse")
                
        except Exception as e:
            print(f"❌ Edge Impulse send failed: {e}")

    def poll_sensor_data(self):
        """Poll for latest sensor data from Rust backend"""
        if not self.monitoring_active:
            return
            
        try:
            # Get latest sensor data
            response = requests.get(self.get_backend_url("/api/data"), timeout=5)
            if response.status_code == 200:
                sensor_data_list = response.json()
                if sensor_data_list:
                    # Take the latest data point
                    latest_data = sensor_data_list[-1]
                    self.update_sensor_display(latest_data)
                    
                    # ✅ Kirim ke Edge Impulse
                    self.send_to_edge_impulse(latest_data)
                    
            # Also update status
            status_response = requests.get(self.get_backend_url("/api/status"), timeout=5)
            if status_response.status_code == 200:
                self.update_status_display(status_response.json())
                
        except Exception as e:
            print(f"Polling failed: {e}")

    def update_status_display(self, data):
        """Update status display dengan data REAL dari Rust"""
        state_names = ["IDLE", "PRE_COND", "RAMP_UP", "HOLD", "PURGE", "RECOVERY", "DONE"]
        current_state = data.get('current_state', 0)
        state_name = state_names[current_state] if current_state < len(state_names) else "UNKNOWN"
        
        self.state_label.setText(f"State: {state_name}")
        self.level_label.setText(f"Level: {data.get('current_level', 0)}")
        self.data_count_label.setText(f"Data Points: {data.get('data_points', 0)}")
        
        # ✅ Update sampling status dari Arduino data
        sampling_active = data.get('current_level', 0)  # Arduino kirim samplingActive di current_level
        sampling_state = data.get('current_state', 0)  # Arduino kirim state di current_state
        
        if sampling_active == 1:  # Jika sampling aktif
            if sampling_state == 1:
                self.actuator_status.setText("Actuator: 🌀 KIPAS (2 menit)")
            elif sampling_state == 2:
                self.actuator_status.setText("Actuator: 💧 POMPA (4 menit)")
        else:
            self.actuator_status.setText("Actuator: -")
        
        # Update connection status
        if data.get('arduino_connected', False):
            self.connection_status.setText("🟢 Arduino Connected")
            self.connection_status.setStyleSheet("font-weight: bold; padding: 4px 8px; background-color: #065f46; border-radius: 4px; color: #e6fff3;")
        else:
            self.connection_status.setText("🔴 Arduino Disconnected")
            self.connection_status.setStyleSheet("font-weight: bold; padding: 4px 8px; background-color: #7f1d1d; border-radius: 4px; color: #fff;")

    def update_sensor_display(self, sensor_data):
        """Update sensor display dengan data REAL dari Rust backend"""
        value_style = "font-weight: bold; color: #e2e8f0; font-size: 12px;"
        
        # Update labels dengan data aktual
        self.no2_label.setText(f"{sensor_data.get('no2', 0):.3f}")
        self.no2_label.setStyleSheet(value_style)
        
        self.eth_gm_label.setText(f"{sensor_data.get('eth_gm', 0):.3f}")
        self.eth_gm_label.setStyleSheet(value_style)
        
        self.voc_gm_label.setText(f"{sensor_data.get('voc_gm', 0):.3f}")
        self.voc_gm_label.setStyleSheet(value_style)
        
        self.co_gm_label.setText(f"{sensor_data.get('co_gm', 0):.3f}")
        self.co_gm_label.setStyleSheet(value_style)
        
        self.co_mics_label.setText(f"{sensor_data.get('co_m', 0):.3f}")
        self.co_mics_label.setStyleSheet(value_style)
        
        self.eth_mics_label.setText(f"{sensor_data.get('eth_m', 0):.3f}")
        self.eth_mics_label.setStyleSheet(value_style)
        
        self.voc_mics_label.setText(f"{sensor_data.get('voc_m', 0):.3f}")
        self.voc_mics_label.setStyleSheet(value_style)
        
        # Update data buffers untuk plotting
        self.data_count += 1
        self.timestamps.append(self.data_count)
        
        self.no2_data.append(sensor_data.get('no2', 0))
        self.eth_gm_data.append(sensor_data.get('eth_gm', 0))
        self.voc_gm_data.append(sensor_data.get('voc_gm', 0))
        self.co_gm_data.append(sensor_data.get('co_gm', 0))
        self.co_mics_data.append(sensor_data.get('co_m', 0))
        self.eth_mics_data.append(sensor_data.get('eth_m', 0))
        self.voc_mics_data.append(sensor_data.get('voc_m', 0))
        
        # Trim buffers jika terlalu panjang
        if len(self.timestamps) > self.max_data_points:
            self.timestamps.pop(0)
            self.no2_data.pop(0)
            self.eth_gm_data.pop(0)
            self.voc_gm_data.pop(0)
            self.co_gm_data.pop(0)
            self.co_mics_data.pop(0)
            self.eth_mics_data.pop(0)
            self.voc_mics_data.pop(0)
        
        # Update plots dengan data REAL
        if len(self.timestamps) > 1:
            self.curve_no2.setData(self.timestamps, self.no2_data)
            self.curve_eth_gm.setData(self.timestamps, self.eth_gm_data)
            self.curve_voc_gm.setData(self.timestamps, self.voc_gm_data)
            self.curve_co_gm.setData(self.timestamps, self.co_gm_data)
            self.curve_co_mics.setData(self.timestamps, self.co_mics_data)
            self.curve_eth_mics.setData(self.timestamps, self.eth_mics_data)
            self.curve_voc_mics.setData(self.timestamps, self.voc_mics_data)

    def update_elapsed_time(self):
        """Update elapsed time display"""
        self.elapsed_time += 1
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        self.elapsed_label.setText(f"Elapsed: {minutes:02d}:{seconds:02d}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    font = QtGui.QFont("Segoe UI", 9)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    print("🚀 E-NOSE Frontend Started!")
    print(f"📡 Rust Backend: {RUST_IP}:{RUST_PORT}")
    print(f"🎯 Arduino Direct Control: {ARDUINO_IP}:{ARDUINO_PORT}")
    print(f"🧠 Edge Impulse Project: {EI_PROJECT_ID} (Device: {EI_DEVICE_ID})")
    print("💡 Using HTTP API for monitoring + Direct TCP for control + Edge Impulse for ML")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
