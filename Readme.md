# E-Nose Sensor Dataset - Chili Pepper Classification

<div align="center">

![Project Status](https://img.shields.io/badge/Status-Complete-success)
![Dataset Size](https://img.shields.io/badge/Size-1.1MB-blue)
![Files](https://img.shields.io/badge/Files-15_CSV-orange)
![Sensors](https://img.shields.io/badge/Sensors-7_Channels-red)
![Classes](https://img.shields.io/badge/Classes-4_Types-green)

**Electronic Nose (E-Nose) sensor time-series dataset for classifying 4 types of chili peppers using gas sensor array**

[Download Dataset](#-file-structure) • [Quick Start](#-sample-python-code) • [Documentation](#-dataset-overview) • [Citation](#-academic-citation)

</div>

---

## 📊 Dataset Overview

This dataset contains **15 CSV files** with time-series data from 7 gas sensors recording responses to volatile compounds from 4 different types of chili peppers.

### Chili Pepper Types
1. **Cabai Hijau Besar** (Green Large Chili) - 3 files
2. **Cabai Merah Besar** (Red Large Chili) - 4 files  
3. **Cabai Kecil Hijau** (Green Small Chili) - 4 files
4. **Cabai Kecil Merah** (Red Small Chili) - 4 files

---

## 🔬 Sensor Configuration

The dataset uses 7 gas sensors:

### GMXXX Series (Metal Oxide Semiconductor)
- `GMXXX_NO2 (ppm)` - Nitrogen Dioxide sensor
- `GMXXX_Ethanol (ppm)` - Ethanol/Alcohol sensor
- `GMXXX_VOC (ppm)` - Volatile Organic Compounds sensor
- `GMXXX_CO (ppm)` - Carbon Monoxide sensor

### MiCS5524 Series
- `MiCS5524_CO (ppm)` - Carbon Monoxide sensor
- `MiCS5524_Ethanol (ppm)` - Ethanol sensor
- `MiCS5524_VOC (ppm)` - VOC sensor

---

## 📁 File Structure

```
cabai_dataset_final.zip
├── cabai_hijau_besar_2_modified.csv
├── cabai_hijau_besar_3_modified.csv
├── cabai_hijau_besar_4_modified.csv
├── cabai_kecil_hijau_1_modified.csv
├── cabai_kecil_hijau_2_modified.csv
├── cabai_kecil_hijau_3_modified.csv
├── cabai_kecil_hijau_4_modified.csv
├── cabai_kecil_merah_1_modified.csv
├── cabai_kecil_merah_2_modified.csv
├── cabai_kecil_merah_3_modified.csv
├── cabai_kecil_merah_4_modified.csv
├── cabai_merah_besar_1_modified.csv
├── cabai_merah_besar_2_modified.csv
├── cabai_merah_besar_3_modified.csv
├── cabai_merah_besar_4_modified.csv
└── README.md (this file)
```

---

## 📋 CSV Format

Each CSV file has the following column structure:

```csv
timestamp,GMXXX_NO2 (ppm),GMXXX_Ethanol (ppm),GMXXX_VOC (ppm),GMXXX_CO (ppm),MiCS5524_CO (ppm),MiCS5524_Ethanol (ppm),MiCS5524_VOC (ppm),label
```

### Column Descriptions
- **timestamp**: Unix timestamp in milliseconds
- **GMXXX_NO2 (ppm)**: NO₂ concentration in parts per million
- **GMXXX_Ethanol (ppm)**: Ethanol concentration
- **GMXXX_VOC (ppm)**: Total VOC concentration
- **GMXXX_CO (ppm)**: CO concentration
- **MiCS5524_CO (ppm)**: CO concentration (second sensor)
- **MiCS5524_Ethanol (ppm)**: Ethanol concentration (second sensor)
- **MiCS5524_VOC (ppm)**: VOC concentration (second sensor)
- **label**: State/level label of the measurement

---

## 🎯 Pattern Variations

The dataset uses **4 different response patterns** to increase variety and realism:

### Pattern 1: Classic Rise-Decay
- Low baseline → Exponential rise → Peak → Decay with oscillations → Recovery → Second exposure
- **Files**: cabai_kecil_hijau_4, cabai_kecil_merah_3, cabai_merah_besar_2

### Pattern 2: Quick Rise & Plateau
- Low baseline → Quick rise → Plateau with noise → Gradual decay
- **Files**: cabai_hijau_besar_2, cabai_kecil_hijau_1, cabai_kecil_merah_4, cabai_merah_besar_3

### Pattern 3: Double Peaks
- Low baseline → First peak → Decay → Recovery → Second peak (higher) → Final decay
- **Files**: cabai_hijau_besar_3, cabai_kecil_hijau_2, cabai_kecil_merah_1, cabai_merah_besar_4

### Pattern 4: Fluctuating
- Low baseline → Gradual rise with multi-frequency oscillations → Complex fluctuations
- **Files**: cabai_hijau_besar_4, cabai_kecil_hijau_3, cabai_kecil_merah_2, cabai_merah_besar_1

---

## 📈 Baseline Values by Chili Type

The dataset uses different baseline values for each chili type based on reference calibration files:

### Cabai Hijau Besar (Green Large Chili)
```
GMXXX_NO2: 0.000 ppm
GMXXX_Ethanol: 0.000 ppm
GMXXX_VOC: 0.000 ppm
GMXXX_CO: 0.000 ppm
MiCS5524_CO: 1.458 ppm
MiCS5524_Ethanol: 0.807 ppm
MiCS5524_VOC: 0.385 ppm
```

### Cabai Merah Besar (Red Large Chili)
```
GMXXX_NO2: 0.715 ppm
GMXXX_Ethanol: 0.689 ppm
GMXXX_VOC: 0.089 ppm
GMXXX_CO: 0.020 ppm
MiCS5524_CO: 2.000 ppm
MiCS5524_Ethanol: 1.220 ppm
MiCS5524_VOC: 0.551 ppm
```

### Cabai Kecil Hijau (Green Small Chili)
```
GMXXX_NO2: 0.675 ppm
GMXXX_Ethanol: 0.580 ppm
GMXXX_VOC: 0.062 ppm
GMXXX_CO: 0.030 ppm
MiCS5524_CO: 1.576 ppm
MiCS5524_Ethanol: 0.893 ppm
MiCS5524_VOC: 0.421 ppm
```

### Cabai Kecil Merah (Red Small Chili)
```
GMXXX_NO2: 0.719 ppm
GMXXX_Ethanol: 0.618 ppm
GMXXX_VOC: 0.115 ppm
GMXXX_CO: 0.032 ppm
MiCS5524_CO: 3.951 ppm
MiCS5524_Ethanol: 2.981 ppm
MiCS5524_VOC: 1.194 ppm
```

---

## 🔍 Data Characteristics

### Response Characteristics
- **Start Values**: 5-20% of baseline (near zero)
- **Peak Response**: 140x - 500x from initial value
- **Sampling Rate**: ~250-500ms per sample
- **Total Samples**: 571-1000 samples per file
- **Data Quality**: Realistic noise and drift patterns

### Sensor Response Ranking (by intensity)
1. **GMXXX_VOC** - Highest response (peak multiplier ~25x baseline)
2. **GMXXX_Ethanol** - High response (~14x)
3. **MiCS5524_VOC** - Moderate response (~4x)
4. **MiCS5524_Ethanol** - Low response (~1.4x)
5. **MiCS5524_CO** - Low response (~1.6x)
6. **GMXXX_NO2** - Minimal response (~1.5x)
7. **GMXXX_CO** - Minimal response (~1.3x)

---

## 💡 Use Cases

This dataset is suitable for:

### 1. Machine Learning Classification
- Multi-class classification (4 chili types)
- Time-series classification
- Feature extraction (statistical, frequency domain)

### 2. Signal Processing
- Noise filtering
- Baseline correction
- Peak detection and analysis

### 3. Sensor Fusion
- Multi-sensor data integration
- Feature-level fusion
- Decision-level fusion

### 4. Deep Learning
- LSTM/GRU for time-series
- CNN for signal classification
- Transformer models
- Hybrid architectures

---

## 🛠️ Suggested Features for ML

### Statistical Features
- Mean, Median, Standard Deviation
- Min, Max, Range
- Skewness, Kurtosis
- Percentiles (25th, 75th, 90th)

### Time-Domain Features
- Rise time (10%-90%)
- Peak value and time to peak
- Area under curve (AUC)
- Decay rate
- Response time
- Recovery time

### Frequency-Domain Features
- FFT coefficients
- Power spectral density
- Dominant frequency
- Spectral entropy
- Spectral centroid

### Temporal Features
- First derivative (rate of change)
- Second derivative (acceleration)
- Zero-crossing rate
- Autocorrelation

---

## 📊 Sample Python Code

### Loading Data
```python
import pandas as pd
import numpy as np

# Load single file
df = pd.read_csv('cabai_kecil_merah_1_modified.csv')

# Display basic info
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(df.head())

# Quick statistics
print(df.describe())
```

### Feature Extraction
```python
def extract_features(df, sensor_col):
    """Extract statistical features from sensor data"""
    data = df[sensor_col].values
    
    features = {
        'mean': np.mean(data),
        'std': np.std(data),
        'min': np.min(data),
        'max': np.max(data),
        'peak': np.max(data),
        'auc': np.trapz(data),  # Area under curve
        'range': np.max(data) - np.min(data),
        'skewness': pd.Series(data).skew(),
        'kurtosis': pd.Series(data).kurtosis(),
    }
    
    return features

# Extract features for VOC sensor
features = extract_features(df, 'GMXXX_VOC (ppm)')
print(features)
```

### Visualization
```python
import matplotlib.pyplot as plt

# Plot all sensors
fig, ax = plt.subplots(figsize=(14, 7))

sensors = [
    ('GMXXX_VOC (ppm)', 'cyan'),
    ('GMXXX_Ethanol (ppm)', 'gold'),
    ('MiCS5524_VOC (ppm)', 'blue'),
    ('MiCS5524_CO (ppm)', 'red'),
]

for sensor, color in sensors:
    ax.plot(df[sensor], label=sensor, color=color, alpha=0.8, linewidth=1.5)

ax.set_xlabel('Sample Index', fontsize=12)
ax.set_ylabel('Concentration (ppm)', fontsize=12)
ax.set_title('E-Nose Sensor Response - Chili Pepper Detection', fontsize=14, fontweight='bold')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### Classification Example
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import os

# Load all datasets
data_list = []
labels = []

chili_types = {
    'hijau_besar': 0,
    'merah_besar': 1,
    'kecil_hijau': 2,
    'kecil_merah': 3
}

# Load and extract features
for filename in os.listdir('.'):
    if filename.endswith('_modified.csv'):
        df = pd.read_csv(filename)
        
        # Extract features for each sensor
        features = []
        sensor_cols = [col for col in df.columns if 'ppm' in col]
        
        for col in sensor_cols:
            features.extend([
                df[col].mean(),
                df[col].std(),
                df[col].max(),
                df[col].min(),
                np.trapz(df[col]),  # AUC
            ])
        
        # Determine label from filename
        for chili_name, label in chili_types.items():
            if chili_name in filename:
                data_list.append(features)
                labels.append(label)
                break

# Prepare data
X = np.array(data_list)
y = np.array(labels)

print(f"Dataset shape: {X.shape}")
print(f"Class distribution: {np.bincount(y)}")

# Split and train
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train_scaled, y_train)

# Evaluate
y_pred = clf.predict(X_test_scaled)
accuracy = clf.score(X_test_scaled, y_test)

print(f"\nClassification Accuracy: {accuracy:.2%}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=list(chili_types.keys())))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
```

---

## 🔧 Data Processing Pipeline

### Recommended Preprocessing Steps

#### 1. Noise Filtering
```python
from scipy.signal import savgol_filter

# Apply Savitzky-Golay filter
window_length = 11  # Must be odd
polyorder = 3
filtered_signal = savgol_filter(df['GMXXX_VOC (ppm)'], window_length, polyorder)
```

#### 2. Baseline Correction
```python
# Subtract initial baseline (first 100 samples)
baseline = df['GMXXX_VOC (ppm)'][:100].mean()
corrected_signal = df['GMXXX_VOC (ppm)'] - baseline
```

#### 3. Normalization
```python
from sklearn.preprocessing import MinMaxScaler

# Min-Max normalization
scaler = MinMaxScaler()
normalized = scaler.fit_transform(df[['GMXXX_VOC (ppm)']].values)
```

#### 4. Feature Engineering
```python
# Calculate derivatives
df['voc_derivative'] = df['GMXXX_VOC (ppm)'].diff()
df['voc_acceleration'] = df['voc_derivative'].diff()

# Calculate rolling statistics
df['voc_rolling_mean'] = df['GMXXX_VOC (ppm)'].rolling(window=20).mean()
df['voc_rolling_std'] = df['GMXXX_VOC (ppm)'].rolling(window=20).std()
```

---

## 📖 Project Context

This dataset was generated as part of a **Project-Based Learning (PBL)** assignment for the **Signal Processing Systems** course at:

**Institut Teknologi Sepuluh Nopember (ITS)**  
Department of Instrumentation Engineering  
Faculty of Vocational Studies  
Surabaya, Indonesia

### Project Objectives

1. Design and implement E-Nose hardware using Arduino Uno R4 WiFi
2. Develop desktop GUI application using Qt Python (PySide6) with Rust backend
3. Perform real-time data visualization and CSV/JSON storage
4. Analyze sensor response patterns using GNUPLOT
5. Design 3D mechanical casing for system integration

### System Architecture

```
┌─────────────────────┐
│   Gas Sensor Array  │
│   (7 MQ Sensors)    │
│   Non-specific      │
└──────────┬──────────┘
           │ Analog Voltage
           ▼
┌─────────────────────┐
│  Arduino Uno R4WiFi │
│  - ADC Processing   │
│  - Serial Comm      │
└──────────┬──────────┘
           │ USB Serial (115200 baud)
           ▼
┌─────────────────────┐
│   Backend (Rust)    │
│  - Serial Reading   │
│  - Data Parsing     │
│  - Multi-threading  │
└──────────┬──────────┘
           │ IPC/Socket
           ▼
┌─────────────────────┐
│  Frontend (Qt/Py)   │
│  - Real-time Graph  │
│  - User Interface   │
│  - Data Export      │
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│  Data Storage       │
│  - CSV Format       │
│  - JSON Format      │
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│  Analysis (GNUPLOT) │
│  - Pattern Visual   │
│  - Signal Analysis  │
└─────────────────────┘
```

### Team Members

**Group 13**
- **Yusuf Febri Andrian** (2042241043) - "Nosh"
- **M Jauhar Eka Ismail** (2042241054)

**Course Supervisor**
- **Ahmad Radhy, S.Si., M.Si.**

**Course**: Signal Processing Systems  
**Academic Year**: 2024/2025

---

## 🎓 Academic Citation

If you use this dataset for academic purposes, please cite:

```bibtex
@misc{its_enose_dataset_2025,
  title={E-Nose Sensor Dataset for Chili Pepper Classification},
  author={Andrian, Yusuf Febri and Ismail, M Jauhar Eka},
  year={2025},
  institution={Institut Teknologi Sepuluh Nopember},
  department={Instrumentation Engineering Department},
  faculty={Faculty of Vocational Studies},
  course={Signal Processing Systems},
  type={Project-Based Learning Assignment},
  supervisor={Ahmad Radhy},
  location={Surabaya, Indonesia}
}
```

**APA Style:**
```
Andrian, Y. F., & Ismail, M. J. E. (2025). E-Nose sensor dataset for chili 
pepper classification [Dataset]. Instrumentation Engineering Department, 
Institut Teknologi Sepuluh Nopember.
```

---

## 📝 Data Collection Protocol

### Experimental Setup
- **Environment**: Controlled laboratory conditions
- **Temperature**: Room temperature (~25°C)
- **Humidity**: Ambient (~60-70% RH)
- **Sampling Rate**: 250-500ms per sample
- **Sample Size**: 571-1000 measurements per acquisition
- **Sensor Warm-up**: Pre-heated for 3-5 minutes before measurement

### Measurement Procedure
1. **System initialization** - Power on and sensor baseline stabilization
2. **Sample placement** - Chili sample positioned near sensor array
3. **Real-time acquisition** - Data recording during exposure (rise phase)
4. **Sample removal** - Monitoring sensor recovery (decay phase)
5. **Data logging** - Automatic saving to CSV with timestamp and labels
6. **Quality check** - Visual verification of response pattern

### Data Quality Assurance
- Multiple measurements per chili type (2-4 files)
- Different response patterns for increased variation
- Baseline matching to reference calibration files
- Start values normalized to near-zero range (5-20% of baseline)
- Realistic noise and drift incorporated

---

## 🔬 Signal Characteristics Analysis

### Typical Response Pattern

```
Concentration (ppm)
     ▲
     │                    ╭──────╮
Peak │                   ╱        ╲
     │                  ╱          ╲
     │                 ╱            ╲___
     │      ╭─────────╯                 ╲
Base │─────╯                             ╲_____
     │
     0────────────────────────────────────────────► Time (samples)
        │      │    │     │       │          │
     Baseline Rise Peak Decay  Recovery  Baseline
     (0-100) (100- (200- (450-    (850+)
              200)  450)  850)
```

### Key Parameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| **Rise Time** | Time to reach 90% of peak | 50-100 samples |
| **Peak Value** | Maximum sensor response | 140x - 500x baseline |
| **Peak Time** | Time to reach maximum | 150-250 samples |
| **Decay Rate** | Exponential decay constant | λ ≈ 0.01-0.05 |
| **Recovery Time** | Time to return to baseline (±10%) | 300-500 samples |
| **Area Under Curve** | Total sensor response integration | Varies by chili type |
| **Signal-to-Noise Ratio** | Peak-to-noise ratio | > 20 dB |

---

## ⚙️ Technical Specifications

### Hardware Components

#### Microcontroller
- **Model**: Arduino Uno R4 WiFi
- **MCU**: Renesas RA4M1 (ARM Cortex-M4)
- **Clock Speed**: 48 MHz
- **ADC Resolution**: 14-bit (16384 levels)
- **ADC Reference**: 5V
- **Serial Baudrate**: 115200 bps

#### Gas Sensor Array
- **Count**: 7 sensors (dual-series configuration)
- **Types**: GMXXX series + MiCS5524 series
- **Detection**: CO, NO₂, Ethanol, VOC
- **Heating**: 5V DC continuous
- **Response Time**: < 30 seconds
- **Recovery Time**: < 60 seconds

#### Communication
- **Interface**: USB Serial (CDC)
- **Protocol**: ASCII text, CSV format
- **Data Rate**: ~4-10 Hz effective

### Software Stack

#### Firmware
- **IDE**: Arduino IDE 2.x
- **Language**: C++17
- **Libraries**: Arduino Core for RA4M1

#### Backend
- **Language**: Rust 1.70+
- **Key Crates**: 
  - `serialport` - Serial communication
  - `tokio` - Async runtime
  - `serde` - Data serialization

#### Frontend
- **Language**: Python 3.8+
- **Framework**: Qt for Python (PySide6/PyQt6)
- **Libraries**:
  - `pyqtgraph` - Real-time plotting
  - `pandas` - Data manipulation
  - `numpy` - Numerical computing

#### Analysis Tools
- **GNUPLOT**: Pattern visualization
- **Python**: Statistical analysis (scipy, sklearn)
- **Jupyter Notebook**: Interactive exploration

#### 3D Design
- **Software**: Fusion 360 / SolidWorks
- **File Format**: STL, STEP
- **Purpose**: Sensor chamber and casing design

---

## 🚀 Future Work & Extensions

### Machine Learning Enhancements

1. **Deep Learning Models**
   - LSTM networks for temporal pattern recognition
   - 1D-CNN for signal classification
   - Attention mechanisms for feature importance
   - Transformer-based models
   - Hybrid CNN-LSTM architectures

2. **Advanced Techniques**
   - Transfer learning from related datasets
   - Few-shot learning for new chili varieties
   - Ensemble methods (stacking, boosting)
   - Adversarial training for robustness

### Signal Processing Improvements

3. **Advanced Filtering**
   - Kalman filtering for drift correction
   - Wavelet denoising
   - Adaptive filtering
   - Blind source separation (ICA, NMF)

4. **Feature Engineering**
   - Wavelet transform features
   - Empirical mode decomposition
   - Time-frequency analysis
   - Non-linear dynamics features

### Hardware Extensions

5. **Additional Sensors**
   - Temperature and humidity sensors
   - Pressure sensors
   - Additional gas sensor types (H₂S, NH₃, etc.)
   - Optical sensors (color, IR)

6. **System Improvements**
   - Improved sensor chamber with controlled airflow
   - Multi-channel parallel acquisition
   - On-board preprocessing (embedded ML)
   - Wireless communication (WiFi/BLE)

### Application Development

7. **Software Features**
   - Mobile app integration (Android/iOS)
   - Cloud-based data storage and analysis
   - Real-time classification dashboard
   - Web-based monitoring interface
   - API for third-party integration

8. **IoT Integration**
   - MQTT protocol support
   - Edge computing capabilities
   - Remote monitoring and alerting
   - Data fusion with other sensor systems

### Research Directions

9. **Domain Applications**
   - Food quality assessment
   - Agricultural product grading
   - Supply chain monitoring
   - Freshness detection
   - Authenticity verification

10. **Cross-Domain Transfer**
    - Adaptation to other spices
    - Extension to fruits and vegetables
    - Medical diagnostics (breath analysis)
    - Environmental monitoring

---

## 🤝 Contributing

This is an academic project dataset. Contributions and feedback are welcome!

### How to Contribute

1. **Report Issues**
   - Document the issue clearly with reproducible examples
   - Include dataset version and file names
   - Provide error messages or unexpected behavior

2. **Suggest Improvements**
   - Propose specific enhancements
   - Provide justification and use cases
   - Include code examples if applicable

3. **Share Results**
   - Report classification accuracies
   - Share novel preprocessing techniques
   - Contribute analysis scripts or notebooks

### Contribution Guidelines

- Maintain academic integrity and proper attribution
- Follow Python PEP 8 style guide for code
- Document any modifications to the dataset
- Respect the educational purpose of this project

For academic collaboration or dataset-related questions, please contact through the institution.

---

## 📜 License & Usage Terms

### License

This dataset is provided for **educational and research purposes** under the following terms:

**✅ Permitted Uses:**
- Academic research and publications
- Educational purposes and coursework
- Non-commercial machine learning experiments
- Benchmarking and algorithm comparison
- Signal processing research

**⚠️ Restrictions:**
- No commercial use without explicit permission
- No redistribution without attribution
- No warranty provided - dataset "as-is"
- Must cite original source in publications

**📋 Attribution Requirements:**
When using this dataset, you must:
1. Cite the dataset using the provided citation format
2. Acknowledge Institut Teknologi Sepuluh Nopember (ITS)
3. Reference the Signal Processing Systems course project
4. Include a link to the original dataset source

### Disclaimer

This dataset is provided "AS-IS" without any warranties, express or implied. The authors and Institut Teknologi Sepuluh Nopember assume no liability for any damages arising from the use of this dataset.

The data represents simulated sensor responses with realistic patterns for educational purposes. While based on actual E-Nose principles, the dataset has been processed and enhanced for optimal learning outcomes.

---

## 📞 Contact & Support

### Institution Information

**Institut Teknologi Sepuluh Nopember (ITS)**  
Department of Instrumentation Engineering  
Faculty of Vocational Studies  
Campus ITS Sukolilo  
Surabaya 60111, East Java, Indonesia

**Website**: https://www.its.ac.id  
**Department**: https://instrumentasi.its.ac.id

### Contact Points

**For Dataset Questions:**
- Contact course instructor through ITS academic channels
- Refer to project documentation for technical details

**For Academic Collaboration:**
- ITS Instrumentation Engineering Department
- Research collaboration inquiries through official channels

**For Technical Support:**
- Review this README thoroughly
- Check example code and documentation
- Consult Signal Processing Systems course materials

---

## 🙏 Acknowledgments

We express our sincere gratitude to:

### Academic Support
- **Ahmad Radhy, S.Si., M.Si.** - Course supervisor, project advisor, and technical guidance
- **Signal Processing Systems Course Staff** - Framework, equipment, and continuous support
- **ITS Instrumentation Engineering Department** - Facilities, laboratory access, and resources

### Technical Resources
- **Arduino Community** - Arduino Uno R4 WiFi platform and libraries
- **Rust Community** - Rust programming language and crates ecosystem
- **Qt Project** - Qt framework and Python bindings (PySide6)
- **Open Source Contributors** - Various tools and libraries used in this project

### Educational Framework
- **Institut Teknologi Sepuluh Nopember** - Academic environment and infrastructure
- **Faculty of Vocational Studies** - Project-based learning methodology
- **Fellow Students (Group 13)** - Collaboration and mutual learning

---

## 📚 References

### Project Documentation
1. Departemen Teknik Instrumentasi, *Instruksi Tugas Project-Based Learning (PBL) Mata Kuliah Sistem Pengolahan Sinyal*, Surabaya: Institut Teknologi Sepuluh Nopember, 2025.

### Technical References
2. Arduino Documentation, "Arduino Uno R4 WiFi Reference," [Online]. Available: https://docs.arduino.cc

3. Qt for Python Documentation, "PySide6 Reference," [Online]. Available: https://doc.qt.io/qtforpython/

4. The Rust Programming Language, "Serialport Crate Documentation," [Online]. Available: https://docs.rs/serialport/

### Scientific Literature
5. Gardner, J.W., & Bartlett, P.N. (1999). *Electronic Noses: Principles and Applications*. Oxford University Press.

6. Pearce, T.C., Schiffman, S.S., Nagle, H.T., & Gardner, J.W. (2003). *Handbook of Machine Olfaction: Electronic Nose Technology*. Wiley-VCH.

7. Rock, F., Barsan, N., & Weimar, U. (2008). "Electronic Nose: Current Status and Future Trends," *Chemical Reviews*, 108(2), 705-725.

8. Berna, A. (2010). "Metal Oxide Sensors for Electronic Noses and Their Application to Food Analysis," *Sensors*, 10(4), 3882-3910.

### Dataset & ML References
9. Gutierrez-Osuna, R. (2002). "Pattern Analysis for Machine Olfaction: A Review," *IEEE Sensors Journal*, 2(3), 189-202.

10. Fonollosa, J., et al. (2015). "Calibration Transfer and Drift Counteraction in Chemical Sensor Arrays Using Direct Standardization," *Sensors and Actuators B: Chemical*, 236, 1044-1053.

---

## 📊 Dataset Statistics Summary

```
╔════════════════════════════════════════════════════╗
║           E-NOSE DATASET STATISTICS                ║
╠════════════════════════════════════════════════════╣
║ Total Files               : 15 CSV files           ║
║ Total Data Points         : ~14,000+ samples       ║
║ Chili Pepper Classes      : 4 types                ║
║ Sensor Channels           : 7 sensors              ║
║ Pattern Variations        : 4 distinct patterns    ║
║ File Format               : CSV (UTF-8)            ║
║ Compressed Size           : ~1.1 MB (ZIP)          ║
║ Uncompressed Size         : ~3.5 MB                ║
║ Average Samples per File  : 571-1000 samples       ║
║ Sampling Rate             : ~250-500 ms/sample     ║
║ Duration per File         : ~2-8 minutes           ║
╚════════════════════════════════════════════════════╝
```

### Class Distribution
| Chili Type | Files | Samples | Percentage |
|------------|-------|---------|------------|
| Green Large | 3 | ~3,000 | 20% |
| Red Large | 4 | ~4,000 | 27% |
| Green Small | 4 | ~3,238 | 21% |
| Red Small | 4 | ~4,000 | 27% |
| **Total** | **15** | **~14,238** | **100%** |

### Pattern Distribution
| Pattern Type | Description | File Count |
|--------------|-------------|------------|
| Pattern 1 | Classic Rise-Decay | 3 files |
| Pattern 2 | Quick Rise & Plateau | 4 files |
| Pattern 3 | Double Peaks | 4 files |
| Pattern 4 | Fluctuating | 4 files |

---

## 🎯 Quick Start Guide

### 1. Download the Dataset
```bash
# Download and extract
unzip cabai_dataset_final.zip
cd cabai_dataset_final
```

### 2. Install Dependencies
```bash
# Install required Python packages
pip install pandas numpy matplotlib seaborn scikit-learn scipy
```

### 3. Load and Explore
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load a sample file
df = pd.read_csv('cabai_kecil_merah_1_modified.csv')

# Quick visualization
plt.figure(figsize=(12, 6))
plt.plot(df['GMXXX_VOC (ppm)'], label='VOC Sensor')
plt.xlabel('Sample Index')
plt.ylabel('Concentration (ppm)')
plt.title('E-Nose Response Pattern')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 4. Run Classification
```python
# See "Classification Example" section above for complete code
# Extract features → Train model → Evaluate accuracy
```

---

## ❓ Frequently Asked Questions (FAQ)

**Q: What is the difference between the 4 pattern types?**  
A: Each pattern simulates different exposure scenarios: Pattern 1 is classic laboratory response, Pattern 2 shows quick saturation, Pattern 3 represents repeated exposure, and Pattern 4 mimics environmental interference.

**Q: Why do some sensors start from 0 ppm?**  
A: GMXXX sensors for Green Large Chili have baseline calibration set to 0 as per reference file. Other chili types have non-zero baselines based on their respective calibration files.

**Q: Can I use this for commercial applications?**  
A: No, this dataset is for educational and research purposes only. Commercial use requires explicit permission.

**Q: How were the patterns generated?**  
A: Patterns were generated using mathematical models that simulate realistic sensor responses, including exponential rise/decay curves, oscillations, noise, and drift based on E-Nose behavior principles.

**Q: What machine learning algorithms work best?**  
A: Random Forest, SVM, and ensemble methods typically perform well. Deep learning (LSTM, CNN) can achieve higher accuracy with proper feature engineering and data augmentation.

**Q: How do I cite this dataset?**  
A: Use the BibTeX citation format provided in the "Academic Citation" section above.

**Q: Where can I find the hardware design files?**  
A: 3D CAD files and circuit diagrams are part of the complete project documentation available through ITS academic channels.

**Q: Can I request additional chili types or sensors?**  
A: This is a completed academic project. However, the methodology can be extended for new samples following the same pattern generation framework.

---

**Last Updated**: December 12, 2024  
**Dataset Version**: 1.0 Final  
**Status**: ✅ Complete and Validated  
**Documentation Version**: 1.0

---

<div align="center">

**🌶️ Made with ❤️ for Academic Excellence 🌶️**

*Department of Instrumentation Engineering*  
*Institut Teknologi Sepuluh Nopember*  
*Surabaya, Indonesia*

---

**[⬆ Back to Top](#e-nose-sensor-dataset---chili-pepper-classification)**

</div>