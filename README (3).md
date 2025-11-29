#  AI-Powered Health Monitoring System

An intelligent, real-time health monitoring platform that leverages machine learning and data analytics to track vital signs, detect anomalies, and predict health trends. Built with Streamlit, scikit-learn, and advanced visualization libraries.

---

##  Overview

The AI Health Monitoring System is a comprehensive web-based application designed to revolutionize personal and clinical health monitoring. It combines real-time data collection, AI-powered anomaly detection, predictive analytics, and intuitive visualizations to provide actionable health insights for both patients and healthcare providers.

###  Purpose

This system addresses the growing need for continuous, intelligent health monitoring by:
- **Democratizing Health Analytics**: Making advanced AI-powered health insights accessible to everyone
- **Early Warning Detection**: Identifying potential health issues before they become critical
- **Predictive Healthcare**: Using machine learning to forecast health trends and prevent complications
- **Data-Driven Decisions**: Empowering patients and doctors with comprehensive, visual health data

---

##  What It Does

### Core Capabilities

#### 1. **Real-Time Vital Sign Monitoring** 
- Continuously tracks key health metrics:
  - Heart Rate (BPM)
  - Blood Oxygen Saturation (%)
  - Body Temperature (°C)
  - Respiration Rate (breaths/min)
  - Activity Level
- Displays current values with trend indicators
- Calculates overall health scores (0-100 scale)
- Provides personalized baselines for each user

#### 2. **AI-Powered Anomaly Detection** 
- Uses **Isolation Forest** machine learning algorithm to identify abnormal health patterns
- Supports multi-user simultaneous monitoring
- Features include:
  - Real-time anomaly flagging with severity levels
  - Interactive time-series visualizations
  - Heatmap analysis across users and time
  - Distribution plots for pattern recognition
  - Configurable contamination rates (1%-20%)
  - Exportable detection reports

#### 3. **Predictive Health Analytics** 
- **LSTM Neural Networks** for time-series forecasting
- Predicts future vital signs based on historical patterns
- Features include:
  - Customizable prediction horizons (5-20 minutes)
  - Confidence interval calculations
  - Visual comparison of historical vs. predicted values
  - Risk assessment algorithms
  - Health score trend projections

#### 4. **Intelligent Alert System** 
- Automatic threshold-based alerts for critical vitals
- Three severity levels:
  -  **CRITICAL**: Immediate attention required
  -  **HIGH**: Concerning values, monitor closely
  -  **MODERATE**: Minor deviations from baseline
- Alert history tracking
- Configurable thresholds for personalized monitoring

#### 5. **Comprehensive Reporting** 
- Multi-format data export:
  - **CSV**: Raw data for analysis
  - **Excel**: Formatted spreadsheets with multiple sheets
  - **PDF**: Professional reports with charts and summaries
  - **TXT**: Plain text summaries
- Customizable time periods (last 24h, week, month, all-time)
- Statistical summaries with min/max/average values
- Shareable reports for doctor consultations

#### 6. **Multi-User Dashboard** 
- **Patient View**:
  - Personal health dashboard with metric cards
  - Manual vital entry or simulated data generation
  - Medication and appointment tracking
  - Historical trend visualization
  - Personalized health insights
  
- **Doctor View**:
  - Patient selection and monitoring
  - Configurable alert thresholds
  - Multi-patient overview
  - Alert history for each patient
  - Real-time status monitoring

---

##  Technical Highlights

### Machine Learning & AI
- **Isolation Forest**: Unsupervised anomaly detection with contamination tuning
- **LSTM Networks**: Deep learning for time-series prediction
- **Health Scoring Algorithm**: Multi-factor composite scoring
- **Risk Assessment**: Rule-based and ML-hybrid approaches

### Data Processing
- **Real-time preprocessing**: Normalization, scaling, feature engineering
- **Temporal analysis**: Time-series decomposition and trend extraction
- **Statistical baselines**: Per-user personalized normal ranges

### Visualization
- **Interactive Plotly Charts**: Zoom, pan, hover, and export capabilities
- **Multi-metric dashboards**: Synchronized time-series plots
- **Heatmaps**: Pattern recognition across users and time
- **Gauge indicators**: Intuitive health score displays
- **Distribution plots**: Statistical analysis visualizations

---

##  Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project:**
   ```bash
   cd "C:\Users\eng~lyne\Desktop\AIFINAL-PROJECT"
   ```

2. **Install dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Access the application:**
   - Open your browser to: `http://localhost:8501`

### Demo Credentials

The system comes with pre-configured demo accounts:

- **Patient Account**
  - Username: `patient1`
  - Password: `pass1`
  - Access: Dashboard, Predictions, Anomaly Detection, Reports

