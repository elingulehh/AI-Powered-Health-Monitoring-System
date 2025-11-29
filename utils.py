import json
import os
from cryptography.fernet import Fernet
import smtplib
from email.mime.text import MIMEText
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import StandardScaler

# Generate or load encryption key
def get_encryption_key():
    key_file = 'encryption_key.key'
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        return key

# Encrypt data
def encrypt_data(data):
    fernet = Fernet(get_encryption_key())
    return fernet.encrypt(data.encode()).decode()

# Decrypt data
def decrypt_data(encrypted_data):
    fernet = Fernet(get_encryption_key())
    return fernet.decrypt(encrypted_data.encode()).decode()

# Save data to JSON
def save_data_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Load data from JSON
def load_data_from_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

# Send alert email (simulation)
def send_alert_email(to_email, subject, message):
    # Note: In real app, configure SMTP server
    # For demo, just print
    print(f"Alert sent to {to_email}: {subject} - {message}")

# Generate PDF report
def generate_pdf_report(data, filename):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "Health Report")
    y = 700
    for key, value in data.items():
        c.drawString(100, y, f"{key}: {value}")
        y -= 20
    c.save()

# Generate Excel report
def generate_excel_report(df, filename):
    df.to_excel(filename, index=False)

# Schedule reminders (basic simulation)
def schedule_reminder(reminder_time, message):
    # Use schedule library for real scheduling
    print(f"Reminder scheduled for {reminder_time}: {message}")

# Calculate baseline for user
def calculate_baseline(user_data):
    if not user_data:
        return {}
    df = pd.DataFrame(user_data)
    baseline = {}
    for col in ['heart_rate', 'blood_oxygen', 'temperature']:
        if col in df.columns:
            baseline[col] = df[col].mean()
    return baseline

# Generate personalized insight
def generate_insight(current_vitals, baseline):
    insights = []
    if 'heart_rate' in current_vitals and 'heart_rate' in baseline:
        if current_vitals['heart_rate'] > baseline['heart_rate'] * 1.2:
            insights.append("Your heart rate is above your normal baseline.")
    if 'blood_oxygen' in current_vitals and 'blood_oxygen' in baseline:
        if current_vitals['blood_oxygen'] < baseline['blood_oxygen'] * 0.95:
            insights.append("Your oxygen levels are trending down.")
    if 'temperature' in current_vitals:
        if current_vitals['temperature'] > 37.5:
            insights.append("You may have a fever.")
    return insights

# Preprocess data for anomaly detection
def preprocess_data(df):
    """Preprocess health data with activity level encoding and scaling"""
    features = ['heart_rate', 'blood_oxygen', 'temperature', 'respiration_rate']
    
    # Create a copy for processing
    df_processed = df.copy()
    
    # Encode activity level if present
    if 'activity_level' in df_processed.columns:
        activity_mapping = {'low': 0, 'moderate': 1, 'high': 2}
        df_processed['activity_level_encoded'] = df_processed['activity_level'].map(activity_mapping)
        features.append('activity_level_encoded')
    
    # Select only available features
    available_features = [f for f in features if f in df_processed.columns]
    
    if not available_features:
        raise ValueError("No valid features found in dataframe")
    
    df_for_scaling = df_processed[available_features].copy()
    
    # Scale the data
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_for_scaling)
    
    return df_processed, df_scaled, available_features

def create_lstm_sequences(data, time_steps=10):
    """Create sequences for LSTM model training"""
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:i+time_steps])
        y.append(data[i+time_steps])
    return np.array(X), np.array(y)

def normalize_data(data):
    """Normalize data for neural network input"""
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    return scaler.fit_transform(data.reshape(-1, 1)).flatten(), scaler

