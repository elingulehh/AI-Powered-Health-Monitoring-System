import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score, f1_score
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("⚠️ TensorFlow not available. LSTM predictions will not be available.")

# Anomaly Detection using IsolationForest with evaluation
def detect_anomalies_with_evaluation(df_scaled, contamination=0.05, test_size=0.2):
    """
    Detect anomalies and provide evaluation metrics
    Returns: predictions, model, metrics_dict
    """
    # Split data for evaluation
    if len(df_scaled) > 50:  # Only split if we have enough data
        train_data, test_data = train_test_split(df_scaled, test_size=test_size, random_state=42)
    else:
        train_data = test_data = df_scaled
    
    # Train model
    model = IsolationForest(contamination=contamination, random_state=42, n_estimators=100)
    model.fit(train_data)
    
    # Predict on all data
    all_preds = model.fit_predict(df_scaled)
    test_preds = model.predict(test_data)
    
    # Calculate metrics
    anomaly_count = sum(all_preds == -1)
    normal_count = sum(all_preds == 1)
    
    metrics = {
        'total_samples': len(df_scaled),
        'anomalies_detected': int(anomaly_count),
        'normal_samples': int(normal_count),
        'anomaly_percentage': round((anomaly_count / len(df_scaled)) * 100, 2),
        'contamination_used': contamination
    }
    
    return all_preds, model, metrics

# Simple anomaly detection (backward compatible)
def detect_anomalies(df_scaled, contamination=0.05):
    model = IsolationForest(contamination=contamination, random_state=42)
    preds = model.fit_predict(df_scaled)
    return preds, model

# Simple Risk Prediction Model (e.g., for BP risk)
def train_risk_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42, n_estimators=100)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    return model, report

# LSTM for Time-Series Prediction (e.g., heart rate prediction)
def build_lstm_model(input_shape):
    """Build LSTM model for time-series prediction"""
    if not TENSORFLOW_AVAILABLE:
        raise ImportError("TensorFlow not available. Cannot build LSTM model.")
    
    model = keras.Sequential([
        layers.LSTM(64, activation='relu', return_sequences=True, input_shape=input_shape),
        layers.Dropout(0.2),
        layers.LSTM(32, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(16, activation='relu'),
        layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def prepare_sequences_for_lstm(data, time_steps=10):
    """Prepare sequences for LSTM training"""
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:i+time_steps])
        y.append(data[i+time_steps])
    return np.array(X), np.array(y)

def train_lstm_model(data, time_steps=10, epochs=20, verbose=0):
    """Train LSTM model on time-series data"""
    if not TENSORFLOW_AVAILABLE:
        print("⚠️ LSTM training skipped - TensorFlow not available.")
        return None, None
    
    if len(data) < time_steps + 10:
        print("⚠️ Not enough data for LSTM training. Need at least", time_steps + 10, "samples.")
        return None, None
    
    # Prepare sequences
    X, y = prepare_sequences_for_lstm(data, time_steps)
    
    # Reshape for LSTM [samples, time_steps, features]
    X = X.reshape((X.shape[0], X.shape[1], 1))
    
    # Split data
    split_idx = int(0.8 * len(X))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # Build and train model
    model = build_lstm_model((time_steps, 1))
    history = model.fit(
        X_train, y_train, 
        epochs=epochs, 
        batch_size=32, 
        validation_data=(X_test, y_test),
        verbose=verbose
    )
    
    return model, history

def predict_future_values(model, recent_data, time_steps=10, future_steps=10):
    """Predict future values using trained LSTM model"""
    if model is None or not TENSORFLOW_AVAILABLE:
        return None
    
    predictions = []
    current_sequence = recent_data[-time_steps:].copy()
    
    for _ in range(future_steps):
        # Reshape for prediction
        input_data = current_sequence.reshape((1, time_steps, 1))
        
        # Predict next value
        next_pred = model.predict(input_data, verbose=0)[0, 0]
        predictions.append(next_pred)
        
        # Update sequence
        current_sequence = np.append(current_sequence[1:], next_pred)
    
    return np.array(predictions)

# Predict risks (enhanced rule-based)
def predict_risks(vitals):
    """Predict health risks based on vital signs"""
    risks = []
    
    heart_rate = vitals.get('heart_rate', 0)
    blood_oxygen = vitals.get('blood_oxygen', 100)
    temperature = vitals.get('temperature', 36.5)
    respiration_rate = vitals.get('respiration_rate', 15)
    
    # Heart rate risks
    if heart_rate > 100:
        severity = "HIGH" if heart_rate > 120 else "MEDIUM"
        risks.append(f"[{severity}] Tachycardia - Heart rate {heart_rate} BPM is elevated")
    elif heart_rate < 60 and heart_rate > 0:
        risks.append(f"[MEDIUM] Bradycardia - Heart rate {heart_rate} BPM is low")
    
    # Oxygen saturation risks
    if blood_oxygen < 95 and blood_oxygen > 0:
        severity = "CRITICAL" if blood_oxygen < 90 else "HIGH"
        risks.append(f"[{severity}] Hypoxia - Blood oxygen {blood_oxygen}% is low")
    
    # Temperature risks
    if temperature > 37.5:
        severity = "HIGH" if temperature > 38.5 else "MEDIUM"
        risks.append(f"[{severity}] Fever - Temperature {temperature}°C is elevated")
    elif temperature < 36.0:
        risks.append(f"[HIGH] Hypothermia - Temperature {temperature}°C is low")
    
    # Respiration risks
    if respiration_rate > 20:
        risks.append(f"[MEDIUM] Tachypnea - Respiration rate {respiration_rate} is elevated")
    elif respiration_rate < 12 and respiration_rate > 0:
        risks.append(f"[MEDIUM] Bradypnea - Respiration rate {respiration_rate} is low")
    
    return risks

def calculate_health_score(vitals):
    """Calculate overall health score from 0-100"""
    score = 100
    
    heart_rate = vitals.get('heart_rate', 75)
    blood_oxygen = vitals.get('blood_oxygen', 98)
    temperature = vitals.get('temperature', 36.5)
    respiration_rate = vitals.get('respiration_rate', 16)
    
    # Deduct points for abnormal values
    if heart_rate > 100 or heart_rate < 60:
        score -= min(20, abs(heart_rate - 80) / 2)
    
    if blood_oxygen < 95:
        score -= (95 - blood_oxygen) * 3
    
    if temperature > 37.5 or temperature < 36.0:
        score -= abs(temperature - 36.5) * 10
    
    if respiration_rate > 20 or respiration_rate < 12:
        score -= min(15, abs(respiration_rate - 16) * 2)
    
    return max(0, min(100, round(score, 1)))
