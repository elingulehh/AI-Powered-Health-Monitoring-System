import pandas as pd
import json
from datetime import datetime, timedelta
import numpy as np
from utils import save_data_to_json, load_data_from_json, encrypt_data, decrypt_data

# Simulate database with JSON files
USER_DATA_FILE = 'user_data.json'
HEALTH_DATA_FILE = 'health_data.json'
MEDICATIONS_FILE = 'medications.json'
APPOINTMENTS_FILE = 'appointments.json'

# User management
def save_user_data(user_data):
    encrypted_data = encrypt_data(json.dumps(user_data))
    save_data_to_json({'data': encrypted_data}, USER_DATA_FILE)

def load_user_data():
    data = load_data_from_json(USER_DATA_FILE)
    if 'data' in data:
        decrypted = decrypt_data(data['data'])
        return json.loads(decrypted)
    return {}

def add_user(username, password, role='Patient', profile=None):
    users = load_user_data()
    users[username] = {'password': password, 'role': role, 'profile': profile or {}}
    save_user_data(users)

def authenticate_user(username, password):
    users = load_user_data()
    if username in users and users[username]['password'] == password:
        return users[username]
    return None

# Health data management
def save_health_data(health_data):
    save_data_to_json(health_data, HEALTH_DATA_FILE)

def load_health_data():
    return load_data_from_json(HEALTH_DATA_FILE)

def add_health_record(user_id, vitals):
    data = load_health_data()
    if user_id not in data:
        data[user_id] = []
    record = {'timestamp': datetime.now().isoformat(), **vitals}
    data[user_id].append(record)
    save_health_data(data)

# Medications
def save_medications(medications):
    save_data_to_json(medications, MEDICATIONS_FILE)

def load_medications():
    return load_data_from_json(MEDICATIONS_FILE)

def add_medication(user_id, med_name, schedule):
    meds = load_medications()
    if user_id not in meds:
        meds[user_id] = []
    meds[user_id].append({'name': med_name, 'schedule': schedule})
    save_medications(meds)

# Appointments
def save_appointments(appointments):
    save_data_to_json(appointments, APPOINTMENTS_FILE)

def load_appointments():
    return load_data_from_json(APPOINTMENTS_FILE)

def add_appointment(user_id, doctor, date_time, reason):
    appts = load_appointments()
    if user_id not in appts:
        appts[user_id] = []
    appts[user_id].append({'doctor': doctor, 'date_time': date_time, 'reason': reason})
    save_appointments(appts)

# Enhanced health data simulation with anomaly injection
def simulate_health_data(user_id, minutes=300, inject_anomalies=True, anomaly_rate=0.05):
    """Simulate realistic health data with optional anomaly injection"""
    start_time = datetime.now() - timedelta(minutes=minutes)
    data = []
    timestamp = start_time
    
    # User-specific baseline variations
    np.random.seed(hash(user_id) % 2**32)
    hr_baseline = np.random.randint(65, 80)
    o2_baseline = np.random.randint(95, 99)
    temp_baseline = round(np.random.uniform(36.2, 36.8), 1)
    resp_baseline = np.random.randint(14, 18)
    
    # Determine anomaly indices
    anomaly_indices = set()
    if inject_anomalies:
        num_anomalies = int(minutes * anomaly_rate)
        anomaly_indices = set(np.random.choice(minutes, num_anomalies, replace=False))
    
    for i in range(minutes):
        is_anomaly = i in anomaly_indices
        
        if is_anomaly:
            # Generate anomalous values
            anomaly_type = np.random.choice(['high_hr', 'low_o2', 'high_temp', 'high_resp'])
            
            if anomaly_type == 'high_hr':
                heart_rate = np.random.randint(110, 140)
                blood_oxygen = o2_baseline + np.random.randint(-2, 3)
                temperature = temp_baseline + round(np.random.uniform(-0.3, 0.3), 2)
                respiration_rate = resp_baseline + np.random.randint(-2, 3)
            elif anomaly_type == 'low_o2':
                heart_rate = hr_baseline + np.random.randint(-3, 8)
                blood_oxygen = np.random.randint(85, 92)
                temperature = temp_baseline + round(np.random.uniform(-0.2, 0.4), 2)
                respiration_rate = np.random.randint(20, 28)
            elif anomaly_type == 'high_temp':
                heart_rate = hr_baseline + np.random.randint(5, 20)
                blood_oxygen = o2_baseline + np.random.randint(-3, 1)
                temperature = round(np.random.uniform(38.0, 39.5), 2)
                respiration_rate = resp_baseline + np.random.randint(2, 6)
            else:  # high_resp
                heart_rate = hr_baseline + np.random.randint(5, 15)
                blood_oxygen = o2_baseline + np.random.randint(-2, 2)
                temperature = temp_baseline + round(np.random.uniform(-0.2, 0.5), 2)
                respiration_rate = np.random.randint(25, 35)
        else:
            # Generate normal values with small variations
            heart_rate = hr_baseline + np.random.randint(-5, 10)
            blood_oxygen = o2_baseline + np.random.randint(-2, 3)
            temperature = temp_baseline + round(np.random.uniform(-0.4, 0.4), 2)
            respiration_rate = resp_baseline + np.random.randint(-3, 4)
        
        # Ensure values stay within reasonable bounds
        heart_rate = max(40, min(180, heart_rate))
        blood_oxygen = max(80, min(100, blood_oxygen))
        temperature = max(34.0, min(42.0, temperature))
        respiration_rate = max(8, min(40, respiration_rate))
        
        activity_level = np.random.choice(["low", "moderate", "high"], p=[0.5, 0.35, 0.15])
        
        data.append({
            "user_id": user_id,
            "timestamp": timestamp.isoformat(),
            "heart_rate": int(heart_rate),
            "blood_oxygen": int(blood_oxygen),
            "temperature": round(temperature, 2),
            "respiration_rate": int(respiration_rate),
            "activity_level": activity_level
        })
        timestamp += timedelta(minutes=1)
    
    return data

def simulate_multi_user_data(num_users=3, minutes_per_user=300, contamination=0.05):
    """Generate data for multiple users simultaneously"""
    all_data = []
    
    for i in range(num_users):
        user_id = f"User_{i+1}"
        user_data = simulate_health_data(user_id, minutes_per_user, True, contamination)
        all_data.extend(user_data)
    
    return pd.DataFrame(all_data)

# Get user health data as DataFrame
def get_user_health_df(user_id):
    data = load_health_data()
    if user_id in data:
        return pd.DataFrame(data[user_id])
    return pd.DataFrame()