- **Doctor Account**
  - Username: `doctor1`
  - Password: `pass1`
  - Access: Patient Monitoring, Alert Configuration, Multi-patient Dashboard

---

##  Using the Application

### For Patients

1. **Initial Setup**
   - Log in with patient credentials
   - Generate sample health data or manually enter vitals
   - Review your baseline metrics

2. **Daily Monitoring**
   - Check dashboard for current vital signs
   - Review health score and active alerts
   - Track trends over time

3. **Anomaly Analysis**
   - Navigate to "Anomaly Detection"
   - Simulate multi-user scenarios
   - Identify unusual patterns in your data

4. **Predictive Insights**
   - Use "AI Predictions" for LSTM forecasts
   - View risk assessments
   - Monitor health score trends

5. **Report Generation**
   - Export data in preferred format
   - Share reports with healthcare providers
   - Maintain personal health records

### For Healthcare Providers

1. **Patient Selection**
   - Access doctor dashboard
   - Select patient from dropdown

2. **Monitoring**
   - Review current vitals and health scores
   - Set custom alert thresholds
   - Check alert history

3. **Analysis**
   - Examine trend visualizations
   - Identify concerning patterns
   - Generate comprehensive reports

---

##  Key Features Breakdown

| Feature | Description | Technologies |
|---------|-------------|--------------|
| **Authentication** | Secure login with role-based access | streamlit-authenticator, cryptography |
| **Data Simulation** | Realistic health data generation with anomalies | NumPy, Pandas |
| **Anomaly Detection** | AI-powered outlier identification | scikit-learn (Isolation Forest) |
| **LSTM Predictions** | Neural network forecasting | TensorFlow/Keras (optional) |
| **Interactive Dashboards** | Real-time, zoomable visualizations | Plotly |
| **Multi-format Exports** | CSV, Excel, PDF, TXT reports | Pandas, openpyxl, reportlab |
| **Alert System** | Threshold-based notifications | Custom algorithms |
| **Health Scoring** | Composite health metrics (0-100) | Custom algorithms |

---

##  Data Privacy & Security

- Secure password hashing using industry-standard algorithms
- Session-based authentication with configurable expiry
- Local data storage (no external transmission)
- Role-based access control (Patient/Doctor)

---

##  Troubleshooting

### Common Issues

**"TensorFlow not available" warning:**
- LSTM predictions require TensorFlow
- Install with: `pip install tensorflow`
- Note: TensorFlow may not be available for all Python versions on Windows

**"ModuleNotFoundError" errors:**
```bash
python -m pip install plotly pandas numpy scikit-learn streamlit
```

**Authentication issues:**
- Ensure you're using the correct credentials (patient1/pass1)
- Clear browser cache and cookies
- Restart the Streamlit server

**Charts not displaying:**
```bash
python -m pip install --upgrade plotly
```

---

##  Project Structure

```
AIFINAL-PROJECT/
├── app.py                      # Main application entry point
├── pages/                      # Streamlit pages
│   ├── dashboard.py           # Patient/Doctor dashboards
│   ├── anomaly_detection.py   # Anomaly detection interface
│   ├── ai_predictions.py      # LSTM predictions & risk assessment
│   ├── reports.py             # Report generation & export
│   ├── medications_appointments.py
│   └── chatbot.py
├── data.py                     # Data management & simulation
├── models.py                   # ML models & algorithms
├── utils.py                    # Helper functions
├── visualizations.py           # Plotly chart generators
├── alerts.py                   # Alert system logic
├── config.yaml                 # Application configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

##  Future Enhancements

- [ ] Real device integration (Fitbit, Apple Watch, etc.)
- [ ] Mobile app companion
- [ ] Cloud deployment with multi-tenant support
- [ ] Advanced ML models (Transformers, AutoML)
- [ ] Telemedicine integration
- [ ] Wearable device APIs
- [ ] Speech-based health assistant
- [ ] Integration with electronic health records (EHR)

---

##  Contributing

This is a demonstration project showcasing AI-powered health monitoring capabilities. Feel free to extend and customize for your specific needs.

---

##  License

This project is provided as-is for educational and demonstration purposes.

---

##  Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Web application framework
- [scikit-learn](https://scikit-learn.org/) - Machine learning library
- [Plotly](https://plotly.com/) - Interactive visualization library
- [TensorFlow](https://www.tensorflow.org/) - Deep learning framework
- [Pandas](https://pandas.pydata.org/) - Data manipulation library

---

##  Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the [walkthrough documentation](walkthrough.md)
3. Ensure all dependencies are properly installed

---

**Made with Lynn for better health monitoring**
